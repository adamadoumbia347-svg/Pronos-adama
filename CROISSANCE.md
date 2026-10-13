# Escale : plan pour attirer plus de visiteurs

Ce qui est déjà fait dans le code, puis ce qu'il reste à faire, dans l'ordre où ça rapporte le plus.

## Déjà en place

| Amélioration | Pourquoi |
|---|---|
| Titre, description, mots-clés, `lang="fr"` | Google comprend de quoi parle le site |
| Données structurées `WebSite` et `FAQPage` | La FAQ peut apparaître directement dans les résultats Google |
| Image de partage (`og-image.png`) + balises Open Graph | Un bel aperçu quand le lien est partagé sur WhatsApp, Facebook, X |
| Liens de recherche partageables (`?type=vols&from=CDG&to=BKO…`) | Un visiteur envoie sa recherche à sa famille, qui arrive directement sur les résultats |
| Bouton « Partager sur WhatsApp » et « Copier le lien » | Le bouche-à-oreille est le premier canal pour la diaspora |
| Section « Destinations populaires » (Paris–Bamako, Dakar, Abidjan, Kinshasa…) | Contenu utile et mots-clés recherchés |
| FAQ de 6 questions | Répond aux vraies questions et nourrit le référencement |
| Appli installable (`manifest.webmanifest`, icônes) | « Ajouter à l'écran d'accueil » sur téléphone |
| `robots.txt` et `sitemap.xml` | À compléter avec le vrai domaine (voir étape 1) |
| Emplacements pour vos identifiants d'affiliation (`AFFILIATE` dans `index.html`) | Le site peut gagner de l'argent sans rien changer d'autre |

## À faire

### 1. Mettre le site en ligne avec un vrai nom (priorité absolue)
- Hébergement gratuit : Netlify, Cloudflare Pages ou GitHub Pages.
- Nom de domaine court et mémorisable (environ 10 €/an), par exemple `escale-voyage.fr`.
- Remplacer `VOTRE-DOMAINE` dans `robots.txt` et `sitemap.xml`, et ajouter dans `index.html` :
  `<link rel="canonical" href="https://votre-domaine/">` et l'URL absolue de `og:image`.

### 2. Être trouvé sur Google
- Déclarer le site dans **Google Search Console** et **Bing Webmaster Tools**, puis envoyer le `sitemap.xml`.
- **Le levier n°1 : une page par trajet populaire** (« Vol pas cher Paris Bamako », « Paris Dakar », etc.).
  Chaque page : durée du vol, compagnies, aéroports, meilleure période pour réserver, bagages, puis le formulaire déjà rempli.
  Ces recherches précises ont moins de concurrence que « vol pas cher ».
- Ajouter ensuite des pages hôtels par ville (« Hôtel pas cher à Dakar ») et quelques guides
  (« Quand réserver pour la Tabaski », « Franchise bagage vers l'Afrique par compagnie »).

### 3. Gagner de l'argent avec l'affiliation
Inscrivez-vous, puis collez vos identifiants dans l'objet `AFFILIATE` de `index.html` :
- **Travelpayouts** : un seul compte pour de nombreuses marques (vols, hôtels, voitures). Depuis le 27 avril 2026,
  on crée un « Project » et la plateforme y connecte les programmes compatibles. La commission dépend de chaque marque :
  vérifiez-la dans votre tableau de bord.
- **Booking.com Affiliate Partner Program** (paramètre `aid`), **Agoda Partners** (`cid`).
- **Skyscanner** (programme via Impact) et **Discover Cars** (programme partenaire).
- Une mention « liens partenaires » s'affiche automatiquement dans le pied de page dès qu'un identifiant est rempli.

### 4. Afficher de vrais prix sur le site
Afficher « Paris → Bamako dès 489 € » attire beaucoup plus de clics. Attention :
**l'offre gratuite Amadeus Self-Service a fermé en juillet 2026**. Pistes :
- l'API de données de Travelpayouts / Aviasales (prix en cache, réservée aux partenaires) ;
- **Ignav** : 1 000 requêtes gratuites, puis environ 2 $ pour 1 000 (à vérifier sur leur site).
Il faudra un petit serveur (par exemple Netlify Functions) pour cacher la clé d'accès.

### 5. Réseaux sociaux et bouche-à-oreille
- Une **chaîne WhatsApp** « Bons plans billets Afrique » avec 2 ou 3 bons plans par semaine et le lien de recherche.
- Vidéos courtes TikTok et Instagram : « J'ai trouvé Paris–Dakar à X € : voici comment ».
- Groupes Facebook de la diaspora (Maliens, Sénégalais, Ivoiriens de France), en respectant leurs règles.

### 6. Faire revenir les visiteurs
- **Alertes prix** par e-mail ou WhatsApp quand un trajet baisse (nécessite les prix réels de l'étape 4).
- Newsletter mensuelle (Brevo a une offre gratuite).

### 7. Mesurer
- Statistiques sans bannière de cookies : Plausible, GoatCounter ou Cloudflare Web Analytics.
- Suivre : visiteurs, pages trajets les plus vues, clics « Voir les prix » par site partenaire.

### 8. Élargir le public
- Version anglaise, affichage en francs CFA (XOF) en plus des euros.
- Plus d'aéroports et de villes (actuellement environ 85).

### 9. Obligations légales (France)
- Page **mentions légales** (obligatoire) et **politique de confidentialité** si vous ajoutez des statistiques ou une newsletter.

## Sources
- [Travelpayouts : fonctionnement des programmes](https://support.travelpayouts.com/hc/en-us/articles/203955763)
- [PhocusWire : fermeture d'Amadeus Self-Service](https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers)
- [Ignav : alternative après la fermeture d'Amadeus Self-Service](https://ignav.com/docs/amadeus-self-service-shutdown)
