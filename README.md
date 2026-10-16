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
| `docs/quiz.html`, `docs/age-humain.html` | Outils interactifs (quiz « quelle méthode ? », calculateur d'âge), logique dans `docs/js/outils.js` |
| `docs/en/`, `docs/it/` | Versions anglaise et italienne des 13 pages |
| `docs/sitemap.xml` | Plan du site (3 langues) à envoyer dans Google Search Console |
| `docs/mentions-legales.html` | Mentions légales, déclaration d'affiliation |

## Langues

Le site existe en français (`docs/`), anglais (`docs/en/`) et italien (`docs/it/`), avec les mêmes noms de fichiers.
Après tout ajout ou suppression de page, lancez `python3 tools/langues.py` : il met à jour le sélecteur FR · EN · IT,
les balises `hreflang` et `docs/sitemap.xml` (`tools/publier_article.py` le fait automatiquement).

## Activer les commissions (plusieurs pays)

Ouvrez `docs/js/config.js` : chaque boutique Amazon (France, Italie, Espagne, Allemagne, Royaume-Uni, États-Unis, Canada)
a son propre champ `tag`. Inscrivez-vous au programme Partenaires de chaque pays et collez l'identifiant correspondant.
Le site choisit automatiquement la boutique du visiteur (pays du navigateur, sinon langue de la page).
Une boutique sans tag fonctionne mais ne rapporte rien.

Pour un autre programme (Zooplus via Awin, etc.), ajoutez un lien précis dans `liensPersonnalises`, par boutique et par clé `data-aff`.

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

## Articles : sommaire, progression, « À lire aussi »

Le sommaire et la barre de progression sont générés automatiquement par `docs/js/main.js` sur toute page contenant `.container.article`.
Le bloc « À lire aussi » est écrit dans le HTML par `python3 tools/lire_aussi.py` (lancé automatiquement par `tools/publier_article.py`).

## Publier un article

Voir `ARTICLES.md` (règles de rédaction, liste des sujets) :

```
python3 tools/publier_article.py articles/AAAA-MM-JJ-slug.html
python3 tools/verifier_site.py
```

## Illustrations

Dessins vectoriels sans texte (libres de droits) dans `docs/img/illu/`, générés par `node tools/illustrations/scenes.js`
et placés dans les pages (légendes FR/EN/IT, images des cartes) par `python3 tools/illustrations/integrer.py`.

## Lettre d'information (Brevo)

`python3 tools/lettre.py` écrit `lettres/AAAA-MM-JJ.html` avec les 3 derniers articles de `docs/conseils.html`.
Dans Brevo : Campagnes > Créer une campagne e-mail > Éditeur « Coller votre code HTML », puis coller le contenu du fichier.
