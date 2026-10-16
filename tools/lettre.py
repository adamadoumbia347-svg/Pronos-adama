"""Prépare l'e-mail de la semaine pour Brevo à partir des derniers articles du site.

Usage : python3 tools/lettre.py [nombre_d_articles=3]
Sortie : lettres/AAAA-MM-JJ.html (à coller dans Brevo : Campagnes > Créer > Éditeur HTML « Coller votre code »).

Les articles sont lus dans docs/conseils.html (les plus récents en premier).
Balises Brevo utilisées : {{ mirror }} (version en ligne) et {{ unsubscribe }} (désinscription).
"""
import datetime
import html
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://educanimaux.fr"
CARTE = re.compile(r'<a class="card card-link" href="([^"]+)">\s*<span class="icon">.*?</span>\s*'
                   r'<span class="tag">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', re.S)
ORANGE, CREME, TEXTE, GRIS, VERT = "#b44c1c", "#fff7ee", "#2b2420", "#6b5d52", "#2f7d6d"
UTM = "?utm_source=brevo&utm_medium=email&utm_campaign=lettre-{date}"


def bloc_article(href, tag, titre, resume, date, premier):
    slug = href[:-5]
    lien = f"{SITE}/{href}{UTM.format(date=date)}"
    image = f"{SITE}/img/partage/fr-{slug}.jpg"
    taille = "22px" if premier else "18px"
    return f"""
          <tr><td style="padding:0 28px 28px">
            <a href="{lien}" style="text-decoration:none"><img src="{image}" width="544" alt="{html.escape(html.unescape(titre), quote=True)}" style="display:block;width:100%;max-width:544px;height:auto;border-radius:14px;border:1px solid #eadfd3"></a>
            <p style="margin:14px 0 4px;font:700 12px/1.4 Arial,Helvetica,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:{VERT}">{tag}</p>
            <h2 style="margin:0 0 8px;font:800 {taille}/1.3 Arial,Helvetica,sans-serif;color:{TEXTE}"><a href="{lien}" style="color:{TEXTE};text-decoration:none">{titre}</a></h2>
            <p style="margin:0 0 14px;font:15px/1.6 Arial,Helvetica,sans-serif;color:{GRIS}">{resume}</p>
            <a href="{lien}" style="display:inline-block;background:{ORANGE};color:#ffffff;font:700 15px/1 Arial,Helvetica,sans-serif;text-decoration:none;padding:13px 22px;border-radius:999px">Lire l'article →</a>
          </td></tr>"""


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    conseils = (RACINE / "docs/conseils.html").read_text(encoding="utf-8")
    articles = CARTE.findall(conseils)[:n]
    date = datetime.date.today().isoformat()
    blocs = "".join(bloc_article(*a, date, i == 0) for i, a in enumerate(articles))
    titres = " · ".join(html.unescape(a[2]) for a in articles)
    contenu = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Les conseils de la semaine – Éduc'Animaux</title></head>
<body style="margin:0;padding:0;background:{CREME}">
<div style="display:none;max-height:0;overflow:hidden">{html.escape(titres)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{CREME}"><tr><td align="center" style="padding:24px 12px">
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:20px;border:1px solid #eadfd3">
    <tr><td style="padding:26px 28px 6px;font:800 24px/1.2 Arial,Helvetica,sans-serif;color:{TEXTE}">🐾 Éduc'<span style="color:{ORANGE}">Animaux</span></td></tr>
    <tr><td style="padding:6px 28px 22px">
      <h1 style="margin:0 0 10px;font:800 26px/1.25 Arial,Helvetica,sans-serif;color:{TEXTE}">Les conseils de la semaine</h1>
      <p style="margin:0;font:16px/1.6 Arial,Helvetica,sans-serif;color:{GRIS}">Bonjour,<br>voici nos nouveaux articles pour éduquer votre animal avec douceur. Bonne lecture, et bonnes séances !</p>
    </td></tr>{blocs}
    <tr><td style="padding:4px 28px 28px">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#e6f3ef;border-radius:14px"><tr><td style="padding:18px 20px;font:15px/1.6 Arial,Helvetica,sans-serif;color:{TEXTE}">
        🧩 <strong>Votre animal a un problème précis ?</strong> Notre <a href="{SITE}/quiz.html{UTM.format(date=date)}" style="color:{VERT};font-weight:700">quiz gratuit</a> vous indique la bonne méthode en 4 questions.
      </td></tr></table>
    </td></tr>
    <tr><td style="padding:18px 28px 26px;border-top:1px solid #eadfd3;font:12px/1.6 Arial,Helvetica,sans-serif;color:#9a8a7e;text-align:center">
      Vous recevez cet e-mail car vous vous êtes inscrit(e) sur <a href="{SITE}" style="color:#9a8a7e">educanimaux.fr</a>.<br>
      Certains liens du site sont des liens d'affiliation : nous pouvons toucher une commission, sans surcoût pour vous.<br>
      <a href="{{{{ mirror }}}}" style="color:#9a8a7e">Voir dans le navigateur</a> · <a href="{{{{ unsubscribe }}}}" style="color:#9a8a7e">Se désinscrire</a>
    </td></tr>
  </table>
</td></tr></table>
</body></html>
"""
    sortie = RACINE / "lettres" / f"{date}.html"
    sortie.write_text(contenu, encoding="utf-8")
    print(f"Lettre écrite : {sortie.relative_to(RACINE)} ({len(articles)} articles : {titres})")


if __name__ == "__main__":
    main()
