"""Construit l'index de la recherche du site : docs/recherche.json, docs/en/recherche.json, docs/it/recherche.json.

Usage : python3 tools/recherche.py   (lancé aussi par tools/publier_article.py)
Pour chaque page : titre (h1), description, intertitres et début du texte, utilisés par la recherche de docs/js/main.js.
"""
import html
import json
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
LANGUES = {"fr": DOCS, "en": DOCS / "en", "it": DOCS / "it"}
EXCLUES = {"404.html", "mentions-legales.html", "bienvenue.html"}


def texte(fragment):
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def main():
    total = 0
    for code, dossier in LANGUES.items():
        index = []
        for p in sorted(dossier.glob("*.html")):
            if p.name in EXCLUES:
                continue
            s = p.read_text(encoding="utf-8")
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
            desc = re.search(r'<meta name="description" content="([^"]*)"', s)
            principal = s[s.find("<main>"):s.find("</main>")]
            principal = re.sub(r"<!-- lire-aussi -->.*?<!-- /lire-aussi -->", " ", principal, flags=re.S)
            intertitres = [texte(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", principal, re.S)]
            index.append({
                "u": p.name if p.name != "index.html" else "./",
                "t": texte(h1.group(1)) if h1 else p.stem,
                "d": html.unescape(desc.group(1)) if desc else "",
                "h": " · ".join(intertitres)[:600],
                "x": texte(principal)[:2500],
            })
        (dossier / "recherche.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        total += len(index)
    print(f"Recherche : {total} pages indexées.")


if __name__ == "__main__":
    main()
