"""Optimisations pour les moteurs de recherche et les réseaux sociaux (idempotent).

Usage : python3 tools/seo.py   (lancé aussi par tools/publier_article.py)

- image de partage propre à chaque page (og:image, twitter:image) : docs/img/partage/<langue>-<page>.jpg,
  générée par `node tools/partage/rendu.js` ;
- données structurées : fil d'Ariane (BreadcrumbList) sur toutes les pages, WebSite + Organization
  sur l'accueil, Article complété (image, éditeur, date de mise à jour) ;
- robots.txt avec l'adresse du sitemap.
"""
import html
import json
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
SITE = "https://educanimaux.fr"
LANGUES = {"fr": "", "en": "en/", "it": "it/"}
EXCLUES = {"404.html"}
NOM = "Éduc'Animaux"
ORGA = {"@type": "Organization", "name": NOM, "url": SITE + "/", "logo": f"{SITE}/img/partage/fr-index.jpg"}


def url(prefixe, nom):
    return f"{SITE}/{prefixe}" + ("" if nom == "index.html" else nom)


def ld(obj):
    return '  <script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", **obj}, ensure_ascii=False) + "</script>\n"


def fil_ariane(s, prefixe, nom):
    m = re.search(r'<p class="breadcrumb">(.*?)</p>', s, re.S)
    if not m:
        return None
    morceaux = [x.strip() for x in m.group(1).split("›")]
    elements = []
    for i, x in enumerate(morceaux, 1):
        lien = re.search(r'href="([^"]+)"[^>]*>(.*?)</a>', x)
        if lien:
            cible = lien.group(1).split("#")[0]
            nom_lien, adresse = lien.group(2), url(prefixe, cible)
        else:
            nom_lien, adresse = x, url(prefixe, nom)
        elements.append({"@type": "ListItem", "position": i, "name": html.unescape(re.sub(r"<[^>]+>", "", nom_lien)).strip(), "item": adresse})
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def main():
    n = 0
    for code, prefixe in LANGUES.items():
        for chemin in sorted((DOCS / prefixe).glob("*.html")):
            nom = chemin.name
            if nom in EXCLUES:
                continue
            s = chemin.read_text(encoding="utf-8")
            avant = s
            image = f"{SITE}/img/partage/{code}-{nom[:-5]}.jpg"
            if (DOCS / "img/partage" / f"{code}-{nom[:-5]}.jpg").exists():
                s = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{image}">', s)
                if 'name="twitter:image"' in s:
                    s = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{image}">', s)
                else:
                    s = s.replace('<meta name="twitter:card" content="summary_large_image">',
                                  f'<meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:image" content="{image}">', 1)
            else:
                image = f"{SITE}/img/partage.png"

            # Article : compléter les champs recommandés par Google
            def article(m):
                d = json.loads(m.group(1))
                if d.get("@type") != "Article":
                    return m.group(0)
                d["image"] = [image]
                d.setdefault("dateModified", d.get("datePublished"))
                d["author"] = {"@type": "Organization", "name": NOM, "url": SITE + "/"}
                d["publisher"] = ORGA
                d["mainEntityOfPage"] = url(prefixe, nom)
                return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
            s = re.sub(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "Article".*?)</script>', article, s)

            blocs = ""
            if nom == "index.html":
                blocs += ld({"@type": "WebSite", "name": NOM, "url": url(prefixe, nom), "inLanguage": code, "publisher": ORGA})
                blocs += ld(ORGA)
            fil = fil_ariane(s, prefixe, nom)
            if fil:
                blocs += ld(fil)
            bloc = f"<!-- seo -->\n{blocs}  <!-- /seo -->"
            if "<!-- seo -->" in s:
                s = re.sub(r"<!-- seo -->.*?<!-- /seo -->", lambda _: bloc, s, flags=re.S)
            else:
                s = s.replace("<!-- langues -->", bloc + "\n<!-- langues -->", 1)
            if s != avant:
                chemin.write_text(s, encoding="utf-8")
                n += 1
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"SEO : {n} pages mises à jour, robots.txt écrit.")


if __name__ == "__main__":
    main()
