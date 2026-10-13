# Escale

Comparateur de voyages : vols les moins chers, hôtels et locations de voitures.

Une seule page (`index.html`, sans dépendance ni serveur). Vous remplissez un formulaire et Escale
prépare la recherche, déjà triée par prix, sur les grands comparateurs :

- **Vols** : Google Flights, Skyscanner, Kayak, momondo (dates flexibles ±3 jours, vols directs,
  classe, enfants, destination « partout »), plus une grille jour par jour.
- **Hôtels** : Booking.com, Google Hôtels, Kayak, Hotels.com, Agoda, Airbnb.
- **Voitures** : Kayak, momondo, recherche Google, Rentalcars et Discover Cars.

Les prix réels s'affichent sur les sites partenaires, où se fait la réservation.

Aussi : liens de recherche partageables (WhatsApp), destinations populaires, FAQ, référencement
(données structurées, Open Graph, sitemap), appli installable, emplacements pour l'affiliation.

Pour faire grandir le site : voir [CROISSANCE.md](CROISSANCE.md).

## Structure

- `site/` : le site publié (page d'accueil, pages générées, icônes).
- `scripts/build_pages.py` : génère les pages trajets, légales, contact et le sitemap. Lancé automatiquement par Netlify.
- `netlify/functions/prix.mts` : prix indicatifs (variable `TRAVELPAYOUTS_TOKEN`).
- `netlify.toml` : configuration Netlify.

## Lancer

```
python3 scripts/build_pages.py
python3 -m http.server -d site 8000
```

En ligne : https://escale-voyage.netlify.app (projet Netlify `escale-voyage`).
