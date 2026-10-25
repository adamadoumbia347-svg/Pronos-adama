# Pronos Adama — pronostics football

Appli web statique (HTML/CSS/JS, aucune dépendance) qui calcule des pronostics à partir des résultats passés
de 7 championnats : Ligue 1, Premier League, LaLiga, Serie A, Bundesliga, Liga Portugal, Eredivisie.

## Ce que fait l'appli

| Onglet | Contenu |
|---|---|
| Pronostics | Prochains matchs : probabilités 1N2, score probable, buts attendus, conseils avec niveau de confiance |
| Analyser un match | N'importe quelle affiche : cotes justes, top des scores, grille de probabilité des scores, plus/moins de buts, les deux équipes marquent, double chance, forces attaque/défense, forme (10 derniers, domicile/extérieur), confrontations directes, détecteur de value bet (quart de Kelly) |
| Classement | Classement de la saison avec forme, Elo et forces du modèle |
| Fiabilité | Le modèle rejoue chaque semaine de la saison 2025/26 sans connaître les résultats : taux de réussite, calibration, réussite selon la confiance |
| Méthode | Explication du modèle, limites, jeu responsable |

## Le modèle (`js/modele.js`)

- Forces d'attaque et de défense par équipe (modèle de Poisson), pondérées dans le temps (demi-vie 200 jours), avantage du terrain par championnat.
- Correction Dixon-Coles des petits scores (0-0, 1-0, 0-1, 1-1).
- Classement Elo avec prise en compte de l'écart de buts.

Validation sur 2025/26 (issue la plus probable) : 46 à 57 % de bons 1N2 selon le championnat,
contre 40 à 48 % en pariant toujours sur le domicile.

## Lancer l'appli

Ouvrez `pronos/index.html` dans un navigateur (fonctionne même sans serveur), ou :

```bash
cd pronos && python3 -m http.server 8000   # puis http://localhost:8000
```

Mise en ligne gratuite : glissez le dossier `pronos` sur app.netlify.com/drop.

## Données

Source : [openfootball/football.json](https://github.com/openfootball/football.json) (domaine public), saisons 2024/25 à 2026/27.
Au chargement, l'appli récupère la saison en cours en direct ; sans connexion, elle utilise la copie de `data/`.
Pour rafraîchir la copie locale :

```bash
python3 pronos/tools/maj_donnees.py
```

Les données ne contiennent ni blessures, ni compositions, ni cotes : les pronostics restent des probabilités.
18+ — Joueurs Info Service : 09 74 75 13 13.
