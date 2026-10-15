# Guide de publication des articles — educanimaux.fr

Ce fichier décrit comment écrire et publier un nouvel article. Il sert aux sessions
automatiques hebdomadaires comme à toute personne qui ajoute un article à la main.
Il n'est pas publié sur le site (seul le dossier `docs/` l'est).

## Procédure (une publication = un article)

1. Choisir le **premier sujet non coché** de la liste « Sujets à venir » ci-dessous.
   Vérifier dans `docs/conseils.html` qu'aucun article ne traite déjà ce sujet.
2. Écrire le fichier source `articles/AAAA-MM-JJ-<slug>.html` (date du jour),
   au format décrit plus bas. S'inspirer de `docs/rappel-chien.html` pour le ton et la mise en page.
3. Publier : `python3 tools/publier_article.py articles/AAAA-MM-JJ-<slug>.html`
4. Vérifier : `python3 tools/verifier_site.py` doit afficher « Aucun problème ».
5. Cocher le sujet dans la liste ci-dessous (`- [x]`) et ajouter le lien de l'article.
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

## Liens d'affiliation

- **2 à 4 produits par article**, seulement s'ils sont réellement utiles au sujet.
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

## Sujets à venir

Les sessions hebdomadaires prennent le premier sujet non coché. On peut réordonner ou ajouter
des sujets librement.

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
- [ ] Choisir le bon harnais pour son chien
- [ ] Adopter un chien adulte : les premières semaines

## Articles publiés

- 2026-10-15 — Comment apprendre le rappel à son chien en 7 étapes (`rappel-chien.html`)
- 2026-10-15 — Chien qui tire en laisse : la méthode pour qu'il arrête (`marche-en-laisse.html`)
- 2026-10-15 — Chat qui griffe le canapé : 6 solutions qui marchent (`chat-griffe-canape.html`)
- 2026-10-15 — Mon chiot mord : que faire ? (`chiot-mord.html`)
- 2026-10-15 — Propreté du chiot : la méthode pour qu'il soit propre rapidement (`proprete-chiot.html`)
