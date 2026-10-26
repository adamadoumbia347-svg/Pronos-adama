"""Relie les guides (chien.html, chat.html) aux articles qui les approfondissent (idempotent).

Usage : python3 tools/guides.py   (lancé aussi par tools/publier_article.py)

Pour chaque langue (fr, en, it) :
  - dans les sections du guide, un paragraphe « À lire » vers les articles du même sujet
    (seulement ceux qui existent dans la langue) ;
  - en bas du guide, un bloc « Tous nos articles sur le chien / le chat » avec les cartes
    de docs/<langue>/conseils.html, classées d'après leur catégorie ;
  - sur la page Matériel, la liste de tous les comparatifs (pages « meilleur… »).
"""
import html
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
LANGUES = {"fr": "", "en": "en/", "it": "it/"}
CATEGORIES = {"chien": {"Chien", "Chiot", "Dog", "Puppy", "Cane", "Cucciolo"}, "chat": {"Chat", "Chaton", "Cat", "Kitten", "Gatto", "Gattino"}}
# Pages de bons plans : utiles, mais hors sujet dans un guide d'éducation
EXCLUES = {"black-friday-animaux.html", "promos-animaux.html", "produits-tendance-animaux.html"}
COMMUNES = {"idees-cadeaux-noel-chien-chat.html"}   # dans les deux guides
# Sections du guide → articles liés (repère : id de la carte, ou emoji du titre <h2> de la carte)
SECTIONS = {
    "chien": {
        "chiot": ["kit-accueil-chiot"],
        "proprete": ["proprete-chiot"],
        "assis-couche": ["apprendre-assis-couche-pas-bouger", "meilleures-friandises-education-chien", "meilleure-pochette-friandises"],
        "rappel": ["rappel-chien"],
        "laisse": ["marche-en-laisse", "meilleur-harnais-chien"],
        "solitude": ["chien-aboie-seul", "meilleurs-jouets-occupation-chien", "meilleure-camera-animaux"],
        "aboiements": ["chien-aboie-seul"],
        "mordille": ["chiot-mord"],
    },
    "chat": {
        "🪣": ["chat-urine-hors-litiere", "meilleure-litiere-chat"],
        "💅": ["chat-griffe-canape", "meilleur-griffoir-chat"],
        "🔘": ["meilleur-clicker"],
        "🎣": ["chat-miaule-la-nuit"],
    },
}
TXT = {
    "fr": {"lire": "👉 À lire :", "chien": "Tous nos articles sur le chien", "chat": "Tous nos articles sur le chat",
           "intro": "Nos articles détaillés, étape par étape, et nos comparatifs pour bien choisir le matériel.",
           "comparatifs": "Nos comparatifs pour bien choisir"},
    "en": {"lire": "👉 Read:", "chien": "All our dog articles", "chat": "All our cat articles",
           "intro": "Our detailed step-by-step articles, and our comparisons to help you choose the right gear.",
           "comparatifs": "Our comparisons to help you choose"},
    "it": {"lire": "👉 Da leggere:", "chien": "Tutti i nostri articoli sul cane", "chat": "Tutti i nostri articoli sul gatto",
           "intro": "I nostri articoli dettagliati passo dopo passo e i confronti per scegliere l'attrezzatura giusta.",
           "comparatifs": "I nostri confronti per scegliere bene"},
}
CARTE = re.compile(r'<a class="card card-link" href="([^"]+)">\s*<span class="icon">(.*?)</span>\s*<span class="tag">([^<]*)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</a>', re.S)


def cartes(dossier):
    s = (dossier / "conseils.html").read_text(encoding="utf-8")
    return [dict(zip(("href", "icone", "tag", "titre", "resume"), m.groups())) for m in CARTE.finditer(s)]


def voir_aussi(code, liste, titres):
    liens = " · ".join(f'<a href="{c}.html">{titres[c + ".html"]}</a>' for c in liste if c + ".html" in titres)
    return f'            <p class="voir-aussi">{TXT[code]["lire"]} {liens}</p>\n' if liens else ""


def main():
    n = 0
    for code, prefixe in LANGUES.items():
        dossier = DOCS / prefixe
        toutes = cartes(dossier)
        titres = {c["href"]: c["titre"] for c in toutes}
        for guide, sections in SECTIONS.items():
            p = dossier / f"{guide}.html"
            s = avant = p.read_text(encoding="utf-8")
            s = re.sub(r'            <p class="voir-aussi">.*?</p>\n', "", s)
            # liens dans les sections
            def section(m):
                carte = m.group(0)
                ident = re.search(r'id="([^"]+)"', carte.split(">", 1)[0])
                h2 = re.search(r"<h2>\s*(\S+)", carte)
                cle = ident.group(1) if ident and ident.group(1) in sections else (h2.group(1) if h2 and h2.group(1) in sections else None)
                if not cle:
                    return carte
                return carte.replace("          </article>", voir_aussi(code, sections[cle], titres) + "          </article>")
            s = re.sub(r'          <article class="card".*?          </article>', section, s, flags=re.S)
            # bloc des articles en bas du guide
            liste = [c for c in toutes if c["href"] not in EXCLUES and (c["tag"] in CATEGORIES[guide] or c["href"] in COMMUNES)]
            cartes_html = "".join(f'          <a class="card card-link" href="{c["href"]}"><h3>{c["titre"]}</h3><p>{c["resume"]}</p></a>\n' for c in liste)
            bloc = (f'<!-- articles-guide -->\n    <section id="articles">\n      <div class="container">\n'
                    f'        <h2>📚 {TXT[code][guide]}</h2>\n        <p>{TXT[code]["intro"]}</p>\n'
                    f'        <div class="grid grid-2">\n{cartes_html}        </div>\n      </div>\n    </section>\n    <!-- /articles-guide -->')
            if "<!-- articles-guide -->" in s:
                s = re.sub(r"<!-- articles-guide -->.*?<!-- /articles-guide -->", lambda _: bloc, s, flags=re.S)
            else:
                s = s.replace("  </main>", "    " + bloc + "\n  </main>", 1)
            if s != avant:
                p.write_text(s, encoding="utf-8")
                n += 1
        # page Matériel : tous les comparatifs (pages « meilleur… »)
        p = dossier / "materiel.html"
        s = avant = p.read_text(encoding="utf-8")
        comp = "".join(f'          <a class="card card-link" href="{c["href"]}"><span class="icon">{c["icone"]}</span>'
                       f'<h3>{c["titre"]}</h3><p>{c["resume"]}</p></a>\n' for c in toutes if c["href"].startswith("meilleur"))
        bloc = (f'<!-- comparatifs -->\n        <h2>{TXT[code]["comparatifs"]}</h2>\n'
                f'        <div class="grid grid-3" style="margin-bottom:50px">\n{comp}        </div>\n        <!-- /comparatifs -->')
        if "<!-- comparatifs -->" in s:
            s = re.sub(r"<!-- comparatifs -->.*?<!-- /comparatifs -->", lambda _: bloc, s, flags=re.S)
        else:
            s = s.replace("<!-- /materiel-plus -->\n", "<!-- /materiel-plus -->\n        " + bloc + "\n", 1)
        if s != avant:
            p.write_text(s, encoding="utf-8")
            n += 1
    print(f"Guides : {n} pages mises à jour.")


if __name__ == "__main__":
    main()
