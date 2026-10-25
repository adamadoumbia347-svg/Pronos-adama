#!/usr/bin/env python3
"""Prépare la version « page Claude » de l'appli dans un dossier (par défaut pronos/build-artifact).

La page publiée est enveloppée automatiquement dans <html><head><body> : on garde donc
seulement le contenu de <head> (titre, styles) et de <body>, et on copie css/, js/ et data/.

Usage : python3 pronos/tools/construire_artifact.py [dossier]
"""
import pathlib
import re
import shutil
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent


def main():
    sortie = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "build-artifact"
    if sortie.exists():
        shutil.rmtree(sortie)
    for dossier in ("css", "js", "data"):
        shutil.copytree(RACINE / dossier, sortie / dossier)
    page = (RACINE / "index.html").read_text(encoding="utf-8")
    tete = re.search(r"<head>(.*)</head>", page, re.S).group(1)
    corps = re.search(r"<body>(.*)</body>", page, re.S).group(1)
    tete = re.sub(r'<meta charset[^>]*>\n|<meta name="viewport"[^>]*>\n', "", tete)
    tete = tete.replace("</title>", '</title>\n<meta name="claude:viewport-fit-sides" content="cover">', 1)
    (sortie / "pronos-adama.html").write_text(tete.strip() + "\n" + corps.strip() + "\n", encoding="utf-8")
    print(sortie / "pronos-adama.html")


if __name__ == "__main__":
    main()
