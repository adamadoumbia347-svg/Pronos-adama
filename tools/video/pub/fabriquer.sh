#!/bin/sh
# Vidéo de pub TikTok du site (30 s) : captures du site -> animation -> MP4 1080×1920
# Usage : sh tools/video/pub/fabriquer.sh   (le site doit être servi sur http://localhost:8766 depuis docs/)
set -e
ICI=$(cd "$(dirname "$0")" && pwd); RACINE="$ICI/../../.."
export NODE_PATH=$(npm root -g)
node "$ICI/captures.js"
TMP=$(mktemp -d)
node "$ICI/../drole/rendu.js" "$ICI/pub.html" "$TMP"
python3 "$ICI/../drole/audio.py" "$TMP/sons.json" 2 "$TMP/son.wav"
mkdir -p "$RACINE/videos/fr"
ffmpeg -nostdin -y -v error -framerate 30 -i "$TMP/f%04d.png" -i "$TMP/son.wav" -vf scale=1080:1920:flags=lanczos \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart "$RACINE/videos/fr/pub-site-educanimaux.mp4"
rm -r "$TMP"
echo "Vidéo : videos/fr/pub-site-educanimaux.mp4"
