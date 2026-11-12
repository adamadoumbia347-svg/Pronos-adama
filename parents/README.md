# Parents Sereins — site de conseils pour les parents

Site statique (HTML/CSS/JS, aucune dépendance), séparé d'Éduc'Animaux (`docs/`), avec liens d'affiliation Amazon.

**Design** : polices Fraunces (titres) et Nunito (texte) via Google Fonts ; animations (apparition au défilement,
parallaxe, compteurs, bandeau défilant, cartes qui se soulèvent, barre de lecture) désactivées automatiquement si le
visiteur a demandé « réduire les animations ». Photos libres de droits Unsplash dans `img/`.

**Options pour le visiteur** (gardées sur son appareil) : thème clair / sombre / automatique, favoris (`favoris.html`),
taille du texte, partage, temps de lecture et sommaire automatiques, bouton retour en haut.

## Pages

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil, articles phares, outils, FAQ |
| `conseils.html` | Liste des articles par âge, avec recherche (`conseils.html?q=dents`) |
| `sommeil-bebe.html` | Faire dormir bébé : 10 conseils + sécurité du couchage |
| `coleres-enfant.html` | Les colères de 2 à 6 ans |
| `ecrans-enfants.html` | Écrans et enfants : repères par âge |
| `diversification-alimentaire.html` | La diversification mois par mois |
| `proprete-enfant.html` | Apprendre la propreté |
| `poussees-dentaires.html` | Poussées dentaires et brossage |
| `devoirs-sans-crise.html` | Les devoirs sans crise |
| `langage-enfant.html` | Les premiers mots |
| `freres-et-soeurs.html` | Jalousie et disputes entre frères et sœurs |
| `adaptation-creche-ecole.html` | Crèche, nounou, école : la séparation |
| `voyager-avec-enfants.html` | Voyager avec des enfants |
| `confiance-en-soi-enfant.html` | La confiance en soi |
| `favoris.html` | Articles enregistrés par le visiteur |
| `activites-enfants-maison.html` | 30 activités sans écran |
| `outils.html` | Calculateurs : sommeil, repères écrans, diversification, budget de la 1re année, idée d'activité au hasard, argent de poche |
| `routine-enfant.html` | Tableau de routine matin/soir à imprimer, avec le prénom de l'enfant |
| `liste-naissance.html` | Check-list de naissance à cocher (gardée dans le navigateur du visiteur) |
| `materiel.html` | Sélection de matériel par âge |
| `mentions-legales.html` | Mentions légales — **compléter nom, contact et hébergeur** |

La logique des outils est dans `js/outils.js`, les liens d'affiliation dans `js/main.js`.

## Affiliation

`js/config.js` reprend les identifiants Amazon d'Éduc'Animaux. Avant la mise en ligne, ajoutez l'adresse de ce
nouveau site dans votre compte Partenaires Amazon (Paramètres du compte → Sites web et applis), sinon Amazon peut
refuser les commissions. Un produit s'ajoute partout ainsi :

```html
<a class="aff" data-aff="mon-produit" data-q="mots clés recherche amazon" href="https://www.amazon.fr/s?k=mots+cles">Voir le produit</a>
```

## Mettre en ligne

- **Netlify** : glissez-déposez le dossier `parents` sur app.netlify.com/drop.
- Remplacez `https://parents-sereins.fr` dans `sitemap.xml` et `robots.txt` par votre vraie adresse,
  puis envoyez `sitemap.xml` dans Google Search Console.
