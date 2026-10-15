"""Vérifie le site : liens internes, ancres, liens d'affiliation, langues et sitemap.

Usage : python3 tools/verifier_site.py   (code de sortie 1 en cas de problème)
"""
import pathlib
import posixpath
import sys
import xml.dom.minidom
from html.parser import HTMLParser
from urllib.parse import urlparse

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
BASE = "https://educanimaux.fr/"
DOMAINES_AMAZON = {"www.amazon.fr", "www.amazon.it", "www.amazon.es", "www.amazon.de",
                   "www.amazon.co.uk", "www.amazon.com", "www.amazon.ca"}
LANGUE_DU_DOSSIER = {"": "fr", "en": "en", "it": "it"}


class Analyse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.liens, self.dans_lien, self.erreurs = set(), [], 0, []
        self.lang, self.assets = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "a":
            if self.dans_lien:
                self.erreurs.append("lien <a> imbriqué dans un autre lien")
            self.dans_lien += 1
        if tag == "li" and self.dans_lien:
            self.erreurs.append("<li> à l'intérieur d'un lien <a>")
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.liens.append(a)
        if tag == "link" and a.get("rel") == "stylesheet" and not a["href"].startswith("http"):
            self.assets.append(a["href"])
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])

    def handle_endtag(self, tag):
        if tag == "a" and self.dans_lien:
            self.dans_lien -= 1


def main():
    pages = {p.relative_to(DOCS).as_posix(): p for p in DOCS.rglob("*.html")}
    analyses = {}
    for nom, p in pages.items():
        an = Analyse()
        an.feed(p.read_text(encoding="utf-8"))
        analyses[nom] = an
    problemes, nb_aff = [], 0
    for nom, an in analyses.items():
        dossier = posixpath.dirname(nom)
        attendu = LANGUE_DU_DOSSIER.get(dossier)
        if attendu and an.lang != attendu:
            problemes.append(f"{nom} : lang=\"{an.lang}\" au lieu de \"{attendu}\"")
        for err in sorted(set(an.erreurs)):
            problemes.append(f"{nom} : {err}")
        for asset in an.assets:
            if not (DOCS / posixpath.normpath(posixpath.join(dossier, asset))).exists():
                problemes.append(f"{nom} : fichier introuvable {asset}")
        for a in an.liens:
            href = a["href"]
            if "aff" in a.get("class", "").split():
                nb_aff += 1
                u = urlparse(href)
                if u.netloc not in DOMAINES_AMAZON or u.path != "/s" or not a.get("data-q") or not a.get("data-aff"):
                    problemes.append(f"{nom} : lien d'affiliation mal formé ({href})")
                continue
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            fichier, _, ancre = href.partition("#")
            fichier = fichier.split("?")[0]
            cible = posixpath.normpath(posixpath.join(dossier, fichier)) if fichier else nom
            if cible not in pages:
                problemes.append(f"{nom} : lien cassé vers {href}")
            elif ancre and ancre not in analyses[cible].ids:
                problemes.append(f"{nom} : ancre #{ancre} absente de {cible}")
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    xml.dom.minidom.parseString(sitemap)
    for nom in pages:
        dossier, fichier = posixpath.split(nom)
        loc = BASE + (dossier + "/" if dossier else "") + ("" if fichier == "index.html" else fichier)
        if f"<loc>{loc}</loc>" not in sitemap:
            problemes.append(f"sitemap.xml : {nom} absent")
    print(f"{len(pages)} pages, {nb_aff} liens d'affiliation vérifiés.")
    if problemes:
        print("PROBLÈMES :\n" + "\n".join(problemes))
        sys.exit(1)
    print("Aucun problème.")


if __name__ == "__main__":
    main()
