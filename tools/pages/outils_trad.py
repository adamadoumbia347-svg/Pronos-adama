"""Versions anglaise et italienne des outils : programme chiot 30 jours, budget, quiz « Quel animal pour moi ? ».

Usage : python3 tools/pages/outils_trad.py
Reprend la structure de tools/pages/outils_fr.py (liens des jours, postes du budget, points du quiz)
avec les textes traduits, dans le même ordre.
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402
import outils_fr as FR  # noqa: E402

e = html.escape
# Pages qui n'existent qu'en français : pas de lien dans les autres langues
SEULEMENT_FR = {"noms-chien-chat.html"}

JOURS = {
"en": [
 ("Teach them their name", "Say their name in a happy voice; as soon as they look at you, a treat. 5 times, 3 times a day."),
 ("Their resting spot", "Set up their bed somewhere quiet. Drop a treat or a chew there when they lie down on their own."),
 ("The toilet routine", "Take them out when they wake up, after every meal, after play and every 1 to 2 hours. Praise them outside, at that very moment."),
 ("Gentle handling", "Touch a paw, an ear, look at their teeth for one second, then a treat. Stop if they tense up."),
 ("Alone for a few seconds", "Leave the room for 10 seconds and come back calmly, before they cry. Build up very gradually."),
 ("Chewing the right things", "Give them a suitable chew toy; if they nibble your hands, swap them for the toy."),
 ("Review break", "A day with nothing new: calm games, cuddles, sleep. Puppies sleep a lot, that's normal."),
 ("Sit", "Hold a treat above their head: as soon as their bottom touches the floor, \"yes!\" and a treat."),
 ("Look at me", "Reward every time they look you in the eyes on their own. It's the foundation of attention."),
 ("Hand target", "Hold your open hand near their nose: when they touch it with their nose, a treat."),
 ("Down", "From the sit, lower the treat between their paws, then forward along the floor."),
 ("The harness", "Show the harness, treat. Put it on for one second, treat. Then fasten it for a few seconds, at home."),
 ("The clicker (optional)", "Click then give a treat, 10 times: they learn that the click means a reward is coming."),
 ("Review break", "Practise their name, sit and the hand target in 3 one-minute mini-sessions."),
 ("Discovering sounds", "Play everyday sounds at low volume (vacuum, doorbell) while you play with them. Stop if they're scared."),
 ("Meeting people", "Let them watch calm people from a distance and reward them. No forced contact. Before vaccinations are complete, ask your vet for advice."),
 ("First steps on the lead", "At home or in the garden: every time the lead is loose and they're near you, a treat."),
 ("Recall at home", "Call them in a happy voice from 2 metres, celebrate and treat when they arrive. Never call them for something unpleasant."),
 ("Sniffing game", "Hide a few pieces of kibble in a snuffle mat or under cups: they search with their nose."),
 ("The car", "Settle them in the car with the engine off, with a treat, for a few minutes. Then a very short trip."),
 ("Review break", "A quiet walk where they sniff at their own pace: it's very tiring mentally."),
 ("Stay", "Sitting, count 1 second, reward, then release them with a word (\"okay\"). Build up very slowly."),
 ("Leave it", "A treat in your closed fist: as soon as they stop trying to get it, a treat from the other hand."),
 ("The calm mat", "Reward every time they lie down on a mat. Little by little, the mat becomes their place to settle."),
 ("Brushing and grooming", "One stroke of the brush, one treat. Very short, very pleasant, so they enjoy it."),
 ("Recall outdoors", "In a safe place, with a long line: call them, reward generously, then let them go back to playing."),
 ("A \"happy\" vet visit", "If your vet agrees, drop in to say hello: treats and cuddles, no treatment."),
 ("Alone a little longer", "With a stuffed chew toy, leave for a few minutes and come back calmly. They should stay relaxed."),
 ("Revision on walks", "Sit, look at me and recall, once each on a walk, with a great reward."),
 ("Well done!", "30 days of foundations. Keep going a few minutes a day: training lasts a lifetime, in a good mood."),
],
"it": [
 ("Insegnargli il suo nome", "Di' il suo nome con voce allegra; appena ti guarda, un bocconcino. 5 volte, 3 volte al giorno."),
 ("La sua cuccia", "Sistema la cuccia in un posto tranquillo. Lasciaci un bocconcino o un gioco da masticare quando ci si sdraia da solo."),
 ("La routine dei bisogni", "Portalo fuori al risveglio, dopo ogni pasto, dopo il gioco e ogni 1-2 ore. Lodalo fuori, proprio in quel momento."),
 ("Manipolazioni delicate", "Tocca una zampa, un orecchio, guardagli i denti per un secondo, poi un bocconcino. Fermati se si irrigidisce."),
 ("Solo per qualche secondo", "Esci dalla stanza per 10 secondi e torna con calma, prima che pianga. Allunga i tempi molto gradualmente."),
 ("Masticare le cose giuste", "Dagli un gioco da masticare adatto; se mordicchia le mani, sostituiscile con il gioco."),
 ("Pausa e ripasso", "Una giornata senza novità: giochi tranquilli, coccole, sonno. Un cucciolo dorme tanto, è normale."),
 ("Seduto", "Con un bocconcino sopra la sua testa: appena il sedere tocca terra, «sì!» e bocconcino."),
 ("Guardami", "Premialo ogni volta che ti guarda negli occhi di sua iniziativa. È la base dell'attenzione."),
 ("Il tocco della mano", "Avvicina la mano aperta al suo naso: quando la tocca con il naso, bocconcino."),
 ("Terra", "Dal seduto, abbassa il bocconcino tra le zampe, poi in avanti rasoterra."),
 ("La pettorina", "Mostra la pettorina, bocconcino. Appoggiala un secondo, bocconcino. Poi chiudila per qualche secondo, in casa."),
 ("Il clicker (facoltativo)", "Fai clic e poi dai un bocconcino, 10 volte: impara che il clic annuncia un premio."),
 ("Pausa e ripasso", "Ripassa il nome, il seduto e il tocco della mano in 3 mini-sessioni da un minuto."),
 ("Scoprire i rumori", "Fagli ascoltare a basso volume rumori di casa (aspirapolvere, campanello) mentre giochi con lui. Fermati se ha paura."),
 ("Incontrare le persone", "Lascialo osservare da lontano persone tranquille e premialo. Nessun contatto forzato. Prima della fine dei vaccini, chiedi consiglio al veterinario."),
 ("Primi passi al guinzaglio", "In casa o in giardino: ogni volta che il guinzaglio è morbido ed è vicino a te, bocconcino."),
 ("Il richiamo in casa", "Chiamalo con voce allegra a 2 metri, festa e bocconcino quando arriva. Mai chiamarlo per qualcosa di sgradevole."),
 ("Gioco olfattivo", "Nascondi qualche crocchetta in un tappeto olfattivo o sotto dei bicchieri: cerca con il naso."),
 ("L'auto", "Sistemalo in auto a motore spento, con un bocconcino, per qualche minuto. Poi un tragitto brevissimo."),
 ("Pausa e ripasso", "Una passeggiata tranquilla in cui annusa al suo ritmo: stanca molto mentalmente."),
 ("Resta", "Seduto, conta 1 secondo, premia, poi liberalo con una parola («ok»). Aumenta molto piano."),
 ("Lascia", "Un bocconcino nel pugno chiuso: appena smette di cercare di prenderlo, bocconcino dall'altra mano."),
 ("Il tappetino della calma", "Premialo ogni volta che si sdraia su un tappetino. A poco a poco diventa il suo posto per rilassarsi."),
 ("Spazzola e toelettatura", "Una passata di spazzola, un bocconcino. Brevissimo e piacevole, perché ami quel momento."),
 ("Il richiamo all'aperto", "In un posto sicuro, con una lunghina: chiamalo, premialo generosamente, poi lascialo tornare a giocare."),
 ("Visita dal veterinario «per niente»", "Se il veterinario è d'accordo, passate a salutare: bocconcini e coccole, nessuna cura."),
 ("Solo un po' più a lungo", "Con un gioco da riempire, esci per qualche minuto e torna con calma. Deve restare sereno."),
 ("Ripasso in passeggiata", "Seduto, guardami e richiamo, una volta ciascuno in passeggiata, con un super premio."),
 ("Bravo!", "30 giorni di basi. Continua qualche minuto al giorno: l'educazione dura tutta la vita, con il sorriso."),
]}

T = {
"en": {
 "home": "Home", "jour": "Day", "plus": "Read more",
 "prog_fil": "Puppy programme", "prog_titre": "30 days with my puppy: the day-by-day training plan", "prog_h1": "🐶 30 days with my puppy: the training programme",
 "prog_desc": "One exercise a day for 30 days to train your puppy gently: name, toilet training, sit, recall, lead. Progress saved, no sign-up.",
 "prog_lead": "One small exercise a day, 5 to 10 minutes, to lay the foundations gently: their name, toilet training, sit, recall, the lead… Tick each successful day: your progress is saved on this device, no sign-up.",
 "prog_zero": "0 / 30 days", "prog_note": "No pressure: if an exercise is hard, do it again the next day. Every puppy learns at their own pace.", "prog_raz": "Start again",
 "semaines": {1: "Week 1 · Settling in and trust", 2: "Week 2 · First basics", 3: "Week 3 · Discovering the world", 4: "Week 4 · Consolidating"},
 "prog_regles": "<strong>Programme rules:</strong> very short sessions, always with rewards, never punishment. Stop before they get bored. For outings and meetings before vaccinations are complete, follow your vet's advice.",
 "prog_liens": 'Read more: <a href="kit-accueil-chiot.html">what you need for a new puppy</a> · <a href="meilleures-friandises-education-chien.html">which treats to choose?</a> · <a href="chien.html">the complete dog guide</a>.',
 "menu_prog": "🐶 30-day puppy plan", "menu_budget": "💶 Pet budget calculator", "menu_quiz": "🤔 Which pet for me?",
 "b_fil": "Budget", "b_titre": "How much does a dog or cat cost? Work out your budget", "b_h1": "💶 How much does a dog or cat cost? Work out your budget",
 "b_desc": "Work out your dog's or cat's budget with your own figures: food, vet, insurance, pet care. Cost per month, per year and for the first year.",
 "b_lead": "Before adopting, or to take stock: enter your own amounts (vet quotes, the price of their food, insurance…) and get the cost per month, per year and for the first year.",
 "chien": "🐕 Dog", "chat": "🐈 Cat", "animal": "Pet",
 "groupes": ["Regular costs (per month)", "Yearly costs (per year)", "One-off costs (once)"],
 "postes": {"alim": "Food (kibble, wet food)", "friandises": "Treats and toys", "litiere": "Cat litter", "assurance": "Pet health insurance",
            "antiparasitaire": "Flea and worm treatment (if paid monthly)", "veto": "Vet: vaccinations and check-up", "toilettage": "Grooming",
            "garde": "Pet sitting or boarding during holidays", "education": "Training classes", "divers": "Unexpected and miscellaneous",
            "adoption": "Adoption or purchase", "identification": "Microchip, first vaccinations", "sterilisation": "Spaying or neutering",
            "materiel": "Starter kit (bed, bowls, lead or carrier…)"},
 "t_mois": "Per month:", "t_an": "Per year:", "t_premiere": "First year (including one-off costs):",
 "b_note": "The calculation only adds up your amounts. Your figures stay on your device.",
 "b_ou": "Where to find the right amounts?", "b_conseils": [
   "<strong>Food</strong>: check the recommended daily amount on the bag for your pet's weight, and how long a bag lasts.",
   "<strong>Vet</strong>: ask the price of a consultation, vaccinations and, if needed, spaying or neutering. Prices vary between clinics.",
   "<strong>Insurance</strong>: compare several quotes, looking at the limits and what is excluded.",
   "<strong>Pet care</strong>: boarding, pet sitter or family: plan it before the holidays.",
   "<strong>The unexpected</strong>: accidents and illness happen. Putting a little aside each month avoids nasty surprises."],
 "b_liens": 'To prepare for their arrival: <a href="kit-accueil-chiot.html">what you need for a puppy</a> · <a href="promos-animaux.html">current pet deals</a> · <a href="quel-animal.html">which pet is right for you?</a>',
 "q_fil": "Which pet for me?", "q_titre": "Which pet is right for me? The quiz before adopting", "q_h1": "🤔 Which pet is right for me?",
 "q_desc": "Dog, cat, rabbits, small rodents or bird: 6 questions about your home, your time and your wishes to find the right pet before adopting.",
 "q_lead": "Active dog, calm dog, cat, rabbits, small rodents or bird? 6 questions about your home, your time and your wishes to find the companion who suits you.",
 "q_noscript": "This quiz needs JavaScript.",
 "questions": [("Where do you live?", ["Flat", "House without a garden", "House with a garden"]),
               ("How much time can you give them each day?", ["Less than an hour", "1 to 2 hours", "More than 2 hours"]),
               ("Your days away from home?", ["Often more than 8 hours", "A few hours", "I'm often at home"]),
               ("How much do you want to walk and be active?", ["Sport, hiking, I love moving", "Quiet walks", "More of a homebody"]),
               ("Noise and mess?", ["No problem", "I prefer calm"]),
               ("What kind of relationship are you looking for?", ["A companion who follows me everywhere", "An independent companion", "Watching and interacting at their own moments"])],
 "resultats": [("🐕 An active dog", "You have time, energy and love to move: an active dog will be a great partner for walks and games. Plan time every day for training and outings."),
               ("🐕 A calm dog", "A dog with a calm temperament will suit you: they enjoy quiet walks and family life. Learn about the breed or adopt an adult whose character is known."),
               ("🐈 A cat", "A cat adapts well to your routine and your home. Provide scratching posts, play every day and high places so they're happy."),
               ("🐇 Rabbits", "Rabbits are sociable animals who live better in pairs and need space to run every day, not just a cage. They need time and regular care."),
               ("🐀 Small rodents", "Rats, guinea pigs or gerbils could suit you: often sociable with their own kind (adopt several, depending on the species), they need a large home and daily attention."),
               ("🦜 A bird", "A pet bird needs a lot of presence, interaction and stimulation. They can be noisy and live a long time: learn about the species before committing.")],
 "q_avant": "Before adopting, ask yourself these questions", "q_conseils": [
   "<strong>How many years am I committing to?</strong> A dog or cat often lives more than 10 years: think about your plans (moving, children, work).",
   "<strong>Who looks after them during holidays?</strong> Plan a solution before adopting.",
   "<strong>What budget?</strong> Work it out with our <a href=\"budget-animal.html\">budget calculator</a>.",
   "<strong>Does everyone agree?</strong> Including allergies: spend time with the species before deciding.",
   "<strong>What about a rescue?</strong> Many animals are waiting for a family, and an adult's character is already known."],
 "q_note": "This quiz gives a direction, not a certainty: every animal has their own personality.",
},
"it": {
 "home": "Home", "jour": "Giorno", "plus": "Per saperne di più",
 "prog_fil": "Programma cucciolo", "prog_titre": "30 giorni con il mio cucciolo: il programma giorno per giorno", "prog_h1": "🐶 30 giorni con il mio cucciolo: il programma di educazione",
 "prog_desc": "Un esercizio al giorno per 30 giorni per educare il cucciolo con dolcezza: nome, bisogni, seduto, richiamo, guinzaglio. Progressi salvati, senza iscrizione.",
 "prog_lead": "Un piccolo esercizio al giorno, da 5 a 10 minuti, per porre le basi con dolcezza: il nome, i bisogni, il seduto, il richiamo, il guinzaglio… Spunta ogni giorno riuscito: i progressi restano su questo dispositivo, senza iscrizione.",
 "prog_zero": "0 / 30 giorni", "prog_note": "Nessuna fretta: se un esercizio è difficile, rifallo il giorno dopo. Ogni cucciolo impara al suo ritmo.", "prog_raz": "Ricomincia da zero",
 "semaines": {1: "Settimana 1 · Ambientamento e fiducia", 2: "Settimana 2 · Le prime basi", 3: "Settimana 3 · Scoprire il mondo", 4: "Settimana 4 · Consolidare"},
 "prog_regles": "<strong>Le regole del programma:</strong> sessioni brevissime, sempre con premi, mai punizioni. Fermati prima che si annoi. Per uscite e incontri prima della fine dei vaccini, segui i consigli del veterinario.",
 "prog_liens": 'Per saperne di più: <a href="kit-accueil-chiot.html">cosa serve per accogliere un cucciolo</a> · <a href="meilleures-friandises-education-chien.html">quali bocconcini scegliere?</a> · <a href="chien.html">la guida completa al cane</a>.',
 "menu_prog": "🐶 Programma cucciolo 30 giorni", "menu_budget": "💶 Calcola il budget", "menu_quiz": "🤔 Quale animale per me?",
 "b_fil": "Budget", "b_titre": "Quanto costa un cane o un gatto? Calcola il tuo budget", "b_h1": "💶 Quanto costa un cane o un gatto? Calcola il tuo budget",
 "b_desc": "Calcola il budget del tuo cane o gatto con i tuoi importi: cibo, veterinario, assicurazione, pensione. Costo al mese, all'anno e per il primo anno.",
 "b_lead": "Prima di adottare, o per fare il punto: inserisci i tuoi importi (preventivi del veterinario, prezzo delle crocchette, assicurazione…) e ottieni il costo al mese, all'anno e per il primo anno.",
 "chien": "🐕 Cane", "chat": "🐈 Gatto", "animal": "Animale",
 "groupes": ["Spese regolari (al mese)", "Spese annuali (all'anno)", "Spese iniziali (una volta sola)"],
 "postes": {"alim": "Cibo (crocchette, umido)", "friandises": "Snack e giochi", "litiere": "Lettiera", "assurance": "Assicurazione sanitaria",
            "antiparasitaire": "Antiparassitari (se paghi al mese)", "veto": "Veterinario: vaccini e controllo", "toilettage": "Toelettatura",
            "garde": "Pensione o pet sitter in vacanza", "education": "Corsi di educazione", "divers": "Imprevisti e varie",
            "adoption": "Adozione o acquisto", "identification": "Microchip, primi vaccini", "sterilisation": "Sterilizzazione o castrazione",
            "materiel": "Attrezzatura iniziale (cuccia, ciotole, guinzaglio o trasportino…)"},
 "t_mois": "Al mese:", "t_an": "All'anno:", "t_premiere": "Primo anno (con le spese iniziali):",
 "b_note": "Il calcolo somma solo i tuoi importi. I tuoi dati restano sul tuo dispositivo.",
 "b_ou": "Dove trovare gli importi giusti?", "b_conseils": [
   "<strong>Cibo</strong>: guarda la razione consigliata sulla confezione per il peso del tuo animale e quanto dura un sacco.",
   "<strong>Veterinario</strong>: chiedi il prezzo di una visita, dei vaccini e, se serve, della sterilizzazione. I prezzi variano da una clinica all'altra.",
   "<strong>Assicurazione</strong>: confronta più preventivi, guardando massimali ed esclusioni.",
   "<strong>Pensione</strong>: pensione, pet sitter o parenti: pensaci prima delle vacanze.",
   "<strong>Imprevisti</strong>: un incidente o una malattia possono capitare. Mettere da parte un po' ogni mese evita brutte sorprese."],
 "b_liens": 'Per preparare il suo arrivo: <a href="kit-accueil-chiot.html">cosa serve per un cucciolo</a> · <a href="promos-animaux.html">le offerte del momento</a> · <a href="quel-animal.html">quale animale fa per te?</a>',
 "q_fil": "Quale animale per me?", "q_titre": "Quale animale fa per me? Il quiz prima di adottare", "q_h1": "🤔 Quale animale fa per me?",
 "q_desc": "Cane, gatto, conigli, roditori o uccello: 6 domande sulla tua casa, il tuo tempo e i tuoi desideri per trovare l'animale giusto prima di adottare.",
 "q_lead": "Cane sportivo, cane tranquillo, gatto, conigli, roditori o uccello? 6 domande sulla tua casa, il tuo tempo e i tuoi desideri per trovare il compagno che fa per te.",
 "q_noscript": "Questo quiz richiede JavaScript.",
 "questions": [("Dove vivi?", ["Appartamento", "Casa senza giardino", "Casa con giardino"]),
               ("Quanto tempo puoi dedicargli ogni giorno?", ["Meno di un'ora", "Da 1 a 2 ore", "Più di 2 ore"]),
               ("Le tue giornate fuori casa?", ["Spesso più di 8 ore", "Qualche ora", "Sono spesso a casa"]),
               ("Quanta voglia hai di passeggiate e movimento?", ["Sport, trekking, adoro muovermi", "Passeggiate tranquille", "Piuttosto casalingo"]),
               ("Rumore e disordine?", ["Nessun problema", "Preferisco la calma"]),
               ("Che tipo di rapporto cerchi?", ["Un compagno che mi segue ovunque", "Un compagno indipendente", "Osservare e interagire nei suoi momenti"])],
 "resultats": [("🐕 Un cane sportivo", "Hai tempo, energia e voglia di muoverti: un cane attivo sarà un ottimo compagno di passeggiate e giochi. Prevedi tempo ogni giorno per l'educazione e le uscite."),
               ("🐕 Un cane tranquillo", "Un cane dal temperamento calmo fa per te: ama le passeggiate tranquille e la vita di famiglia. Informati sulla razza o adotta un adulto dal carattere conosciuto."),
               ("🐈 Un gatto", "Un gatto si adatta bene ai tuoi ritmi e alla tua casa. Prevedi tiragraffi, giochi ogni giorno e posti in alto perché sia felice."),
               ("🐇 Dei conigli", "Il coniglio è un animale socievole, che vive meglio in coppia e ha bisogno di spazio per correre ogni giorno, non solo di una gabbia. Richiede tempo e cure regolari."),
               ("🐀 Dei roditori", "Ratti, porcellini d'India o gerbilli potrebbero fare per te: spesso socievoli tra loro (da adottare in più esemplari secondo la specie), hanno bisogno di un grande habitat e di attenzioni ogni giorno."),
               ("🦜 Un uccello", "Un uccello da compagnia richiede tanta presenza, interazione e stimoli. Può essere rumoroso e vivere a lungo: informati bene sulla specie prima di impegnarti.")],
 "q_avant": "Prima di adottare, fatti queste domande", "q_conseils": [
   "<strong>Per quanti anni mi impegno?</strong> Un cane o un gatto vive spesso più di 10 anni: pensa ai tuoi progetti (trasloco, figli, lavoro).",
   "<strong>Chi se ne occupa in vacanza?</strong> Prevedi una soluzione prima di adottare.",
   "<strong>Quale budget?</strong> Fai il calcolo con il nostro <a href=\"budget-animal.html\">calcolatore di budget</a>.",
   "<strong>Sono tutti d'accordo?</strong> Anche per le allergie: passa del tempo con la specie prima di decidere.",
   "<strong>E se adottassi in canile o gattile?</strong> Tanti animali aspettano una famiglia, e il carattere di un adulto è già conosciuto."],
 "q_note": "Questo quiz dà un orientamento, non una certezza: ogni animale ha la sua personalità.",
}}


def programme(code):
    t = T[code]
    blocs = ""
    for s, titre_s in t["semaines"].items():
        items = ""
        for i, ((sem, _, _, lien), (titre, consigne)) in enumerate(zip(FR.JOURS, JOURS[code]), 1):
            if sem != s:
                continue
            lien_html = f' <a href="{lien}">{t["plus"]}</a>' if lien and lien.split("#")[0] not in SEULEMENT_FR else ""
            items += (f'          <li class="jour"><label><input type="checkbox" data-jour="{i}"> <strong>{t["jour"]} {i} · {e(titre)}</strong></label>'
                      f'<p>{e(consigne)}{lien_html}</p></li>\n')
        blocs += f'        <h2>{titre_s}</h2>\n        <ol class="jours">\n{items}        </ol>\n'
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">{t["home"]}</a> › {t["prog_fil"]}</p>
        <h1>{t["prog_h1"]}</h1>
        <p class="lead">{t["prog_lead"]}</p>
        <div class="card progression"><p><strong id="prog-texte">{t["prog_zero"]}</strong></p><div class="barre-prog"><span id="prog-barre"></span></div>
          <p class="small muted">{t["prog_note"]}</p>
          <button type="button" class="btn btn-sm btn-outline" id="prog-raz">{t["prog_raz"]}</button></div>
{blocs}        <div class="callout">{t["prog_regles"]}</div>
        <p>{t["prog_liens"]}</p>
      </div>
    </section>"""


def budget(code):
    t = T[code]
    groupes = ""
    for titre, (_, periode, champs) in zip(t["groupes"], FR.POSTES):
        lignes = "".join(f'<div class="poste" data-especes="{esp}"><label for="b-{k}">{e(t["postes"][k])}</label><input id="b-{k}" type="number" min="0" step="1" inputmode="decimal" placeholder="0" data-periode="{periode}"> <span>€</span></div>'
                         for k, _, esp in champs)
        groupes += f'          <fieldset><legend>{titre}</legend>{lignes}</fieldset>\n'
    conseils = "".join(f"<li>{c}</li>" for c in t["b_conseils"])
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">{t["home"]}</a> › {t["b_fil"]}</p>
        <h1>{t["b_h1"]}</h1>
        <p class="lead">{t["b_lead"]}</p>
        <div class="card" id="calc-budget">
          <div class="choix-espece" role="radiogroup" aria-label="{t["animal"]}">
            <label><input type="radio" name="b-espece" value="c" checked><span>{t["chien"]}</span></label>
            <label><input type="radio" name="b-espece" value="t"><span>{t["chat"]}</span></label>
          </div>
{groupes}          <div class="budget-total" aria-live="polite">
            <p>{t["t_mois"]} <strong id="t-mois">0 €</strong></p>
            <p>{t["t_an"]} <strong id="t-an">0 €</strong></p>
            <p>{t["t_premiere"]} <strong id="t-premiere">0 €</strong></p>
          </div>
          <p class="small muted">{t["b_note"]}</p>
        </div>
        <h2>{t["b_ou"]}</h2>
        <ul>{conseils}</ul>
        <p>{t["b_liens"]}</p>
      </div>
    </section>"""


def quel_animal(code):
    t = T[code]
    donnees = {"q": [{"t": q, "r": [{"t": rt, "p": p} for rt, (_, p) in zip(reps, fr_r)]} for (q, reps), (_, fr_r) in zip(t["questions"], FR.QUIZ)],
               "res": [{"t": rt, "d": rd, "l": l} for (rt, rd), (_, _, l) in zip(t["resultats"], FR.RESULTATS)]}
    conseils = "".join(f"<li>{c}</li>" for c in t["q_conseils"])
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">{t["home"]}</a> › {t["q_fil"]}</p>
        <h1>{t["q_h1"]}</h1>
        <p class="lead">{t["q_lead"]}</p>
        <div class="card" id="quel-animal"><div class="qa-zone" aria-live="polite"><noscript>{t["q_noscript"]}</noscript></div></div>
        <script type="application/json" id="donnees-quel-animal">{json.dumps(donnees, ensure_ascii=False)}</script>
        <h2>{t["q_avant"]}</h2>
        <ul>{conseils}</ul>
        <p class="small muted">{t["q_note"]}</p>
      </div>
    </section>"""


if __name__ == "__main__":
    for code in ("en", "it"):
        t = T[code]
        assert len(JOURS[code]) == len(FR.JOURS)
        creer_page.creer(code, "programme-chiot-30-jours", t["prog_titre"], t["prog_desc"], programme(code), scripts=["js/programme.js"], menu=t["menu_prog"])
        creer_page.creer(code, "budget-animal", t["b_titre"], t["b_desc"], budget(code), scripts=["js/budget.js"], menu=t["menu_budget"])
        creer_page.creer(code, "quel-animal", t["q_titre"], t["q_desc"], quel_animal(code), scripts=["js/quel-animal.js"], menu=t["menu_quiz"])
    creer_page.finir()
