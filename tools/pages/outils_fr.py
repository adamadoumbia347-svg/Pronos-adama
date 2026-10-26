"""Outils interactifs (français) : programme « 30 jours avec mon chiot », calculateur de budget, quiz « Quel animal pour moi ? ».

Usage : python3 tools/pages/outils_fr.py
Les données sont intégrées à la page (JSON) et lues par js/programme.js, js/budget.js et js/quel-animal.js.
Aucun montant n'est fourni : le calculateur additionne uniquement les montants saisis par le visiteur.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

e = html.escape

# ---------- Programme 30 jours ----------
# (semaine, titre, consigne, lien)
JOURS = [
 (1, "Lui apprendre son nom", "Dites son nom d'une voix joyeuse ; dès qu'il vous regarde, une friandise. 5 fois, 3 fois dans la journée.", "noms-chien-chat.html"),
 (1, "Son coin repos", "Installez son couchage dans un endroit calme. Déposez-y une friandise ou un jouet à mâcher quand il s'y couche de lui-même.", "kit-accueil-chiot.html"),
 (1, "La routine pipi", "Sortez-le au réveil, après chaque repas, après le jeu et toutes les 1 à 2 heures. Félicitez-le dehors, au moment même.", "proprete-chiot.html"),
 (1, "Les manipulations douces", "Touchez une patte, une oreille, regardez ses dents une seconde, puis friandise. Arrêtez s'il se crispe.", "methodes.html#cooperative-care"),
 (1, "Seul quelques secondes", "Sortez de la pièce 10 secondes et revenez calmement, avant qu'il ne pleure. Allongez très progressivement.", "chien-aboie-seul.html"),
 (1, "Mâchouiller les bonnes choses", "Proposez-lui un jouet à mâcher adapté ; s'il mordille vos mains, remplacez-les par le jouet.", "chiot-mord.html"),
 (1, "Pause bilan", "Une journée sans nouveauté : jeux calmes, câlins, sommeil. Un chiot dort beaucoup, c'est normal.", ""),
 (2, "Assis", "Avec une friandise au-dessus de sa tête : dès que ses fesses touchent le sol, « oui ! » et friandise.", "apprendre-assis-couche-pas-bouger.html"),
 (2, "Regarde-moi", "Récompensez chaque fois qu'il vous regarde dans les yeux de lui-même. C'est la base de l'attention.", "methodes.html#capture"),
 (2, "Le toucher de main", "Présentez votre main ouverte près de son nez : quand il la touche avec sa truffe, friandise.", "methodes.html#ciblage"),
 (2, "Couché", "Depuis l'assis, descendez la friandise entre ses pattes, puis vers l'avant au ras du sol.", "apprendre-assis-couche-pas-bouger.html"),
 (2, "Le harnais", "Montrez le harnais, friandise. Posez-le une seconde, friandise. Puis fermez-le quelques secondes, à la maison.", "meilleur-harnais-chien.html"),
 (2, "Le clicker (facultatif)", "Cliquez puis donnez une friandise, 10 fois : il apprend que le clic annonce une récompense.", "meilleur-clicker.html"),
 (2, "Pause bilan", "Révisez son nom, assis et le toucher de main, en 3 mini-séances d'une minute.", ""),
 (3, "Découvrir des bruits", "Faites écouter à faible volume des bruits du quotidien (aspirateur, sonnette) en jouant avec lui. Arrêtez s'il a peur.", "methodes.html#desensibilisation"),
 (3, "Rencontrer des personnes", "Laissez-le observer des gens calmes de loin et récompensez-le. Pas de contact forcé. Avant la fin des vaccins, demandez conseil à votre vétérinaire.", "methodes.html#socialisation"),
 (3, "Premiers pas en laisse", "À la maison ou au jardin : chaque fois que la laisse est détendue et qu'il est près de vous, friandise.", "marche-en-laisse.html"),
 (3, "Le rappel à la maison", "Appelez-le d'une voix joyeuse à 2 mètres, fête et friandise quand il arrive. Jamais de rappel pour une chose désagréable.", "rappel-chien.html"),
 (3, "Jeu de flair", "Cachez quelques croquettes dans un tapis de fouille ou sous des gobelets : il cherche avec son nez.", "meilleurs-jouets-occupation-chien.html"),
 (3, "La voiture", "Installez-le dans la voiture moteur éteint, avec une friandise, quelques minutes. Puis un tout petit trajet.", ""),
 (3, "Pause bilan", "Une balade tranquille où il renifle à son rythme : c'est très fatigant mentalement.", ""),
 (4, "Pas bouger", "Assis, comptez 1 seconde, récompensez, puis libérez-le avec un mot (« ok »). Augmentez très doucement.", "apprendre-assis-couche-pas-bouger.html"),
 (4, "Laisse ça", "Une friandise dans votre poing fermé : dès qu'il arrête d'essayer de l'avoir, friandise de l'autre main.", "methodes.html#renforcement-positif"),
 (4, "Le tapis calme", "Récompensez chaque fois qu'il se couche sur un tapis. Peu à peu, le tapis devient son endroit pour se poser.", "methodes.html#faconnage"),
 (4, "Brossage et toilettage", "Un coup de brosse, une friandise. Très court, très agréable, pour qu'il aime ce moment.", "methodes.html#cooperative-care"),
 (4, "Rappel dehors", "Dans un endroit sûr, avec une longe : appelez-le, récompensez généreusement, puis relâchez-le jouer.", "rappel-chien.html"),
 (4, "Visite vétérinaire « pour rien »", "Si votre vétérinaire l'accepte, passez dire bonjour : friandises et caresses, sans soin.", ""),
 (4, "Seul un peu plus longtemps", "Avec un jouet à garnir, partez quelques minutes, revenez calmement. Il doit rester serein.", "chien-aboie-seul.html"),
 (4, "Révisions en balade", "Assis, regarde-moi et rappel, chacun une fois en balade, avec une super récompense.", ""),
 (4, "Bravo !", "30 jours de bases posées. Continuez quelques minutes par jour : l'éducation dure toute la vie, dans la bonne humeur.", "chien.html"),
]
SEMAINES = {1: "Semaine 1 · Installation et confiance", 2: "Semaine 2 · Les premières bases", 3: "Semaine 3 · Découvrir le monde", 4: "Semaine 4 · Consolider"}


def programme():
    blocs = ""
    for s, titre_s in SEMAINES.items():
        items = ""
        for i, (sem, t, c, lien) in enumerate(JOURS, 1):
            if sem != s:
                continue
            lien_html = f' <a href="{lien}">En savoir plus</a>' if lien else ""
            items += (f'          <li class="jour"><label><input type="checkbox" data-jour="{i}"> <strong>Jour {i} · {e(t)}</strong></label>'
                      f'<p>{e(c)}{lien_html}</p></li>\n')
        blocs += f'        <h2>{titre_s}</h2>\n        <ol class="jours">\n{items}        </ol>\n'
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Programme chiot</p>
        <h1>🐶 30 jours avec mon chiot : le programme d'éducation</h1>
        <p class="lead">Un petit exercice par jour, 5 à 10 minutes, pour poser les bases en douceur : son nom, la propreté, assis, le rappel, la laisse… Cochez chaque jour réussi : votre progression est gardée sur cet appareil, sans inscription.</p>
        <div class="card progression"><p><strong id="prog-texte">0 / 30 jours</strong></p><div class="barre-prog"><span id="prog-barre"></span></div>
          <p class="small muted">Pas de pression : si un exercice est difficile, refaites-le le lendemain. Chaque chiot avance à son rythme.</p>
          <button type="button" class="btn btn-sm btn-outline" id="prog-raz">Recommencer à zéro</button></div>
{blocs}        <div class="callout"><strong>Les règles du programme :</strong> séances très courtes, toujours avec des récompenses, jamais de punition. Arrêtez avant qu'il se lasse. Pour les sorties et les rencontres avant la fin des vaccins, suivez les conseils de votre vétérinaire.</div>
        <p>Pour aller plus loin : <a href="kit-accueil-chiot.html">le matériel pour accueillir un chiot</a> · <a href="meilleures-friandises-education-chien.html">quelles friandises choisir ?</a> · <a href="chien.html">le guide complet du chien</a>.</p>
      </div>
    </section>"""


# ---------- Budget ----------
POSTES = [
 ("Dépenses régulières (par mois)", "mois", [
   ("alim", "Alimentation (croquettes, pâtée)", "ct"), ("friandises", "Friandises et jouets", "ct"), ("litiere", "Litière", "t"),
   ("assurance", "Assurance santé animale", "ct"), ("antiparasitaire", "Antiparasitaires (si vous payez au mois)", "ct")]),
 ("Dépenses annuelles (par an)", "an", [
   ("veto", "Vétérinaire : vaccins et visite de contrôle", "ct"), ("toilettage", "Toilettage", "ct"), ("garde", "Garde ou pension pendant les vacances", "ct"),
   ("education", "Cours d'éducation", "c"), ("divers", "Imprévus et divers", "ct")]),
 ("Dépenses de départ (une seule fois)", "unique", [
   ("adoption", "Adoption ou achat", "ct"), ("identification", "Identification, premiers vaccins", "ct"), ("sterilisation", "Stérilisation ou castration", "ct"),
   ("materiel", "Matériel de départ (couchage, gamelles, laisse ou caisse…)", "ct")]),
]


def budget():
    groupes = ""
    for titre, periode, champs in POSTES:
        lignes = "".join(f'<div class="poste" data-especes="{esp}"><label for="b-{k}">{e(lab)}</label><input id="b-{k}" type="number" min="0" step="1" inputmode="decimal" placeholder="0" data-periode="{periode}"> <span>€</span></div>'
                         for k, lab, esp in champs)
        groupes += f'          <fieldset><legend>{titre}</legend>{lignes}</fieldset>\n'
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Budget</p>
        <h1>💶 Combien coûte un chien ou un chat ? Calculez votre budget</h1>
        <p class="lead">Avant d'adopter, ou pour faire le point : entrez vos propres montants (devis du vétérinaire, prix de ses croquettes, assurance…) et obtenez le coût par mois, par an et pour la première année.</p>
        <div class="card" id="calc-budget">
          <div class="choix-espece" role="radiogroup" aria-label="Animal">
            <label><input type="radio" name="b-espece" value="c" checked><span>🐕 Chien</span></label>
            <label><input type="radio" name="b-espece" value="t"><span>🐈 Chat</span></label>
          </div>
{groupes}          <div class="budget-total" aria-live="polite">
            <p>Par mois : <strong id="t-mois">0 €</strong></p>
            <p>Par an : <strong id="t-an">0 €</strong></p>
            <p>Première année (avec les dépenses de départ) : <strong id="t-premiere">0 €</strong></p>
          </div>
          <p class="small muted">Le calcul additionne uniquement vos montants. Vos chiffres restent sur votre appareil.</p>
        </div>
        <h2>Où trouver les bons montants ?</h2>
        <ul>
          <li><strong>Alimentation</strong> : regardez la ration conseillée sur le paquet pour le poids de votre animal, et combien de temps dure un sac.</li>
          <li><strong>Vétérinaire</strong> : demandez le prix d'une consultation, des vaccins et, si besoin, de la stérilisation. Les tarifs varient selon les cliniques.</li>
          <li><strong>Assurance</strong> : comparez plusieurs devis, en regardant les plafonds et ce qui est exclu.</li>
          <li><strong>Garde</strong> : pension, pet-sitter ou proche : pensez-y avant les vacances.</li>
          <li><strong>Imprévus</strong> : un accident ou une maladie arrive. Mettre un peu de côté chaque mois évite les mauvaises surprises.</li>
        </ul>
        <p>Pour bien préparer l'arrivée : <a href="kit-accueil-chiot.html">la liste du matériel pour un chiot</a> · <a href="promos-animaux.html">les promos animalerie du moment</a> · <a href="quel-animal.html">quel animal est fait pour vous ?</a></p>
      </div>
    </section>"""


# ---------- Quiz « Quel animal pour moi ? » ----------
# points : chien_actif, chien_calme, chat, lapin, rongeur, oiseau
QUIZ = [
 ("Où vivez-vous ?", [("Appartement", [0, 2, 3, 2, 3, 2]), ("Maison sans jardin", [1, 2, 3, 2, 2, 2]), ("Maison avec jardin", [3, 2, 2, 3, 1, 2])]),
 ("Combien de temps pouvez-vous lui consacrer chaque jour ?", [("Moins d'une heure", [0, 0, 3, 1, 3, 1]), ("1 à 2 heures", [1, 3, 2, 3, 2, 2]), ("Plus de 2 heures", [3, 3, 2, 2, 1, 3])]),
 ("Vos journées d'absence ?", [("Souvent plus de 8 heures", [0, 0, 3, 2, 3, 0]), ("Quelques heures", [2, 3, 2, 2, 2, 2]), ("Je suis souvent à la maison", [3, 3, 2, 2, 2, 3])]),
 ("Votre envie de balades et d'activité ?", [("Sport, randonnée, j'adore bouger", [3, 1, 0, 0, 0, 0]), ("Balades tranquilles", [1, 3, 1, 1, 1, 1]), ("Plutôt cocooning", [0, 1, 3, 2, 2, 1])]),
 ("Le bruit et le désordre ?", [("Pas de souci", [2, 2, 2, 1, 1, 3]), ("Je préfère le calme", [1, 2, 3, 2, 2, 0])]),
 ("Quelle relation recherchez-vous ?", [("Un compagnon qui me suit partout", [3, 3, 1, 1, 0, 1]), ("Un compagnon indépendant", [0, 0, 3, 1, 2, 0]), ("Observer et interagir à ses moments", [0, 0, 1, 3, 3, 2])]),
]
RESULTATS = [
 ("🐕 Un chien sportif", "Vous avez du temps, de l'énergie et l'envie de bouger : un chien actif sera un super partenaire de balades et de jeux. Prévoyez du temps chaque jour pour l'éducation et les sorties.", "chien.html"),
 ("🐕 Un chien calme", "Un chien d'un tempérament posé vous conviendra : il aime les balades tranquilles et la vie de famille. Renseignez-vous sur la race ou adoptez un adulte au caractère connu.", "chien.html"),
 ("🐈 Un chat", "Un chat s'adapte bien à votre rythme et à votre logement. Prévoyez des griffoirs, des jeux chaque jour et des endroits en hauteur pour qu'il soit heureux.", "chat.html"),
 ("🐇 Des lapins", "Le lapin est un animal sociable, qui vit mieux à deux, et qui a besoin d'espace pour courir chaque jour, pas seulement d'une cage. Il demande du temps et des soins réguliers.", "nac.html"),
 ("🐀 Des rongeurs", "Rats, cochons d'Inde ou gerbilles peuvent vous convenir : souvent sociables entre eux (à adopter à plusieurs selon l'espèce), ils demandent un grand habitat et de l'attention chaque jour.", "nac.html"),
 ("🦜 Un oiseau", "Un oiseau de compagnie demande beaucoup de présence, d'interactions et de stimulation. Il peut être bruyant et vivre longtemps : renseignez-vous bien sur l'espèce avant de vous engager.", "nac.html"),
]


def quel_animal():
    donnees = {"q": [{"t": q, "r": [{"t": t, "p": p} for t, p in r]} for q, r in QUIZ],
               "res": [{"t": t, "d": d, "l": l} for t, d, l in RESULTATS]}
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Quel animal pour moi ?</p>
        <h1>🤔 Quel animal est fait pour moi ?</h1>
        <p class="lead">Chien sportif, chien calme, chat, lapins, rongeurs ou oiseau ? 6 questions sur votre logement, votre temps et vos envies pour trouver le compagnon qui vous correspond.</p>
        <div class="card" id="quel-animal"><div class="qa-zone" aria-live="polite"><noscript>Ce quiz nécessite JavaScript.</noscript></div></div>
        <script type="application/json" id="donnees-quel-animal">{json.dumps(donnees, ensure_ascii=False)}</script>
        <h2>Avant d'adopter, posez-vous ces questions</h2>
        <ul>
          <li><strong>Sur combien d'années je m'engage ?</strong> Un chien ou un chat vit souvent plus de 10 ans : pensez à vos projets (déménagement, enfants, travail).</li>
          <li><strong>Qui s'en occupe pendant les vacances ?</strong> Prévoyez une solution de garde avant d'adopter.</li>
          <li><strong>Quel budget ?</strong> Faites le calcul avec notre <a href="budget-animal.html">calculateur de budget</a>.</li>
          <li><strong>Tout le monde est d'accord ?</strong> Y compris pour les allergies : passez du temps avec l'espèce avant de vous décider.</li>
          <li><strong>Et si j'adoptais en refuge ?</strong> Beaucoup d'animaux attendent une famille, et le caractère d'un adulte est déjà connu.</li>
        </ul>
        <p class="small muted">Ce quiz donne une orientation, pas une certitude : chaque animal a sa personnalité.</p>
      </div>
    </section>"""


if __name__ == "__main__":
    creer_page.creer("fr", "programme-chiot-30-jours", "30 jours avec mon chiot : le programme d'éducation jour par jour",
                     "Un exercice par jour pendant 30 jours pour éduquer votre chiot en douceur : nom, propreté, assis, rappel, laisse. Progression gardée, sans inscription.",
                     programme(), scripts=["js/programme.js"], menu="🐶 Programme chiot 30 jours")
    creer_page.creer("fr", "budget-animal", "Combien coûte un chien ou un chat ? Calculez votre budget",
                     "Calculez le budget de votre chien ou chat avec vos propres montants : alimentation, vétérinaire, assurance, garde. Coût par mois, par an et la 1re année.",
                     budget(), scripts=["js/budget.js"], menu="💶 Calculer son budget")
    creer_page.creer("fr", "quel-animal", "Quel animal est fait pour moi ? Le quiz avant d'adopter",
                     "Chien, chat, lapins, rongeurs ou oiseau : 6 questions sur votre logement, votre temps et vos envies pour trouver l'animal qui vous correspond avant d'adopter.",
                     quel_animal(), scripts=["js/quel-animal.js"], menu="🤔 Quel animal pour moi ?")
    creer_page.finir()
