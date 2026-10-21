"""Bot Bitcoin 4H : signaux forts d'achat/vente et actualités fortes, envoyés par courriel.

Lancé toutes les heures par GitHub Actions (.github/workflows/bot-bitcoin.yml) :
  - à chaque nouvelle bougie 4H fermée : suivi du trade en cours, puis recherche d'un signal fort ;
  - à chaque passage : lecture des actualités, envoi des seules nouvelles importantes.
La mémoire du bot (dernier signal, trade suivi, actualités déjà envoyées) est dans etat.json.

  python3 bot.py           exécution normale
  python3 bot.py --test    envoie un courriel d'essai pour vérifier la configuration
  python3 bot.py --demo    génère des aperçus HTML dans apercus/ avec des données simulées, sans rien envoyer
"""
import json
import os
import random
import sys
import time

import courriel
import donnees
import strategie
import tableau

ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER_ETAT = os.path.join(ICI, "etat.json")
SEUIL = int(os.environ.get("SEUIL_SIGNAL", "70"))
CAPITAL = float(os.environ.get("CAPITAL", "1000"))
RISQUE_PCT = float(os.environ.get("RISQUE_PCT", "1"))
BILANS = os.environ.get("ENVOYER_BILANS", "1") == "1"
DUREE_MAX = 42  # bougies (7 jours) avant de fermer un trade qui n'aboutit pas
PARTS = (1 / 3, 1 / 3, 1 / 3)  # sorties partielles aux objectifs 1, 2, 3


def charger_etat():
    try:
        with open(FICHIER_ETAT, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def sauver_etat(etat):
    with open(FICHIER_ETAT, "w", encoding="utf-8") as f:
        json.dump(etat, f, ensure_ascii=False, indent=1)
        f.write("\n")


def statistiques(etat):
    h = etat.get("historique", [])
    gagnants = sum(1 for t in h if t["r"] > 0)
    return {"total": len(h), "gagnants": gagnants, "taux": 100 * gagnants / len(h) if h else 0,
            "r_total": sum(t["r"] for t in h)}


def _r(trade, prix):
    return trade["sens"] * (prix - trade["entree"]) / trade["risque"]


def _cloturer(etat, trade, r_reste, t):
    """Ajoute la part restante au résultat et range le trade dans l'historique."""
    trade["r_resultat"] = trade.get("r_acquis", 0) + trade.get("reste", 1) * r_reste
    etat.setdefault("historique", []).append(
        {"t": trade["t"], "sens": trade["sens"], "entree": round(trade["entree"], 2),
         "r": round(trade["r_resultat"], 2), "fin": t})
    etat["historique"] = etat["historique"][-200:]
    etat["trade"] = None


def suivre_trade(etat, bougie, envois):
    """Fait avancer le trade suivi d'une bougie : stop, objectifs, durée maximale."""
    tr = etat.get("trade")
    if not tr or bougie["t"] <= tr["t"]:
        return
    s = tr["sens"]
    tr["bougies"] = tr.get("bougies", 0) + 1
    defavorable = bougie["l"] if s == 1 else bougie["h"]
    if (defavorable - tr["stop"]) * s <= 0:
        _cloturer(etat, tr, _r(tr, tr["stop"]), bougie["t"])
        envois.append(("bilan", dict(tr), "stop", tr["stop"]))
        return
    favorable = bougie["h"] if s == 1 else bougie["l"]
    for n, cle in enumerate(("tp1", "tp2", "tp3")):
        if tr.get(cle + "_touche") or (favorable - tr[cle]) * s < 0:
            continue
        tr[cle + "_touche"] = True
        tr["r_acquis"] = tr.get("r_acquis", 0) + PARTS[n] * _r(tr, tr[cle])
        tr["reste"] = tr.get("reste", 1) - PARTS[n]
        if cle == "tp1":
            tr["stop"] = tr["entree"]  # stop remonté au prix d'entrée
        if cle == "tp3":
            _cloturer(etat, tr, 0, bougie["t"])
        envois.append(("bilan", dict(tr), cle, tr[cle]))
        if cle == "tp3":
            return
    if tr["bougies"] >= DUREE_MAX:
        _cloturer(etat, tr, _r(tr, bougie["c"]), bougie["t"])
        envois.append(("bilan", dict(tr), "temps", bougie["c"]))


def chercher_signal(etat, bougies, peur, envois):
    a = strategie.analyser(bougies, peur, CAPITAL, RISQUE_PCT)
    derniere = bougies[-1]
    print(f"  bougie {courriel.heure(derniere['t'])} · {'achat' if a['sens'] == 1 else 'vente'} "
          f"score {a['score']}/100 · déclencheurs : {a['declencheurs'] or 'aucun'}")
    if a["score"] < SEUIL or not a["declencheurs"]:
        return None
    tr = etat.get("trade")
    if tr and tr["sens"] == a["sens"]:
        print("  signal ignoré : un trade dans le même sens est déjà suivi")
        return None
    if tr:
        _cloturer(etat, tr, _r(tr, derniere["c"]), derniere["t"])
        envois.append(("bilan", dict(tr), "inverse", derniere["c"]))
    p = a["plan"]
    etat["trade"] = {"t": derniere["t"], "sens": a["sens"], "entree": p["entree"], "stop": p["stop"],
                     "risque": abs(p["entree"] - p["stop"]), "tp1": p["tp1"], "tp2": p["tp2"], "tp3": p["tp3"],
                     "score": a["score"]}
    envois.append(("signal", a))
    return a


def traiter_actus(etat, articles, maintenant, prix, var4h):
    deja = set(etat.get("actus_envoyees", []))
    forts = [a for a in donnees.actualites_fortes(articles, maintenant) if donnees.cle_article(a) not in deja]
    print(f"  {len(articles)} articles lus, {len(forts)} actualité(s) forte(s) nouvelle(s)")
    if not forts:
        return
    forts = forts[:3]
    sujet, html_, texte = courriel.actus(forts, prix, var4h, maintenant)
    if courriel.envoyer(sujet, html_, texte, priorite=forts[0]["score"] >= 9):
        etat["actus_envoyees"] = (etat.get("actus_envoyees", []) + [donnees.cle_article(a) for a in forts])[-300:]


def executer():
    maintenant = time.time()
    etat = charger_etat()
    source, bougies = donnees.bougies_4h(maintenant)
    peur, peur_txt = donnees.peur_avidite()
    prix, var4h = bougies[-1]["c"], 100 * (bougies[-1]["c"] / bougies[-2]["c"] - 1)
    print(f"Source {source}, {len(bougies)} bougies, dernier prix {courriel.usd(prix)}, Fear & Greed {peur}")

    envois = []
    precedente = etat.get("derniere_bougie")
    nouvelles = [b for b in bougies if precedente is None or b["t"] > precedente]
    if precedente is None:
        nouvelles = nouvelles[-1:]  # premier lancement : on ne rejoue pas l'historique
    for b in nouvelles:
        suivre_trade(etat, b, envois)
    if nouvelles:
        chercher_signal(etat, bougies, peur, envois)
        etat["derniere_bougie"] = bougies[-1]["t"]
    else:
        print("  pas de nouvelle bougie 4H fermée depuis le dernier passage")

    stats = statistiques(etat)
    for envoi in envois:
        if envoi[0] == "signal":
            courriel.envoyer(*courriel.signal(envoi[1], source, peur, peur_txt, stats, maintenant), priorite=True)
        elif BILANS:
            _, tr, evt, px = envoi
            courriel.envoyer(*courriel.bilan(tr, evt, px, stats, maintenant))

    articles = donnees.lire_flux()
    traiter_actus(etat, articles, maintenant, prix, var4h)
    sauver_etat(etat)
    tableau.ecrire(tableau.construire(bougies, source, peur, peur_txt, etat, articles, maintenant, SEUIL))


# ---------------------------------------------------------------- essai et démonstration

def bougies_simulees(n=600, graine=7):
    """Marche aléatoire avec phases de tendance, pour tester sans connexion."""
    rnd = random.Random(graine)
    t0 = int(time.time()) // 14400 * 14400 - n * 14400
    prix, derive, out = 62000.0, 0.0, []
    for i in range(n):
        if i % 60 == 0:
            derive = rnd.choice([-0.004, -0.002, 0.0, 0.002, 0.004])
        o = prix
        c = o * (1 + derive + rnd.gauss(0, 0.012))
        h = max(o, c) * (1 + abs(rnd.gauss(0, 0.005)))
        l = min(o, c) * (1 - abs(rnd.gauss(0, 0.005)))
        out.append({"t": t0 + i * 14400, "o": o, "h": h, "l": l, "c": c, "v": abs(rnd.gauss(1500, 500)) + 200})
        prix = c
    return out


def demo():
    dossier = os.path.join(ICI, "apercus")
    toutes = bougies_simulees()
    etat, envois, trouves = {}, [], []
    for i in range(260, len(toutes)):
        fenetre = toutes[:i + 1]
        suivre_trade(etat, fenetre[-1], envois)
        a = chercher_signal(etat, fenetre, 22, envois)
        if a:
            trouves.append(a)
    stats = statistiques(etat)
    print(f"\n{len(trouves)} signaux forts sur {len(toutes) - 260} bougies ; bilan simulé : {stats}")
    maintenant = time.time()
    signaux = [x for x in envois if x[0] == "signal"]
    for nom, (_, a) in (("signal-achat", next(x for x in signaux if x[1]["sens"] == 1)),
                        ("signal-vente", next(x for x in signaux if x[1]["sens"] == -1))):
        sujet, h, _ = courriel.signal(a, "Kraken (simulation)", 22, "Extreme Fear", stats, maintenant)
        print(nom, ":", sujet, "->", courriel.sauver_apercu(dossier, nom, sujet, h))
    _, tr, evt, px = next(x for x in envois if x[0] == "bilan" and x[2] == "tp2")
    sujet, h, _ = courriel.bilan(tr, evt, px, stats, maintenant)
    print("bilan :", sujet, "->", courriel.sauver_apercu(dossier, "bilan", sujet, h))
    fausses = [
        {"source": "CoinDesk", "titre": "SEC approves spot Bitcoin ETF options as BlackRock record inflows hit $1.2B",
         "lien": "https://example.com/a", "resume": "Les options sur les ETF bitcoin au comptant sont autorisées.",
         "t": maintenant - 1800},
        {"source": "The Block", "titre": "SEC approves options on spot Bitcoin ETFs, BlackRock leads",
         "lien": "https://example.com/b", "resume": "", "t": maintenant - 1500},
        {"source": "Cointelegraph", "titre": "Bitcoin liquidations top $400M as Fed's Powell signals rate cut pause",
         "lien": "https://example.com/c", "resume": "Les positions longues ont été liquidées.", "t": maintenant - 3000},
        {"source": "Journal du Coin", "titre": "Bitcoin : les ETF américains enregistrent 5 jours d'entrées consécutives",
         "lien": "https://example.com/e", "resume": "Les fonds BlackRock et Fidelity mènent la danse.", "t": maintenant - 9000},
        {"source": "Cryptoast", "titre": "Bitcoin : le CPI américain attendu jeudi, les traders prudents",
         "lien": "https://example.com/f", "resume": "L'inflation américaine reste la donnée clé de la semaine.", "t": maintenant - 20000},
        {"source": "Decrypt", "titre": "Ethereum developer call recap", "lien": "https://example.com/d",
         "resume": "", "t": maintenant - 600},
    ]
    forts = donnees.actualites_fortes(fausses, maintenant)
    sujet, h, _ = courriel.actus(forts, toutes[-1]["c"], 1.8, maintenant)
    print("actus :", sujet, "->", courriel.sauver_apercu(dossier, "actus", sujet, h))
    page = tableau.construire(toutes, "Kraken (simulation)", 22, "Extreme Fear", etat, fausses, maintenant, SEUIL)
    tableau.ecrire(page, os.path.join(dossier, "tableau"))
    print("tableau de bord : copiez docs/btc-cffec35843/index.html dans", os.path.join(dossier, "tableau"))


def test():
    toutes = bougies_simulees()
    etat, envois = {}, []
    for i in range(260, len(toutes)):
        if chercher_signal(etat, toutes[:i + 1], 22, envois):
            break
    a = envois[-1][1]
    sujet, h, t = courriel.signal(a, "TEST (données simulées)", 22, "Extreme Fear", statistiques({}), time.time())
    if not courriel.envoyer("[TEST] " + sujet, h, t, priorite=True):
        sys.exit("Échec : configurez les secrets MAIL_EXPEDITEUR et MAIL_MOT_DE_PASSE.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--test" in sys.argv:
        test()
    else:
        executer()
