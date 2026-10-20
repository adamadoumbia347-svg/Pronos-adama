"""Ajoute un bloc « À lire aussi » (3 articles liés) en bas de chaque article, dans chaque langue.

Usage : python3 tools/lire_aussi.py

Les articles sont lus dans la page Conseils de chaque langue (cartes .card-link) :
on propose d'abord les articles de la même catégorie, puis les plus récents.
En français, un encadré « promos du moment » précède ce bloc.
Le script est idempotent (bloc entre <!-- lire-aussi --> et <!-- /lire-aussi -->).
"""
import html
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
DOSSIERS = {"fr": DOCS, "en": DOCS / "en", "it": DOCS / "it"}
TITRE = {"fr": "À lire aussi", "en": "Read next", "it": "Leggi anche"}
# Encadré « promos du moment » placé avant « À lire aussi » (pages françaises : la page promos n'existe qu'en français)
PROMO = {"fr": '        <div class="callout encadre-promo"><span><strong>🏷️ Bons plans :</strong> retrouvez les offres du jour et les meilleures ventes animalerie, '
               'mises à jour en direct.</span> <a class="btn btn-sm" href="promos-animaux.html">Voir les promos du moment</a> <a class="btn btn-sm btn-outline" href="produits-tendance-animaux.html">Produits tendance</a></div>\n'}
CARTE = re.compile(
    r'<a class="card card-link" href="([^"]+)">\s*<span class="icon">(.*?)</span>\s*'
    r'<span class="tag">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</a>', re.S)


def main():
    total = 0
    for code, dossier in DOSSIERS.items():
        conseils = (dossier / "conseils.html").read_text(encoding="utf-8")
        cartes = [dict(zip(("href", "icone", "tag", "titre", "resume"), m)) for m in CARTE.findall(conseils)]
        for i, c in enumerate(cartes):
            page = dossier / c["href"]
            if not page.exists():
                continue
            autres = [x for x in cartes if x["href"] != c["href"]]
            meme = [x for x in autres if x["tag"] == c["tag"]]
            choix = (meme + [x for x in autres if x not in meme])[:3]
            blocs = "".join(
                f'\n          <a class="card card-link" href="{x["href"]}"><span class="icon">{x["icone"]}</span>'
                f'<h3>{x["titre"]}</h3><p>{x["resume"]}</p></a>' for x in choix)
            promo = PROMO.get(code, "") if c["href"] != "promos-animaux.html" else ""
            section = (f'<!-- lire-aussi -->\n    <section class="lire-aussi" style="padding-top:0">\n      <div class="container">\n{promo}'
                       f'        <h2>{html.escape(TITRE[code])}</h2>\n        <div class="grid grid-3">{blocs}\n        </div>\n'
                       f'      </div>\n    </section>\n    <!-- /lire-aussi -->')
            s = page.read_text(encoding="utf-8")
            if "<!-- lire-aussi -->" in s:
                s = re.sub(r"<!-- lire-aussi -->.*?<!-- /lire-aussi -->", lambda _: section, s, flags=re.S)
            else:
                s = s.replace("\n  </main>", "\n    " + section + "\n  </main>", 1)
            page.write_text(s, encoding="utf-8")
            total += 1
    print(f"« À lire aussi » mis à jour sur {total} articles.")


if __name__ == "__main__":
    main()
