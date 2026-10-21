"""Mise en page des courriels (pensés pour l'écran d'un téléphone) et envoi.

Trois modèles :
  - « Ticket de trade »  : signal fort d'ACHAT ou de VENTE, avec graphique de bougies,
                           échelle des prix (stop / entrée / objectifs) et jauge de confluence.
  - « Flash actu »       : actualités fortes, regroupées et notées.
  - « Bilan »            : le signal précédent a touché un objectif ou son stop.

Uniquement du HTML en tableaux et des styles en ligne : c'est ce que Gmail, Outlook
et Apple Mail affichent correctement (pas de SVG, pas de CSS externe).
"""
import html
import json
import os
import smtplib
import ssl
import urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from zoneinfo import ZoneInfo

FOND = "#0b0f17"
CARTE = "#141a26"
LIGNE = "#232c3d"
TEXTE = "#e8ecf3"
DOUX = "#8a95a8"
VERT = "#16e08a"
ROUGE = "#ff4d6d"
OR = "#f7b733"
POLICE = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
CHIFFRES = "'SF Mono',Menlo,Consolas,'Roboto Mono',monospace"


def fuseau():
    try:
        return ZoneInfo(os.environ.get("FUSEAU", "Europe/Paris"))
    except Exception:  # noqa: BLE001
        return timezone.utc


def heure(t):
    return datetime.fromtimestamp(t, fuseau()).strftime("%d/%m %H:%M")


def usd(x, dec=0):
    return f"{x:,.{dec}f} $".replace(",", " ")


def e(t):
    return html.escape(str(t))


def _page(preheader, contenu):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark">
<meta name="supported-color-schemes" content="dark"></head>
<body style="margin:0;padding:0;background:{FOND};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{e(preheader)}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{FOND};">
<tr><td align="center" style="padding:18px 10px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:480px;font-family:{POLICE};color:{TEXTE};">
{contenu}
<tr><td style="padding:22px 8px 6px;font-size:11px;line-height:16px;color:{DOUX};text-align:center;">
Bot Bitcoin 4H · analyse automatique, pas un conseil financier.<br>Ne risquez que ce que vous acceptez de perdre.
</td></tr></table></td></tr></table></body></html>"""


def _graphique(x, n=42, hauteur=120, niveaux=None):
    """Bougies dessinées avec des <div> empilés : chaque colonne = mèche haute, corps, mèche basse."""
    o, h, l, c = (x[k][-n:] for k in ("o", "h", "l", "c"))
    bas, haut = min(l), max(h)
    if niveaux:
        bas, haut = min(bas, *niveaux.values()), max(haut, *niveaux.values())
    echelle = hauteur / (haut - bas or 1)
    px = lambda v: max(0, round((haut - v) * echelle))  # noqa: E731
    cols = []
    for i in range(n):
        couleur = VERT if c[i] >= o[i] else ROUGE
        haut_corps, bas_corps = max(o[i], c[i]), min(o[i], c[i])
        a, b, d = px(h[i]), px(haut_corps), px(bas_corps)
        corps = max(2, d - b)
        meche_h, meche_b = b - a, max(0, px(l[i]) - b - corps)
        derniere = i == n - 1
        fond = f"background:{'#1f2a3d' if derniere else 'transparent'};"
        cols.append(
            f'<td valign="top" style="padding:0 1px;{fond}">'
            f'<div style="height:{a}px;line-height:{a}px;font-size:0;">&nbsp;</div>'
            f'<div style="width:1px;height:{meche_h}px;margin:0 auto;background:{couleur};font-size:0;line-height:0;">&nbsp;</div>'
            f'<div style="height:{corps}px;background:{couleur};border-radius:1px;font-size:0;line-height:0;">&nbsp;</div>'
            f'<div style="width:1px;height:{meche_b}px;margin:0 auto;background:{couleur};font-size:0;line-height:0;">&nbsp;</div>'
            "</td>")
    reperes = ""
    if niveaux:
        lignes = []
        for nom, v in sorted(niveaux.items(), key=lambda kv: -kv[1]):
            coul = ROUGE if nom == "STOP" else OR if nom == "ENTRÉE" else VERT
            lignes.append((px(v), nom, coul))
        cellules, y = [], 0
        for pos, nom, coul in lignes:
            pos = max(pos - 6, y)
            cellules.append(f'<div style="height:{pos - y}px;font-size:0;line-height:0;">&nbsp;</div>'
                            f'<div style="height:12px;font:700 9px/12px {CHIFFRES};color:{coul};white-space:nowrap;">◂ {nom}</div>')
            y = pos + 12
        reperes = f'<td valign="top" width="52" style="padding-left:4px;">{"".join(cellules)}</td>'
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="table-layout:fixed;height:{hauteur}px;">'
            f'<tr>{"".join(cols)}{reperes}</tr></table>')


def _jauge(score, couleur):
    seg = []
    for k in range(10):
        allume = score >= (k + 1) * 10 - 5
        seg.append(f'<td style="padding:0 2px;"><div style="height:10px;border-radius:3px;'
                   f'background:{couleur if allume else LIGNE};font-size:0;line-height:0;">&nbsp;</div></td>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{"".join(seg)}</tr></table>'


def _perforation():
    """Séparateur façon ticket : deux encoches rondes et une ligne pointillée."""
    return (f'<tr><td style="padding:0;background:{CARTE};"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td width="12" style="font-size:0;"><div style="width:24px;height:24px;margin-left:-12px;border-radius:12px;background:{FOND};">&nbsp;</div></td>'
            f'<td style="border-top:2px dashed {LIGNE};font-size:0;line-height:0;">&nbsp;</td>'
            f'<td width="12" style="font-size:0;"><div style="width:24px;height:24px;border-radius:12px;background:{FOND};">&nbsp;</div></td>'
            "</tr></table></td></tr>")


def _bloc(contenu, haut=False, bas=False):
    r = f"border-radius:{'18px 18px' if haut else '0 0'} {'18px 18px' if bas else '0 0'};"
    return f'<tr><td style="background:{CARTE};padding:16px 20px;{r}">{contenu}</td></tr>'


def _historique(stats):
    if not stats["total"]:
        return "Premier signal suivi par le bot."
    return (f"Historique du bot : {stats['total']} signaux clôturés · {stats['gagnants']} gagnants · "
            f"<b style='color:{TEXTE}'>{stats['taux']:.0f} %</b> · {stats['r_total']:+.1f} R cumulés")


def signal(analyse, source, peur, peur_txt, stats, maintenant):
    p = analyse["plan"]
    achat = p["sens"] == 1
    coul = VERT if achat else ROUGE
    mot = "ACHAT" if achat else "VENTE"
    fleche = "▲" if achat else "▼"
    score = analyse["score"]
    qualite = "EXCEPTIONNEL" if score >= 85 else "FORT"
    x = analyse["indic"]
    var24 = 100 * (x["c"][-1] / x["c"][-7] - 1)

    sujet = f"{'🟢' if achat else '🔴'} {mot} {qualite} BTC · {usd(p['entree'])} · {score}/100"
    pre = f"{mot} Bitcoin 4H, score {score}/100. Stop {usd(p['stop'])}, objectif 1 {usd(p['tp1'])}."

    entete = f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};">BTC / USD · BOUGIE 4H</td>
<td align="right" style="font:600 11px/14px {POLICE};color:{DOUX};">{heure(maintenant)}</td></tr></table>
<div style="margin-top:14px;font:900 46px/48px {POLICE};letter-spacing:-1px;color:{coul};">{fleche} {mot}</div>
<div style="margin-top:4px;font:700 13px/18px {POLICE};letter-spacing:3px;color:{TEXTE};">SIGNAL {qualite}</div>
<div style="margin-top:14px;font:700 30px/34px {CHIFFRES};color:{TEXTE};">{usd(p['entree'])}</div>
<div style="font:600 13px/18px {CHIFFRES};color:{VERT if var24 >= 0 else ROUGE};">{var24:+.2f} % sur 24 h</div>"""

    jauge = f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};">CONFLUENCE</td>
<td align="right" style="font:800 20px/22px {CHIFFRES};color:{coul};">{score}<span style="font-size:12px;color:{DOUX};">/100</span></td></tr></table>
<div style="height:8px;font-size:0;">&nbsp;</div>{_jauge(score, coul)}"""

    niveaux = {"OBJ 2": p["tp2"], "OBJ 1": p["tp1"], "ENTRÉE": p["entree"], "STOP": p["stop"]}
    graph = f"""<div style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};margin-bottom:10px;">LES 7 DERNIERS JOURS</div>
{_graphique(x, niveaux=niveaux)}"""

    echelle = []
    for nom, val, c_ in (("Objectif 3", p["tp3"], VERT), ("Objectif 2", p["tp2"], VERT), ("Objectif 1", p["tp1"], VERT),
                         ("Entrée", p["entree"], OR), ("Stop", p["stop"], ROUGE)):
        ecart = 100 * (val / p["entree"] - 1)
        r_mult = {"Objectif 1": "1,5 R", "Objectif 2": "2,5 R", "Objectif 3": "4 R", "Stop": "−1 R"}.get(nom, "")
        echelle.append(
            f'<tr><td style="border-left:4px solid {c_};padding:8px 0 8px 12px;font:600 13px/16px {POLICE};color:{DOUX};">{nom}'
            f'<span style="font-size:11px;"> {r_mult}</span></td>'
            f'<td align="right" style="padding:8px 0;font:700 15px/16px {CHIFFRES};color:{TEXTE};">{usd(val)}</td>'
            f'<td align="right" width="70" style="padding:8px 0;font:600 12px/16px {CHIFFRES};color:{c_};">'
            f'{"" if nom == "Entrée" else f"{ecart:+.1f} %"}</td></tr>')
    plan = f"""<div style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};margin-bottom:6px;">PLAN DE TRADE</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{"".join(echelle)}</table>
<div style="margin-top:12px;padding:10px 12px;border-radius:10px;background:{FOND};font:500 12px/18px {POLICE};color:{DOUX};">
Taille conseillée pour risquer {usd(p['perte_max'])} : <b style="color:{TEXTE};font-family:{CHIFFRES};">{p['taille_btc']:.5f} BTC</b>
(≈ {usd(p['taille_usd'])}).<br>À l'objectif 1, remontez le stop au prix d'entrée : le trade ne peut plus perdre.</div>"""

    lignes = []
    for nom, pts, mx, txt in analyse["criteres"]:
        largeur = round(100 * pts / mx)
        lignes.append(
            f'<tr><td style="padding:5px 0;font:600 12px/15px {POLICE};color:{TEXTE};">{e(nom)}'
            f'<div style="font:400 11px/14px {POLICE};color:{DOUX};">{e(txt)}</div></td>'
            f'<td width="90" style="padding:5px 0 5px 8px;"><div style="background:{LIGNE};border-radius:4px;height:6px;font-size:0;">'
            f'<div style="width:{largeur}%;height:6px;border-radius:4px;background:{coul if pts else LIGNE};font-size:0;">&nbsp;</div></div></td>'
            f'<td width="38" align="right" style="font:700 11px/14px {CHIFFRES};color:{DOUX};">{pts}/{mx}</td></tr>')
    pourquoi = f"""<div style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};margin-bottom:8px;">POURQUOI MAINTENANT</div>
{"".join(f'<div style="font:600 13px/20px {POLICE};color:{TEXTE};">⚡ {e(d)}</div>' for d in analyse["declencheurs"])}
<div style="height:10px;font-size:0;">&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{"".join(lignes)}</table>"""

    meteo = _meteo(peur, peur_txt)
    pied = f"""<div style="font:500 12px/18px {POLICE};color:{DOUX};">{meteo}<br>
Volatilité (ATR 4H) : <b style="color:{TEXTE};font-family:{CHIFFRES};">{usd(p['atr'])}</b> · prix : {e(source)}<br>
{_historique(stats)}</div>"""

    corps = (_bloc(entete, haut=True) + _bloc(jauge) + _perforation() + _bloc(graph) + _bloc(plan)
             + _perforation() + _bloc(pourquoi) + _bloc(pied, bas=True))
    texte = (f"{mot} {qualite} BTC 4H — score {score}/100\nEntrée {usd(p['entree'])}\nStop {usd(p['stop'])}\n"
             f"Obj. 1 {usd(p['tp1'])} · Obj. 2 {usd(p['tp2'])} · Obj. 3 {usd(p['tp3'])}\n"
             "Déclencheurs : " + ", ".join(analyse["declencheurs"]))
    return sujet, _page(pre, corps), texte


def _meteo(peur, peur_txt):
    if peur is None:
        return "Météo du marché : indisponible"
    icone = "⛈️" if peur <= 25 else "🌧️" if peur <= 45 else "⛅" if peur <= 55 else "☀️" if peur <= 75 else "🔥"
    return f"Météo du marché : {icone} <b style='color:{TEXTE}'>{peur}/100</b> ({e(peur_txt)})"


def actus(liste, prix, var4h, maintenant):
    top = liste[0]
    sujet = f"⚡ ACTU FORTE BTC · {top['titre'][:70]}"
    if len(liste) > 1:
        sujet += f" (+{len(liste) - 1})"
    entete = f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{OR};">⚡ FLASH ACTU BITCOIN</td>
<td align="right" style="font:600 11px/14px {POLICE};color:{DOUX};">{heure(maintenant)}</td></tr></table>
<div style="margin-top:12px;font:700 26px/30px {CHIFFRES};color:{TEXTE};">{usd(prix)}
<span style="font-size:14px;color:{VERT if var4h >= 0 else ROUGE};">{var4h:+.2f} % sur 4 h</span></div>"""
    blocs = [_bloc(entete, haut=True)]
    for n, a in enumerate(liste):
        impact = "🔴🔴🔴" if a["score"] >= 9 else "🔴🔴" if a["score"] >= 7 else "🔴"
        badges = "".join(f'<span style="display:inline-block;margin:0 4px 4px 0;padding:2px 8px;border-radius:9px;'
                         f'background:{FOND};font:700 10px/16px {POLICE};color:{OR};">{e(t)}</span>' for t in a["etiquettes"])
        contenu = f"""<div style="font:700 11px/14px {POLICE};color:{DOUX};">IMPACT {impact} · {e(" · ".join(a["sources"]))} · {heure(a["t"])}</div>
<div style="margin:8px 0;font:800 18px/24px {POLICE};color:{TEXTE};">{e(a["titre"])}</div>
<div style="font:400 13px/19px {POLICE};color:{DOUX};margin-bottom:8px;">{e(a["resume"][:220])}</div>
{badges}<div style="margin-top:10px;"><a href="{e(a["lien"])}" style="display:inline-block;padding:10px 16px;border-radius:10px;
background:{OR};color:#111;font:800 13px/16px {POLICE};text-decoration:none;">Lire l'article →</a></div>"""
        blocs.append(_perforation())
        blocs.append(_bloc(contenu, bas=n == len(liste) - 1))
    texte = "\n\n".join(f"[{a['score']}] {a['titre']}\n{a['lien']}" for a in liste)
    return sujet, _page(top["titre"], "".join(blocs)), texte


def bilan(trade, evenement, prix, stats, maintenant):
    r_res = trade.get("r_resultat")
    gagne = r_res > 0 if r_res is not None else evenement != "stop"
    coul = VERT if gagne else ROUGE
    mot = "ACHAT" if trade["sens"] == 1 else "VENTE"
    titres = {"tp1": "OBJECTIF 1 ATTEINT", "tp2": "OBJECTIF 2 ATTEINT", "tp3": "OBJECTIF 3 ATTEINT · TRADE CLÔTURÉ",
              "stop": "STOP TOUCHÉ" if not trade.get("tp1_touche") else "SORTIE AU PRIX D'ENTRÉE",
              "inverse": "SIGNAL INVERSE · TRADE CLÔTURÉ", "temps": "TRADE CLÔTURÉ APRÈS 7 JOURS"}
    conseils = {"tp1": "Prenez une partie des gains et remontez le stop au prix d'entrée.",
                "tp2": "Encaissez une deuxième partie, laissez courir le reste vers l'objectif 3.",
                "tp3": "Objectif final atteint. Bravo, trade terminé.",
                "stop": "Le stop a fait son travail : la perte reste limitée à ce qui était prévu.",
                "inverse": "Le marché s'est retourné : le bot ferme ce trade et suit le nouveau signal.",
                "temps": "Le trade n'a pas abouti en 7 jours : le bot le ferme au prix du marché."}
    sujet = f"{'✅' if gagne else '❌'} BTC {mot} · {titres[evenement]} · {usd(prix)}"
    contenu = f"""<div style="font:700 11px/14px {POLICE};letter-spacing:2px;color:{DOUX};">SUIVI DU SIGNAL DU {heure(trade['t'])}</div>
<div style="margin-top:12px;font:900 26px/30px {POLICE};color:{coul};">{titres[evenement]}</div>
<div style="margin-top:10px;font:700 24px/28px {CHIFFRES};color:{TEXTE};">{usd(prix)}</div>
<div style="font:500 13px/18px {POLICE};color:{DOUX};">{mot} ouvert à {usd(trade['entree'])}
{f" · résultat {r_res:+.1f} R" if r_res is not None else ""}</div>
<div style="margin-top:14px;padding:10px 12px;border-radius:10px;background:{FOND};font:500 13px/19px {POLICE};color:{TEXTE};">{conseils[evenement]}</div>"""
    corps = _bloc(contenu, haut=True) + _perforation() + _bloc(
        f'<div style="font:500 12px/18px {POLICE};color:{DOUX};">{_historique(stats)}</div>', bas=True)
    return sujet, _page(titres[evenement], corps), f"{titres[evenement]} — {usd(prix)}"


def envoyer(sujet, html_, texte, priorite=False):
    """Envoie par courriel (SMTP) et, si NTFY_SUJET est défini, une notification push sur le téléphone."""
    exp, mdp = os.environ.get("MAIL_EXPEDITEUR"), os.environ.get("MAIL_MOT_DE_PASSE")
    dest = os.environ.get("MAIL_DESTINATAIRE") or exp
    envoye = False
    if exp and mdp:
        msg = EmailMessage()
        msg["Subject"], msg["From"], msg["To"] = sujet, f"Bot Bitcoin 4H <{exp}>", dest
        if priorite:
            msg["X-Priority"], msg["Importance"] = "1", "high"
        msg.set_content(texte)
        msg.add_alternative(html_, subtype="html")
        hote = os.environ.get("SMTP_HOTE", "smtp.gmail.com")
        port = int(os.environ.get("SMTP_PORT", "465"))
        with smtplib.SMTP_SSL(hote, port, context=ssl.create_default_context(), timeout=30) as s:
            s.login(exp, mdp)
            s.send_message(msg)
        envoye = True
        print(f"  courriel envoyé à {dest} : {sujet}")
    sujet_ntfy = os.environ.get("NTFY_SUJET")
    if sujet_ntfy:
        corps = json.dumps({"topic": sujet_ntfy, "title": sujet, "message": texte,
                            "priority": 5 if priorite else 3}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/", data=corps), timeout=15).read()
            envoye = True
            print("  notification ntfy envoyée")
        except Exception as ex:  # noqa: BLE001
            print(f"  ntfy indisponible : {ex}")
    if not envoye:
        print("  (aucun envoi : MAIL_EXPEDITEUR / MAIL_MOT_DE_PASSE non configurés)")
    return envoye


def sauver_apercu(dossier, nom, sujet, html_):
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom + ".html")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html_.replace("<body", f"<!-- Objet : {e(sujet)} --><body", 1))
    return chemin
