"""Récupération des données : bougies 4H, indice Fear & Greed, actualités (flux RSS).

Toutes les sources sont publiques et gratuites, sans clé. Si une bourse ne répond pas,
on passe à la suivante.
"""
import email.utils
import html
from datetime import datetime
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

QUATRE_H = 4 * 3600
ENTETES = {"User-Agent": "Mozilla/5.0 (bot-bitcoin-4h)"}


def _lire(url, delai=20):
    req = urllib.request.Request(url, headers=ENTETES)
    with urllib.request.urlopen(req, timeout=delai) as r:
        return r.read()


def _kraken():
    d = json.loads(_lire("https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=240"))
    lignes = next(v for k, v in d["result"].items() if k != "last")
    return [{"t": int(r[0]), "o": float(r[1]), "h": float(r[2]), "l": float(r[3]),
             "c": float(r[4]), "v": float(r[6])} for r in lignes]


def _bitstamp():
    d = json.loads(_lire("https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=14400&limit=500"))
    return [{"t": int(r["timestamp"]), "o": float(r["open"]), "h": float(r["high"]), "l": float(r["low"]),
             "c": float(r["close"]), "v": float(r["volume"])} for r in d["data"]["ohlc"]]


def _binance():
    d = json.loads(_lire("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=500"))
    return [{"t": int(r[0]) // 1000, "o": float(r[1]), "h": float(r[2]), "l": float(r[3]),
             "c": float(r[4]), "v": float(r[5])} for r in d]


SOURCES_PRIX = [("Kraken", _kraken), ("Bitstamp", _bitstamp), ("Binance", _binance)]


def bougies_4h(maintenant=None):
    """Bougies 4H fermées uniquement (la bougie en cours est retirée)."""
    maintenant = maintenant or time.time()
    erreurs = []
    for nom, f in SOURCES_PRIX:
        try:
            b = sorted(f(), key=lambda x: x["t"])
            b = [x for x in b if x["t"] + QUATRE_H <= maintenant]
            if len(b) >= 250:
                return nom, b
            erreurs.append(f"{nom}: seulement {len(b)} bougies")
        except Exception as e:  # noqa: BLE001 - on essaie la source suivante
            erreurs.append(f"{nom}: {e}")
    raise RuntimeError("Aucune source de prix disponible : " + " | ".join(erreurs))


def peur_avidite():
    try:
        d = json.loads(_lire("https://api.alternative.me/fng/?limit=1"))["data"][0]
        return int(d["value"]), d["value_classification"]
    except Exception:  # noqa: BLE001
        return None, None


FLUX = [
    ("Cointelegraph", "https://cointelegraph.com/rss/tag/bitcoin"),
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Decrypt", "https://decrypt.co/feed"),
    ("Bitcoin Magazine", "https://bitcoinmagazine.com/.rss/full/"),
    ("The Block", "https://www.theblock.co/rss.xml"),
    ("Journal du Coin", "https://journalducoin.com/feed/"),
    ("Cryptoast", "https://cryptoast.fr/feed/"),
]

# Mot-clé (expression régulière) -> (poids, étiquette affichée)
MOTS_FORTS = [
    (r"\betfs?\b", 3, "ETF"),
    (r"\bsec\b|gensler|atkins", 3, "Régulateur US"),
    (r"\bfed\b|fomc|powell|rate cut|rate hike|taux directeur|baisse des taux|hausse des taux", 3, "Fed / taux"),
    (r"hack|exploit|piratage|piraté|drained|stolen|vol de", 4, "Piratage"),
    (r"bankrupt|faillite|insolv|collapse|effondrement", 4, "Faillite"),
    (r"\bban\b|bans|interdi", 3, "Interdiction"),
    (r"strategic (bitcoin )?reserve|réserve stratégique", 4, "Réserve d'État"),
    (r"all[- ]time high|\bath\b|record|plus haut historique", 3, "Record"),
    (r"crash|plunge|krach|s'effondre|chute brutale|dégringol", 3, "Chute brutale"),
    (r"surge|soars|skyrocket|s'envole|bondit|explose", 2, "Envolée"),
    (r"liquidat", 2, "Liquidations"),
    (r"blackrock|fidelity|vanguard|jpmorgan|goldman", 2, "Institutionnels"),
    (r"microstrategy|\bstrategy\b|saylor", 2, "Strategy (Saylor)"),
    (r"\bcpi\b|inflation|nonfarm|payrolls|emploi américain", 2, "Macro US"),
    (r"trump|white house|maison blanche|congress|sénat|senate", 2, "Politique US"),
    (r"halving", 2, "Halving"),
    (r"tariff|droits de douane", 2, "Droits de douane"),
    (r"mt\.? ?gox|government (sells|moves)|vend ses bitcoins|transfert.*gouvernement", 3, "Ventes d'État"),
    (r"stablecoin|tether|usdt|circle", 1, "Stablecoins"),
]
SUJET_BTC = re.compile(r"bitcoin|\bbtc\b|crypto", re.I)


def _texte(el, *noms):
    for n in noms:
        x = el.find(n)
        if x is not None and (x.text or "").strip():
            return x.text.strip()
    return ""


def _nettoyer(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def _date(texte):
    """Date RSS (RFC 822) ou Atom (ISO 8601) -> horodatage Unix."""
    for lire in (email.utils.parsedate_to_datetime, lambda t: datetime.fromisoformat(t.replace("Z", "+00:00"))):
        try:
            d = lire(texte)
            return d.timestamp() if d.tzinfo else None
        except Exception:  # noqa: BLE001
            continue
    return None


def lire_flux():
    articles = []
    atom = "{http://www.w3.org/2005/Atom}"
    for source, url in FLUX:
        try:
            racine = ET.fromstring(_lire(url, 15))
        except Exception as e:  # noqa: BLE001
            print(f"  flux {source} indisponible : {e}")
            continue
        items = racine.iter("item")
        for it in items:
            titre = _nettoyer(_texte(it, "title"))
            lien = _texte(it, "link")
            resume = _nettoyer(_texte(it, "description"))[:300]
            quand = _date(_texte(it, "pubDate"))
            if titre and lien:
                articles.append({"source": source, "titre": titre, "lien": lien, "resume": resume, "t": quand})
        for it in racine.iter(atom + "entry"):
            lien_el = it.find(atom + "link")
            titre = _nettoyer(_texte(it, atom + "title"))
            if titre and lien_el is not None:
                articles.append({"source": source, "titre": titre, "lien": lien_el.get("href", ""),
                                 "resume": _nettoyer(_texte(it, atom + "summary"))[:300],
                                 "t": _date(_texte(it, atom + "published", atom + "updated"))})
    return articles


def _mots(titre):
    return {m for m in re.findall(r"[a-zà-ÿ0-9]{4,}", titre.lower())}


def actualites_fortes(articles, maintenant=None, fenetre_h=6, seuil=5):
    """Garde les actualités récentes et importantes, regroupe les doublons entre sources.

    Score = somme des poids des mots-clés + 2 points par source supplémentaire
    qui relaie la même information (une nouvelle confirmée par plusieurs médias pèse plus).
    """
    maintenant = maintenant or time.time()
    recents = [a for a in articles if a["t"] and maintenant - a["t"] <= fenetre_h * 3600]
    groupes = []
    for a in sorted(recents, key=lambda a: a["t"]):
        mots = _mots(a["titre"])
        for g in groupes:
            commun = len(mots & g["mots"]) / max(1, min(len(mots), len(g["mots"])))
            if commun >= 0.5:
                g["sources"].add(a["source"]); g["mots"] |= mots
                break
        else:
            groupes.append({**a, "mots": mots, "sources": {a["source"]}})
    forts = []
    for g in groupes:
        texte = g["titre"] + " " + g["resume"]
        if not SUJET_BTC.search(texte):
            continue
        poids, etiquettes = 0, []
        for motif, p, etiq in MOTS_FORTS:
            if re.search(motif, texte, re.I):
                poids += p; etiquettes.append(etiq)
        poids += 2 * (len(g["sources"]) - 1)
        if poids >= seuil:
            g["score"], g["etiquettes"] = poids, etiquettes
            g["sources"] = sorted(g["sources"])
            del g["mots"]
            forts.append(g)
    return sorted(forts, key=lambda g: g["score"], reverse=True)


def cle_article(a):
    return re.sub(r"[^a-z0-9]", "", a["titre"].lower())[:80]
