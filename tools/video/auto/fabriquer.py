"""Fabrique une vidéo TikTok « cartes » (chiens / chats) à partir d'un fichier de description JSON.

Usage : python3 tools/video/auto/fabriquer.py tools/video/auto/sujets/<nom>.json [--apercu]
Sortie : videos/auto/<nom>.mp4 (1080×1920, ~25 s, motion design, musique + bruitages) et videos/auto/<nom>.txt (légende).
Avec --apercu : 6 images de contrôle dans un dossier temporaire (affiché), sans vidéo.

Format du JSON : voir tools/video/auto/README.md.
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile

ICI = pathlib.Path(__file__).resolve().parent
RACINE = ICI.parent.parent.parent
spec_path = pathlib.Path(sys.argv[1]).resolve()
apercu = "--apercu" in sys.argv
spec = json.loads(spec_path.read_text(encoding="utf-8"))
nom = spec_path.stem
(ICI / "spec.js").write_text("window.SPEC = " + json.dumps(spec, ensure_ascii=False) + ";", encoding="utf-8")
env = {**os.environ, "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()}
tmp = pathlib.Path(tempfile.mkdtemp(prefix="video-" + nom + "-"))
rendu = ICI.parent / "drole" / "rendu.js"
# Style : « motion » (motion design, par défaut), « 3d » (motion design 3D, Three.js) ou « cartes » (ancien modèle)
modele = {"cartes": "modele.html", "3d": "modele-3d.html"}.get(spec.get("style"), "modele-motion.html")
shutil.copy(ICI / modele, ICI / "_video.html")
subprocess.run(["node", str(rendu), str(ICI / "_video.html"), str(tmp)] + (["preview"] if apercu else []), check=True, env=env)
if apercu:
    print("Aperçu :", tmp)
    sys.exit(0)
subprocess.run([sys.executable, str(ICI.parent / "drole" / "audio.py"), str(tmp / "sons.json"), str(spec.get("musique", 3)), str(tmp / "son.wav")], check=True)
sortie = RACINE / "videos" / "auto"; sortie.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-framerate", "30", "-i", str(tmp / "f%04d.png"), "-i", str(tmp / "son.wav"),
                "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(sortie / f"{nom}.mp4")], check=True)
(sortie / f"{nom}.txt").write_text(spec.get("legende", "").strip() + "\n\n" + spec.get("hashtags", "").strip() + "\n", encoding="utf-8")
shutil.rmtree(tmp)
print("Vidéo :", sortie / f"{nom}.mp4")
