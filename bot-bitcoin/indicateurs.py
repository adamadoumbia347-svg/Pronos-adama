"""Indicateurs techniques calculés à la main (aucune dépendance externe).

Chaque fonction reçoit des listes de nombres et renvoie une liste de même longueur
(None tant que l'indicateur n'a pas assez d'historique).
"""


def ema(valeurs, periode):
    k = 2 / (periode + 1)
    sortie, prec = [], None
    for i, v in enumerate(valeurs):
        if i + 1 < periode:
            sortie.append(None)
            continue
        if prec is None:
            prec = sum(valeurs[i + 1 - periode:i + 1]) / periode
        else:
            prec = v * k + prec * (1 - k)
        sortie.append(prec)
    return sortie


def sma(valeurs, periode):
    return [None if i + 1 < periode else sum(valeurs[i + 1 - periode:i + 1]) / periode
            for i in range(len(valeurs))]


def lissage_wilder(valeurs, periode):
    """Moyenne de Wilder (RSI, ATR, ADX)."""
    sortie, prec = [], None
    for i, v in enumerate(valeurs):
        if i + 1 < periode:
            sortie.append(None)
            continue
        prec = sum(valeurs[i + 1 - periode:i + 1]) / periode if prec is None else (prec * (periode - 1) + v) / periode
        sortie.append(prec)
    return sortie


def rsi(closes, periode=14):
    hausses = [0.0] + [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
    baisses = [0.0] + [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
    mh, mb = lissage_wilder(hausses[1:], periode), lissage_wilder(baisses[1:], periode)
    sortie = [None]
    for h, b in zip(mh, mb):
        if h is None:
            sortie.append(None)
        else:
            sortie.append(100.0 if b == 0 else 100 - 100 / (1 + h / b))
    return sortie


def macd(closes, rapide=12, lente=26, signal=9):
    er, el = ema(closes, rapide), ema(closes, lente)
    ligne = [None if a is None or b is None else a - b for a, b in zip(er, el)]
    debut = next(i for i, v in enumerate(ligne) if v is not None)
    sig = [None] * debut + ema(ligne[debut:], signal)
    histo = [None if a is None or b is None else a - b for a, b in zip(ligne, sig)]
    return ligne, sig, histo


def true_range(highs, lows, closes):
    return [highs[0] - lows[0]] + [
        max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        for i in range(1, len(closes))]


def atr(highs, lows, closes, periode=14):
    return lissage_wilder(true_range(highs, lows, closes), periode)


def adx(highs, lows, closes, periode=14):
    """Renvoie (adx, +DI, -DI)."""
    plus_dm, moins_dm = [0.0], [0.0]
    for i in range(1, len(closes)):
        haut, bas = highs[i] - highs[i - 1], lows[i - 1] - lows[i]
        plus_dm.append(haut if haut > bas and haut > 0 else 0.0)
        moins_dm.append(bas if bas > haut and bas > 0 else 0.0)
    tr = lissage_wilder(true_range(highs, lows, closes), periode)
    pdm, mdm = lissage_wilder(plus_dm, periode), lissage_wilder(moins_dm, periode)
    pdi, mdi, dx = [], [], []
    for t, p, m in zip(tr, pdm, mdm):
        if t is None or t == 0:
            pdi.append(None); mdi.append(None); dx.append(None)
            continue
        a, b = 100 * p / t, 100 * m / t
        pdi.append(a); mdi.append(b)
        dx.append(0.0 if a + b == 0 else 100 * abs(a - b) / (a + b))
    debut = next(i for i, v in enumerate(dx) if v is not None)
    return [None] * debut + lissage_wilder(dx[debut:], periode), pdi, mdi


def supertrend(highs, lows, closes, periode=10, mult=3.0):
    """Renvoie (ligne, direction) ; direction = 1 haussière, -1 baissière."""
    a = atr(highs, lows, closes, periode)
    ligne, direction = [None] * len(closes), [None] * len(closes)
    haut_f = bas_f = None
    for i in range(len(closes)):
        if a[i] is None:
            continue
        milieu = (highs[i] + lows[i]) / 2
        haut, bas = milieu + mult * a[i], milieu - mult * a[i]
        if haut_f is None:
            haut_f, bas_f, d = haut, bas, 1
        else:
            haut_f = haut if haut < haut_f or closes[i - 1] > haut_f else haut_f
            bas_f = bas if bas > bas_f or closes[i - 1] < bas_f else bas_f
            d = direction[i - 1]
            if d == -1 and closes[i] > haut_f:
                d = 1
            elif d == 1 and closes[i] < bas_f:
                d = -1
        direction[i] = d
        ligne[i] = bas_f if d == 1 else haut_f
    return ligne, direction


def bollinger(closes, periode=20, ecarts=2.0):
    moy = sma(closes, periode)
    haut, bas = [], []
    for i, m in enumerate(moy):
        if m is None:
            haut.append(None); bas.append(None)
            continue
        fen = closes[i + 1 - periode:i + 1]
        et = (sum((x - m) ** 2 for x in fen) / periode) ** 0.5
        haut.append(m + ecarts * et); bas.append(m - ecarts * et)
    return haut, moy, bas


def creux_sommets(valeurs, fenetre=3):
    """Indices des creux et des sommets locaux (pivot entouré de `fenetre` bougies)."""
    creux, sommets = [], []
    for i in range(fenetre, len(valeurs) - fenetre):
        voisins = valeurs[i - fenetre:i] + valeurs[i + 1:i + 1 + fenetre]
        if valeurs[i] <= min(voisins):
            creux.append(i)
        if valeurs[i] >= max(voisins):
            sommets.append(i)
    return creux, sommets
