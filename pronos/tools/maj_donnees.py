#!/usr/bin/env python3
"""Télécharge les résultats (openfootball/football.json) et écrit pronos/data/<ligue>.js.

Les données sont des fichiers .js (et non .json) pour que l'appli marche aussi ouverte
directement depuis le disque (file://), où fetch() est bloqué.

Usage : python3 pronos/tools/maj_donnees.py
"""
import json
import pathlib
import urllib.request

BASE = "https://raw.githubusercontent.com/openfootball/football.json/master"
SAISONS = ["2024-25", "2025-26", "2026-27"]
LIGUES = {
    "fr.1": "Ligue 1",
    "en.1": "Premier League",
    "es.1": "LaLiga",
    "it.1": "Serie A",
    "de.1": "Bundesliga",
    "pt.1": "Liga Portugal",
    "nl.1": "Eredivisie",
}
ENTETE = "window.PRONOS_DONNEES=window.PRONOS_DONNEES||{};\n"
DOSSIER = pathlib.Path(__file__).resolve().parent.parent / "data"


def score_final(m):
    s = m.get("score")
    if isinstance(s, list) and len(s) == 2:
        return s
    if isinstance(s, dict):
        ft = s.get("ft")
        if isinstance(ft, list) and len(ft) == 2:
            return ft
    return None


def telecharger(saison, ligue):
    with urllib.request.urlopen(f"{BASE}/{saison}/{ligue}.json", timeout=30) as r:
        return json.load(r)["matches"]


def main():
    DOSSIER.mkdir(exist_ok=True)
    index = []
    for code, nom in LIGUES.items():
        matchs = []
        for saison in SAISONS:
            try:
                brut = telecharger(saison, code)
            except Exception as e:  # saison absente
                print(f"  {saison} {code} ignorée : {e}")
                continue
            for m in brut:
                ft = score_final(m)
                ligne = [saison, m["date"], m.get("time", ""), m["team1"], m["team2"]]
                ligne += ft if ft else [None, None]
                matchs.append(ligne)
        matchs.sort(key=lambda x: (x[1], x[2]))
        joues = sum(1 for x in matchs if x[5] is not None)
        contenu = json.dumps({"ligue": nom, "code": code, "matchs": matchs}, ensure_ascii=False, separators=(",", ":"))
        (DOSSIER / f"{code}.js").write_text(f"{ENTETE}PRONOS_DONNEES[{json.dumps(code)}]={contenu};\n", encoding="utf-8")
        dernier = max((x[1] for x in matchs if x[5] is not None), default="-")
        index.append({"code": code, "nom": nom, "joues": joues, "aVenir": len(matchs) - joues, "dernier": dernier})
        print(f"{nom:15} {joues:4} joués, {len(matchs) - joues:3} à venir, dernier résultat {dernier}")
    (DOSSIER / "index.js").write_text(
        f"{ENTETE}PRONOS_DONNEES.saisons={json.dumps(SAISONS)};\nPRONOS_DONNEES.index={json.dumps(index, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
