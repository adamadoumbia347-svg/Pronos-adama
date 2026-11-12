"""Ajoute de vraies photos aux pages (fiches races, articles) : compression WebP, crédit, insertion idempotente.

Usage : python3 tools/photos.py

1. Déposer la photo originale dans tools/photos/originaux/<slug>.jpg (ou .jpeg, .png, .webp),
   où <slug> est le nom de la page sans « .html » (ex. race-labrador, chien-saute-sur-les-gens).
2. Indiquer le crédit dans tools/photos/credits.json :
   {"race-labrador": {"alt": "Un labrador sable assis dans l'herbe", "auteur": "Nom", "licence": "CC BY 2.0",
                      "source": "https://…"}}
   Pour vos propres photos : {"auteur": "Éduc'Animaux"} suffit (pas de licence ni de source).
3. Lancer le script : il crée docs/img/photos/<slug>-1200.webp et -600.webp, insère la photo sous le titre
   de la page (FR, et EN/IT si la page existe), et la vignette dans la carte de la page Races.
   Relancer le script après avoir régénéré une page (tools/pages/races.py, publier_article.py…).
"""
import html
import json
import pathlib
import re

from PIL import Image

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
SRC = RACINE / "tools" / "photos"
SORTIE = DOCS / "img" / "photos"
LEGENDE = {"fr": "Photo", "en": "Photo", "it": "Foto"}
e = html.escape


def convertir(orig, slug):
    SORTIE.mkdir(parents=True, exist_ok=True)
    im = Image.open(orig).convert("RGB")
    # Recadrage 3:2 centré, comme l'affichage
    w, h = im.size
    if w / h > 1.5:
        nw = int(h * 1.5); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / 1.5); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    for larg in (1200, 600):
        c = im.copy(); c.thumbnail((larg, larg))
        c.save(SORTIE / f"{slug}-{larg}.webp", "WEBP", quality=78, method=6)


def credit(c, lang):
    txt = f"{LEGENDE[lang]} : {e(c.get('auteur', ''))}"
    if c.get("licence"):
        lic = e(c["licence"])
        txt += f", <a href=\"{e(c['source'])}\" rel=\"nofollow noopener\" target=\"_blank\">{lic}</a>" if c.get("source") else f", {lic}"
    return txt


def figure(slug, c, prefixe, lang):
    return (f'<!-- photo --><figure class="photo"><img src="{prefixe}img/photos/{slug}-1200.webp" '
            f'srcset="{prefixe}img/photos/{slug}-600.webp 600w, {prefixe}img/photos/{slug}-1200.webp 1200w" '
            f'sizes="(max-width: 760px) 100vw, 760px" width="1200" height="800" alt="{e(c.get("alt", ""))}" '
            f'fetchpriority="high"><figcaption>{credit(c, lang)}</figcaption></figure><!-- /photo -->')


def inserer_page(p, slug, c, prefixe, lang):
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"\s*<!-- photo -->.*?<!-- /photo -->", "", s, flags=re.S)
    m = re.search(r'(<p class="meta">.*?</p>)', s, flags=re.S) or re.search(r"(<h1>.*?</h1>)", s, flags=re.S)
    if not m:
        return False
    s = s[:m.end()] + "\n        " + figure(slug, c, prefixe, lang) + s[m.end():]
    p.write_text(s, encoding="utf-8")
    return True


def inserer_carte(p, slug, c, prefixe):
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8")
    motif = re.compile(rf'(<a class="card card-link" href="{slug}\.html"><span class="icon">)(.*?)(</span>)', re.S)
    img = (f'<img class="card-photo" src="{prefixe}img/photos/{slug}-600.webp" alt="" width="600" height="400" '
           f'loading="lazy" decoding="async">')
    s2 = motif.sub(lambda m: m.group(1) + img + m.group(3), s)
    if s2 != s:
        p.write_text(s2, encoding="utf-8")


def main():
    credits = json.loads((SRC / "credits.json").read_text(encoding="utf-8")) if (SRC / "credits.json").exists() else {}
    n = 0
    for orig in sorted((SRC / "originaux").glob("*")) if (SRC / "originaux").exists() else []:
        slug = orig.stem
        if orig.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        c = credits.get(slug, {"auteur": "Éduc'Animaux"})
        convertir(orig, slug)
        for lang, dossier, prefixe in (("fr", DOCS, ""), ("en", DOCS / "en", "../"), ("it", DOCS / "it", "../")):
            page = dossier / f"{slug}.html"
            if page.exists() and inserer_page(page, slug, c, prefixe, lang):
                n += 1
            inserer_carte(dossier / "races.html", slug, c, prefixe)
    print(f"{n} pages illustrées")


if __name__ == "__main__":
    main()
