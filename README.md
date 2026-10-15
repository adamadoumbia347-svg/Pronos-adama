# Éduc'Animaux — site d'éducation animale avec liens d'affiliation

Le site se trouve dans le dossier `docs/`. Site statique (HTML/CSS/JS, aucune dépendance) qui rassemble les méthodes d'éducation pour chiens, chats, lapins, rongeurs, furets et oiseaux, avec des liens d'affiliation vers le matériel recommandé.

## Pages

| Fichier | Contenu |
|---|---|
| `docs/index.html` | Accueil, méthodes phares, kit de démarrage, FAQ |
| `docs/methodes.html` | Catalogue des 17 méthodes, filtrable par animal / niveau / mot-clé (`methodes.html?animal=chat`) |
| `docs/chien.html` | Programme complet pour le chien + tableau du matériel |
| `docs/chat.html` | Litière, griffades, rappel, caisse, clicker |
| `docs/nac.html` | Lapins, rats, furets, oiseaux |
| `docs/materiel.html` | Boutique : tout le matériel conseillé par animal |
| `docs/conseils.html` | Liste des articles |
| `docs/rappel-chien.html`, `marche-en-laisse.html`, `chat-griffe-canape.html`, `chiot-mord.html` | Articles optimisés pour Google |
| `docs/sitemap.xml` | Plan du site à envoyer dans Google Search Console |
| `docs/mentions-legales.html` | Mentions légales, déclaration d'affiliation |

## Activer les commissions

1. Créez un compte sur [Partenaires Amazon](https://partenaires.amazon.fr).
2. Ouvrez `docs/js/config.js` et remplacez `VOTRE-TAG-21` par votre identifiant de suivi.
3. (Optionnel) Pour un autre programme (Zooplus via Awin, Wanimo, etc.), ajoutez un lien précis dans `liensPersonnalises` avec la clé `data-aff` du produit (ex. `harnais`, `clicker`, `kong`).

Tous les liens produits ont la classe `aff` et reçoivent automatiquement `rel="sponsored nofollow noopener"` (recommandé par Google pour les liens affiliés).

Pour ajouter un produit n'importe où :

```html
<a class="aff" data-aff="mon-produit" data-q="mots clés recherche amazon" href="https://www.amazon.fr/s?k=mots+cles">Voir le produit</a>
```

## À compléter avant la mise en ligne

- `docs/mentions-legales.html` : à mettre à jour si votre statut change (ex. micro-entreprise + SIRET).
- Le programme Amazon exige un site public avec du contenu, et des ventes dans les 180 jours suivant l'inscription.

## Mettre en ligne gratuitement

- **GitHub Pages** : Settings → Pages → Branch `main`, dossier `/docs`.
- **Netlify** : glissez-déposez le dossier `docs` sur app.netlify.com/drop.

## Faire venir des visiteurs

Voir `promotion.md` (Search Console, Pinterest, groupes Facebook, scripts vidéo, planning).
