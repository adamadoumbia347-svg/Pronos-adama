# Vidéos TikTok automatiques (chiens et chats)

Rythme : **1 vidéo par jour du 19 octobre au 17 novembre 2026** (lundi 18 h, autres jours 10 h),
puis **3 par semaine** à partir du 18 novembre (lundi 18 h, mercredi 10 h, vendredi 10 h). Fuseau Europe/Rome.

Chaque vidéo = un fichier JSON dans `sujets/AAAA-MM-JJ-<nom>.json` (date de publication prévue).

**Style : motion design 3D** par défaut (voir « Style 3D » ci-dessous). Le motion design 2D (`"style": "motion"`, `modele-motion.html`) : texte cinétique mot par mot, mots-clés surlignés,
formes qui flottent, cercle coloré qui « pousse » derrière l'animal, transitions en iris, numéros 01–05, barre de
progression, soulignés dessinés, fin avec patte dessinée. Pour revenir à l'ancien style « cartes » : `"style": "cartes"` dans le JSON.

```
python3 tools/video/auto/fabriquer.py tools/video/auto/sujets/<fichier>.json --apercu   # 6 images de contrôle
python3 tools/video/auto/fabriquer.py tools/video/auto/sujets/<fichier>.json            # vidéo finale
```
Sortie : `videos/auto/<nom>.mp4` (1080×1920, ~25 s, musique + bruitages) et `videos/auto/<nom>.txt` (légende + hashtags).
Publication : la vidéo est poussée sur `main`, puis programmée sur TikTok via Metricool avec l'adresse
`https://raw.githubusercontent.com/adamadoumbia347-svg/Pronos-adama/main/videos/auto/<nom>.mp4`.

## Style 3D (par défaut)

Toutes les vidéos sont en **motion design 3D** (modèle `modele-3d.html`, Three.js dans `vendor/`) : cartes en relief qui tournent, pièces 3D numérotées, formes brillantes et caméra en mouvement. `"style": "motion"` redonne le motion design 2D, `"style": "cartes"` l'ancien modèle (à ne plus utiliser).

## Format du JSON

```json
{
 "hook": "Texte d'accroche (HTML : <br>, <em>mot en orange</em>)",
 "emoji_hook": "😼",
 "bandeau": "🐾 Petit titre affiché au-dessus des cartes",
 "musique": 1,                       // 0 à 5 : variante de la musique
 "fond": ["#ffe9d6", "#e6f3ef"],     // facultatif : dégradé de fond
 "cartes": [                          // 4 à 6 cartes (5 conseillé)
  {"visuel": {...}, "quoi": "Le comportement / la situation", "sens": "Ce que ça veut dire 😮",
   "conseil": "→ Le conseil pratique", "son": "pop", "badge": "facultatif (sinon 1 / 5)", "couleur": "vert|rouge (facultatif)"}
 ],
 "fin": ["Question pour les commentaires ? 👇", "Tous nos conseils pour…<br>… 🐾"],
 "legende": "Légende TikTok (avec la question et « educanimaux.fr (lien en bio) »)",
 "hashtags": "#chien #educationcanine #dogsoftiktok #educanimaux"   // 4 maximum
}
```

Visuels possibles :
- chat : `{"type":"chat","queue":"droite|question|fouette|gonflee|enroulee","yeux":"normal|content|agace|peur|dort","oreilles":"|plaquees|avion|detendues","deco":"coeur|zzz|os|balle|friandise|interdit|ok"}`
- chien : `{"type":"chien","pose":"assis|debout|couche","tete":-15..15,"deco":"coeur|zzz|os|balle|friandise|interdit|ok"}`
- illustration du site : `{"type":"illu","nom":"laisse|rappel|harnais|griffoir|chiot-jouet|assis-leurre|chat-clicker|lapin|…"}`
- emoji : `{"type":"emoji","texte":"🦴"}`

Sons : pop, pop2, ding, miaou, ouaf, whoosh, boom, crash, scratch, fete.

## Règles de contenu

- Tutoiement (ton TikTok), phrases très courtes, 1 emoji par ligne maximum.
- **4 hashtags maximum** dans le champ `hashtags`, dont toujours `#educanimaux` (ex. chien : `#chien #educationcanine #dogsoftiktok #educanimaux` ; chat : `#chat #comportementchat #catsoftiktok #educanimaux`).
- Uniquement des conseils exacts et bienveillants (comme sur le site) : jamais de punition, pas de chiffres inventés,
  renvoi au vétérinaire pour la santé.
- Accroche forte (« 5 erreurs… », « Ton chat fait ça ? », « Ce que ton chien essaie de te dire »…),
  question à la fin pour faire commenter.
- Varier : chien / chat / chien la même semaine ou chat / chien / chat, et alterner les formats.

## Sujets à venir (cocher quand la vidéo est faite)

- [x] 5 erreurs qui stressent ton chien (2026-10-19)
- [x] 5 choses que ton chat déteste (2026-10-21)
- [x] Ton chien fait ça ? Ce que ça veut dire (2026-10-23)
- [x] 5 signes que ton chien t'aime (2026-10-22)
- [x] Pourquoi ton chat fait ses griffes sur le canapé (et la solution) (2026-10-26)
- [x] 5 aliments dangereux pour ton chien (2026-10-27)
- [x] 5 aliments dangereux pour ton chat (2026-10-28)
- [x] Ton chat fait ça ? Ce que ça veut dire (2026-10-20)
- [x] 5 jeux pour occuper ton chien quand il pleut (2026-10-25)
- [x] 5 signes que ton chat s'ennuie (2026-10-24)
- [x] Chiot : les 5 règles de la première semaine (2026-10-29)
- [x] Pourquoi ton chien tire en laisse (et comment arrêter) (2026-10-31)
- [x] Mythe ou réalité : les idées reçues sur les chats (2026-10-30)
- [x] Mythe ou réalité : les idées reçues sur les chiens (2026-10-27)
- [x] 5 signes que ton chien est stressé (2026-10-22)
- [x] 5 bruits du quotidien qui font peur aux chats (2026-11-01)
- [ ] Comment apprendre « assis » en 3 étapes
- [ ] 5 erreurs avec la litière
- [x] Ce que la position de sommeil de ton chien veut dire (2026-11-03)
- [x] 5 choses que ton chien déteste (2026-11-08)
- [x] Chat d'intérieur : 5 idées pour qu'il soit heureux (2026-10-25, en 3D)
- [x] Le rappel du chien en 4 étapes (2026-11-05)
- [x] 5 signes que ton chat te fait confiance (2026-11-07)
- [ ] Préparer son chien aux pétards du Nouvel An (à publier fin décembre)
- [x] 5 cadeaux de Noël utiles pour chien et chat (2026-12-02)
- [ ] Ton chien mange trop vite ? 5 astuces
- [ ] Pourquoi ton chat ronronne (pas que de bonheur)
- [ ] 5 erreurs quand on adopte un chaton
- [ ] Chien seul à la maison : 5 conseils
- [ ] Pourquoi ton chat te mordille pendant les caresses
- [ ] 5 signes que ton chien a mal (vétérinaire)
- [ ] Comment présenter un chat à un chien
- [ ] 5 plantes toxiques pour les chats
- [ ] Pourquoi ton chien mange de l'herbe
- [ ] Chiot qui mordille : que faire
- [x] Pourquoi ton chat miaule la nuit (2026-11-04)
- [ ] 5 règles pour une balade réussie
- [ ] Brosser son chat : 5 astuces
- [ ] Ton chien aboie à la porte ? 4 étapes
- [ ] 5 signes que ton chat est stressé
- [ ] Apprendre « couché » en 3 étapes
- [ ] Pourquoi ton chat dort autant
- [ ] 5 erreurs de récompense avec ton chien
- [ ] Le bon griffoir pour ton chat
- [ ] Chien qui saute sur les gens : la solution
- [ ] Pourquoi ton chat renverse son verre d'eau
- [ ] 5 choses à faire avant d'adopter un chien
- [ ] Ton chat et le transport chez le vétérinaire
- [ ] Chien et chaleur/froid : 5 conseils
- [ ] Comment apprendre « au pied » en douceur
- [ ] Pourquoi ton chat aime les cartons
- [x] Changement d'heure : ton chien ne le sait pas (2026-10-24)
- [x] POV : ton chat fait semblant de ne pas t'avoir vu (2026-10-28)
- [x] Halloween : 5 dangers pour chien et chat (2026-10-30)
- [x] Ton chat fait pipi à côté de sa litière ? 5 raisons (2026-11-02)
- [x] Ton chat te réveille à 4 h du matin ? (2026-11-04)
- [x] Quelle litière ton chat préfère vraiment ? (2026-11-06)
