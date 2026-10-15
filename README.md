# Éduc'Animaux — site d'éducation animale avec liens d'affiliation

Site statique (HTML/CSS/JS, aucune dépendance) qui rassemble les méthodes d'éducation pour chiens, chats, lapins, rongeurs, furets et oiseaux, avec des liens d'affiliation vers le matériel recommandé.

## Pages

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil, méthodes phares, kit de démarrage, FAQ |
| `methodes.html` | Catalogue des 17 méthodes, filtrable par animal / niveau / mot-clé (`methodes.html?animal=chat`) |
| `chien.html` | Programme complet pour le chien + tableau du matériel |
| `chat.html` | Litière, griffades, rappel, caisse, clicker |
| `nac.html` | Lapins, rats, furets, oiseaux |
| `materiel.html` | Boutique : tout le matériel conseillé par animal |
| `mentions-legales.html` | Mentions légales, déclaration d'affiliation (à compléter) |

## Activer les commissions

1. Créez un compte sur [Partenaires Amazon](https://partenaires.amazon.fr).
2. Ouvrez `js/config.js` et remplacez `VOTRE-TAG-21` par votre identifiant de suivi.
3. (Optionnel) Pour un autre programme (Zooplus via Awin, Wanimo, etc.), ajoutez un lien précis dans `liensPersonnalises` avec la clé `data-aff` du produit (ex. `harnais`, `clicker`, `kong`).

Tous les liens produits ont la classe `aff` et reçoivent automatiquement `rel="sponsored nofollow noopener"` (recommandé par Google pour les liens affiliés).

Pour ajouter un produit n'importe où :

```html
<a class="aff" data-aff="mon-produit" data-q="mots clés recherche amazon" href="https://www.amazon.fr/s?k=mots+cles">Voir le produit</a>
```

## À compléter avant la mise en ligne

- `mentions-legales.html` : vos nom, contact, statut, hébergeur (obligatoire en France).
- Le programme Amazon exige un site public avec du contenu, et des ventes dans les 180 jours suivant l'inscription.

## Mettre en ligne gratuitement

- **GitHub Pages** : Settings → Pages → Branch `main`, dossier `/ (root)`.
- **Netlify** : glissez-déposez le dossier sur app.netlify.com/drop.
