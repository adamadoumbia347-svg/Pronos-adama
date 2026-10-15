"""Publie un article à partir d'un fichier source (métadonnées + corps HTML).

Usage : python3 tools/publier_article.py articles/AAAA-MM-JJ-slug.html

Le fichier source commence par des lignes « clé: valeur », puis une ligne
« --- », puis le contenu HTML de l'article (une <section class="page-hero">
contenant <div class="container article">…</div>).

Clés obligatoires : slug, titre, titre_court, description, resume, icone,
categorie, date (AAAA-MM-JJ).

Le script :
  - crée docs/<slug>.html avec l'en-tête, le menu et le pied de page du site,
    les balises Google / réseaux sociaux et les données structurées Article ;
  - ajoute la carte de l'article en tête de docs/conseils.html ;
  - met l'article en tête des « derniers conseils » de docs/index.html (4 max) ;
  - ajoute l'adresse dans docs/sitemap.xml.
"""
import html
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
BASE = "https://educanimaux.fr/"
MODELE = DOCS / "rappel-chien.html"
CLES = ["slug", "titre", "titre_court", "description", "resume", "icone", "categorie", "date"]


def lire_source(chemin):
    texte = pathlib.Path(chemin).read_text(encoding="utf-8")
    meta, corps = texte.split("\n---\n", 1)
    m = dict(l.split(":", 1) for l in meta.strip().splitlines() if l.strip())
    m = {k.strip(): v.strip() for k, v in m.items()}
    manquantes = [k for k in CLES if not m.get(k)]
    if manquantes:
        sys.exit(f"Clés manquantes : {', '.join(manquantes)}")
    if not re.fullmatch(r"[a-z0-9-]+", m["slug"]):
        sys.exit("Le slug ne doit contenir que des minuscules, chiffres et tirets.")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m["date"]):
        sys.exit("La date doit être au format AAAA-MM-JJ.")
    return m, corps.strip()


def construire_page(m, corps):
    modele = MODELE.read_text(encoding="utf-8")
    entete = modele[: modele.index("<main>")]
    pied = modele[modele.index("</main>") + len("</main>"):]
    titre_page = f"{m['titre']} – Éduc'Animaux"
    url = BASE + m["slug"] + ".html"
    e = lambda x: html.escape(x, quote=True)
    entete = re.sub(r"<title>.*?</title>", f"<title>{e(titre_page)}</title>", entete)
    entete = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{e(m["description"])}">', entete)
    entete = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{url}">', entete)
    entete = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{e(titre_page)}">', entete)
    entete = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{e(m["description"])}">', entete)
    entete = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{url}">', entete)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": m["titre"],
          "description": m["description"], "inLanguage": "fr", "datePublished": m["date"],
          "author": {"@type": "Organization", "name": "Éduc'Animaux"}}
    entete = re.sub(r'<script type="application/ld\+json">.*?</script>',
                    lambda _: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
                    entete, flags=re.S)
    return entete + "<main>\n" + corps + "\n  </main>" + pied


def ajouter_a_conseils(m):
    p = DOCS / "conseils.html"
    s = p.read_text(encoding="utf-8")
    if f'href="{m["slug"]}.html"' in s:
        return
    carte = (f'          <a class="card card-link" href="{m["slug"]}.html">\n'
             f'            <span class="icon">{m["icone"]}</span>\n'
             f'            <span class="tag">{html.escape(m["categorie"])}</span>\n'
             f'            <h3>{html.escape(m["titre"])}</h3>\n'
             f'            <p>{html.escape(m["resume"])}</p>\n'
             f'          </a>\n')
    repere = '        <div class="grid grid-2">\n'
    if repere not in s:
        sys.exit("Grille introuvable dans conseils.html")
    p.write_text(s.replace(repere, repere + carte, 1), encoding="utf-8")


def ajouter_a_accueil(m):
    p = DOCS / "index.html"
    s = p.read_text(encoding="utf-8")
    debut = s.index("<h2>Nos derniers conseils</h2>")
    g0 = s.index('<div class="grid grid-4" style="margin-top:22px">\n', debut)
    g0 = s.index("\n", g0) + 1
    g1 = s.index("        </div>", g0)
    cartes = [l for l in s[g0:g1].splitlines() if 'class="card card-link"' in l]
    if any(f'href="{m["slug"]}.html"' in c for c in cartes):
        return
    nouvelle = (f'          <a class="card card-link" href="{m["slug"]}.html"><span class="icon">{m["icone"]}</span>'
                f'<h3>{html.escape(m["titre_court"])}</h3></a>')
    cartes = [nouvelle] + cartes[:3]
    p.write_text(s[:g0] + "\n".join(cartes) + "\n" + s[g1:], encoding="utf-8")


def ajouter_au_sitemap(m):
    p = DOCS / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    url = BASE + m["slug"] + ".html"
    if f"<loc>{url}</loc>" in s:
        return
    ligne = f"  <url><loc>{url}</loc><lastmod>{m['date']}</lastmod><priority>0.7</priority></url>\n"
    p.write_text(s.replace("</urlset>", ligne + "</urlset>"), encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    m, corps = lire_source(sys.argv[1])
    cible = DOCS / f"{m['slug']}.html"
    if cible.exists():
        sys.exit(f"{cible.name} existe déjà : choisissez un autre slug.")
    cible.write_text(construire_page(m, corps), encoding="utf-8")
    ajouter_a_conseils(m)
    ajouter_a_accueil(m)
    ajouter_au_sitemap(m)
    print(f"Publié : docs/{cible.name}")


if __name__ == "__main__":
    main()
