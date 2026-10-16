"""Relie entre elles les versions française, anglaise et italienne du site.

Usage : python3 tools/langues.py

Pour chaque page de docs/ (français), docs/en/ (anglais) et docs/it/ (italien) :
  - ajoute dans <head> les balises hreflang vers les versions existantes ;
  - ajoute le sélecteur de langue FR · EN · IT dans l'en-tête (vers la même page
    dans l'autre langue si elle existe, sinon vers l'accueil de cette langue) ;
puis régénère docs/sitemap.xml avec toutes les pages et leurs équivalents.

Le script est idempotent : on peut le relancer après chaque ajout de page.
"""
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
BASE = "https://educanimaux.fr/"
LANGUES = {"fr": "", "en": "en/", "it": "it/"}  # code -> sous-dossier
ETIQUETTES = {"fr": "FR", "en": "EN", "it": "IT"}
NOMS = {"fr": "Français", "en": "English", "it": "Italiano"}
X_DEFAULT = "fr"


def dossier(code):
    return DOCS / LANGUES[code] if LANGUES[code] else DOCS


EXCLUES = {"404.html"}  # pages techniques, hors sélecteur de langue et hors sitemap


def pages(code):
    return sorted(p.name for p in dossier(code).glob("*.html") if p.name not in EXCLUES)


def url(code, nom):
    return BASE + LANGUES[code] + ("" if nom == "index.html" else nom)


def lien_relatif(depuis, vers, nom):
    """Chemin relatif d'une page de la langue `depuis` vers `nom` dans la langue `vers`."""
    prefixe = "../" if LANGUES[depuis] else ""
    return prefixe + LANGUES[vers] + nom


def remplacer_bloc(texte, balise, contenu, avant):
    debut, fin = f"<!-- {balise} -->", f"<!-- /{balise} -->"
    bloc = f"{debut}{contenu}{fin}"
    if debut in texte:
        return re.sub(re.escape(debut) + r".*?" + re.escape(fin), lambda _: bloc, texte, flags=re.S)
    if avant not in texte:
        raise SystemExit(f"Repère introuvable : {avant!r}")
    return texte.replace(avant, bloc + "\n" + avant, 1)


def main():
    existantes = {code: set(pages(code)) for code in LANGUES}
    for code in LANGUES:
        for nom in sorted(existantes[code]):
            chemin = dossier(code) / nom
            s = chemin.read_text(encoding="utf-8")
            versions = [c for c in LANGUES if nom in existantes[c]]
            liens = "".join(f'\n  <link rel="alternate" hreflang="{c}" href="{url(c, nom)}">' for c in versions)
            if X_DEFAULT in versions:
                liens += f'\n  <link rel="alternate" hreflang="x-default" href="{url(X_DEFAULT, nom)}">'
            s = remplacer_bloc(s, "langues", liens + "\n  ", "</head>")
            choix = []
            for c in LANGUES:
                cible = nom if nom in existantes[c] else "index.html"
                courant = ' aria-current="true"' if c == code else ""
                choix.append(f'<a href="{lien_relatif(code, c, cible)}" hreflang="{c}" lang="{c}" title="{NOMS[c]}"{courant}>{ETIQUETTES[c]}</a>')
            switch = '<div class="lang-switch">' + "".join(choix) + "</div>"
            s = remplacer_bloc(s, "choix-langue", switch, '<button class="nav-toggle"')
            chemin.write_text(s, encoding="utf-8")

    lignes = []
    for code in LANGUES:
        for nom in sorted(existantes[code]):
            prio = "1.0" if nom == "index.html" else "0.3" if nom == "mentions-legales.html" else "0.8" if nom in ("methodes.html", "conseils.html") else "0.7"
            alternates = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{url(c, nom)}"/>'
                for c in LANGUES if nom in existantes[c])
            contenu = (dossier(code) / nom).read_text(encoding="utf-8")
            images = "".join(
                f"\n    <image:image><image:loc>https://educanimaux.fr/img/illu/{i}.svg</image:loc></image:image>"
                for i in dict.fromkeys(re.findall(r'img/illu/([\w-]+)\.svg', contenu)))
            lignes.append(f"  <url>\n    <loc>{url(code, nom)}</loc>{alternates}{images}\n    <priority>{prio}</priority>\n  </url>")
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(lignes) + "\n</urlset>\n", encoding="utf-8")
    total = sum(len(v) for v in existantes.values())
    print(f"{total} pages reliées ({', '.join(f'{c}: {len(existantes[c])}' for c in LANGUES)}), sitemap régénéré.")


if __name__ == "__main__":
    main()
