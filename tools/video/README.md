# Générateur de vidéos TikTok

Vidéos verticales 1080×1920 de 22 s : accroche, 3 astuces, appel à l'action vers educanimaux.fr.

1. Ajouter une entrée dans `serie.json` (couleurs, accroche, 3 astuces, appel à l'action).
2. Générer les images (Playwright + Chromium) : `node serie-frames.js <index> full <dossier>`
   (`preview` au lieu de `full` pour 6 images de contrôle).
3. Générer la musique originale : `python3 musique-serie.py <index> musique.wav`
4. Assembler : `ffmpeg -framerate 30 -i <dossier>/f%04d.png -i musique.wav -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -shortest video.mp4`

Garder les textes hors du bas de l'écran et du bord droit (zones des boutons TikTok).

## Vidéos humoristiques (`drole/`)

Chaque sketch est une page HTML (`1-retour-maison.html`…) avec une fonction `render(t)` et la liste des bruitages (`son(t, type)`).

1. Images : `node drole/rendu.js <sketch.html> <dossier>` (ajouter `preview` pour 6 images de contrôle) ; écrit aussi `sons.json`.
2. Bande-son (musique + bruitages : pop, ding, miaou, whoosh, boom, crash, scratch, fete) : `python3 drole/audio.py <dossier>/sons.json <variante> son.wav`
3. Assemblage avec ffmpeg comme ci-dessus.
