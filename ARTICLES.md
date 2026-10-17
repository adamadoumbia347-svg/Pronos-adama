# Guide de publication des articles — educanimaux.fr

Ce fichier décrit comment écrire et publier un nouvel article. Il sert aux sessions
automatiques hebdomadaires comme à toute personne qui ajoute un article à la main.
Il n'est pas publié sur le site (seul le dossier `docs/` l'est).

## Rythme : chaque lundi, 3 articles

Chaque lundi, on publie **1 article de conseil + 2 comparatifs d'achat** :
- l'article de conseil = le premier sujet non coché de « Conseils à venir » ;
- les 2 comparatifs = les 2 premiers sujets non cochés de « Comparatifs à venir »
  (on peut en prendre d'autres plus loin dans la liste s'ils sont plus proches du conseil du jour).

**Maillage obligatoire entre les trois** : l'article de conseil renvoie vers les 2 comparatifs
(dans le texte, là où le matériel est évoqué, et dans « Pour aller plus loin ») ; chaque comparatif
renvoie vers l'article de conseil et vers au moins un article ou guide existant. C'est ce qui
transforme un lecteur qui cherche une solution en acheteur, sans surcharger les articles de liens.

## Procédure (pour chacun des 3 articles)

1. Choisir le sujet comme indiqué ci-dessus.
   Vérifier dans `docs/conseils.html` qu'aucun article ne traite déjà ce sujet (sinon le cocher et passer au suivant).
2. Écrire le fichier source `articles/AAAA-MM-JJ-<slug>.html` (date du jour),
   au format décrit plus bas. Modèles : `docs/rappel-chien.html` (conseil),
   `docs/meilleur-harnais-chien.html` (comparatif).
3. Publier : `python3 tools/publier_article.py articles/AAAA-MM-JJ-<slug>.html`
   (publier d'abord les 2 comparatifs, puis l'article de conseil, pour qu'il soit en tête).
4. Vérifier : `python3 tools/verifier_site.py` doit afficher « Aucun problème ».
5. Cocher les sujets dans les listes ci-dessous (`- [x]`) et ajouter les articles dans « Articles publiés ».
6. Commiter sur `main` et pousser (`git push origin main`). GitHub Pages met le site
   à jour automatiquement en 1 à 2 minutes.

## Langues

Les articles hebdomadaires sont publiés en français uniquement. Sur les versions anglaise et italienne,
le sélecteur de langue renvoie alors vers l'accueil de la langue. Pour traduire un article, créer
`docs/en/<slug>.html` et/ou `docs/it/<slug>.html` (même nom de fichier, contenu traduit, `lang` et adresses
`https://educanimaux.fr/en/…` ou `/it/…`, liens Amazon vers amazon.com ou amazon.it avec des mots-clés traduits),
ajouter la carte dans `docs/en/conseils.html` / `docs/it/conseils.html`, puis lancer `python3 tools/langues.py`.

## Format du fichier source

```
slug: proprete-chiot
titre: Propreté du chiot : la méthode pour qu'il soit propre rapidement
titre_court: Rendre son chiot propre
description: 150-160 caractères, avec le mot-clé principal, qui donne envie de cliquer.
resume: Une phrase affichée sur la carte de la page Conseils.
icone: 🚽
categorie: Chiot
date: 2026-10-15
---
    <section class="page-hero">
      <div class="container article">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › <a href="conseils.html">Conseils</a> › Fil d'Ariane court</p>
        <h1>Même texte que « titre »</h1>
        <p class="meta">🐕 Chien · Niveau débutant · Lecture 5 min</p>
        <p class="lead">Introduction de 2-3 phrases qui reprend le problème du lecteur.</p>
        <h2>…</h2>
        …
      </div>
    </section>
```

`categorie` : Chien, Chiot, Chat, Chaton, Lapin, Rongeur, Furet ou Oiseau.

## Règles de rédaction

- **Français**, tutoiement interdit : on vouvoie le lecteur. Ton chaleureux, concret, sans jargon.
- **800 à 1 300 mots**, 5 à 8 intertitres `<h2>`, paragraphes courts, listes à puces.
- **Méthodes bienveillantes uniquement** (renforcement positif, gestion de l'environnement,
  désensibilisation…). Ne jamais recommander de punition physique, de collier étrangleur,
  à pointes, électrique ou anti-aboiement, ni la théorie de la « dominance ».
- **Exactitude** : pas de chiffres inventés, pas de promesse de résultat garanti.
  Pour tout ce qui touche à la santé (malpropreté soudaine, agressivité, douleur, perte d'appétit…),
  conseiller de consulter un vétérinaire.
- Terminer par une boîte `<div class="callout"><strong>À retenir :</strong> …</div>`, et
  ajouter un `<div class="callout warn">` pour ce qu'il ne faut pas faire quand c'est utile.
- **Maillage interne** : au moins 3 liens vers d'autres pages du site — méthodes
  (`methodes.html#renforcement-positif`, `#clicker`, `#leurre`, `#capture`, `#faconnage`,
  `#ciblage`, `#desensibilisation`, `#gestion`, `#socialisation`, `#cooperative-care`,
  `#premack`, `#rien-gratuit`, `#lat`, `#bat`, `#imitation`, `#modele-rival`, `#extinction`,
  `#aversif`), guides (`chien.html`, `chat.html`, `nac.html`) et autres articles.
  Finir par un paragraphe « Pour aller plus loin : … ».

## Comparatifs d'achat (« Quel … choisir ? »)

- Slug commençant par `meilleur-`, `meilleure-`, `meilleurs-` ou `meilleures-` ; `<p class="meta">… · Guide d'achat · Lecture N min</p>`.
- **900 à 1 400 mots** : une boîte `callout` « En bref » en haut (la recommandation en 2 phrases),
  les critères de choix, **un tableau comparatif par type** (`<div class="table-wrap"><table>…`),
  une section par type avec sa boîte produit, la taille / le bon usage, les erreurs à éviter, « À retenir ».
- **3 à 6 boîtes produit**, toujours vers des **recherches** Amazon par type de produit.
  Ne citer une marque ou un modèle que s'il est réel et connu (sinon rester générique) ;
  pas de prix, de notes ou de classement « n°1 » inventés, pas de faux tests (« nous avons testé… »).
- Comparer des **types** de produits et dire honnêtement pour qui chacun convient, y compris les limites.

## Liens d'affiliation

- **Articles de conseil : 2 à 4 produits**, seulement s'ils sont réellement utiles au sujet
  (les comparatifs en ont 3 à 6, voir ci-dessus).
- Toujours dans une « boîte produit » :

```html
        <div class="product-box">
          <span class="icon">🦺</span>
          <div><strong>Nom générique du produit</strong><p>Pourquoi il est utile ici, en une phrase honnête.</p></div>
          <a class="btn btn-sm aff" data-aff="cle-produit" data-q="mots clés recherche amazon" href="https://www.amazon.fr/s?k=mots+cles+recherche+amazon">Voir les prix</a>
        </div>
```

- Le lien pointe vers une **recherche** Amazon (`https://www.amazon.fr/s?k=…`), jamais vers un
  produit précis ni une marque inventée. `data-q` = mêmes mots-clés que `k=`.
- Ne pas écrire le tag d'affiliation dans le HTML : `docs/js/config.js` l'ajoute automatiquement.
- `data-aff` : réutiliser une clé existante si le produit existe déjà sur le site
  (ex. `harnais`, `longe`, `clicker`, `pochette`, `friandises`, `kong`, `tapis-fouille`,
  `griffoir`, `litiere`, `caisse-transport`, `diffuseur-apaisant`), sinon en créer une en minuscules avec tirets.

## Conseils à venir

Les sessions du lundi prennent le premier sujet non coché. On peut réordonner ou ajouter des sujets librement.

- [x] Propreté du chiot : la méthode pour qu'il soit propre rapidement
- [ ] Chien qui aboie quand il est seul : comprendre et agir
- [ ] Chat qui fait pipi hors de sa litière : causes et solutions
- [ ] Apprendre « assis », « couché » et « pas bouger » à son chien
- [ ] Le clicker training expliqué aux débutants (chien et chat)
- [ ] Chien qui saute sur les gens : la méthode douce
- [ ] Chien qui a peur des pétards et de l'orage
- [ ] Habituer son chat à la caisse de transport et à la voiture
- [ ] Rendre son lapin propre : bac à litière et astuces
- [ ] Chiot qui pleure la nuit : que faire ?
- [ ] Chien qui mange tout dehors : apprendre « laisse »
- [ ] Présenter un nouveau chat à son chat
- [ ] Chien et chat : les faire cohabiter sereinement
- [ ] Apprendre à son perroquet à monter sur la main
- [ ] Couper les griffes de son chien sans stress
- [ ] Chien réactif en laisse face aux autres chiens
- [ ] Occuper son chien en appartement : 10 jeux d'intelligence
- [ ] Chaton qui mord et griffe en jouant
- [ ] Adopter un chien adulte : les premières semaines

## Comparatifs à venir

Chaque lundi, les 2 premiers non cochés (entre parenthèses : l'article de conseil lié).

- [x] Quel harnais choisir pour son chien ? (`meilleur-harnais-chien.html`)
- [x] Quel griffoir choisir pour son chat ? (`meilleur-griffoir-chat.html`)
- [x] Quel clicker choisir ? (`meilleur-clicker.html`)
- [ ] Jouets d'occupation pour chien seul : tapis de fouille, jouets à remplir… lequel choisir ? (chien qui aboie seul)
- [ ] Quelle caméra pour surveiller son chien ou son chat ? (chien qui aboie seul)
- [ ] Quelle litière choisir pour son chat ? (pipi hors litière)
- [ ] Quel bac ou maison de toilette choisir pour son chat ? (pipi hors litière)
- [ ] Quelles friandises d'éducation choisir pour son chien ? (assis, couché, pas bouger)
- [ ] Quelle pochette à friandises choisir ? (clicker training)
- [ ] Quelle laisse choisir pour son chien ? (chien qui saute sur les gens / marche en laisse)
- [ ] Quelle longe choisir pour travailler le rappel ? (rappel)
- [ ] Peur des pétards et de l'orage : quels accessoires peuvent aider ? (peur des pétards)
- [ ] Quelle caisse de transport choisir pour son chat ? (caisse de transport)
- [ ] Quel bac à litière et quel foin pour son lapin ? (lapin propre)
- [ ] Quels jouets à mâcher pour un chiot ? (chiot qui pleure la nuit / chiot qui mord)
- [ ] Quel parc ou quelle cage pour un chiot ? (chiot qui pleure la nuit)
- [ ] Quelle muselière panier choisir (et comment l'habituer en douceur) ? (chien qui mange tout dehors)
- [ ] Quels jouets choisir pour un chat d'intérieur ? (présenter un nouveau chat / chaton qui mord)
- [ ] Quel arbre à chat choisir ? (chien et chat)
- [ ] Quels jouets et perchoirs pour un perroquet ? (perroquet sur la main)
- [ ] Quel coupe-griffes choisir pour son chien ? (couper les griffes)
- [ ] Quelle gamelle anti-glouton choisir ? (chien réactif / occuper son chien)
- [ ] Quels jeux d'intelligence pour chien ? (occuper son chien en appartement)
- [ ] Quel lit ou panier pour un chien adopté adulte ? (adopter un chien adulte)

Quand une liste est presque vide, ajouter 6 nouveaux sujets utiles et non traités.

## Articles publiés

- 2026-10-15 — Comment apprendre le rappel à son chien en 7 étapes (`rappel-chien.html`)
- 2026-10-15 — Chien qui tire en laisse : la méthode pour qu'il arrête (`marche-en-laisse.html`)
- 2026-10-15 — Chat qui griffe le canapé : 6 solutions qui marchent (`chat-griffe-canape.html`)
- 2026-10-15 — Mon chiot mord : que faire ? (`chiot-mord.html`)
- 2026-10-15 — Propreté du chiot : la méthode pour qu'il soit propre rapidement (`proprete-chiot.html`)
- 2026-10-16 — Quel clicker choisir pour éduquer son animal ? (`meilleur-clicker.html`)
- 2026-10-16 — Quel griffoir choisir pour son chat ? Le comparatif (`meilleur-griffoir-chat.html`)
- 2026-10-16 — Quel harnais choisir pour son chien ? Le comparatif (`meilleur-harnais-chien.html`)
- 2026-10-16 — Idées cadeaux de Noël pour chien et chat : 15 cadeaux utiles qui leur font plaisir (`idees-cadeaux-noel-chien-chat.html`)
- 2026-10-16 — Black Friday 2026 pour chien et chat : quoi acheter (et quoi éviter) (`black-friday-animaux.html`)
- 2026-10-16 — Accueillir un chiot : la liste complète du matériel (`kit-accueil-chiot.html`)
