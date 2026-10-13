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

| 14 pages trajets (`/vol-paris-bamako/`, `/vol-paris-dakar/`…) avec FAQ structurée | Capter les recherches Google précises (« vol pas cher Paris Bamako ») |
| Pages Mentions légales, Confidentialité, Contact (formulaire Netlify) | Obligations légales et confiance des visiteurs |
| Fonction `/api/prix` (Travelpayouts) + encart « dès X € » | Affiche un prix réel dès que la clé est configurée |
| Projet Netlify `escale-voyage` créé, public, formulaires activés | Adresse : https://escale-voyage.netlify.app |
| Sitemap, robots.txt, liens canoniques sur cette adresse | Générés par `scripts/build_pages.py` |

## À faire

### 1. Site en ligne ✔
Publié sur https://escale-voyage.netlify.app (dépôt du dossier du projet sur Netlify).
Pour publier une mise à jour : redéposer le dossier du projet dans l'onglet Deploys, ou relier le dépôt GitHub
(Project configuration > Build & deploy > Link repository) pour des mises à jour automatiques.
Plus tard : un nom de domaine à vous (environ 10 €/an) ; changer alors `DOMAIN` dans `scripts/build_pages.py`
et l'adresse dans `site/index.html`.

### 2. Google ✔ (13 octobre 2026)
Site validé dans Google Search Console (fichier `site/google07cf151d39bf7608.html`, à ne pas supprimer) et sitemap envoyé.
À suivre chaque semaine dans Search Console : pages indexées, requêtes qui amènent des visiteurs.
Pour aller plus loin : ajouter des pages trajets (une par ligne recherchée) et des pages hôtels par ville,
puis les déclarer aussi dans Bing Webmaster Tools (import direct depuis Search Console).

### 3. Gagner de l'argent avec l'affiliation
Inscrivez-vous, puis collez vos identifiants dans l'objet `AFFILIATE` de `index.html` :
- **Travelpayouts** : un seul compte pour de nombreuses marques (vols, hôtels, voitures). Depuis le 27 avril 2026,
  on crée un « Project » et la plateforme y connecte les programmes compatibles. La commission dépend de chaque marque :
  vérifiez-la dans votre tableau de bord.
- **Booking.com Affiliate Partner Program** (paramètre `aid`), **Agoda Partners** (`cid`).
- **Skyscanner** (programme via Impact) et **Discover Cars** (programme partenaire).
- Une mention « liens partenaires » s'affiche automatiquement dans le pied de page dès qu'un identifiant est rempli.

### 4. Afficher de vrais prix sur le site
**Déjà codé :** créez un compte Travelpayouts, copiez votre jeton API, puis dans Netlify
(Project configuration > Environment variables) ajoutez `TRAVELPAYOUTS_TOKEN` (portée : Functions) et redéployez.
L'encart « Prix repéré récemment : dès X € » apparaît alors au-dessus des résultats de vol.

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
