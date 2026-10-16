"""Insère les illustrations (docs/img/illu/*.svg) dans les pages, avec alt et légende traduits.
Idempotent : chaque figure porte data-illu, on ne l'ajoute pas deux fois.
Usage : python3 tools/illustrations/integrer.py"""
import pathlib, re, html
DOCS = pathlib.Path(__file__).resolve().parent.parent.parent / "docs"
def taille(nom):
    s = (DOCS / "img/illu" / f"{nom}.svg").read_text()
    w, h = re.search(r'viewBox="0 0 (\d+) (\d+)"', s).groups(); return w, h
L = {
 "laisse": {"fr": ("Laisse tendue : le maître s'arrête. Laisse souple : le chien avance à côté de lui.", "À gauche, la laisse est tendue : on s'arrête. À droite, la laisse est souple : on avance et on récompense."),
            "en": ("Tight lead: the owner stops. Loose lead: the dog walks beside them.", "Left: the lead is tight, so you stop. Right: the lead is loose, so you walk on and reward."),
            "it": ("Guinzaglio teso: ci si ferma. Guinzaglio lento: il cane cammina al fianco.", "A sinistra il guinzaglio è teso: ci si ferma. A destra è lento: si avanza e si premia.")},
 "harnais": {"fr": ("Chien avec un harnais en Y comparé à un chien qui tire sur son collier", "Le harnais en Y laisse la gorge libre ; un collier sur lequel le chien tire comprime le cou."),
             "en": ("Dog in a Y-shaped harness compared with a dog pulling on its collar", "A Y-shaped harness leaves the throat free; a collar the dog pulls against presses on the neck."),
             "it": ("Cane con pettorina a Y a confronto con un cane che tira sul collare", "La pettorina a Y lascia libera la gola; un collare su cui il cane tira comprime il collo.")},
 "rappel": {"fr": ("Chien qui accourt vers son maître, une longe derrière lui", "Avec une longe, le chien profite de sa liberté et apprend que revenir vers vous est toujours une fête."),
            "en": ("Dog running back to its owner, trailing a long line", "With a long line, your dog enjoys its freedom and learns that coming back to you is always a party."),
            "it": ("Cane che corre verso il padrone con una lunghina", "Con la lunghina il cane si gode la libertà e impara che tornare da te è sempre una festa.")},
 "griffoir": {"fr": ("Chat qui griffe un canapé, puis un grand griffoir en sisal", "Plutôt que le canapé, proposez un griffoir haut et stable : le chat peut s'y étirer de tout son long."),
              "en": ("Cat scratching a sofa, then a tall sisal scratching post", "Instead of the sofa, offer a tall, stable post: the cat can stretch out fully on it."),
              "it": ("Gatto che graffia un divano, poi un tiragraffi alto in sisal", "Invece del divano, offri un tiragraffi alto e stabile: il gatto può allungarsi del tutto.")},
 "chiot-jouet": {"fr": ("Chiot qui mordille une main, puis qui mâche un os-jouet", "Les mains ne sont pas des jouets : proposez toujours un jouet à mâcher à la place."),
                 "en": ("Puppy nipping a hand, then chewing a toy bone", "Hands aren't toys: always offer a chew toy instead."),
                 "it": ("Cucciolo che mordicchia una mano, poi mastica un osso giocattolo", "Le mani non sono giochi: offri sempre un gioco da masticare.")},
 "proprete-moments": {"fr": ("Réveil, repas, jeu, coucher, puis sortie dehors et récompense", "Au réveil, après le repas, après le jeu et avant de dormir : direction dehors… puis récompense !"),
                      "en": ("Waking, meal, play, bedtime, then going outside and a reward", "On waking, after meals, after play and before bed: outside you go… then a reward!"),
                      "it": ("Risveglio, pasto, gioco, nanna, poi fuori e premio", "Al risveglio, dopo il pasto, dopo il gioco e prima di dormire: fuori… e poi premio!")},
 "chat-clicker": {"fr": ("Chat qui regarde une baguette de ciblage tenue par une main avec un clicker", "Le clic marque l'instant précis où l'animal touche la cible ; la friandise suit."),
                  "en": ("Cat looking at a target stick held by a hand with a clicker", "The click marks the exact moment the pet touches the target; the treat follows."),
                  "it": ("Gatto che guarda un bastoncino target tenuto da una mano con il clicker", "Il clic segna l'istante preciso in cui l'animale tocca il bersaglio; poi arriva il premio.")},
 "assis-couche-pasbouger": {"fr": ("Chien assis, couché, puis qui reste en place", "1. Assis : friandise au-dessus de la tête · 2. Couché : friandise vers le sol · 3. Pas bouger : main levée, un pas en arrière."),
                            "en": ("Dog sitting, lying down, then staying", "1. Sit: treat above the head · 2. Down: treat towards the floor · 3. Stay: hand raised, one step back."),
                            "it": ("Cane seduto, a terra, poi che resta fermo", "1. Seduto: premio sopra la testa · 2. Terra: premio verso il pavimento · 3. Resta: mano alzata, un passo indietro.")},
 "assis-leurre": {"fr": ("Le leurre : la friandise guide la tête vers le haut et le chien s'assoit", "La friandise guide la tête vers le haut, les fesses descendent… et voilà l'assis !"),
                  "en": ("Luring: the treat guides the head up and the dog sits", "The treat guides the head up, the bottom goes down… and there's the sit!"),
                  "it": ("L'adescamento: il premio guida la testa in alto e il cane si siede", "Il premio guida la testa verso l'alto, il sedere scende… ed ecco il seduto!")},
 "lapin": {"fr": ("Lapin dans un bac à litière garni de foin, puis lapin à qui l'on tend une feuille", "Du foin dans le bac aide le lapin à devenir propre ; une feuille tendue avec douceur l'aide à prendre confiance."),
           "en": ("Rabbit in a litter tray filled with hay, then a rabbit being offered a leaf", "Hay in the tray helps rabbits learn to use it; a gently offered leaf helps them build trust."),
           "it": ("Coniglio in una lettiera con il fieno, poi coniglio a cui si offre una foglia", "Il fieno nella lettiera aiuta il coniglio a diventare pulito; una foglia offerta con calma lo aiuta a fidarsi.")},
 "rat-furet": {"fr": ("Rat qui touche une cible avec son nez, et furet qui joue avec une balle", "Le rat apprend vite à toucher une cible ; le furet se défoule sur un jouet plutôt que sur vos mains."),
               "en": ("Rat touching a target with its nose, and a ferret playing with a ball", "Rats quickly learn to touch a target; ferrets let off steam on a toy rather than your hands."),
               "it": ("Ratto che tocca un bersaglio con il naso e furetto che gioca con una palla", "Il ratto impara in fretta a toccare un bersaglio; il furetto si sfoga su un gioco invece che sulle tue mani.")},
 "oiseau-main": {"fr": ("Perroquet qui passe de son perchoir à la main", "Main posée juste au-dessus des pattes, sous le ventre : l'oiseau apprend à monter tout seul."),
                 "en": ("Parrot stepping from its perch onto a hand", "Hand held just above the feet, under the belly: the bird learns to step up on its own."),
                 "it": ("Pappagallo che passa dal trespolo alla mano", "Mano appena sopra le zampe, sotto la pancia: l'uccello impara a salire da solo.")},
 "quiz": {"fr": ("Un chien et un chat entourés de points d'interrogation", "Répondez à 4 questions : on vous indique la bonne méthode."),
          "en": ("A dog and a cat surrounded by question marks", "Answer 4 questions and we'll point you to the right method."),
          "it": ("Un cane e un gatto circondati da punti interrogativi", "Rispondi a 4 domande: ti indichiamo il metodo giusto.")},
 "age": {"fr": ("Un chiot, un chien adulte, puis un chien âgé à lunettes, et un gâteau d'anniversaire", "Chiot, adulte, senior : chaque âge a ses besoins."),
         "en": ("A puppy, an adult dog, then an older dog in glasses, and a birthday cake", "Puppy, adult, senior: every age has its own needs."),
         "it": ("Un cucciolo, un cane adulto, poi un cane anziano con gli occhiali e una torta di compleanno", "Cucciolo, adulto, senior: ogni età ha i suoi bisogni.")},
}
# (page, langue, repère exact, illustration) : la figure est insérée juste après le repère
PLACES = [
 ("marche-en-laisse.html", "fr", "<h2>La règle d'or : laisse tendue = on s'arrête</h2>", "laisse"),
 ("en/marche-en-laisse.html", "en", "<h2>The golden rule: tight lead = we stop</h2>", "laisse"),
 ("it/marche-en-laisse.html", "it", "<h2>La regola d'oro: guinzaglio teso = ci si ferma</h2>", "laisse"),
 ("marche-en-laisse.html", "fr", "<h2>Le bon équipement</h2>", "harnais"),
 ("en/marche-en-laisse.html", "en", "<h2>The right equipment</h2>", "harnais"),
 ("it/marche-en-laisse.html", "it", "<h2>L'attrezzatura giusta</h2>", "harnais"),
 ("meilleur-harnais-chien.html", "fr", "<h2>Pourquoi un harnais plutôt qu'un collier ?</h2>", "harnais"),
 ("rappel-chien.html", "fr", "<h2>Étape 4 : passer dehors… avec une longe</h2>", "rappel"),
 ("en/rappel-chien.html", "en", "<h2>Step 4: go outside… with a long line</h2>", "rappel"),
 ("it/rappel-chien.html", "it", "<h2>Tappa 4: all'aperto… con la lunghina</h2>", "rappel"),
 ("chat-griffe-canape.html", "fr", "<h2>1. Un griffoir plus attirant que le canapé</h2>", "griffoir"),
 ("en/chat-griffe-canape.html", "en", "<h2>1. A scratching post more attractive than the sofa</h2>", "griffoir"),
 ("it/chat-griffe-canape.html", "it", "<h2>1. Un tiragraffi più attraente del divano</h2>", "griffoir"),
 ("meilleur-griffoir-chat.html", "fr", "<h2>Les 4 critères qui comptent vraiment</h2>", "griffoir"),
 ("chiot-mord.html", "fr", "<h2>2. Toujours proposer une alternative</h2>", "chiot-jouet"),
 ("en/chiot-mord.html", "en", "<h2>2. Always offer an alternative</h2>", "chiot-jouet"),
 ("it/chiot-mord.html", "it", "<h2>2. Proporre sempre un'alternativa</h2>", "chiot-jouet"),
 ("proprete-chiot.html", "fr", "<h2>1. Sortir aux bons moments</h2>", "proprete-moments"),
 ("en/proprete-chiot.html", "en", "<h2>1. Go out at the right times</h2>", "proprete-moments"),
 ("it/proprete-chiot.html", "it", "<h2>1. Uscire nei momenti giusti</h2>", "proprete-moments"),
 ("meilleur-clicker.html", "fr", "<h2>Rappel : à quoi sert un clicker ?</h2>", "chat-clicker"),
 ("chien.html", "fr", "<h2>🪑 Assis, couché, pas bouger</h2>", "assis-couche-pasbouger"),
 ("en/chien.html", "en", "<h2>🪑 Sit, down, stay</h2>", "assis-couche-pasbouger"),
 ("it/chien.html", "it", "<h2>🪑 Seduto, terra, resta</h2>", "assis-couche-pasbouger"),
 ("chien.html", "fr", "<h2>🦮 La marche en laisse</h2>", "laisse"),
 ("en/chien.html", "en", "<h2>🦮 Loose-lead walking</h2>", "laisse"),
 ("it/chien.html", "it", "<h2>🦮 Camminare al guinzaglio</h2>", "laisse"),
 ("chat.html", "fr", "<h2>💅 Les griffades</h2>", "griffoir"),
 ("en/chat.html", "en", "<h2>💅 Scratching</h2>", "griffoir"),
 ("it/chat.html", "it", "<h2>💅 I graffi</h2>", "griffoir"),
 ("chat.html", "fr", "<h2>🔘 Le clicker avec un chat</h2>", "chat-clicker"),
 ("en/chat.html", "en", "<h2>🔘 Clicker training a cat</h2>", "chat-clicker"),
 ("it/chat.html", "it", "<h2>🔘 Il clicker con il gatto</h2>", "chat-clicker"),
 ("methodes.html", "fr", "<h3>🍖 Le leurre (luring)</h3>", "assis-leurre"),
 ("en/methodes.html", "en", "<h3>🍖 Luring</h3>", "assis-leurre"),
 ("it/methodes.html", "it", "<h3>🍖 L'adescamento (luring)</h3>", "assis-leurre"),
 ("methodes.html", "fr", "<h3>🎯 Le ciblage (targeting)</h3>", "chat-clicker"),
 ("en/methodes.html", "en", "<h3>🎯 Targeting</h3>", "chat-clicker"),
 ("it/methodes.html", "it", "<h3>🎯 Il targeting</h3>", "chat-clicker"),
 ("nac.html", "fr", "<h2>🐇 Le lapin</h2>", "lapin"),
 ("en/nac.html", "en", "<h2>🐇 Rabbits</h2>", "lapin"),
 ("it/nac.html", "it", "<h2>🐇 Il coniglio</h2>", "lapin"),
 ("nac.html", "fr", "<h2 style=\"margin-top:48px\">🐀 Rats, souris et furets</h2>", "rat-furet"),
 ("en/nac.html", "en", "<h2 style=\"margin-top:48px\">🐀 Rats, mice and ferrets</h2>", "rat-furet"),
 ("it/nac.html", "it", "<h2 style=\"margin-top:48px\">🐀 Ratti, topi e furetti</h2>", "rat-furet"),
 ("nac.html", "fr", "<h2>🦜 Les oiseaux</h2>", "oiseau-main"),
 ("en/nac.html", "en", "<h2>🦜 Birds</h2>", "oiseau-main"),
 ("it/nac.html", "it", "<h2>🦜 Gli uccelli</h2>", "oiseau-main"),
 ("quiz.html", "fr", "recevez les méthodes, les articles et le matériel adaptés à votre situation.</p>", "quiz"),
 ("en/quiz.html", "en", "get the methods, articles and gear that fit your situation.</p>", "quiz"),
 ("it/quiz.html", "it", "ricevi i metodi, gli articoli e gli accessori adatti alla tua situazione.</p>", "quiz"),
 ("age-humain.html", "fr", "vous donnons les conseils adaptés à son étape de vie.</p>", "age"),
 ("en/age-humain.html", "en", "give you tips suited to its life stage.</p>", "age"),
 ("it/age-humain.html", "it", "ti diamo i consigli adatti alla sua fase di vita.</p>", "age"),
 ("en/meilleur-harnais-chien.html", "en", "<h2>Why a harness rather than a collar?</h2>", "harnais"),
 ("it/meilleur-harnais-chien.html", "it", "<h2>Perché una pettorina e non un collare?</h2>", "harnais"),
 ("en/meilleur-griffoir-chat.html", "en", "<h2>The 4 criteria that really matter</h2>", "griffoir"),
 ("it/meilleur-griffoir-chat.html", "it", "<h2>I 4 criteri che contano davvero</h2>", "griffoir"),
 ("en/meilleur-clicker.html", "en", "<h2>Reminder: what is a clicker for?</h2>", "chat-clicker"),
 ("it/meilleur-clicker.html", "it", "<h2>Promemoria: a cosa serve un clicker?</h2>", "chat-clicker"),
]
HERO = {"fr": "Un chien et un chat assis côte à côte", "en": "A dog and a cat sitting side by side", "it": "Un cane e un gatto seduti fianco a fianco"}
n = 0
for page, lang, repere, nom in PLACES:
    p = DOCS / page; s = p.read_text(encoding="utf-8")
    if f'data-illu="{nom}"' in s: continue
    assert repere in s, (page, repere)
    pre = "../" if "/" in page else ""; w, h = taille(nom); alt, leg = L[nom][lang]
    fig = (f'\n            <figure class="illu" data-illu="{nom}"><img src="{pre}img/illu/{nom}.svg" alt="{html.escape(alt, quote=True)}" '
           f'width="{w}" height="{h}" loading="lazy" decoding="async"><figcaption>{html.escape(leg)}</figcaption></figure>')
    s = s.replace(repere, repere + fig, 1); p.write_text(s, encoding="utf-8"); n += 1
for lang, page in (("fr", "index.html"), ("en", "en/index.html"), ("it", "it/index.html")):
    p = DOCS / page; s = p.read_text(encoding="utf-8"); pre = "../" if "/" in page else ""
    old = '<div class="hero-emoji" aria-hidden="true">🐕🐈<br>🐇🦜</div>'
    if old in s:
        s = s.replace(old, f'<div class="hero-illu"><img src="{pre}img/illu/accueil.svg" alt="{HERO[lang]}" width="600" height="480" fetchpriority="high"></div>')
        p.write_text(s, encoding="utf-8"); n += 1
# Images en tête des cartes (accueil, page Conseils) : remplacent l'emoji de la carte
CARTES = {"chien.html": "portrait-chien", "chat.html": "portrait-chat", "nac.html#lapin": "portrait-lapin", "nac.html#oiseau": "portrait-oiseau",
          "quiz.html": "quiz", "age-humain.html": "age", "meilleur-harnais-chien.html": "harnais", "meilleur-griffoir-chat.html": "griffoir",
          "meilleur-clicker.html": "chat-clicker", "proprete-chiot.html": "proprete-moments", "rappel-chien.html": "rappel",
          "marche-en-laisse.html": "laisse", "chat-griffe-canape.html": "griffoir", "chiot-mord.html": "chiot-jouet",
          "kit-accueil-chiot.html": "chiot-jouet", "idees-cadeaux-noel-chien-chat.html": "accueil", "black-friday-animaux.html": "harnais"}
CARTE = re.compile(r'(<a class="card card-link" href="([^"]+)">\s*)<span class="icon">([^<]*)</span>')
for d in ("", "en/", "it/"):
    for page in ("index.html", "conseils.html"):
        p = DOCS / d / page; s = p.read_text(encoding="utf-8"); pre = "../" if d else ""
        def rempl(m):
            nom = CARTES.get(m.group(2))
            if not nom: return m.group(0)
            w, h = taille(nom)
            return (f'{m.group(1)}<span class="icon"><img class="card-img" src="{pre}img/illu/{nom}.svg" alt="" '
                    f'width="{w}" height="{h}" loading="lazy" decoding="async"></span>')
        s2, k = CARTE.subn(rempl, s)
        if s2 != s: p.write_text(s2, encoding="utf-8"); n += sum(1 for m in CARTE.finditer(s) if m.group(2) in CARTES)
print(n, "illustrations insérées")
