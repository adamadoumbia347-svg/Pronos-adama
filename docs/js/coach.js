/* Coach 5 minutes (#coach) : une séance d'éducation par jour, minuteur, série de jours et progression.
   Tout est gardé sur l'appareil (localStorage). Textes en fr / en / it. */
(function () {
  var bloc = document.getElementById("coach");
  if (!bloc) return;
  var zone = bloc.querySelector(".coach-zone");
  var lang = { fr: 1, en: 1, it: 1 }[document.documentElement.lang] ? document.documentElement.lang : "fr";
  var CLE = "coach-5min", DUREE = 300, ACQUIS = 3;

  var T = {
    fr: {
      nom: "Comment s'appelle votre animal ?", nomPh: "Son nom", espece: "C'est…", go: "Commencer",
      especes: { chien: "🐕 Un chien", chat: "🐈 Un chat", lapin: "🐇 Un lapin", oiseau: "🦜 Un oiseau" },
      jour: "La séance du jour de {n}", bonus: "Séance bonus de {n}", serie: ["jour de suite", "jours de suite"], seances: ["séance", "séances"], acquis: "acquis",
      but: "Objectif", astuce: "Astuce", guide: "Lire le guide complet", demarrer: "▶ Démarrer les 5 minutes", pause: "⏸ Pause",
      reprendre: "▶ Reprendre", fini: "✓ Séance terminée", autre: "Proposer un autre exercice",
      comment: "Comment ça s'est passé ?", notes: ["😅 Difficile", "🙂 Ça progresse", "🤩 Facile !"],
      bravo: "Bravo, séance faite !", demain: "Revenez demain pour la suite : la régularité compte plus que la durée.",
      msg: ["Pas grave : la prochaine fois, rendez l'exercice plus facile (moins de distractions, meilleure friandise).",
            "C'est exactement comme ça qu'on avance. On reprend cet exercice à la prochaine séance.",
            "Excellent ! {n} est sur la bonne voie."],
      nouveau: "⭐ Exercice acquis : {t}", encore: "Faire une séance bonus", temps: "Temps écoulé ! Terminez sur une réussite.",
      parcours: "Le parcours de {n}", semaine: ["L", "M", "M", "J", "V", "S", "D"], revision: "Révision",
      tout: "🎓 Tout le parcours est acquis ! On entretient avec des révisions.", changer: "Changer d'animal ou recommencer",
      effacer: "Effacer toute la progression ?", partager: "Partager ma série", partage: "{n} en est à {s} jours de suite avec le Coach 5 minutes 🐾"
    },
    en: {
      nom: "What is your pet's name?", nomPh: "Name", espece: "It's…", go: "Start",
      especes: { chien: "🐕 A dog", chat: "🐈 A cat", lapin: "🐇 A rabbit", oiseau: "🦜 A bird" },
      jour: "{n}'s session of the day", bonus: "{n}'s bonus session", serie: ["day in a row", "days in a row"], seances: ["session", "sessions"], acquis: "learned",
      but: "Goal", astuce: "Tip", guide: "Read the full guide", demarrer: "▶ Start the 5 minutes", pause: "⏸ Pause",
      reprendre: "▶ Resume", fini: "✓ Session done", autre: "Suggest another exercise",
      comment: "How did it go?", notes: ["😅 Hard", "🙂 Getting there", "🤩 Easy!"],
      bravo: "Well done, session complete!", demain: "Come back tomorrow: consistency matters more than length.",
      msg: ["No problem: next time, make it easier (fewer distractions, a better treat).",
            "That is exactly how progress happens. We will repeat this exercise next session.",
            "Excellent! {n} is on the right track."],
      nouveau: "⭐ Exercise learned: {t}", encore: "Do a bonus session", temps: "Time's up! End on a success.",
      parcours: "{n}'s path", semaine: ["M", "T", "W", "T", "F", "S", "S"], revision: "Review",
      tout: "🎓 The whole path is learned! Keep it up with review sessions.", changer: "Change pet or start over",
      effacer: "Clear all progress?", partager: "Share my streak", partage: "{n} is on a {s}-day streak with the 5-Minute Coach 🐾"
    },
    it: {
      nom: "Come si chiama il tuo animale?", nomPh: "Il suo nome", espece: "È…", go: "Inizia",
      especes: { chien: "🐕 Un cane", chat: "🐈 Un gatto", lapin: "🐇 Un coniglio", oiseau: "🦜 Un uccello" },
      jour: "La sessione di oggi di {n}", bonus: "Sessione bonus di {n}", serie: ["giorno di fila", "giorni di fila"], seances: ["sessione", "sessioni"], acquis: "imparati",
      but: "Obiettivo", astuce: "Consiglio", guide: "Leggi la guida completa", demarrer: "▶ Avvia i 5 minuti", pause: "⏸ Pausa",
      reprendre: "▶ Riprendi", fini: "✓ Sessione terminata", autre: "Proponi un altro esercizio",
      comment: "Com'è andata?", notes: ["😅 Difficile", "🙂 Migliora", "🤩 Facile!"],
      bravo: "Bravo, sessione fatta!", demain: "Torna domani: la costanza conta più della durata.",
      msg: ["Nessun problema: la prossima volta rendi l'esercizio più facile (meno distrazioni, un premio migliore).",
            "È proprio così che si fanno progressi. Riprendiamo questo esercizio alla prossima sessione.",
            "Ottimo! {n} è sulla buona strada."],
      nouveau: "⭐ Esercizio imparato: {t}", encore: "Fai una sessione bonus", temps: "Tempo scaduto! Finisci con un successo.",
      parcours: "Il percorso di {n}", semaine: ["L", "M", "M", "G", "V", "S", "D"], revision: "Ripasso",
      tout: "🎓 Tutto il percorso è imparato! Continua con i ripassi.", changer: "Cambia animale o ricomincia",
      effacer: "Cancellare tutti i progressi?", partager: "Condividi la mia serie", partage: "{n} è a {s} giorni di fila con il Coach 5 minuti 🐾"
    }
  }[lang];

  // Exercices : [identifiant, page du guide, { langue: [titre, objectif, étape 1, étape 2, étape 3, astuce] }]
  var EXOS = {
    chien: [
      ["nom", "methodes.html#renforcement-positif", {
        fr: ["Réagir à son nom", "Votre chien vous regarde dès qu'il entend son nom.", "Dites son nom une seule fois, d'une voix gaie.", "À l'instant où il vous regarde, donnez une friandise.", "Faites 10 répétitions, puis changez de pièce.", "Ne répétez pas le nom en boucle : dites-le une fois et attendez."],
        en: ["Responding to their name", "Your dog looks at you as soon as they hear their name.", "Say the name once, in a cheerful voice.", "The instant they look at you, give a treat.", "Do 10 repetitions, then change rooms.", "Do not repeat the name over and over: say it once and wait."],
        it: ["Rispondere al nome", "Il cane ti guarda appena sente il suo nome.", "Di' il nome una sola volta, con voce allegra.", "Nell'istante in cui ti guarda, dai un premio.", "Fai 10 ripetizioni, poi cambia stanza.", "Non ripetere il nome a raffica: dillo una volta e aspetta."] }],
      ["assis", "apprendre-assis-couche-pas-bouger.html", {
        fr: ["Assis", "Votre chien s'assoit sur demande, sans qu'on le touche.", "Tenez une friandise contre sa truffe et montez-la lentement au-dessus de sa tête.", "Dès que l'arrière-train touche le sol, récompensez.", "Après 5 réussites, dites « assis » juste avant le geste.", "S'il saute, la friandise est trop haute : gardez-la près du nez."],
        en: ["Sit", "Your dog sits on cue, without being touched.", "Hold a treat at their nose and slowly raise it above their head.", "As soon as their bottom touches the floor, reward.", "After 5 successes, say “sit” just before the gesture.", "If they jump, the treat is too high: keep it close to the nose."],
        it: ["Seduto", "Il cane si siede a richiesta, senza essere toccato.", "Tieni un premio vicino al tartufo e alzalo lentamente sopra la testa.", "Appena il sedere tocca terra, premia.", "Dopo 5 successi, di' «seduto» subito prima del gesto.", "Se salta, il premio è troppo in alto: tienilo vicino al naso."] }],
      ["couche", "apprendre-assis-couche-pas-bouger.html", {
        fr: ["Couché", "Votre chien se couche sur demande.", "Partez de la position assise, friandise contre la truffe.", "Descendez la main lentement vers le sol, entre ses pattes avant.", "Dès que les coudes touchent le sol, récompensez au sol.", "Travaillez sur un tapis : beaucoup de chiens hésitent sur un sol dur ou froid."],
        en: ["Down", "Your dog lies down on cue.", "Start from a sit, with a treat at the nose.", "Slowly lower your hand to the floor, between the front paws.", "As soon as the elbows touch the floor, reward on the floor.", "Work on a mat: many dogs hesitate on a hard or cold floor."],
        it: ["Terra", "Il cane si sdraia a richiesta.", "Parti dal seduto, con un premio vicino al tartufo.", "Abbassa lentamente la mano verso terra, tra le zampe anteriori.", "Appena i gomiti toccano terra, premia a terra.", "Lavora su un tappetino: molti cani esitano su un pavimento duro o freddo."] }],
      ["pasbouger", "apprendre-assis-couche-pas-bouger.html", {
        fr: ["Pas bouger", "Votre chien reste en place quelques secondes.", "Chien assis, montrez la paume et comptez 2 secondes.", "Récompensez pendant qu'il est encore en place, puis libérez-le d'un « OK ».", "Allongez d'une seconde à chaque réussite, puis reculez d'un pas.", "Augmentez soit la durée, soit la distance, jamais les deux à la fois."],
        en: ["Stay", "Your dog stays in place for a few seconds.", "With your dog sitting, show your palm and count 2 seconds.", "Reward while they are still in place, then release with “OK”.", "Add one second per success, then take one step back.", "Increase either duration or distance, never both at once."],
        it: ["Resta", "Il cane resta fermo per qualche secondo.", "Con il cane seduto, mostra il palmo e conta 2 secondi.", "Premia mentre è ancora fermo, poi liberalo con «OK».", "Aggiungi un secondo a ogni successo, poi fai un passo indietro.", "Aumenta la durata oppure la distanza, mai entrambe insieme."] }],
      ["rappel", "rappel-chien.html", {
        fr: ["Le rappel", "Votre chien revient vers vous en courant.", "À la maison, à 2 mètres, dites « viens ! » d'une voix joyeuse.", "Accroupissez-vous et récompensez généreusement à son arrivée.", "Augmentez la distance, puis passez au jardin avec une longe.", "Ne rappelez jamais pour gronder ou finir la promenade : le rappel doit toujours payer."],
        en: ["Recall", "Your dog runs back to you.", "At home, from 2 metres, say “come!” in a happy voice.", "Crouch down and reward generously when they arrive.", "Increase the distance, then move to the garden on a long line.", "Never call your dog to scold or to end the walk: coming back must always pay."],
        it: ["Il richiamo", "Il cane torna da te di corsa.", "In casa, a 2 metri, di' «vieni!» con voce allegra.", "Accovacciati e premia generosamente al suo arrivo.", "Aumenta la distanza, poi passa in giardino con una lunghina.", "Non richiamare mai per sgridare o finire la passeggiata: tornare deve sempre convenire."] }],
      ["laisse", "marche-en-laisse.html", {
        fr: ["Marcher sans tirer", "La laisse reste détendue pendant la marche.", "Dans un endroit calme, avancez : récompensez chaque pas fait laisse détendue.", "Dès que la laisse se tend, arrêtez-vous sans tirer.", "Repartez quand il revient vers vous et que la laisse se détend.", "Donnez la friandise le long de votre jambe : c'est là qu'il apprendra à se placer."],
        en: ["Loose-lead walking", "The lead stays slack during the walk.", "In a quiet place, walk: reward every step taken on a slack lead.", "As soon as the lead tightens, stop without pulling.", "Set off again when they come back and the lead slackens.", "Give the treat beside your leg: that is where they learn to walk."],
        it: ["Camminare senza tirare", "Il guinzaglio resta morbido durante la passeggiata.", "In un posto tranquillo, cammina: premia ogni passo con il guinzaglio morbido.", "Appena il guinzaglio si tende, fermati senza tirare.", "Riparti quando torna verso di te e il guinzaglio si allenta.", "Dai il premio lungo la tua gamba: è lì che imparerà a stare."] }],
      ["sauter", "chien-saute-sur-les-gens.html", {
        fr: ["Dire bonjour sans sauter", "Votre chien garde les 4 pattes au sol pour saluer.", "Approchez-vous : tant que les 4 pattes sont au sol, caressez et récompensez.", "S'il saute, détournez-vous sans un mot ni un regard.", "Revenez dès qu'il est au sol et récompensez aussitôt.", "Récompensez bas, au niveau de son museau : cela l'invite à rester au sol."],
        en: ["Greeting without jumping", "Your dog keeps all 4 paws on the floor to say hello.", "Approach: while all 4 paws are on the floor, pet and reward.", "If they jump, turn away without a word or a look.", "Come back as soon as they are on the floor and reward at once.", "Reward low, at muzzle height: it invites them to stay down."],
        it: ["Salutare senza saltare", "Il cane tiene le 4 zampe a terra per salutare.", "Avvicinati: finché le 4 zampe sono a terra, accarezza e premia.", "Se salta, girati senza una parola né uno sguardo.", "Torna appena è a terra e premia subito.", "Premia in basso, all'altezza del muso: lo invita a restare giù."] }],
      ["panier", "chien.html", {
        fr: ["Au panier", "Votre chien va se poser sur son tapis sur demande.", "Lancez une friandise sur le tapis et récompensez encore quand il est dessus.", "Attendez qu'il s'y couche de lui-même : jackpot de friandises.", "Ajoutez le mot « au panier », puis demandez-le d'un peu plus loin.", "Le panier est un refuge : on n'y envoie jamais le chien pour le punir."],
        en: ["Go to your bed", "Your dog settles on their mat on cue.", "Toss a treat onto the mat and reward again while they are on it.", "Wait for them to lie down on their own: jackpot of treats.", "Add the words “on your bed”, then ask from a little further away.", "The bed is a safe place: never send your dog there as a punishment."],
        it: ["A cuccia", "Il cane va a sistemarsi sul suo tappetino a richiesta.", "Lancia un premio sul tappetino e premia ancora mentre ci sta sopra.", "Aspetta che si sdrai da solo: jackpot di premi.", "Aggiungi la parola «a cuccia», poi chiedilo da un po' più lontano.", "La cuccia è un rifugio: non mandarci mai il cane per punizione."] }]
    ],
    chat: [
      ["nom", "chat.html", {
        fr: ["Venir à l'appel", "Votre chat vient quand vous l'appelez.", "Juste avant le repas, dites son nom puis un mot (« viens »), toujours le même.", "Donnez aussitôt une friandise ou posez la gamelle.", "Recommencez à 1 mètre, puis depuis une autre pièce.", "Travaillez avant le repas, jamais après : la motivation fait tout."],
        en: ["Coming when called", "Your cat comes when you call.", "Just before a meal, say their name then one word (“come”), always the same.", "Give a treat or put the bowl down straight away.", "Repeat from 1 metre, then from another room.", "Train before meals, never after: motivation is everything."],
        it: ["Venire al richiamo", "Il gatto arriva quando lo chiami.", "Subito prima del pasto, di' il suo nome e poi una parola («vieni»), sempre la stessa.", "Dai subito un premio o appoggia la ciotola.", "Ripeti a 1 metro, poi da un'altra stanza.", "Lavora prima del pasto, mai dopo: la motivazione è tutto."] }],
      ["cible", "clicker-training-debutant.html", {
        fr: ["Toucher la cible", "Votre chat touche du nez un objet que vous présentez.", "Présentez deux doigts (ou une baguette) à 5 cm de son nez.", "Dès qu'il les touche du nez, dites « oui » ou cliquez, puis récompensez.", "Déplacez la cible de quelques centimètres pour qu'il la suive.", "3 minutes suffisent : arrêtez avant qu'il ne se lasse."],
        en: ["Touching a target", "Your cat touches an object you present with their nose.", "Present two fingers (or a stick) 5 cm from their nose.", "As soon as they touch with their nose, say “yes” or click, then reward.", "Move the target a few centimetres so they follow it.", "3 minutes is enough: stop before they lose interest."],
        it: ["Toccare il target", "Il gatto tocca con il naso un oggetto che gli presenti.", "Presenta due dita (o una bacchetta) a 5 cm dal naso.", "Appena le tocca con il naso, di' «sì» o fai clic, poi premia.", "Sposta il target di qualche centimetro perché lo segua.", "Bastano 3 minuti: smetti prima che si stanchi."] }],
      ["griffoir", "chat-griffe-canape.html", {
        fr: ["Griffer au bon endroit", "Votre chat utilise son griffoir plutôt que le canapé.", "Placez le griffoir près de l'endroit qu'il griffe ou de son couchage.", "Jouez avec un plumeau contre le griffoir pour qu'il y pose les griffes.", "Félicitez et récompensez chaque griffade au bon endroit.", "Un griffoir stable et assez haut pour s'étirer est bien plus utilisé."],
        en: ["Scratching in the right place", "Your cat uses the scratching post rather than the sofa.", "Put the post near the spot they scratch or near their bed.", "Play with a wand toy against the post so they put their claws on it.", "Praise and reward every scratch in the right place.", "A stable post tall enough for a full stretch gets used far more."],
        it: ["Graffiare nel posto giusto", "Il gatto usa il tiragraffi invece del divano.", "Metti il tiragraffi vicino al punto che graffia o alla sua cuccia.", "Gioca con una cannetta contro il tiragraffi perché ci appoggi le unghie.", "Loda e premia ogni graffiata nel posto giusto.", "Un tiragraffi stabile e abbastanza alto per stirarsi viene usato molto di più."] }],
      ["caisse", "chat-caisse-transport-voiture.html", {
        fr: ["Aimer la caisse de transport", "Votre chat entre de lui-même dans sa caisse.", "Laissez la caisse ouverte dans le salon, avec une couverture.", "Déposez des friandises à l'entrée, puis de plus en plus au fond.", "Quand il y entre volontiers, fermez la porte 2 secondes, puis rouvrez et récompensez.", "Laissez la caisse sortie toute l'année : elle devient un meuble comme un autre."],
        en: ["Loving the carrier", "Your cat walks into the carrier on their own.", "Leave the carrier open in the living room, with a blanket.", "Place treats at the entrance, then further and further inside.", "Once they go in happily, close the door for 2 seconds, then open and reward.", "Leave the carrier out all year: it becomes just another piece of furniture."],
        it: ["Amare il trasportino", "Il gatto entra da solo nel trasportino.", "Lascia il trasportino aperto in salotto, con una coperta.", "Metti dei premi all'ingresso, poi sempre più in fondo.", "Quando entra volentieri, chiudi la porta per 2 secondi, poi riapri e premia.", "Lascia il trasportino fuori tutto l'anno: diventa un mobile come un altro."] }],
      ["assis", "clicker-training-debutant.html", {
        fr: ["Assis", "Votre chat s'assoit sur demande.", "Tenez une friandise devant son nez et montez-la lentement au-dessus de sa tête.", "Dès qu'il s'assoit, dites « oui » ou cliquez, puis récompensez.", "Après quelques réussites, dites « assis » juste avant le geste.", "S'il se dresse sur ses pattes arrière, baissez la friandise."],
        en: ["Sit", "Your cat sits on cue.", "Hold a treat in front of their nose and slowly raise it above their head.", "As soon as they sit, say “yes” or click, then reward.", "After a few successes, say “sit” just before the gesture.", "If they stand on their hind legs, lower the treat."],
        it: ["Seduto", "Il gatto si siede a richiesta.", "Tieni un premio davanti al naso e alzalo lentamente sopra la testa.", "Appena si siede, di' «sì» o fai clic, poi premia.", "Dopo qualche successo, di' «seduto» subito prima del gesto.", "Se si alza sulle zampe posteriori, abbassa il premio."] }],
      ["soins", "chat.html", {
        fr: ["Accepter les soins", "Votre chat se laisse toucher les pattes et les oreilles.", "Touchez une patte une seconde, puis donnez une friandise.", "Allongez peu à peu : tenir la patte, écarter doucement un doigt.", "Faites de même avec les oreilles, puis en soulevant une babine.", "S'il retire la patte ou s'agite, revenez à l'étape précédente : il ne doit jamais se sentir forcé."],
        en: ["Accepting handling", "Your cat lets you touch their paws and ears.", "Touch one paw for a second, then give a treat.", "Build up little by little: hold the paw, gently spread a toe.", "Do the same with the ears, then by lifting a lip.", "If they pull away or get restless, go back a step: they should never feel forced."],
        it: ["Accettare le cure", "Il gatto si lascia toccare zampe e orecchie.", "Tocca una zampa per un secondo, poi dai un premio.", "Aumenta poco a poco: tieni la zampa, allarga delicatamente un dito.", "Fai lo stesso con le orecchie, poi sollevando un labbro.", "Se ritira la zampa o si agita, torna al passo precedente: non deve mai sentirsi forzato."] }]
    ],
    lapin: [
      ["confiance", "nac.html", {
        fr: ["Gagner sa confiance", "Votre lapin s'approche de vous sans crainte.", "Asseyez-vous par terre, près de lui, sans chercher à le toucher.", "Posez un petit morceau de légume près de vous et attendez qu'il vienne.", "Rapprochez la friandise à chaque séance, jusqu'à votre main.", "Restez à sa hauteur : vu d'en haut, vous ressemblez à un prédateur."],
        en: ["Earning their trust", "Your rabbit comes up to you without fear.", "Sit on the floor near them, without trying to touch.", "Put a small piece of vegetable near you and wait for them to come.", "Bring the treat closer each session, up to your hand.", "Stay at their level: seen from above, you look like a predator."],
        it: ["Conquistare la fiducia", "Il coniglio si avvicina a te senza paura.", "Siediti per terra vicino a lui, senza cercare di toccarlo.", "Appoggia un pezzetto di verdura vicino a te e aspetta che arrivi.", "Avvicina il premio a ogni sessione, fino alla tua mano.", "Resta alla sua altezza: visto dall'alto, sembri un predatore."] }],
      ["appel", "nac.html", {
        fr: ["Venir à l'appel", "Votre lapin vient quand vous l'appelez.", "Dites son nom, puis tendez aussitôt une friandise.", "Recommencez à 1 mètre : il doit faire quelques pas vers vous.", "Augmentez la distance peu à peu, toujours avec le même mot.", "De toutes petites portions : un brin de persil ou de coriandre suffit."],
        en: ["Coming when called", "Your rabbit comes when you call.", "Say their name, then offer a treat straight away.", "Repeat from 1 metre: they should take a few steps towards you.", "Increase the distance little by little, always with the same word.", "Tiny portions: a sprig of parsley or coriander is enough."],
        it: ["Venire al richiamo", "Il coniglio arriva quando lo chiami.", "Di' il suo nome, poi porgi subito un premio.", "Ripeti a 1 metro: deve fare qualche passo verso di te.", "Aumenta la distanza poco a poco, sempre con la stessa parola.", "Porzioni minuscole: basta un rametto di prezzemolo o di coriandolo."] }],
      ["cible", "methodes.html#clicker", {
        fr: ["Toucher la cible", "Votre lapin touche du nez un objet que vous présentez.", "Présentez une baguette ou une cuillère en bois à quelques centimètres de son nez.", "Dès qu'il la touche du nez, dites « oui » et récompensez.", "Déplacez la cible pour qu'il fasse un pas, puis deux.", "La cible servira ensuite à le guider sans le porter."],
        en: ["Touching a target", "Your rabbit touches an object you present with their nose.", "Present a stick or a wooden spoon a few centimetres from their nose.", "As soon as they touch it with their nose, say “yes” and reward.", "Move the target so they take one step, then two.", "The target will later help you guide them without picking them up."],
        it: ["Toccare il target", "Il coniglio tocca con il naso un oggetto che gli presenti.", "Presenta una bacchetta o un cucchiaio di legno a pochi centimetri dal naso.", "Appena lo tocca con il naso, di' «sì» e premia.", "Sposta il target perché faccia un passo, poi due.", "Il target servirà poi a guidarlo senza prenderlo in braccio."] }],
      ["litiere", "nac.html", {
        fr: ["Utiliser la litière", "Votre lapin fait ses besoins dans son bac.", "Placez le bac dans le coin qu'il a déjà choisi, avec du foin à portée.", "Déposez-y quelques crottes pour lui indiquer l'endroit.", "Récompensez-le quand il y saute de lui-même.", "Jamais de litière minérale ou agglomérante : préférez une litière végétale."],
        en: ["Using the litter tray", "Your rabbit uses their tray.", "Put the tray in the corner they have already chosen, with hay within reach.", "Place a few droppings in it to show the spot.", "Reward them when they hop in on their own.", "Never use clay or clumping litter: choose a plant-based one."],
        it: ["Usare la lettiera", "Il coniglio fa i bisogni nella sua cassetta.", "Metti la cassetta nell'angolo che ha già scelto, con del fieno a portata.", "Mettici qualche pallina per indicargli il posto.", "Premialo quando ci salta dentro da solo.", "Mai lettiera minerale o agglomerante: scegli una lettiera vegetale."] }],
      ["caisse", "nac.html", {
        fr: ["Entrer dans la caisse", "Votre lapin entre de lui-même dans sa caisse de transport.", "Laissez la caisse ouverte dans son espace, garnie de foin.", "Déposez une friandise à l'entrée, puis au fond.", "Quand il y entre volontiers, fermez 2 secondes, rouvrez et récompensez.", "Un lapin qui entre seul dans sa caisse n'a pas besoin d'être attrapé."],
        en: ["Going into the carrier", "Your rabbit hops into the carrier on their own.", "Leave the carrier open in their space, filled with hay.", "Put a treat at the entrance, then at the back.", "Once they go in happily, close it for 2 seconds, open and reward.", "A rabbit who enters the carrier alone never needs to be caught."],
        it: ["Entrare nel trasportino", "Il coniglio entra da solo nel trasportino.", "Lascia il trasportino aperto nel suo spazio, con del fieno.", "Metti un premio all'ingresso, poi in fondo.", "Quando entra volentieri, chiudi per 2 secondi, riapri e premia.", "Un coniglio che entra da solo nel trasportino non deve essere acchiappato."] }]
    ],
    oiseau: [
      ["presence", "nac.html", {
        fr: ["S'habituer à vous", "Votre oiseau reste calme quand vous êtes près de la cage.", "Asseyez-vous près de la cage et parlez-lui doucement.", "Rapprochez-vous un peu à chaque séance, tant qu'il reste détendu.", "Terminez en déposant une friandise dans sa mangeoire.", "Plumes plaquées, recul au fond de la cage : vous êtes trop près, reculez."],
        en: ["Getting used to you", "Your bird stays calm when you are near the cage.", "Sit near the cage and talk to them softly.", "Move a little closer each session, as long as they stay relaxed.", "Finish by putting a treat in their feeder.", "Slicked-down feathers, backing away: you are too close, move back."],
        it: ["Abituarsi a te", "L'uccello resta calmo quando sei vicino alla gabbia.", "Siediti vicino alla gabbia e parlagli piano.", "Avvicinati un po' a ogni sessione, finché resta rilassato.", "Finisci mettendo un premio nella mangiatoia.", "Piume aderenti, arretra in fondo alla gabbia: sei troppo vicino, allontanati."] }],
      ["main", "nac.html", {
        fr: ["Manger dans la main", "Votre oiseau prend une friandise entre vos doigts.", "Présentez une grappe de millet à travers les barreaux.", "Quand il mange sans hésiter, présentez-la main dans la cage, immobile.", "Raccourcissez la grappe pour qu'il s'approche de vos doigts.", "Gardez la main sous le niveau de sa tête : c'est moins impressionnant."],
        en: ["Eating from your hand", "Your bird takes a treat from your fingers.", "Offer a spray of millet through the bars.", "When they eat without hesitating, offer it with your hand inside the cage, held still.", "Shorten the spray so they come closer to your fingers.", "Keep your hand below their head level: it is less intimidating."],
        it: ["Mangiare dalla mano", "L'uccello prende un premio dalle tue dita.", "Offri una spiga di panico attraverso le sbarre.", "Quando mangia senza esitare, offrila con la mano dentro la gabbia, ferma.", "Accorcia la spiga perché si avvicini alle dita.", "Tieni la mano sotto il livello della sua testa: fa meno paura."] }],
      ["monte", "nac.html", {
        fr: ["Monter sur le doigt", "Votre oiseau monte sur votre doigt sur demande.", "Présentez le doigt (ou un perchoir) juste au-dessus de ses pattes, contre le ventre.", "Tenez la friandise de l'autre côté : il doit monter pour l'atteindre.", "Dites « monte » au moment où il pose la patte, puis récompensez.", "Ne poussez pas son ventre : c'est lui qui choisit de monter."],
        en: ["Stepping up", "Your bird steps onto your finger on cue.", "Offer your finger (or a perch) just above their feet, against the belly.", "Hold the treat on the other side: they have to step up to reach it.", "Say “step up” as the foot lands, then reward.", "Do not push against the belly: stepping up is their choice."],
        it: ["Salire sul dito", "L'uccello sale sul tuo dito a richiesta.", "Presenta il dito (o un posatoio) appena sopra le zampe, contro la pancia.", "Tieni il premio dall'altro lato: deve salire per raggiungerlo.", "Di' «sali» nel momento in cui appoggia la zampa, poi premia.", "Non spingere sulla pancia: è lui a scegliere di salire."] }],
      ["cible", "methodes.html#clicker", {
        fr: ["Toucher la cible", "Votre oiseau touche du bec le bout d'une baguette.", "Présentez une baguette (une pique en bois) à quelques centimètres de son bec.", "Dès qu'il la touche, dites « oui » et récompensez.", "Déplacez la baguette pour qu'il fasse un pas le long du perchoir.", "Récompensez le simple toucher, pas le mordillement prolongé."],
        en: ["Touching a target", "Your bird touches the tip of a stick with their beak.", "Present a stick (a wooden skewer) a few centimetres from their beak.", "As soon as they touch it, say “yes” and reward.", "Move the stick so they take a step along the perch.", "Reward a simple touch, not prolonged chewing."],
        it: ["Toccare il target", "L'uccello tocca con il becco la punta di una bacchetta.", "Presenta una bacchetta (uno stecchino di legno) a pochi centimetri dal becco.", "Appena la tocca, di' «sì» e premia.", "Sposta la bacchetta perché faccia un passo lungo il posatoio.", "Premia il semplice tocco, non il mordicchiare prolungato."] }],
      ["rappel", "nac.html", {
        fr: ["Venir vers vous", "Votre oiseau rejoint votre main sur demande.", "Oiseau sur un perchoir, présentez la main à 10 cm et dites « viens ».", "Récompensez dès qu'il saute ou vole jusqu'à vous.", "Augmentez la distance de quelques centimètres à chaque réussite.", "Avant toute sortie de cage : fenêtres fermées, rideaux tirés, autres animaux à l'écart."],
        en: ["Coming to you", "Your bird joins your hand on cue.", "With the bird on a perch, offer your hand 10 cm away and say “come”.", "Reward as soon as they hop or fly to you.", "Increase the distance by a few centimetres with each success.", "Before any time out of the cage: windows closed, curtains drawn, other pets away."],
        it: ["Venire verso di te", "L'uccello raggiunge la tua mano a richiesta.", "Con l'uccello su un posatoio, presenta la mano a 10 cm e di' «vieni».", "Premia appena salta o vola fino a te.", "Aumenta la distanza di qualche centimetro a ogni successo.", "Prima di ogni uscita dalla gabbia: finestre chiuse, tende tirate, altri animali lontani."] }]
    ]
  };

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function txt(s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); }
  function lire() { try { return JSON.parse(localStorage.getItem(CLE)) || {}; } catch (e) { return {}; } }
  function ecrire() { try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) {} }
  function cle(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
  function jourMoins(n) { var d = new Date(); d.setHours(12, 0, 0, 0); d.setDate(d.getDate() - n); return d; }

  var etat = lire();
  if (!EXOS[etat.espece]) etat = {};
  var decalage = 0, bonus = false, minuteur = null, reste = DUREE, finA = 0;

  function exos() { return EXOS[etat.espece]; }
  function points(id) { return (etat.points && etat.points[id]) || 0; }
  function nbAcquis() { return exos().filter(function (x) { return points(x[0]) >= ACQUIS; }).length; }
  function serie() {
    var j = etat.jours || {}, n = 0, i = j[cle(jourMoins(0))] ? 0 : 1;
    while (j[cle(jourMoins(i))]) { n++; i++; }
    return n;
  }
  function total() { var j = etat.jours || {}, n = 0; for (var k in j) n += j[k]; return n; }
  // Exercice proposé : le premier non acquis (ou une révision quand tout est acquis), décalé par « autre exercice »
  function courant() {
    var liste = exos(), aFaire = liste.filter(function (x) { return points(x[0]) < ACQUIS; });
    if (!aFaire.length) return liste[(total() + decalage) % liste.length];
    var premier = liste.indexOf(aFaire[0]);
    // on peut alterner entre l'exercice en cours, le suivant et les acquis à réviser
    var choix = [aFaire[0]].concat(aFaire.slice(1, 2), liste.slice(0, premier));
    return choix[decalage % choix.length];
  }

  function accueil() {
    var boutons = Object.keys(T.especes).map(function (k) {
      return '<label><input type="radio" name="c-espece" value="' + k + '"' + (k === "chien" ? " checked" : "") + "><span>" + T.especes[k] + "</span></label>";
    }).join("");
    zone.innerHTML = '<form class="coach-form"><div><label for="c-nom">' + T.nom + '</label><input id="c-nom" type="text" maxlength="20" autocomplete="off" placeholder="' + T.nomPh + '" required></div>' +
      '<div><span class="coach-label">' + T.espece + '</span><div class="choix-espece coach-especes" role="radiogroup" aria-label="' + T.espece + '">' + boutons + "</div></div>" +
      '<button class="btn" type="submit">' + T.go + "</button></form>";
    zone.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var nom = zone.querySelector("#c-nom").value.trim();
      if (!nom) return;
      etat = { nom: nom, espece: zone.querySelector("input[name=c-espece]:checked").value, points: {}, jours: {} };
      ecrire(); tableau();
    });
  }

  function chiffres() {
    return '<div class="coach-chiffres"><div><strong>🔥 ' + serie() + "</strong><span>" + T.serie[+(serie() > 1)] + "</span></div><div><strong>" + total() + "</strong><span>" + T.seances[+(total() > 1)] +
      "</span></div><div><strong>⭐ " + nbAcquis() + "/" + exos().length + "</strong><span>" + T.acquis + "</span></div></div>";
  }
  function semaine() {
    var j = etat.jours || {}, h = "";
    for (var i = 6; i >= 0; i--) {
      var d = jourMoins(i);
      h += '<span class="' + (j[cle(d)] ? "ok" : "") + (i === 0 ? " auj" : "") + '">' + T.semaine[(d.getDay() + 6) % 7] + "</span>";
    }
    return '<div class="coach-semaine" aria-hidden="true">' + h + "</div>";
  }
  function parcours() {
    var premierLibre = true;
    var items = exos().map(function (x) {
      var p = Math.min(points(x[0]), ACQUIS), etatExo = p >= ACQUIS ? "acquis" : premierLibre ? "encours" : "attente";
      if (p < ACQUIS) premierLibre = false;
      var pastilles = ""; for (var i = 0; i < ACQUIS; i++) pastilles += "<i" + (i < p ? ' class="on"' : "") + "></i>";
      return '<li class="' + etatExo + '"><span>' + (etatExo === "acquis" ? "⭐" : etatExo === "encours" ? "▶" : "•") + " " + esc(x[2][lang][0]) + '</span><span class="coach-pastilles">' + pastilles + "</span></li>";
    }).join("");
    return "<h3>" + esc(txt(T.parcours, { n: etat.nom })) + '</h3><ol class="coach-parcours">' + items + "</ol>";
  }
  function pied() {
    return parcours() + '<button type="button" class="quiz-retour coach-raz">' + T.changer + "</button>";
  }
  function brancherPied() {
    zone.querySelector(".coach-raz").addEventListener("click", function () {
      if (!confirm(T.effacer)) return;
      arreter(); etat = {}; try { localStorage.removeItem(CLE); } catch (e) {}
      decalage = 0; bonus = false; accueil();
    });
  }

  function mmss(s) { return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function arreter() { if (minuteur) { clearInterval(minuteur); minuteur = null; } }
  function bip() {
    try {
      var C = window.AudioContext || window.webkitAudioContext, ctx = new C(), o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = 880; g.gain.value = 0.15; o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.5);
      o.onended = function () { ctx.close(); };
    } catch (e) {}
    if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
  }

  function tableau() {
    arreter(); reste = DUREE;
    var faitAuj = (etat.jours || {})[cle(jourMoins(0))];
    if (faitAuj && !bonus) return repos();
    var x = courant(), d = x[2][lang], revision = points(x[0]) >= ACQUIS;
    zone.innerHTML = '<p class="quiz-etape">' + esc(txt(bonus ? T.bonus : T.jour, { n: etat.nom })) + "</p>" + chiffres() + semaine() +
      '<div class="coach-seance">' + (revision ? '<span class="tag green">' + T.revision + "</span>" : "") + "<h2>" + esc(d[0]) + "</h2>" +
      "<p><strong>" + T.but + " :</strong> " + esc(d[1]) + "</p><ol><li>" + esc(d[2]) + "</li><li>" + esc(d[3]) + "</li><li>" + esc(d[4]) + "</li></ol>" +
      '<p class="coach-astuce"><strong>💡 ' + T.astuce + " :</strong> " + esc(d[5]) + '</p><p><a href="' + x[1] + '">' + T.guide + " →</a></p></div>" +
      '<div class="coach-minuteur"><div class="coach-temps" role="timer" aria-live="off">' + mmss(DUREE) + '</div><div class="quiz-barre"><i style="width:0%"></i></div>' +
      '<p class="coach-fin" aria-live="polite" hidden>' + T.temps + "</p>" +
      '<div class="btn-row"><button type="button" class="btn coach-go">' + T.demarrer + '</button><button type="button" class="btn btn-outline coach-fini">' + T.fini + "</button></div></div>" +
      '<button type="button" class="quiz-retour coach-autre">' + T.autre + "</button>" + pied();
    var temps = zone.querySelector(".coach-temps"), barre = zone.querySelector(".coach-minuteur .quiz-barre i"), go = zone.querySelector(".coach-go");
    function tic() {
      reste = Math.max(0, Math.round((finA - Date.now()) / 1000));
      temps.textContent = mmss(reste); barre.style.width = ((DUREE - reste) / DUREE * 100) + "%";
      if (!reste) { arreter(); go.hidden = true; zone.querySelector(".coach-fin").hidden = false; bip(); }
    }
    go.addEventListener("click", function () {
      if (minuteur) { arreter(); go.textContent = T.reprendre; return; }
      finA = Date.now() + reste * 1000; minuteur = setInterval(tic, 250); go.textContent = T.pause;
    });
    zone.querySelector(".coach-fini").addEventListener("click", function () { arreter(); noter(x); });
    zone.querySelector(".coach-autre").addEventListener("click", function () { decalage++; tableau(); });
    brancherPied();
  }

  function noter(x) {
    zone.innerHTML = "<h2>" + T.comment + '</h2><div class="quiz-options">' +
      T.notes.map(function (n, i) { return '<button type="button" class="quiz-choix" data-v="' + i + '">' + n + "</button>"; }).join("") + "</div>";
    zone.querySelectorAll(".quiz-choix").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = +b.getAttribute("data-v"), avant = points(x[0]), k = cle(jourMoins(0));
        etat.points = etat.points || {}; etat.jours = etat.jours || {};
        etat.points[x[0]] = avant + v;                       // difficile 0, ça progresse 1, facile 2
        etat.jours[k] = (etat.jours[k] || 0) + 1;
        ecrire(); decalage = 0; bonus = false;
        repos(txt(T.msg[v], { n: esc(etat.nom) }), avant < ACQUIS && avant + v >= ACQUIS ? txt(T.nouveau, { t: esc(x[2][lang][0]) }) : "");
      });
    });
    bloc.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function repos(message, etoile) {
    var fini = nbAcquis() === exos().length;
    zone.innerHTML = '<p class="quiz-etape">' + esc(etat.nom) + "</p><h2>🎉 " + T.bravo + "</h2>" +
      (etoile ? '<p class="coach-etoile">' + etoile + "</p>" : "") + (message ? "<p>" + message + "</p>" : "") +
      chiffres() + semaine() + "<p>" + (fini ? T.tout : T.demain) + "</p>" +
      '<div class="btn-row"><button type="button" class="btn btn-sm coach-partager">' + T.partager + '</button><button type="button" class="btn btn-sm btn-outline coach-bonus">' + T.encore + "</button></div>" + pied();
    zone.querySelector(".coach-bonus").addEventListener("click", function () { bonus = true; tableau(); });
    zone.querySelector(".coach-partager").addEventListener("click", function () {
      var texte = txt(T.partage, { n: etat.nom, s: serie() }), b = this;
      if (navigator.share) navigator.share({ text: texte, url: location.href }).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(texte + " " + location.href).then(function () { b.textContent = "✓"; });
    });
    brancherPied();
  }

  if (etat.nom) tableau(); else accueil();
})();
