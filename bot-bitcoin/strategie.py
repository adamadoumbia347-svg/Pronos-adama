"""Score de confluence 4H : huit critères notés sur 100, un déclencheur obligatoire.

Un signal n'existe que si la dernière bougie fermée contient un événement précis
(retournement Supertrend, croisement MACD, cassure, rebond RSI, reprise de l'EMA 21).
Sans déclencheur, même un score élevé ne produit rien : on évite ainsi de recevoir
« ACHAT » à chaque bougie pendant une longue tendance.
"""
import indicateurs as ind


def _croise_dessus(a, b, i):
    return None not in (a[i], b[i], a[i - 1], b[i - 1]) and a[i - 1] <= b[i - 1] and a[i] > b[i]


def _divergence(closes, lows, highs, rsi, sens, recence=8):
    """Divergence RSI sur les 40 dernières bougies (creux/sommets confirmés)."""
    debut = len(closes) - 40
    creux, sommets = ind.creux_sommets(lows[debut:] if sens == 1 else highs[debut:])
    pivots = creux if sens == 1 else sommets
    if len(pivots) < 2:
        return False
    p1, p2 = debut + pivots[-2], debut + pivots[-1]
    if len(closes) - 1 - p2 > recence or rsi[p1] is None or rsi[p2] is None:
        return False
    if sens == 1:
        return lows[p2] < lows[p1] and rsi[p2] > rsi[p1] + 2
    return highs[p2] > highs[p1] and rsi[p2] < rsi[p1] - 2


def calculer(bougies):
    o = [b["o"] for b in bougies]; h = [b["h"] for b in bougies]
    l = [b["l"] for b in bougies]; c = [b["c"] for b in bougies]; v = [b["v"] for b in bougies]
    adx, pdi, mdi = ind.adx(h, l, c)
    ligne_macd, sig_macd, histo = ind.macd(c)
    st_ligne, st_dir = ind.supertrend(h, l, c)
    bb_haut, bb_moy, bb_bas = ind.bollinger(c)
    return {"o": o, "h": h, "l": l, "c": c, "v": v,
            "ema21": ind.ema(c, 21), "ema50": ind.ema(c, 50), "ema200": ind.ema(c, 200),
            "rsi": ind.rsi(c), "macd": ligne_macd, "macd_sig": sig_macd, "histo": histo,
            "atr": ind.atr(h, l, c), "adx": adx, "pdi": pdi, "mdi": mdi,
            "st": st_ligne, "st_dir": st_dir, "bb_haut": bb_haut, "bb_bas": bb_bas,
            "vol_moy": ind.sma(v, 20)}


def declencheurs(x, sens):
    i = len(x["c"]) - 1
    c, h, l = x["c"], x["h"], x["l"]
    trouve = []
    if x["st_dir"][i] == sens and x["st_dir"][i - 1] == -sens:
        trouve.append("Retournement du Supertrend")
    if (sens == 1 and _croise_dessus(x["macd"], x["macd_sig"], i)) or \
       (sens == -1 and _croise_dessus(x["macd_sig"], x["macd"], i)):
        trouve.append("Croisement MACD")
    if sens == 1 and c[i] > max(h[i - 20:i]):
        trouve.append("Cassure du plus haut des 20 dernières bougies")
    if sens == -1 and c[i] < min(l[i - 20:i]):
        trouve.append("Cassure du plus bas des 20 dernières bougies")
    r = x["rsi"]
    if sens == 1 and r[i - 1] < 35 <= r[i]:
        trouve.append("Le RSI ressort de la zone de survente")
    if sens == -1 and r[i - 1] > 65 >= r[i]:
        trouve.append("Le RSI ressort de la zone de surachat")
    e21, e50, e200 = x["ema21"], x["ema50"], x["ema200"]
    if sens == 1 and e50[i] > e200[i] and c[i - 1] < e21[i - 1] and c[i] > e21[i]:
        trouve.append("Reprise de l'EMA 21 dans une tendance haussière")
    if sens == -1 and e50[i] < e200[i] and c[i - 1] > e21[i - 1] and c[i] < e21[i]:
        trouve.append("Perte de l'EMA 21 dans une tendance baissière")
    return trouve


def noter(x, sens, peur_avidite=None):
    """Renvoie la liste des critères (nom, points, maximum, explication)."""
    i = len(x["c"]) - 1
    c = x["c"]
    crit = []

    pts, txt = 0, []
    if (c[i] - x["ema200"][i]) * sens > 0:
        pts += 10; txt.append("prix " + ("au-dessus" if sens == 1 else "en dessous") + " de l'EMA 200")
    if (x["ema50"][i] - x["ema200"][i]) * sens > 0:
        pts += 10; txt.append("EMA 50 " + ("au-dessus" if sens == 1 else "sous") + " l'EMA 200")
    crit.append(("Tendance de fond", pts, 20, ", ".join(txt) or "contre la tendance de fond"))

    pts = 0
    if x["st_dir"][i] == sens:
        pts += 10
        if -sens in x["st_dir"][i - 3:i]:
            pts += 5
    crit.append(("Supertrend", pts, 15, "aligné" + (", retournement récent" if pts == 15 else "") if pts else "opposé"))

    hi = x["histo"]
    pts = 0
    if hi[i] * sens > 0:
        pts += 7
    if (hi[i] - hi[i - 1]) * sens > 0:
        pts += 4
    if any(hi[j] * sens > 0 and hi[j - 1] * sens <= 0 for j in range(i - 2, i + 1)):
        pts += 4
    crit.append(("MACD", pts, 15, f"histogramme {hi[i]:+.0f}, " + ("accélère" if (hi[i] - hi[i - 1]) * sens > 0 else "ralentit")))

    r = x["rsi"]
    pts = 0
    if sens == 1:
        if min(r[i - 5:i + 1]) < 35 and r[i] > r[i - 1]:
            pts = 15
        elif 50 < r[i] < 70:
            pts = 10 + (5 if r[i] > r[i - 1] else 0)
        elif r[i] >= 75:
            pts = 0
    else:
        if max(r[i - 5:i + 1]) > 65 and r[i] < r[i - 1]:
            pts = 15
        elif 30 < r[i] < 50:
            pts = 10 + (5 if r[i] < r[i - 1] else 0)
        elif r[i] <= 25:
            pts = 0
    crit.append(("RSI", pts, 15, f"{r[i]:.0f}" + (" (surachat)" if r[i] >= 70 else " (survente)" if r[i] <= 30 else "")))

    pts = 0
    favorable = (x["pdi"][i] - x["mdi"][i]) * sens > 0
    if x["adx"][i] > 20 and favorable:
        pts += 6
        if x["adx"][i] > 25 and x["adx"][i] > x["adx"][i - 1]:
            pts += 4
    crit.append(("Force (ADX)", pts, 10, f"ADX {x['adx'][i]:.0f}" + (", directionnel favorable" if favorable else ", directionnel opposé")))

    ratio = x["v"][i] / x["vol_moy"][i] if x["vol_moy"][i] else 1
    bougie_ok = (c[i] - x["o"][i]) * sens > 0
    pts = 10 if ratio > 1.5 and bougie_ok else 5 if ratio > 1.2 and bougie_ok else 0
    crit.append(("Volume", pts, 10, f"{ratio:.1f}× la moyenne" + ("" if bougie_ok else ", bougie contraire")))

    pts, txt = 0, "rien de notable"
    if (sens == 1 and c[i] > max(x["h"][i - 20:i])) or (sens == -1 and c[i] < min(x["l"][i - 20:i])):
        pts, txt = 10, "cassure de la zone des 20 bougies"
    elif _divergence(c, x["l"], x["h"], r, sens):
        pts, txt = 10, "divergence " + ("haussière" if sens == 1 else "baissière") + " RSI"
    crit.append(("Structure", pts, 10, txt))

    pts, txt = 0, "indisponible"
    if peur_avidite is not None:
        txt = f"Fear & Greed {peur_avidite}"
        if sens == 1:
            pts = 5 if peur_avidite <= 25 else 2 if peur_avidite <= 45 else 0
        else:
            pts = 5 if peur_avidite >= 75 else 2 if peur_avidite >= 55 else 0
    crit.append(("Sentiment (à contre-courant)", pts, 5, txt))
    return crit


def plan_de_trade(x, sens, capital, risque_pct):
    i = len(x["c"]) - 1
    entree, a = x["c"][i], x["atr"][i]
    if sens == 1:
        stop = min(min(x["l"][i - 5:i + 1]) - 0.3 * a, entree - 1.2 * a)
    else:
        stop = max(max(x["h"][i - 5:i + 1]) + 0.3 * a, entree + 1.2 * a)
    r = abs(entree - stop)
    taille = capital * risque_pct / 100 / r if r else 0
    return {"sens": sens, "entree": entree, "stop": stop,
            "tp1": entree + sens * 1.5 * r, "tp2": entree + sens * 2.5 * r, "tp3": entree + sens * 4 * r,
            "risque_pct_prix": 100 * r / entree, "atr": a,
            "taille_btc": taille, "taille_usd": taille * entree, "perte_max": capital * risque_pct / 100}


def analyser(bougies, peur_avidite=None, capital=1000.0, risque_pct=1.0):
    """Analyse la dernière bougie fermée et renvoie le meilleur côté (achat ou vente)."""
    x = calculer(bougies)
    meilleurs = []
    for sens in (1, -1):
        crit = noter(x, sens, peur_avidite)
        score = sum(p for _, p, _, _ in crit)
        meilleurs.append({"sens": sens, "score": score, "criteres": crit,
                          "declencheurs": declencheurs(x, sens)})
    meilleurs.sort(key=lambda m: (bool(m["declencheurs"]), m["score"]), reverse=True)
    choix = meilleurs[0]
    choix["plan"] = plan_de_trade(x, choix["sens"], capital, risque_pct)
    choix["indic"] = x
    return choix
