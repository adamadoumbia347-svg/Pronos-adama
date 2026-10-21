"""Données du tableau de bord (page web privée) : écrit un fichier JSON lu par la page.

Le fichier contient les 30 derniers jours de bougies 4H et leurs indicateurs, le score
des deux côtés (achat et vente), le trade suivi, l'historique et les actualités du jour.
"""
import json
import os

import donnees
import strategie

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_PAGE = os.path.join(ICI, "..", "docs", "btc-cffec35843")
NB_BOUGIES = 180  # 30 jours


def _arrondi(v, n=2):
    return None if v is None else round(v, n)


def construire(bougies, source, peur, peur_txt, etat, articles, maintenant, seuil):
    x = strategie.calculer(bougies)
    cotes = {}
    for sens, nom in ((1, "achat"), (-1, "vente")):
        crit = strategie.noter(x, sens, peur)
        cotes[nom] = {"score": sum(c[1] for c in crit), "declencheurs": strategie.declencheurs(x, sens),
                      "criteres": [{"nom": c[0], "points": c[1], "max": c[2], "texte": c[3]} for c in crit],
                      "plan": {k: _arrondi(v) for k, v in strategie.plan_de_trade(x, sens, 1000, 1).items()
                               if k in ("entree", "stop", "tp1", "tp2", "tp3")}}
    debut = len(bougies) - NB_BOUGIES
    serie = []
    for i in range(debut, len(bougies)):
        b = bougies[i]
        serie.append([b["t"], _arrondi(b["o"]), _arrondi(b["h"]), _arrondi(b["l"]), _arrondi(b["c"]), _arrondi(b["v"], 3),
                      _arrondi(x["ema21"][i]), _arrondi(x["ema50"][i]), _arrondi(x["ema200"][i]),
                      _arrondi(x["st"][i]), x["st_dir"][i]])
    i = len(bougies) - 1
    actus = donnees.actualites_fortes(articles, maintenant, fenetre_h=24, seuil=2)
    return {
        "maj": int(maintenant), "source": source, "seuil": seuil,
        "prix": bougies[-1]["c"], "var24": 100 * (bougies[-1]["c"] / bougies[-7]["c"] - 1),
        "atr": _arrondi(x["atr"][i]), "rsi": _arrondi(x["rsi"][i], 1), "adx": _arrondi(x["adx"][i], 1),
        "peur": peur, "peur_txt": peur_txt,
        "colonnes": ["t", "o", "h", "l", "c", "v", "ema21", "ema50", "ema200", "st", "st_dir"],
        "bougies": serie, "cotes": cotes,
        "trade": etat.get("trade"), "historique": etat.get("historique", [])[-50:],
        "actus": [{"titre": a["titre"], "lien": a["lien"], "resume": a["resume"][:220], "t": int(a["t"]),
                   "sources": a["sources"], "score": a["score"], "etiquettes": a["etiquettes"]}
                  for a in actus[:25]],
    }


def ecrire(donnees_page, dossier=DOSSIER_PAGE):
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "donnees.json"), "w", encoding="utf-8") as f:
        json.dump(donnees_page, f, ensure_ascii=False, separators=(",", ":"))
