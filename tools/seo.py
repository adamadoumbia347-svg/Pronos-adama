"""Optimisations pour les moteurs de recherche et les réseaux sociaux (idempotent).

Usage : python3 tools/seo.py   (lancé aussi par tools/publier_article.py)

- image de partage propre à chaque page (og:image, twitter:image) : docs/img/partage/<langue>-<page>.jpg,
  générée par `node tools/partage/rendu.js` ;
- données structurées : fil d'Ariane (BreadcrumbList) sur toutes les pages, WebSite + Organization
  sur l'accueil, Article complété (image, éditeur, date de mise à jour), Article sur les guides,
  WebApplication sur le quiz et le calculateur d'âge ;
- robots.txt avec l'adresse du sitemap ;
- statistiques de visite sans cookies (GoatCounter) sur toutes les pages.
"""
import html
import json
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
SITE = "https://educanimaux.fr"
LANGUES = {"fr": "", "en": "en/", "it": "it/"}
EXCLUES = {"404.html", "bienvenue.html"}
NOM = "Éduc'Animaux"
# Statistiques de visite sans cookies (GoatCounter) : tableau de bord sur https://dobam.goatcounter.com
STATS = ('<!-- stats --><script data-goatcounter="https://dobam.goatcounter.com/count" '
         'async src="https://gc.zgo.at/count.js"></script><!-- /stats -->')
GUIDES = {"chien.html", "chat.html", "nac.html", "methodes.html"}   # pages piliers : données Article
OUTILS = {"quiz.html", "age-humain.html"}                          # outils en ligne : données WebApplication
ORGA = {"@type": "Organization", "name": NOM, "url": SITE + "/", "logo": f"{SITE}/img/partage/fr-index.jpg"}


MOIS = {"fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
        "en": "January February March April May June July August September October November December",
        "it": "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre"}
MAJ = {"fr": "Mis à jour le {}", "en": "Updated {}", "it": "Aggiornato il {}"}


def date_longue(code, iso):
    a, m, j = iso.split("-")
    mois = MOIS[code].split()[int(m) - 1]
    return f"{mois} {int(j)}, {a}" if code == "en" else f"{int(j)} {mois} {a}"


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

            # Date de mise à jour visible sous le titre des articles (reprend dateModified)
            dm = re.search(r'"@type": "Article".*?"dateModified": "([\d-]+)"', s)
            if dm:
                maj = f'<span class="maj"> · {MAJ[code].format(date_longue(code, dm.group(1)))}</span>'
                s = re.sub(r'<span class="maj">.*?</span>', "", s)
                s = re.sub(r'(<p class="meta">.*?)(</p>)', lambda x: x.group(1) + maj + x.group(2), s, count=1, flags=re.S)
            blocs = ""
            if nom == "index.html":
                blocs += ld({"@type": "WebSite", "name": NOM, "url": url(prefixe, nom), "inLanguage": code, "publisher": ORGA})
                blocs += ld(ORGA)
            desc = re.search(r'<meta name="description" content="([^"]*)"', s)
            desc = html.unescape(desc.group(1)) if desc else ""
            titre = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
            titre = re.sub(r"^[^\wÀ-ÿ«]+", "", html.unescape(re.sub(r"<[^>]+>", "", titre.group(1))).strip()) if titre else NOM
            if nom in GUIDES:
                blocs += ld({"@type": "Article", "headline": titre, "description": desc, "inLanguage": code, "image": [image],
                             "author": {"@type": "Organization", "name": NOM, "url": SITE + "/"}, "publisher": ORGA,
                             "mainEntityOfPage": url(prefixe, nom)})
            if nom in OUTILS:
                blocs += ld({"@type": "WebApplication", "name": titre, "description": desc, "url": url(prefixe, nom), "inLanguage": code,
                             "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
                             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": ORGA})
            fil = fil_ariane(s, prefixe, nom)
            if fil:
                blocs += ld(fil)
            bloc = f"<!-- seo -->\n{blocs}  <!-- /seo -->"
            if "<!-- stats -->" in s:
                s = re.sub(r"<!-- stats -->.*?<!-- /stats -->", lambda _: STATS, s, flags=re.S)
            else:
                s = s.replace("</head>", "  " + STATS + "\n</head>", 1)
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
