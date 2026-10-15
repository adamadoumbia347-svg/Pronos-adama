"""Vérifie le site : liens internes, ancres, liens d'affiliation, sitemap.

Usage : python3 tools/verifier_site.py   (code de sortie 1 en cas de problème)
"""
import pathlib
import sys
import xml.dom.minidom
from html.parser import HTMLParser
from urllib.parse import urlparse

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"


class Analyse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.liens, self.pile = set(), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.liens.append(a)


def main():
    pages = {p.name: p for p in DOCS.glob("*.html")}
    analyses = {}
    for nom, p in pages.items():
        an = Analyse()
        an.feed(p.read_text(encoding="utf-8"))
        analyses[nom] = an
    problemes, nb_aff = [], 0
    for nom, an in analyses.items():
        for a in an.liens:
            href = a["href"]
            if "aff" in a.get("class", "").split():
                nb_aff += 1
                u = urlparse(href)
                if u.netloc != "www.amazon.fr" or u.path != "/s" or not a.get("data-q") or not a.get("data-aff"):
                    problemes.append(f"{nom} : lien d'affiliation mal formé ({href})")
                continue
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            fichier, _, ancre = href.partition("#")
            fichier = fichier.split("?")[0] or nom
            if fichier not in pages:
                problemes.append(f"{nom} : lien cassé vers {href}")
            elif ancre and ancre not in analyses[fichier].ids:
                problemes.append(f"{nom} : ancre #{ancre} absente de {fichier}")
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    xml.dom.minidom.parseString(sitemap)
    for nom in pages:
        loc = "https://educanimaux.fr/" + ("" if nom == "index.html" else nom)
        if f"<loc>{loc}</loc>" not in sitemap:
            problemes.append(f"sitemap.xml : {nom} absent")
    print(f"{len(pages)} pages, {nb_aff} liens d'affiliation vérifiés.")
    if problemes:
        print("PROBLÈMES :\n" + "\n".join(problemes))
        sys.exit(1)
    print("Aucun problème.")


if __name__ == "__main__":
    main()
