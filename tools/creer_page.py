"""Crée ou met à jour une page « outil » ou « guide » du site (hors articles), dans une langue donnée.

Usage depuis Python :
    import creer_page
    creer_page.creer("fr", "aliments-chien-chat", titre, description, corps_html,
                     scripts=["js/aliments.js"], menu="🍎 Peut-il manger… ?")

La page reprend l'en-tête, le menu et le pied de page du modèle (docs/<langue>/rappel-chien.html),
sans données structurées Article. Avec `menu`, un lien est ajouté dans la colonne « Guides » du
pied de page de toutes les pages de la langue. Lancer ensuite `finir()` une seule fois
(images de partage, SEO, langues, sitemap, recherche).
"""
import html
import os
import pathlib
import re
import subprocess

import langues
import recherche
import seo

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
BASE = "https://educanimaux.fr/"


def dossier(lang):
    return DOCS / lang if lang != "fr" else DOCS


def creer(lang, slug, titre, description, corps, scripts=(), menu=None):
    modele = (dossier(lang) / "rappel-chien.html").read_text(encoding="utf-8")
    entete = modele[: modele.index("<main>")]
    pied = modele[modele.index("</main>") + len("</main>"):]
    titre_page = f"{titre} – Éduc'Animaux" if len(titre) <= 50 else titre
    url = BASE + ("" if lang == "fr" else lang + "/") + slug + ".html"
    e = lambda x: html.escape(x, quote=True)
    entete = re.sub(r"<title>.*?</title>", lambda _: f"<title>{e(titre_page)}</title>", entete)
    entete = re.sub(r'<meta name="description" content=".*?">', lambda _: f'<meta name="description" content="{e(description)}">', entete)
    entete = re.sub(r'<link rel="canonical" href=".*?">', lambda _: f'<link rel="canonical" href="{url}">', entete)
    entete = re.sub(r'<meta property="og:title" content=".*?">', lambda _: f'<meta property="og:title" content="{e(titre_page)}">', entete)
    entete = re.sub(r'<meta property="og:description" content=".*?">', lambda _: f'<meta property="og:description" content="{e(description)}">', entete)
    entete = re.sub(r'<meta property="og:url" content=".*?">', lambda _: f'<meta property="og:url" content="{url}">', entete)
    entete = entete.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    # Pas de données Article : seo.py ajoute le fil d'Ariane (et WebApplication pour les outils)
    entete = re.sub(r'\s*<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Article".*?</script>', "", entete, flags=re.S)
    entete = re.sub(r"<!-- seo -->.*?<!-- /seo -->", "<!-- seo -->\n  <!-- /seo -->", entete, flags=re.S)
    for js in scripts:
        src = ("../" if lang != "fr" else "") + js
        pied = pied.replace("</body>", f'  <script src="{src}" defer></script>\n</body>', 1)
    (dossier(lang) / f"{slug}.html").write_text(entete + "<main>\n" + corps.rstrip() + "\n  </main>" + pied, encoding="utf-8")
    if menu:
        ajouter_au_pied(lang, slug, menu)


def ajouter_au_pied(lang, slug, libelle):
    """Lien dans la colonne « Guides » du pied de page, juste après le calculateur d'âge."""
    d = dossier(lang)
    for p in [*d.glob("*.html")]:
        s = p.read_text(encoding="utf-8")
        if f'<li><a href="{slug}.html">' in s:
            continue
        s2 = re.sub(r'(<li><a href="age-humain\.html">[^<]*</a></li>)', lambda m: m.group(1) + f'\n            <li><a href="{slug}.html">{libelle}</a></li>', s, count=1)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")


def finir():
    try:
        racine = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        subprocess.run(["node", str(pathlib.Path(__file__).parent / "partage" / "rendu.js")], check=True,
                       env={**os.environ, "NODE_PATH": racine}, capture_output=True)
    except Exception as ex:
        print("Images de partage non régénérées :", ex)
    seo.main()
    langues.main()
    recherche.main()
