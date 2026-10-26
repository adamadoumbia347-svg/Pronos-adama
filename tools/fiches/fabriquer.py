"""Fiches gratuites à imprimer (PDF A4) + aperçus PNG + page docs/fiches-gratuites.html.

Usage : python3 tools/fiches/fabriquer.py
Sorties : docs/fiches/<nom>.pdf et docs/fiches/<nom>.png (aperçu), page « Fiches gratuites » (français).
"""
import html
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
RACINE = ICI.parent.parent
DOCS = RACINE / "docs"
sys.path.insert(0, str(ICI.parent))
import creer_page  # noqa: E402

CSS = """
@font-face { font-family: 'Nunito'; src: url('../../docs/fonts/nunito-latin.woff2') format('woff2'); font-weight: 400 900; }
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Nunito', sans-serif; color: #2b2420; }
.page { width: 210mm; height: 297mm; padding: 14mm 14mm 12mm; position: relative; background: #fffaf3; overflow: hidden; }
.haut { display: flex; justify-content: space-between; align-items: center; font-weight: 900; color: #b44c1c; font-size: 13pt; }
.haut span { color: #2f7d6d; font-size: 10pt; font-weight: 800; }
h1 { font-size: 25pt; line-height: 1.1; margin: 7mm 0 2mm; }
.sous { color: #6b5f57; font-size: 11.5pt; margin: 0 0 6mm; }
h2 { font-size: 14pt; margin: 6mm 0 2.5mm; color: #b44c1c; }
p, li { font-size: 11pt; line-height: 1.45; }
ul, ol { margin: 0; padding-left: 6mm; }
.boite { background: #fff; border: 1.2pt solid #eadfd3; border-radius: 4mm; padding: 4mm 5mm; margin-top: 4mm; }
.vert { background: #e6f4ef; border-color: #b9e0d2; }
.rouge { background: #fdecea; border-color: #f3c6c0; }
table { width: 100%; border-collapse: collapse; margin-top: 3mm; background: #fff; }
th, td { border: 1pt solid #d9c9b8; padding: 2.4mm 1.5mm; text-align: center; font-size: 10pt; }
th { background: #fbefe2; font-weight: 900; }
table.grand td { height: 13mm; }
td.j { font-weight: 800; text-align: left; padding-left: 3mm; width: 22mm; }
.case { display: inline-block; width: 4.2mm; height: 4.2mm; border: 1.3pt solid #b44c1c; border-radius: 1mm; margin-right: 2.5mm; vertical-align: -0.6mm; }
.check li { list-style: none; margin: 1.6mm 0; }
.check { padding-left: 0; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.pied { position: absolute; left: 14mm; right: 14mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 9pt; color: #6b5f57; border-top: 1pt solid #eadfd3; padding-top: 2.5mm; }
.pied b { color: #b44c1c; }
"""


def page(titre, sous, corps):
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><style>{CSS}</style></head><body><div class="page">
<div class="haut">🐾 Éduc'Animaux <span>Fiche gratuite à imprimer</span></div>
<h1>{titre}</h1><p class="sous">{sous}</p>{corps}
<div class="pied"><span>Méthodes bienveillantes · ne remplace pas l'avis de votre vétérinaire</span><b>educanimaux.fr</b></div>
</div></body></html>"""


JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOMENTS = ["Réveil", "Après repas 1", "Après sieste", "Après repas 2", "Après jeu", "Soir", "Coucher"]
proprete = page("Planning propreté du chiot", "Notez chaque sortie : ✓ pipi dehors · ✗ accident à la maison. En une ou deux semaines, vous verrez ses horaires se dessiner.", f"""
<div class="boite vert"><strong>Les moments où il faut sortir :</strong> au réveil, juste après chaque repas, après le jeu ou une sieste, toutes les 1 à 2 heures en journée, et avant le coucher. Restez avec lui dehors et félicitez-le <strong>au moment même</strong> où il fait.</div>
<table class="grand"><thead><tr><th></th>{"".join(f"<th>{m}</th>" for m in MOMENTS)}</tr></thead>
<tbody>{"".join(f'<tr><td class="j">{j}</td>' + "<td></td>" * len(MOMENTS) + "</tr>" for j in JOURS)}</tbody></table>
<div class="cols">
<div class="boite"><strong>✅ À faire</strong><ul><li>Toujours le même coin dehors</li><li>Une friandise juste après</li><li>Surveiller : il renifle, tourne en rond = on sort</li><li>Nettoyer les accidents avec un nettoyant enzymatique</li></ul></div>
<div class="boite rouge"><strong>❌ À éviter</strong><ul><li>Gronder ou mettre son nez dedans</li><li>L'eau de Javel (odeur proche de l'urine)</li><li>Le laisser seul trop longtemps au début</li><li>Les tapis éducateurs comme solution durable</li></ul></div>
</div>
<div class="boite"><strong>Notes :</strong><br><br><br></div>""")

KIT = [("😴 Repos", ["Un parc ou une barrière", "Un panier ou une caisse confortable", "Un plaid qui sent sa mère ou son ancienne maison"]),
       ("🍽️ Repas", ["Deux gamelles stables", "La même alimentation qu'avant son arrivée", "Des friandises d'éducation pour chiot"]),
       ("🦮 Balade", ["Un harnais léger", "Une laisse de 2 m", "Une médaille avec votre numéro de téléphone", "Des sacs à crottes"]),
       ("🎓 Éducation", ["Une pochette à friandises", "Un clicker (facultatif)", "Une longe de 5 à 10 m (plus tard)"]),
       ("🦴 Jeux", ["Des jouets à mâcher pour la dentition", "Un jouet à remplir pour chiot", "Un jouet de tir ou une peluche solide"]),
       ("🧼 Soins et maison", ["Un nettoyant enzymatique", "Une brosse adaptée à son poil", "Câbles et produits ménagers hors de portée"]),
       ("🩺 Santé", ["Le carnet de santé et l'identification", "Un premier rendez-vous chez le vétérinaire", "Le numéro de votre vétérinaire noté"])]
kit = page("Accueillir un chiot : la check-list", "Cochez au fur et à mesure. Pas besoin de tout acheter le premier jour : l'essentiel, c'est un coin calme, de bonnes habitudes et beaucoup de patience.",
           '<div class="cols">' + "".join(f'<div class="boite"><strong>{t}</strong><ul class="check">' + "".join(f'<li><span class="case"></span>{html.escape(x)}</li>' for x in l) + "</ul></div>" for t, l in KIT) +
           '<div class="boite rouge"><strong>🚫 Inutile ou à éviter</strong><ul><li>Collier étrangleur, à pointes ou électrique</li><li>Une montagne de jouets d\'un coup</li></ul></div></div>')

assis = page("Assis, couché, pas bouger : l'aide-mémoire", "Séances de 3 à 5 minutes, plusieurs fois par jour, avec de toutes petites friandises. Toujours finir sur une réussite.", """
<div class="cols">
<div class="boite"><h2 style="margin-top:0">🪑 Assis</h2><ol><li>Friandise devant sa truffe.</li><li>Montez-la doucement au-dessus de sa tête.</li><li>Ses fesses touchent le sol : « oui ! » + friandise.</li><li>Après 5 à 10 réussites : même geste sans friandise en main.</li><li>Ajoutez le mot « assis » juste avant le geste.</li></ol></div>
<div class="boite"><h2 style="margin-top:0">🛏️ Couché</h2><ol><li>Partez de l'assis.</li><li>Descendez la friandise entre ses pattes avant.</li><li>Puis vers l'avant, au ras du sol.</li><li>Coudes au sol : « oui ! » + friandise au sol.</li><li>Retirez la friandise de la main, ajoutez le mot.</li></ol></div>
</div>
<div class="boite"><h2 style="margin-top:0">🧘 Pas bouger : les 3 D, un seul à la fois</h2>
<p><strong>Mot de libération</strong> (« ok ») pour dire « tu peux bouger ».</p>
<ul><li><strong>Durée</strong> : 1 seconde, récompense pendant qu'il est assis, puis 2, 3, 5, 10…</li><li><strong>Distance</strong> : revenez à une durée courte, faites 1 pas en arrière, revenez récompenser.</li><li><strong>Distractions</strong> : en dernier, dans un endroit facile, en réduisant durée et distance.</li></ul>
<p>Retournez toujours vers lui pour le récompenser : ne l'appelez pas pour finir l'exercice.</p></div>
<div class="cols">
<div class="boite vert"><strong>✅ S'il se trompe</strong><p>Pas de reproche : replacez-le calmement et rendez l'exercice plus facile. Visez une réussite presque à chaque essai.</p></div>
<div class="boite rouge"><strong>❌ À ne pas faire</strong><p>Appuyer sur son dos, tirer sur la laisse, répéter l'ordre (« assis, assis, ASSIS »), punir.</p></div>
</div>
<div class="boite"><strong>Mes progrès :</strong> &nbsp;<span class="case"></span>Assis &nbsp; <span class="case"></span>Couché &nbsp; <span class="case"></span>Pas bouger 5 s &nbsp; <span class="case"></span>Pas bouger 3 pas &nbsp; <span class="case"></span>En balade</div>""")

FICHES = [("planning-proprete-chiot", "Planning propreté du chiot", "Un tableau sur 7 jours pour noter ses sorties et repérer ses horaires, avec les bons réflexes.", proprete, "proprete-chiot.html", "la propreté du chiot"),
          ("checklist-accueil-chiot", "Accueillir un chiot : la check-list", "Tout le matériel à prévoir, classé par thème, à cocher avant et après son arrivée.", kit, "kit-accueil-chiot.html", "la liste complète du matériel"),
          ("aide-memoire-assis-couche", "Assis, couché, pas bouger : l'aide-mémoire", "Les étapes de chaque exercice sur une page, à afficher sur le frigo.", assis, "apprendre-assis-couche-pas-bouger.html", "l'article complet")]

RENDU = """
const { chromium } = require('playwright');
(async () => {
  const [,, html, pdf, png] = process.argv;
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await p.screenshot({ path: png, type: 'png' });
  await b.close();
})();
"""

if __name__ == "__main__":
    sortie = DOCS / "fiches"; sortie.mkdir(exist_ok=True)
    (ICI / "_rendu.js").write_text(RENDU, encoding="utf-8")
    env = {**__import__("os").environ, "NODE_PATH": subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()}
    cartes = ""
    for nom, titre, desc, contenu, lien, lien_txt in FICHES:
        src = ICI / f"_{nom}.html"; src.write_text(contenu, encoding="utf-8")
        png_tmp = ICI / f"_{nom}.png"
        subprocess.run(["node", str(ICI / "_rendu.js"), str(src), str(sortie / f"{nom}.pdf"), str(png_tmp)], check=True, env=env)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(png_tmp), "-vf", "scale=400:-1", str(sortie / f"{nom}.png")], check=True)
        png_tmp.unlink(); src.unlink()
        cartes += (f'          <div class="card fiche"><img src="fiches/{nom}.png" alt="Aperçu : {html.escape(titre)}" width="400" height="566" loading="lazy">'
                   f'<h3>{html.escape(titre)}</h3><p>{html.escape(desc)}</p>'
                   f'<p class="btn-row"><a class="btn btn-sm" href="fiches/{nom}.pdf" download>⬇️ Télécharger le PDF</a></p>'
                   f'<p class="small">Pour aller plus loin : <a href="{lien}">{lien_txt}</a></p></div>\n')
    (ICI / "_rendu.js").unlink()
    corps = f"""    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Fiches gratuites</p>
        <h1>🖨️ Fiches gratuites à imprimer</h1>
        <p class="lead">Des aide-mémoire pratiques à imprimer ou à garder sur votre téléphone : planning propreté, check-list d'accueil du chiot, exercices d'éducation. Gratuit, sans inscription.</p>
        <div class="grid grid-3 fiches">
{cartes}        </div>
        <p>Une idée de fiche qui vous serait utile ? Écrivez-nous depuis la page <a href="apropos.html#contact">contact</a>.</p>
      </div>
    </section>"""
    creer_page.creer("fr", "fiches-gratuites", "Fiches gratuites à imprimer pour chien et chiot",
                     "Planning propreté du chiot, check-list d'accueil, aide-mémoire assis-couché-pas bouger : nos fiches gratuites en PDF, à imprimer, sans inscription.",
                     corps, menu="🖨️ Fiches à imprimer")
    creer_page.finir()
    print(len(FICHES), "fiches")
