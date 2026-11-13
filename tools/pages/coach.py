"""Page « Coach 5 minutes » : une séance d'éducation par jour, avec minuteur et progression (FR / EN / IT).

Usage : python3 tools/pages/coach.py
Les exercices et les textes de l'outil sont dans docs/js/coach.js ; cette page porte le texte d'explication.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

SLUG = "coach-5-minutes"

T = {
    "fr": {
        "titre": "Coach 5 minutes : la séance du jour de votre animal",
        "desc": "Chaque jour, un exercice d'éducation de 5 minutes pour votre chien, chat, lapin ou oiseau : étapes, minuteur et suivi des progrès. Gratuit, sans inscription.",
        "home": "Accueil", "fil": "Coach 5 minutes", "menu": "⏱️ Coach 5 minutes",
        "h1": "⏱️ Coach 5 minutes : la séance du jour",
        "lead": "Un exercice par jour, expliqué en 3 étapes, avec un minuteur. Votre animal progresse, vous gardez le rythme.",
        "alt": "Une personne récompense son chien qui vient de s'asseoir", "legende": "Cinq minutes par jour suffisent pour progresser.",
        "noscript": 'Ce coach nécessite JavaScript. Consultez <a href="methodes.html">toutes les méthodes</a>.',
        "sections": [
            ("Comment ça marche ?", """<ol>
          <li><strong>Indiquez le nom et l'espèce de votre animal.</strong> Le coach prépare un parcours adapté : 8 exercices pour le chien, 6 pour le chat, 5 pour le lapin et 5 pour l'oiseau.</li>
          <li><strong>Faites la séance du jour.</strong> Un seul exercice, 3 étapes, une astuce. Lancez le minuteur de 5 minutes et arrêtez-vous quand il sonne.</li>
          <li><strong>Dites comment ça s'est passé.</strong> Facile : l'exercice avance vite. Difficile : le coach le repropose, sans pression.</li>
          <li><strong>Revenez demain.</strong> Un exercice est « acquis » après plusieurs séances réussies ; le suivant se débloque alors.</li>
        </ol>"""),
            ("Pourquoi seulement 5 minutes ?", """<p>Un animal apprend mieux en séances courtes et fréquentes qu'en longues séances occasionnelles : son attention baisse vite, et il vaut mieux s'arrêter sur une réussite que sur de la lassitude. Cinq minutes, c'est aussi une durée que l'on tient vraiment tous les jours, même en semaine. La série de jours affichée par le coach est là pour ça : vous aider à garder le rythme.</p>
        <p>Toutes les séances reposent sur le <a href="methodes.html#renforcement-positif">renforcement positif</a> : on récompense ce que l'animal fait bien, on ne punit pas. Si un exercice bloque, c'est qu'il est trop difficile pour l'instant : on le simplifie.</p>"""),
            ("Vos données restent sur votre appareil", """<p>Pas de compte, pas d'e-mail : le nom de votre animal et sa progression sont enregistrés uniquement dans votre navigateur. Si vous changez d'appareil ou effacez les données du site, la progression repart de zéro.</p>"""),
            ("Pour aller plus loin", """<ul>
          <li><a href="quiz.html">🧩 Quiz : quelle méthode pour votre animal ?</a></li>
          <li><a href="programme-chiot-30-jours.html">🐶 Programme chiot 30 jours</a></li>
          <li><a href="clicker-training-debutant.html">Le clicker training pour débuter</a></li>
          <li><a href="fiches-gratuites.html">🖨️ Fiches à imprimer</a></li>
        </ul>
        <p>Le coach propose des exercices d'éducation de base. Pour une peur intense, de l'agressivité ou un changement soudain de comportement, consultez d'abord un vétérinaire.</p>"""),
        ],
        "carte": ("Coach 5 minutes", "Chaque jour, une séance guidée avec minuteur et suivi des progrès."),
    },
    "en": {
        "titre": "5-Minute Coach: your pet's training session of the day",
        "desc": "Every day, a 5-minute training exercise for your dog, cat, rabbit or bird: steps, timer, daily streak and progress tracking. Free, no sign-up.",
        "home": "Home", "fil": "5-Minute Coach", "menu": "⏱️ 5-Minute Coach",
        "h1": "⏱️ 5-Minute Coach: the session of the day",
        "lead": "One exercise a day, explained in 3 steps, with a timer. Your pet makes progress, you keep the habit.",
        "alt": "A person rewards their dog who has just sat down", "legende": "Five minutes a day is enough to make progress.",
        "noscript": 'This coach needs JavaScript. See <a href="methodes.html">all the methods</a>.',
        "sections": [
            ("How does it work?", """<ol>
          <li><strong>Enter your pet's name and species.</strong> The coach prepares a suitable path: 8 exercises for dogs, 6 for cats, 5 for rabbits and 5 for birds.</li>
          <li><strong>Do the session of the day.</strong> One exercise, 3 steps, one tip. Start the 5-minute timer and stop when it rings.</li>
          <li><strong>Say how it went.</strong> Easy: the exercise moves on quickly. Hard: the coach offers it again, with no pressure.</li>
          <li><strong>Come back tomorrow.</strong> An exercise is “learned” after several successful sessions; the next one then unlocks.</li>
        </ol>"""),
            ("Why only 5 minutes?", """<p>Pets learn better in short, frequent sessions than in long, occasional ones: their attention drops quickly, and it is better to stop on a success than on boredom. Five minutes is also something you can really do every day, even on weekdays. That is what the daily streak is for: helping you keep the habit.</p>
        <p>Every session relies on <a href="methodes.html#renforcement-positif">positive reinforcement</a>: we reward what the animal does well and we do not punish. If an exercise stalls, it is too hard for now: make it simpler.</p>"""),
            ("Your data stays on your device", """<p>No account, no email: your pet's name and progress are stored only in your browser. If you change device or clear the site's data, progress starts again from zero.</p>"""),
            ("Going further", """<ul>
          <li><a href="quiz.html">🧩 Quiz: which method for your pet?</a></li>
          <li><a href="programme-chiot-30-jours.html">🐶 30-day puppy programme</a></li>
          <li><a href="clicker-training-debutant.html">Clicker training for beginners</a></li>
          <li><a href="methodes.html">All the training methods</a></li>
        </ul>
        <p>The coach offers basic training exercises. For intense fear, aggression or a sudden change in behaviour, see a vet first.</p>"""),
        ],
        "carte": ("5-Minute Coach", "Every day, a guided session with a timer and progress tracking."),
    },
    "it": {
        "titre": "Coach 5 minuti: la sessione di oggi del tuo animale",
        "desc": "Ogni giorno un esercizio di educazione di 5 minuti per cane, gatto, coniglio o uccello: passaggi, timer e progressi. Gratis, senza registrazione.",
        "home": "Home", "fil": "Coach 5 minuti", "menu": "⏱️ Coach 5 minuti",
        "h1": "⏱️ Coach 5 minuti: la sessione di oggi",
        "lead": "Un esercizio al giorno, spiegato in 3 passaggi, con un timer. Il tuo animale migliora, tu mantieni il ritmo.",
        "alt": "Una persona premia il cane che si è appena seduto", "legende": "Bastano cinque minuti al giorno per fare progressi.",
        "noscript": 'Questo coach richiede JavaScript. Consulta <a href="methodes.html">tutti i metodi</a>.',
        "sections": [
            ("Come funziona?", """<ol>
          <li><strong>Indica il nome e la specie del tuo animale.</strong> Il coach prepara un percorso adatto: 8 esercizi per il cane, 6 per il gatto, 5 per il coniglio e 5 per l'uccello.</li>
          <li><strong>Fai la sessione di oggi.</strong> Un solo esercizio, 3 passaggi, un consiglio. Avvia il timer di 5 minuti e fermati quando suona.</li>
          <li><strong>Di' com'è andata.</strong> Facile: l'esercizio avanza in fretta. Difficile: il coach lo ripropone, senza pressione.</li>
          <li><strong>Torna domani.</strong> Un esercizio è «imparato» dopo alcune sessioni riuscite; allora si sblocca il successivo.</li>
        </ol>"""),
            ("Perché solo 5 minuti?", """<p>Un animale impara meglio con sessioni brevi e frequenti che con sessioni lunghe e occasionali: l'attenzione cala in fretta, ed è meglio fermarsi su un successo che sulla noia. Cinque minuti sono anche una durata che si riesce davvero a mantenere ogni giorno. La serie di giorni mostrata dal coach serve a questo: aiutarti a tenere il ritmo.</p>
        <p>Tutte le sessioni si basano sul <a href="methodes.html#renforcement-positif">rinforzo positivo</a>: si premia ciò che l'animale fa bene, non si punisce. Se un esercizio si blocca, per ora è troppo difficile: va semplificato.</p>"""),
            ("I tuoi dati restano sul tuo dispositivo", """<p>Nessun account, nessuna e-mail: il nome del tuo animale e i suoi progressi sono salvati solo nel tuo browser. Se cambi dispositivo o cancelli i dati del sito, i progressi ripartono da zero.</p>"""),
            ("Per approfondire", """<ul>
          <li><a href="quiz.html">🧩 Quiz: quale metodo per il tuo animale?</a></li>
          <li><a href="programme-chiot-30-jours.html">🐶 Programma cucciolo 30 giorni</a></li>
          <li><a href="clicker-training-debutant.html">Il clicker training per iniziare</a></li>
          <li><a href="methodes.html">Tutti i metodi di educazione</a></li>
        </ul>
        <p>Il coach propone esercizi di educazione di base. In caso di paura intensa, aggressività o un cambiamento improvviso del comportamento, consulta prima un veterinario.</p>"""),
        ],
        "carte": ("Coach 5 minuti", "Ogni giorno una sessione guidata con timer e progressi."),
    },
}


def corps(code):
    t = T[code]
    img = ("" if code == "fr" else "../") + "img/illu/assis-leurre.svg"
    sections = "".join(f"        <h2>{h}</h2>\n        {c}\n" for h, c in t["sections"])
    return f"""    <section class="page-hero">
      <div class="container outil">
        <p class="breadcrumb"><a href="index.html">{t["home"]}</a> › {t["fil"]}</p>
        <h1>{t["h1"]}</h1>
        <p class="lead">{t["lead"]}</p>
        <div class="card" id="coach"><div class="coach-zone"><noscript>{t["noscript"]}</noscript></div></div>
        <figure class="illu" data-illu="assis-leurre"><img src="{img}" alt="{t["alt"]}" width="1200" height="460" loading="lazy" decoding="async"><figcaption>{t["legende"]}</figcaption></figure>
{sections}      </div>
    </section>"""


def carte_accueil(code):
    """Carte sur la page d'accueil, juste avant « Quel animal pour moi ? »."""
    p = creer_page.dossier(code) / "index.html"
    s = p.read_text(encoding="utf-8")
    if f'href="{SLUG}.html"><span class="icon">' in s:
        return
    titre, texte = T[code]["carte"]
    carte = f'<a class="card card-link" href="{SLUG}.html"><span class="icon">⏱️</span><h3>{titre}</h3><p>{texte}</p></a>'
    s2 = re.sub(r'([ \t]*)(<a class="card card-link" href="quel-animal\.html">)', lambda m: m.group(1) + carte + "\n" + m.group(1) + m.group(2), s, count=1)
    assert s2 != s, f"carte d'accueil non insérée ({code})"
    p.write_text(s2, encoding="utf-8")


if __name__ == "__main__":
    for code in ("fr", "en", "it"):
        t = T[code]
        creer_page.creer(code, SLUG, t["titre"], t["desc"], corps(code), scripts=["js/coach.js"], menu=t["menu"])
        carte_accueil(code)
    creer_page.finir()
