"""Questions fréquentes ajoutées aux articles français (idempotent, marqueurs <!-- faq -->).

Usage : python3 tools/pages/faq_articles.py
Chaque bloc est inséré avant l'encadré « À retenir » de l'article, avec ses données structurées FAQPage.
Réponses courtes, prudentes, sans chiffre inventé ; renvoi au vétérinaire pour la santé.
"""
import html
import json
import pathlib
import re

DOCS = pathlib.Path(__file__).resolve().parent.parent.parent / "docs"

FAQ = {
"chiot-mord": [
 ("À quel âge un chiot arrête-t-il de mordre ?", "Le mordillement diminue en général nettement après la poussée des dents définitives, vers la fin de la période chiot. Mais il ne disparaît pas tout seul : c'est votre réaction (rediriger vers un jouet, faire une pause) qui lui apprend à contrôler sa bouche."),
 ("Est-ce normal qu'un chiot morde autant ?", "Oui. Le chiot explore le monde avec sa bouche, joue et soulage ses gencives. C'est un comportement normal, qu'il faut guider plutôt que punir."),
 ("Faut-il crier « aïe » quand il mord ?", "Un petit « aïe » calme suivi d'une pause dans le jeu peut aider certains chiots. S'il s'excite davantage, contentez-vous d'arrêter le jeu quelques secondes et proposez-lui un jouet à mâcher."),
 ("Quand faut-il s'inquiéter ?", "Si les morsures s'accompagnent de grognements de peur, de raideur, ou surviennent quand on le manipule ou près de sa gamelle, parlez-en à votre vétérinaire, qui pourra vous orienter vers un professionnel du comportement."),
],
"proprete-chiot": [
 ("À quel âge un chiot est-il propre ?", "Cela varie beaucoup d'un chiot à l'autre. La plupart progressent vite avec des sorties fréquentes et des récompenses, mais il est normal d'avoir encore quelques accidents pendant plusieurs semaines, surtout la nuit."),
 ("Combien de fois faut-il sortir un chiot ?", "Au réveil, après chaque repas, après le jeu ou une sieste, toutes les 1 à 2 heures en journée au début, et juste avant le coucher. Plus vous anticipez, moins il y a d'accidents."),
 ("Faut-il utiliser des tapis éducateurs ?", "Ils peuvent dépanner, mais ils apprennent au chiot qu'il peut faire à l'intérieur. Mieux vaut privilégier les sorties dès que possible."),
 ("Mon chiot était propre et refait dans la maison : pourquoi ?", "Un changement (stress, nouvelle maison) ou un problème de santé, comme une infection urinaire, peut en être la cause. Une malpropreté soudaine justifie un avis vétérinaire."),
],
"rappel-chien": [
 ("À quel âge apprendre le rappel ?", "Dès l'arrivée du chiot, à la maison, avec des récompenses. Plus on commence tôt, plus le rappel devient un réflexe agréable."),
 ("Pourquoi mon chien ne revient-il pas quand je l'appelle ?", "Souvent parce que revenir lui a déjà valu quelque chose de désagréable (la fin du jeu, la laisse, une gronderie), ou parce que l'environnement est plus intéressant que vous. Rendez le retour toujours très agréable."),
 ("Faut-il utiliser un sifflet ?", "C'est possible : un sifflet porte loin et garde toujours le même son. Il s'apprend comme un mot de rappel, en l'associant à une super récompense."),
 ("Quand peut-on lâcher son chien ?", "Quand le rappel fonctionne de façon fiable avec une longe, dans des environnements variés, et seulement dans des lieux où c'est autorisé et sûr."),
],
"marche-en-laisse": [
 ("Pourquoi mon chien tire-t-il en laisse ?", "Parce qu'il va plus vite que nous, que tout l'intéresse, et que tirer lui a souvent permis d'avancer. Il faut lui apprendre que la laisse détendue est ce qui le fait avancer."),
 ("Harnais ou collier pour un chien qui tire ?", "Un harnais bien ajusté (en Y, qui dégage les épaules) évite les pressions sur la gorge. Il ne règle pas le problème seul, mais il rend l'apprentissage plus confortable."),
 ("Combien de temps pour qu'il arrête de tirer ?", "Cela dépend du chien et de la régularité des séances. Les progrès viennent avec des séances courtes et une règle identique pour toute la famille."),
 ("Les colliers anti-traction sont-ils une bonne idée ?", "Nous déconseillons les colliers étrangleurs et à pointes, qui font mal. Privilégiez un harnais confortable et l'éducation par la récompense."),
],
"chat-griffe-canape": [
 ("Pourquoi mon chat griffe-t-il le canapé ?", "Griffer est un besoin naturel : entretenir ses griffes, s'étirer et laisser son odeur. Le canapé est souvent placé au bon endroit et a la bonne texture."),
 ("Comment empêcher un chat de griffer le canapé ?", "Proposez un griffoir stable juste à côté, récompensez-le quand il l'utilise et rendez temporairement le canapé moins attirant (plaid, protection). Ne le punissez pas."),
 ("Quel griffoir préfère un chat ?", "Beaucoup aiment un griffoir haut et stable en sisal, d'autres préfèrent griffer à l'horizontale. Observez où et comment il griffe."),
 ("Faut-il couper les griffes de son chat ?", "Les chats d'intérieur peuvent en avoir besoin. Si vous n'êtes pas à l'aise, demandez à votre vétérinaire de vous montrer. Le dégriffage chirurgical est à proscrire."),
],
"chat-urine-hors-litiere": [
 ("Pourquoi mon chat fait-il pipi sur le lit ?", "Ce n'est jamais de la vengeance. Un problème de santé, un bac qui ne lui convient pas ou un stress peuvent l'expliquer. Le lit, qui porte votre odeur, le rassure."),
 ("Est-ce une urgence ?", "Oui si votre chat va au bac sans réussir à uriner, pousse ou a du sang dans les urines : appelez votre vétérinaire le jour même, surtout pour un mâle."),
 ("Comment enlever l'odeur d'urine de chat ?", "Avec un nettoyant enzymatique, qui détruit les molécules odorantes. Évitez l'eau de Javel et l'ammoniaque, dont l'odeur rappelle l'urine."),
 ("La stérilisation aide-t-elle ?", "Elle réduit nettement le marquage urinaire chez beaucoup de chats. Parlez-en à votre vétérinaire."),
],
"chat-miaule-la-nuit": [
 ("Pourquoi mon chat miaule-t-il la nuit ?", "Faim, ennui, besoin d'attention, chaleurs ou, chez le chat âgé, un problème de santé. Son rythme naturel le rend aussi plus actif à l'aube."),
 ("Faut-il lui répondre ?", "Non, s'il est en bonne santé : répondre (même pour gronder) lui apprend que miauler fonctionne. Récompensez-le plutôt le matin quand il est calme."),
 ("Un chat âgé qui miaule la nuit, est-ce grave ?", "Ce peut être le signe d'un problème de santé ou d'un déclin cognitif. Un changement soudain chez un chat âgé justifie une visite chez le vétérinaire."),
 ("Le distributeur programmable, ça marche ?", "Souvent, oui : le petit-déjeuner n'est plus servi par vous, donc il cesse peu à peu de vous réveiller pour manger."),
],
"chien-aboie-seul": [
 ("Pourquoi mon chien aboie-t-il quand je pars ?", "Ennui, réactions aux bruits extérieurs, manque d'apprentissage de la solitude ou véritable détresse liée à la séparation. Filmer vos départs aide à comprendre la cause."),
 ("Combien de temps un chien peut-il rester seul ?", "Cela dépend de son âge, de son apprentissage et de ses besoins. Un chiot ou un chien qui n'a pas appris la solitude doit commencer par des absences très courtes."),
 ("Le collier anti-aboiement est-il une solution ?", "Non : il punit le symptôme sans régler la cause et peut aggraver l'anxiété. Nous le déconseillons."),
 ("Prendre un deuxième chien peut-il aider ?", "Pas forcément : un chien en détresse lorsqu'il est séparé de vous peut le rester même avec un congénère. Travaillez d'abord la solitude, avec l'aide d'un professionnel si besoin."),
],
"apprendre-assis-couche-pas-bouger": [
 ("À quel âge apprendre « assis » à un chiot ?", "Dès son arrivée, avec des séances d'une ou deux minutes. Les chiots apprennent très vite avec des friandises."),
 ("Combien de temps pour apprendre « assis » ?", "Souvent quelques séances pour la position elle-même. Le rendre fiable partout (dehors, avec des distractions) prend plus de temps."),
 ("Mon chien refuse de se coucher : que faire ?", "Récompensez chaque petite étape vers le sol, travaillez sur un tapis confortable et évitez les sols froids ou glissants. S'il semble gêné, consultez votre vétérinaire."),
 ("Faut-il toujours donner une friandise ?", "Au début, oui. Ensuite, alternez avec d'autres récompenses (caresse, jeu, permission d'aller renifler) tout en gardant des friandises de temps en temps."),
],
"kit-accueil-chiot": [
 ("Que faut-il acheter avant l'arrivée d'un chiot ?", "Un couchage, deux gamelles, la même alimentation qu'avant son arrivée, un harnais léger avec une laisse, des jouets à mâcher, un nettoyant enzymatique et une médaille."),
 ("Faut-il une caisse de transport ou un parc ?", "Un parc ou une barrière aide à sécuriser un espace pendant que vous ne pouvez pas le surveiller. Une caisse doit toujours être introduite en douceur, jamais comme une punition."),
 ("Quelles croquettes donner à un chiot ?", "Gardez d'abord celles de l'éleveur ou du refuge, puis changez progressivement si besoin, avec les conseils de votre vétérinaire."),
 ("Quand faire la première visite chez le vétérinaire ?", "Dans les premiers jours suivant son arrivée, pour un bilan, le suivi des vaccins et des conseils adaptés."),
],
"meilleur-harnais-chien": [
 ("Harnais ou collier : que choisir ?", "Pour la balade, un harnais bien ajusté évite les pressions sur la gorge. Le collier peut porter la médaille d'identification."),
 ("Comment savoir si le harnais est bien ajusté ?", "On doit pouvoir glisser deux doigts sous les sangles, et le harnais ne doit pas gêner le mouvement des épaules ni frotter sous les pattes avant."),
 ("Les harnais anti-traction sont-ils efficaces ?", "Ils peuvent aider à court terme, mais certains modèles gênent la marche. L'éducation à la laisse détendue reste indispensable."),
 ("Quelle taille choisir pour un chiot ?", "Un modèle réglable, à vérifier souvent pendant sa croissance."),
],
"meilleur-griffoir-chat": [
 ("Où placer le griffoir ?", "Près de l'endroit qu'il griffe déjà, près de son couchage ou d'un lieu de passage. Les chats griffent souvent au réveil."),
 ("Combien de griffoirs faut-il ?", "Au moins un par étage, plus dans une maison à plusieurs chats, avec des modèles verticaux et horizontaux."),
 ("Mon chat n'utilise pas son griffoir : pourquoi ?", "Il est peut-être instable, trop petit, mal placé ou d'une texture qu'il n'aime pas. Essayez un autre emplacement ou un autre type."),
 ("Comment l'attirer vers le griffoir ?", "Jouez avec une canne à plumes autour, récompensez-le quand il l'utilise. L'herbe à chat attire certains chats."),
],
"meilleur-clicker": [
 ("À quoi sert un clicker ?", "Il marque l'instant exact où l'animal fait le bon geste, juste avant la récompense. L'apprentissage devient plus précis et plus rapide."),
 ("Le clicker marche-t-il avec un chat ?", "Oui, très bien, avec des séances très courtes et des récompenses appétissantes."),
 ("Faut-il cliquer toute la vie ?", "Non : on l'utilise pour apprendre de nouveaux comportements, puis on passe à des mots et à d'autres récompenses."),
 ("Mon animal a peur du bruit du clicker : que faire ?", "Choisissez un clicker à volume réglable, cliquez dans votre poche ou utilisez un mot bref comme « oui ! »."),
],
"meilleure-litiere-chat": [
 ("Quelle litière préfèrent les chats ?", "Beaucoup préfèrent une litière fine, douce sous les pattes et sans parfum, proche du sable."),
 ("Tous les combien changer la litière ?", "Retirez les selles et les boules d'urine chaque jour et changez entièrement la litière régulièrement, selon le type de litière et le nombre de chats."),
 ("Litière parfumée : bonne ou mauvaise idée ?", "Plutôt mauvaise : l'odorat du chat est très sensible et un parfum fort peut le faire fuir son bac."),
 ("Comment changer de litière ?", "Progressivement, en mélangeant l'ancienne et la nouvelle, ou en proposant un deuxième bac à côté."),
],
"meilleurs-jouets-occupation-chien": [
 ("Quel jouet laisser à un chien seul ?", "Un jouet à garnir en caoutchouc robuste, adapté à sa taille et à sa force, est souvent le plus sûr."),
 ("Comment remplir un jouet à garnir ?", "Avec une partie de sa ration (croquettes trempées, pâtée). Le congeler le rend plus long à vider."),
 ("Les jouets d'occupation suffisent-ils pour un chien qui s'ennuie ?", "Non : ils complètent les balades, le flair et les jeux avec vous, sans les remplacer."),
 ("Quels jouets éviter quand il est seul ?", "Les peluches, les jouets à couiner, les cordes effilochées et tout ce qui est plus petit que sa gueule."),
],
"meilleure-camera-animaux": [
 ("Une caméra peut-elle aider un chien qui aboie seul ?", "Elle aide à comprendre quand et pourquoi il aboie, et à suivre ses progrès pendant l'apprentissage de la solitude."),
 ("Faut-il un abonnement ?", "Pas toujours : beaucoup de caméras enregistrent sur carte microSD. Vérifiez les fonctions gratuites avant d'acheter."),
 ("Est-ce une bonne idée de parler à son chien via la caméra ?", "À tester avec prudence : certains chiens sont troublés d'entendre votre voix sans vous voir."),
 ("Où placer la caméra ?", "En hauteur, face à l'endroit où il se repose ou à la porte, avec les câbles hors de portée."),
],
"meilleures-friandises-education-chien": [
 ("Quelle taille pour une friandise d'éducation ?", "Toute petite, de la taille d'un petit pois, pour pouvoir en donner beaucoup sans le rassasier."),
 ("Combien de friandises par jour ?", "Les vétérinaires conseillent généralement que les friandises ne dépassent pas environ 10&nbsp;% de ce qu'il mange dans la journée. Réduisez sa ration les jours de grosses séances."),
 ("Peut-on utiliser ses croquettes ?", "Oui, pour les exercices faciles à la maison. Dehors, une récompense plus appétissante est souvent nécessaire."),
 ("Les friandises maison sont-elles une bonne idée ?", "Du blanc de poulet cuit nature, en petits morceaux, est une excellente récompense. Évitez le sel, les épices et les aliments toxiques."),
],
"meilleure-pochette-friandises": [
 ("Pourquoi utiliser une pochette à friandises ?", "Pour récompenser au bon moment, d'une main, sans fouiller dans vos poches : c'est ce qui rend l'apprentissage clair."),
 ("Quelle pochette pour débuter ?", "Une pochette à clip ou à ceinture qui s'ouvre et se ferme d'une main et se lave facilement."),
 ("Comment la nettoyer ?", "Videz-la après chaque séance et lavez-la régulièrement. Les modèles en silicone se nettoient le plus facilement."),
 ("Pochette ou sac banane ?", "La pochette suffit pour la plupart des balades. Le sac banane est pratique si vous portez aussi vos clés, votre téléphone et des sacs."),
],
"black-friday-animaux": [
 ("Quand a lieu le Black Friday 2026 ?", "Le vendredi 27 novembre 2026. Beaucoup d'offres commencent quelques jours avant et se prolongent jusqu'au lundi suivant."),
 ("Que vaut-il la peine d'acheter ?", "Le matériel durable que vous auriez acheté de toute façon : harnais, griffoir, jouets d'occupation, caméra, fontaine."),
 ("Comment repérer une vraie promotion ?", "Comparez avec le prix habituel sur plusieurs jours : un prix barré n'est pas toujours une vraie baisse."),
 ("Faut-il faire des stocks de croquettes ?", "Seulement si vous restez sur la même alimentation et si la date de conservation le permet. Ne changez pas d'alimentation brutalement pour une promotion."),
],
"idees-cadeaux-noel-chien-chat": [
 ("Quel cadeau pour un chien qui a déjà tout ?", "Un jouet d'occupation, un jeu de flair ou… du temps : une belle balade où il peut renifler à son rythme."),
 ("Quel cadeau pour un chat ?", "Une canne à plumes, un griffoir ou un arbre à chat, un jeu d'intelligence, ou un coin douillet en hauteur."),
 ("Quels dangers à Noël pour les animaux ?", "Le chocolat, les décorations avalées, les guirlandes électriques mâchouillées, certaines plantes et les restes de repas gras ou salés."),
 ("Peut-on offrir un animal à Noël ?", "Adopter est un engagement de plusieurs années : il vaut mieux préparer l'adoption en famille, plutôt que d'en faire une surprise."),
],
}


def bloc(qr):
    items = "".join(f"        <h3>{q}</h3>\n        <p>{r}</p>\n" for q, r in qr)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(r)}} for q, r in qr]}
    return (f'<!-- faq --><h2>Questions fréquentes</h2>\n{items}'
            f'        <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><!-- /faq -->\n\n        ')


if __name__ == "__main__":
    n = 0
    for slug, qr in FAQ.items():
        p = DOCS / f"{slug}.html"
        s = p.read_text(encoding="utf-8")
        b = bloc(qr)
        if "<!-- faq -->" in s:
            s = re.sub(r"<!-- faq -->.*?<!-- /faq -->\n\n        ", lambda _: b, s, flags=re.S)
        else:
            i = s.find('<div class="callout"><strong>À retenir')
            if i == -1:
                i = s.find("<p>Pour aller plus loin")
            if i == -1:
                raise SystemExit(f"Repère introuvable dans {slug}")
            s = s[:i] + b + s[i:]
        p.write_text(s, encoding="utf-8")
        n += 1
    print(n, "articles enrichis")
