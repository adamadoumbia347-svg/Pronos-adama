"""Fiches races (français) + page « Races » qui les regroupe.

Usage : python3 tools/pages/races.py
Contenu volontairement prudent : pas de chiffres (poids, espérance de vie…) ; points de santé
connus pour la race, toujours avec un renvoi vers le vétérinaire et les dépistages des parents.
"""
import html
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

e = html.escape


def boite(icone, nom, pourquoi, cle, q):
    return (f'        <div class="product-box">\n          <span class="icon">{icone}</span>\n'
            f'          <div><strong>{nom}</strong><p>{pourquoi}</p></div>\n'
            f'          <a class="btn btn-sm aff" data-aff="{cle}" data-q="{q}" href="https://www.amazon.fr/s?k={q.replace(" ", "+")}">Voir les prix</a>\n        </div>\n')


HARNAIS = boite("🦺", "Harnais en Y", "Confortable et sans pression sur la gorge, idéal pour apprendre la marche en laisse.", "harnais", "harnais chien en Y deux anneaux")
KONG = boite("🦴", "Jouet à garnir", "Une activité calme qui occupe sa tête, parfait quand il reste seul.", "kong", "jouet à garnir chien kong")
FOUILLE = boite("🧺", "Tapis de fouille", "Il cherche ses croquettes avec son nez : une vraie dépense mentale.", "tapis-fouille", "tapis de fouille chien")
LONGE = boite("🪢", "Longe de rappel", "Pour travailler le rappel en sécurité dans les grands espaces.", "longe", "longe dressage chien 10m")

RACES = [
 {"slug": "race-berger-australien", "icone": "🐕", "nom": "Berger australien",
  "titre": "Berger australien : caractère, éducation et besoins",
  "desc": "Berger australien : caractère, besoins d'exercice, éducation, entretien et points de santé. Est-ce la bonne race pour vous ? Notre fiche complète.",
  "bref": "Un chien de troupeau <strong>très intelligent, énergique et attaché à sa famille</strong>. Idéal pour des maîtres actifs, prêts à lui offrir chaque jour de l'exercice et des activités pour sa tête.",
  "sections": [
   ("Son caractère", "<p>Le berger australien a été sélectionné pour travailler avec les troupeaux : il est vif, attentif, très proche de ses humains et apprend vite. Il peut être réservé avec les inconnus. Comme beaucoup de chiens de berger, il a parfois tendance à vouloir « rassembler » ce qui bouge (enfants, vélos, autres animaux) : c'est un instinct, à canaliser par le jeu et l'éducation, jamais par la punition.</p>"),
   ("Ses besoins", "<p>C'est une race qui a besoin de <strong>beaucoup d'activité</strong>, physique et surtout mentale. Un berger australien qui s'ennuie invente ses propres occupations : aboiements, destructions, poursuites. Prévoyez chaque jour de vraies balades, des jeux de flair, des exercices d'éducation et, si possible, une activité canine (agility, obéissance, troupeau).</p>"),
   ("L'éducation", "<p>Il adore apprendre, ce qui en fait un excellent élève pour le <a href=\"methodes.html#clicker\">clicker</a> et le <a href=\"methodes.html#renforcement-positif\">renforcement positif</a>. Travaillez tôt la <a href=\"methodes.html#socialisation\">socialisation</a>, le calme (savoir ne rien faire) et le <a href=\"rappel-chien.html\">rappel</a>. Sa sensibilité fait qu'il supporte mal les méthodes dures : elles le rendent anxieux.</p>"),
   ("L'entretien", "<p>Son poil mi-long demande un brossage régulier, plus fréquent pendant les mues. Vérifiez aussi les oreilles et faites-lui apprendre les soins en douceur (<a href=\"methodes.html#cooperative-care\">soins coopératifs</a>).</p>"),
   ("Sa santé : points d'attention", "<p>Certains bergers australiens portent une mutation génétique (appelée MDR1) qui les rend sensibles à certains médicaments : un test existe, parlez-en à votre vétérinaire. Comme pour beaucoup de races, demandez à l'éleveur les dépistages des parents (hanches, yeux).</p>"),
  ],
  "produits": HARNAIS + FOUILLE + LONGE,
  "pour": ("Vous êtes sportif, souvent présent et vous aimez éduquer votre chien.", "Vous cherchez un chien calme d'appartement ou vous êtes souvent absent."),
  "liens": '<a href="rappel-chien.html">le rappel</a> · <a href="meilleurs-jouets-occupation-chien.html">les jouets d\'occupation</a> · <a href="chien.html">le guide du chien</a>'},
 {"slug": "race-labrador", "icone": "🦮", "nom": "Labrador retriever",
  "titre": "Labrador : caractère, éducation et besoins",
  "desc": "Labrador retriever : caractère, éducation, exercice, alimentation, entretien et santé. Tout savoir avant d'adopter ce chien de famille.",
  "bref": "Un chien de famille <strong>sociable, joueur et très gourmand</strong>. Facile à motiver avec des friandises, il a besoin d'exercice, d'éducation dès le plus jeune âge et d'une alimentation bien surveillée.",
  "sections": [
   ("Son caractère", "<p>Le labrador est réputé pour sa gentillesse et sa sociabilité, avec les humains comme avec les autres chiens. Jeune, il est souvent très énergique, impulsif et mâchouille beaucoup : il lui faut du temps pour devenir le chien calme qu'on imagine.</p>"),
   ("Ses besoins", "<p>Il a besoin de balades quotidiennes, de jeux de rapport et d'activités de flair. Beaucoup de labradors adorent l'eau. Sans assez d'activité, il peut devenir turbulent et destructeur.</p>"),
   ("L'éducation", "<p>Sa gourmandise est un atout : il apprend très vite avec des friandises. Travaillez tôt la <a href=\"marche-en-laisse.html\">marche en laisse</a> (c'est un chien fort qui tire volontiers), le calme et le fait de ne pas sauter sur les gens. Pensez à déduire les friandises de sa ration.</p>"),
   ("L'entretien", "<p>Son poil court perd beaucoup, surtout pendant les mues : un brossage régulier limite les poils dans la maison. Séchez bien ses oreilles après la baignade.</p>"),
   ("Sa santé : points d'attention", "<p>Le labrador a tendance à prendre du poids : surveillez sa ration et sa silhouette avec votre vétérinaire. Demandez à l'éleveur les dépistages des parents, notamment pour les hanches et les coudes.</p>"),
  ],
  "produits": HARNAIS + KONG + FOUILLE,
  "pour": ("Vous voulez un chien de famille joueur et vous avez du temps pour le sortir.", "Vous ne supportez pas les poils ou vous cherchez un chien qui se dépense peu."),
  "liens": '<a href="marche-en-laisse.html">la marche en laisse</a> · <a href="meilleures-friandises-education-chien.html">les friandises d\'éducation</a> · <a href="chien.html">le guide du chien</a>'},
 {"slug": "race-bouledogue-francais", "icone": "🐶", "nom": "Bouledogue français",
  "titre": "Bouledogue français : caractère, soins et santé",
  "desc": "Bouledogue français : caractère, éducation, besoins, entretien des plis et points de santé liés à son museau court. Notre fiche pour bien l'accueillir.",
  "bref": "Un petit chien <strong>affectueux, drôle et proche de ses maîtres</strong>, qui s'adapte bien à l'appartement. Son museau court demande des précautions, surtout avec la chaleur et l'effort.",
  "sections": [
   ("Son caractère", "<p>Le bouledogue français est un chien de compagnie très attaché à sa famille, souvent clown et têtu à la fois. Il supporte mal de rester seul longtemps et aime suivre ses humains partout.</p>"),
   ("Ses besoins", "<p>Des balades régulières mais adaptées, des jeux calmes et des activités de flair. Il ne faut pas en faire un sportif : son museau court le rend vite essoufflé.</p>"),
   ("L'éducation", "<p>Il répond bien aux récompenses, à condition de garder des séances courtes et ludiques. Travaillez tôt la solitude (<a href=\"chien-aboie-seul.html\">rester seul sans stress</a>) et la propreté.</p>"),
   ("L'entretien", "<p>Nettoyez régulièrement les plis de sa face et gardez-les bien secs. Son poil ras demande peu d'entretien.</p>"),
   ("Sa santé : points d'attention", "<p>Comme les autres races à museau court (dites brachycéphales), il peut avoir des difficultés à respirer et <strong>supporte mal la chaleur</strong> : évitez les efforts quand il fait chaud, gardez-le au frais et consultez si sa respiration est bruyante ou difficile. Préférez un harnais au collier. Avant d'adopter, renseignez-vous auprès de votre vétérinaire et choisissez un éleveur attentif à la santé respiratoire.</p>"),
  ],
  "produits": HARNAIS + KONG + boite("🧊", "Tapis rafraîchissant", "Pour l'aider à rester au frais les jours de chaleur.", "tapis-rafraichissant", "tapis rafraîchissant chien"),
  "pour": ("Vous vivez en appartement et cherchez un compagnon câlin, présent au quotidien.", "Vous voulez un chien sportif ou vous vivez dans une région très chaude sans clim."),
  "liens": '<a href="chien-aboie-seul.html">chien qui aboie seul</a> · <a href="meilleur-harnais-chien.html">quel harnais choisir</a> · <a href="chien.html">le guide du chien</a>'},
 {"slug": "race-golden-retriever", "icone": "🐕‍🦺", "nom": "Golden retriever",
  "titre": "Golden retriever : caractère, éducation et besoins",
  "desc": "Golden retriever : caractère doux, éducation, besoins d'exercice, entretien du poil et santé. Notre fiche complète avant d'adopter.",
  "bref": "Un chien <strong>doux, patient et très sociable</strong>, souvent excellent avec les enfants. Il a besoin d'activité, de présence et d'un brossage régulier de sa belle fourrure.",
  "sections": [
   ("Son caractère", "<p>Le golden est connu pour sa douceur et son envie de faire plaisir. Il aime la compagnie et s'entend généralement bien avec les autres animaux. Jeune, il reste longtemps joueur et peut être très enthousiaste.</p>"),
   ("Ses besoins", "<p>Des balades quotidiennes, des jeux de rapport, de la nage s'il aime l'eau, et des activités pour sa tête. Il n'aime pas être seul toute la journée.</p>"),
   ("L'éducation", "<p>Très réceptif aux récompenses, il apprend vite. Travaillez les bases (<a href=\"apprendre-assis-couche-pas-bouger.html\">assis, couché, pas bouger</a>), le rappel et le calme lors des retrouvailles pour éviter qu'il saute sur les gens.</p>"),
   ("L'entretien", "<p>Son poil long demande un brossage plusieurs fois par semaine pour éviter les nœuds, surtout derrière les oreilles et sur les pattes. Contrôlez régulièrement ses oreilles.</p>"),
   ("Sa santé : points d'attention", "<p>Demandez à l'éleveur les dépistages des parents (hanches, coudes, yeux). Surveillez son poids et faites-le suivre régulièrement par votre vétérinaire.</p>"),
  ],
  "produits": HARNAIS + boite("🪮", "Brosse pour poil long", "Pour démêler sa fourrure et limiter les nœuds.", "brosse-poil-long", "brosse chien poil long démêlante") + FOUILLE,
  "pour": ("Vous cherchez un chien de famille doux et vous aimez les longues balades.", "Vous êtes souvent absent ou les poils vous dérangent."),
  "liens": '<a href="apprendre-assis-couche-pas-bouger.html">assis, couché, pas bouger</a> · <a href="rappel-chien.html">le rappel</a> · <a href="chien.html">le guide du chien</a>'},
 {"slug": "race-jack-russell", "icone": "🐕", "nom": "Jack Russell terrier",
  "titre": "Jack Russell : caractère, éducation et besoins",
  "desc": "Jack Russell terrier : caractère vif, besoins d'activité, éducation, instinct de chasse et entretien. Est-ce le bon petit chien pour vous ?",
  "bref": "Un petit chien <strong>plein d'énergie, malin et intrépide</strong>. Sous sa petite taille se cache un vrai terrier, qui a besoin de beaucoup d'activité et d'une éducation patiente.",
  "sections": [
   ("Son caractère", "<p>Le jack russell est vif, curieux, joueur et très courageux. C'est un terrier : il a un fort instinct de chasse, aime creuser et peut se montrer têtu ou bruyant s'il s'ennuie.</p>"),
   ("Ses besoins", "<p>Beaucoup plus que sa taille ne le laisse penser : des balades actives, des jeux de flair, des jouets à déchiqueter (sous surveillance) et des séances d'éducation. Un jardin ne suffit pas à le dépenser.</p>"),
   ("L'éducation", "<p>Le <a href=\"rappel-chien.html\">rappel</a> est la priorité, car il peut partir à la poursuite d'un animal : travaillez-le avec une longe et de très bonnes récompenses. Canalisez son énergie avec des jeux structurés et apprenez-lui le calme. Les méthodes dures le rendent plus réactif : misez sur la récompense.</p>"),
   ("L'entretien", "<p>Selon son poil (lisse ou dur), un brossage régulier suffit. Vérifiez ses coussinets et ses oreilles après les balades.</p>"),
   ("Sa santé : points d'attention", "<p>C'est généralement un chien robuste. Demandez à l'éleveur les dépistages réalisés sur les parents et faites-le suivre régulièrement par votre vétérinaire.</p>"),
  ],
  "produits": LONGE + KONG + FOUILLE,
  "pour": ("Vous êtes actif, patient et vous aimez les chiens qui ont du caractère.", "Vous cherchez un petit chien calme et tranquille, ou vous avez des rongeurs à la maison."),
  "liens": '<a href="rappel-chien.html">le rappel</a> · <a href="meilleurs-jouets-occupation-chien.html">les jouets d\'occupation</a> · <a href="chien.html">le guide du chien</a>'},
 {"slug": "race-maine-coon", "icone": "🐈", "nom": "Maine coon",
  "titre": "Maine coon : caractère, besoins et entretien",
  "desc": "Maine coon : caractère sociable, besoins, jeux, entretien du poil et points de santé. Tout savoir sur ce grand chat avant de l'adopter.",
  "bref": "Un grand chat <strong>doux, sociable et joueur</strong>, souvent surnommé « chat-chien » tant il aime suivre ses humains. Il lui faut de l'espace, des jeux et un brossage régulier.",
  "sections": [
   ("Son caractère", "<p>Le maine coon est réputé pour sa gentillesse et sa sociabilité. Il est souvent curieux, aime participer à la vie de la maison et peut apprendre des tours au <a href=\"meilleur-clicker.html\">clicker</a>.</p>"),
   ("Ses besoins", "<p>Des séances de jeu de chasse chaque jour, un <strong>arbre à chat solide et grand</strong> adapté à son gabarit, des griffoirs stables et une grande litière. Beaucoup apprécient aussi les promenades en harnais, à condition de les y habituer très progressivement.</p>"),
   ("L'éducation", "<p>Comme tous les chats, il apprend avec des récompenses et des séances très courtes. Proposez-lui des griffoirs avant qu'il ne choisisse le canapé (<a href=\"chat-griffe-canape.html\">voir notre article</a>) et habituez-le tôt à la caisse de transport et aux soins.</p>"),
   ("L'entretien", "<p>Son poil mi-long demande un brossage régulier, plus fréquent pendant la mue, pour éviter les nœuds et les boules de poils. Prévoyez une litière assez grande pour lui (<a href=\"meilleure-litiere-chat.html\">quelle litière choisir</a>).</p>"),
   ("Sa santé : points d'attention", "<p>Une maladie du cœur (la cardiomyopathie hypertrophique) est connue dans la race : un test génétique existe pour une des mutations en cause, et votre vétérinaire peut vous conseiller un suivi. Demandez aussi à l'éleveur les dépistages réalisés sur les parents, notamment pour les hanches.</p>"),
  ],
  "produits": boite("🌳", "Grand arbre à chat stable", "Choisissez un modèle lourd et large, adapté à un grand chat.", "arbre-chat", "arbre à chat grand chat stable") +
              boite("🪶", "Canne à plumes", "Pour ses séances de chasse quotidiennes.", "canne-plumes", "canne à pêche plumes jouet chat") +
              boite("🪮", "Brosse pour chat à poil mi-long", "Pour un brossage régulier sans tirer sur les nœuds.", "brosse-chat", "brosse chat poil long"),
  "pour": ("Vous avez de la place et vous rêvez d'un chat câlin, présent et joueur.", "Vous avez peu d'espace ou peu de temps pour le brossage et le jeu."),
  "liens": '<a href="chat-griffe-canape.html">chat qui griffe le canapé</a> · <a href="meilleure-litiere-chat.html">quelle litière choisir</a> · <a href="chat.html">le guide du chat</a>'},
]


def fiche(r):
    sections = "".join(f"        <h2>{t}</h2>\n        {c}\n" for t, c in r["sections"])
    oui, non = r["pour"]
    return f"""    <section class="page-hero">
      <div class="container article">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › <a href="races.html">Races</a> › {r["nom"]}</p>
        <h1>{r["icone"]} {r["titre"]}</h1>
        <p class="meta">{r["icone"]} Fiche race · Lecture 4 min</p>
        <div class="callout"><strong>En bref :</strong> {r["bref"]}</div>
{sections}        <h2>Est-ce la race pour vous ?</h2>
        <ul><li>✅ <strong>Oui si</strong> : {oui}</li><li>❌ <strong>Plutôt non si</strong> : {non}</li></ul>
        <p>Chaque animal est unique : le caractère dépend aussi de son histoire, de sa socialisation et de son éducation. Pensez à l'adoption en refuge ou en association de race, et passez du temps avec des chiens ou des chats de la race avant de vous décider.</p>
        <h2>Le matériel utile</h2>
{r["produits"]}        <div class="callout warn"><strong>Santé :</strong> cette fiche donne des repères généraux. Pour toute question sur la santé de votre animal, son alimentation ou les dépistages, demandez conseil à votre vétérinaire.</div>
        <p>Pour aller plus loin : {r["liens"]} · <a href="races.html">toutes nos fiches races</a> · <a href="quel-animal.html">quel animal pour moi ?</a></p>
      </div>
    </section>"""


def hub():
    cartes = "".join(f'          <a class="card card-link" href="{r["slug"]}.html"><span class="icon">{r["icone"]}</span><h3>{r["nom"]}</h3><p>{e(re.sub(r"<[^>]+>", "", r["bref"]).split(". ")[0].rstrip(".") + ".")}</p></a>\n' for r in RACES)
    return f"""    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">Accueil</a> › Races</p>
        <h1>🐾 Fiches races de chiens et de chats</h1>
        <p class="lead">Caractère, besoins, éducation, entretien et points de santé : nos fiches pour mieux comprendre la race de votre compagnon, ou choisir celle qui vous correspond.</p>
        <div class="grid grid-3">
{cartes}        </div>
        <h2>Bien choisir, au-delà de la race</h2>
        <p>La race donne des tendances, pas une garantie : l'histoire, la socialisation et l'éducation de chaque animal comptent tout autant. Avant de vous décider, faites notre quiz <a href="quel-animal.html">quel animal est fait pour moi ?</a>, calculez votre <a href="budget-animal.html">budget</a> et pensez à l'adoption en refuge.</p>
      </div>
    </section>"""


if __name__ == "__main__":
    for r in RACES:
        creer_page.creer("fr", r["slug"], r["titre"], r["desc"], fiche(r))
    creer_page.creer("fr", "races", "Fiches races de chiens et de chats",
                     "Berger australien, labrador, bouledogue français, golden, jack russell, maine coon : caractère, besoins, éducation et santé de chaque race.",
                     hub(), menu="🐾 Fiches races")
    creer_page.finir()
    print(len(RACES), "fiches races")
