"""Page « Mon chien ou mon chat peut-il manger… ? » (fr, en, it).

Usage : python3 tools/pages/aliments.py
Chaque aliment : emoji, noms, verdict chien, verdict chat (oui / modere / non) et explication courte.
Contenu volontairement prudent, d'après les listes d'aliments toxiques de référence (ASPCA Animal Poison
Control Center, associations vétérinaires) : en cas de doute, le verdict le plus prudent est retenu.
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import creer_page  # noqa: E402

# (id, emoji, {fr, en, it}, chien, chat, {fr, en, it})
A = [
 ("chocolat", "🍫", {"fr": "Chocolat", "en": "Chocolate", "it": "Cioccolato"}, "non", "non",
  {"fr": "Toxique : il contient de la théobromine. Plus il est noir, plus il est dangereux.",
   "en": "Toxic: it contains theobromine. The darker it is, the more dangerous.",
   "it": "Tossico: contiene teobromina. Più è fondente, più è pericoloso."}),
 ("raisin", "🍇", {"fr": "Raisin et raisins secs", "en": "Grapes and raisins", "it": "Uva e uvetta"}, "non", "non",
  {"fr": "Peut provoquer une atteinte grave des reins chez le chien, même en petite quantité. À éviter aussi chez le chat.",
   "en": "Can cause serious kidney damage in dogs, even in small amounts. Avoid for cats too.",
   "it": "Può causare gravi danni ai reni del cane, anche in piccole quantità. Da evitare anche per il gatto."}),
 ("oignon", "🧅", {"fr": "Oignon, échalote, poireau", "en": "Onion, shallot, leek", "it": "Cipolla, scalogno, porro"}, "non", "non",
  {"fr": "Toxique cru, cuit ou en poudre (soupes, sauces) : abîme les globules rouges. Le chat y est encore plus sensible.",
   "en": "Toxic raw, cooked or powdered (soups, sauces): damages red blood cells. Cats are even more sensitive.",
   "it": "Tossico crudo, cotto o in polvere (zuppe, sughi): danneggia i globuli rossi. Il gatto è ancora più sensibile."}),
 ("ail", "🧄", {"fr": "Ail et ciboulette", "en": "Garlic and chives", "it": "Aglio ed erba cipollina"}, "non", "non",
  {"fr": "Même famille que l'oignon, même danger pour le sang.",
   "en": "Same family as onion, same danger for the blood.",
   "it": "Stessa famiglia della cipolla, stesso pericolo per il sangue."}),
 ("xylitol", "🍬", {"fr": "Xylitol (chewing-gums, bonbons « sans sucre »)", "en": "Xylitol (gum, \"sugar-free\" sweets)", "it": "Xilitolo (gomme, caramelle «senza zucchero»)"}, "non", "non",
  {"fr": "Très dangereux pour le chien (chute du sucre dans le sang, foie). Vérifiez les étiquettes, y compris du beurre de cacahuète.",
   "en": "Very dangerous for dogs (blood sugar crash, liver). Check labels, including peanut butter.",
   "it": "Molto pericoloso per il cane (calo degli zuccheri nel sangue, fegato). Controlla le etichette, anche del burro di arachidi."}),
 ("avocat", "🥑", {"fr": "Avocat", "en": "Avocado", "it": "Avocado"}, "non", "non",
  {"fr": "À éviter : très gras, peut irriter le tube digestif, et le noyau peut boucher l'intestin.",
   "en": "Avoid: very fatty, can upset the gut, and the stone can block the intestine.",
   "it": "Da evitare: molto grasso, può irritare l'apparato digerente e il nocciolo può ostruire l'intestino."}),
 ("cafe", "☕", {"fr": "Café, thé, boissons énergisantes", "en": "Coffee, tea, energy drinks", "it": "Caffè, tè, bevande energetiche"}, "non", "non",
  {"fr": "La caféine est toxique pour les chiens et les chats.",
   "en": "Caffeine is toxic to dogs and cats.",
   "it": "La caffeina è tossica per cani e gatti."}),
 ("alcool", "🍺", {"fr": "Alcool", "en": "Alcohol", "it": "Alcol"}, "non", "non",
  {"fr": "Toxique, même en petite quantité. Attention aussi aux desserts alcoolisés.",
   "en": "Toxic, even in small amounts. Watch out for desserts containing alcohol too.",
   "it": "Tossico anche in piccole quantità. Attenzione anche ai dolci alcolici."}),
 ("noix", "🌰", {"fr": "Noix de macadamia et autres noix", "en": "Macadamia and other nuts", "it": "Noci di macadamia e altra frutta secca"}, "non", "non",
  {"fr": "La macadamia est toxique pour le chien ; les autres noix sont très grasses et parfois moisies. À éviter.",
   "en": "Macadamia nuts are toxic to dogs; other nuts are very fatty and sometimes mouldy. Avoid.",
   "it": "La macadamia è tossica per il cane; l'altra frutta secca è molto grassa e a volte ammuffita. Da evitare."}),
 ("pate-crue", "🫓", {"fr": "Pâte crue (pain, pizza)", "en": "Raw dough (bread, pizza)", "it": "Impasto crudo (pane, pizza)"}, "non", "non",
  {"fr": "La levure continue de gonfler dans l'estomac et produit de l'alcool. Danger.",
   "en": "The yeast keeps rising in the stomach and produces alcohol. Dangerous.",
   "it": "Il lievito continua a gonfiarsi nello stomaco e produce alcol. Pericoloso."}),
 ("os-cuits", "🦴", {"fr": "Os cuits", "en": "Cooked bones", "it": "Ossa cotte"}, "non", "non",
  {"fr": "Ils se brisent en éclats qui peuvent blesser la bouche, l'estomac ou l'intestin.",
   "en": "They splinter into shards that can injure the mouth, stomach or intestine.",
   "it": "Si spezzano in schegge che possono ferire bocca, stomaco o intestino."}),
 ("charcuterie", "🥓", {"fr": "Charcuterie, gras et restes de table", "en": "Processed meats, fat and table scraps", "it": "Salumi, grasso e avanzi di tavola"}, "non", "non",
  {"fr": "Trop salés et trop gras : risque de troubles digestifs et de pancréatite.",
   "en": "Too salty and too fatty: risk of digestive upset and pancreatitis.",
   "it": "Troppo salati e troppo grassi: rischio di disturbi digestivi e pancreatite."}),
 ("noyaux", "🍑", {"fr": "Pêche, abricot, cerise", "en": "Peach, apricot, cherry", "it": "Pesca, albicocca, ciliegia"}, "modere", "modere",
  {"fr": "La chair, en petite quantité, sans noyau : les noyaux peuvent boucher l'intestin et contiennent des substances toxiques.",
   "en": "The flesh, in small amounts, without the stone: stones can block the intestine and contain toxic substances.",
   "it": "La polpa, in piccole quantità, senza nocciolo: i noccioli possono ostruire l'intestino e contengono sostanze tossiche."}),
 ("tomate", "🍅", {"fr": "Tomate", "en": "Tomato", "it": "Pomodoro"}, "modere", "non",
  {"fr": "Chien : un peu de tomate bien mûre. Jamais les parties vertes (tiges, feuilles, fruits verts). Chat : à éviter.",
   "en": "Dog: a little ripe tomato. Never the green parts (stems, leaves, unripe fruit). Cat: avoid.",
   "it": "Cane: un po' di pomodoro ben maturo. Mai le parti verdi (gambi, foglie, frutti acerbi). Gatto: da evitare."}),
 ("agrumes", "🍊", {"fr": "Orange et agrumes", "en": "Orange and citrus", "it": "Arancia e agrumi"}, "modere", "non",
  {"fr": "Chien : un ou deux quartiers sans peau ni pépins. Chat : à éviter, il n'aime pas et la peau l'irrite.",
   "en": "Dog: one or two segments without peel or seeds. Cat: avoid, they dislike it and the peel irritates them.",
   "it": "Cane: uno o due spicchi senza buccia né semi. Gatto: da evitare, non gli piace e la buccia lo irrita."}),
 ("lait", "🥛", {"fr": "Lait de vache", "en": "Cow's milk", "it": "Latte vaccino"}, "modere", "non",
  {"fr": "Beaucoup de chiens et de chats adultes digèrent mal le lactose (diarrhée). Le « bol de lait » du chat est une fausse bonne idée.",
   "en": "Many adult dogs and cats digest lactose poorly (diarrhoea). The cat's \"saucer of milk\" is a bad idea.",
   "it": "Molti cani e gatti adulti digeriscono male il lattosio (diarrea). La «ciotola di latte» per il gatto è una falsa buona idea."}),
 ("fromage", "🧀", {"fr": "Fromage", "en": "Cheese", "it": "Formaggio"}, "modere", "modere",
  {"fr": "Une toute petite quantité en friandise : gras, salé et riche en lactose.",
   "en": "A very small amount as a treat: fatty, salty and high in lactose.",
   "it": "Una quantità piccolissima come premio: grasso, salato e ricco di lattosio."}),
 ("yaourt", "🥣", {"fr": "Yaourt nature", "en": "Plain yoghurt", "it": "Yogurt bianco"}, "modere", "modere",
  {"fr": "Nature, sans sucre ni édulcorant, en petite quantité.",
   "en": "Plain, with no sugar or sweetener, in small amounts.",
   "it": "Bianco, senza zucchero né dolcificanti, in piccole quantità."}),
 ("beurre-cacahuete", "🥜", {"fr": "Beurre de cacahuète", "en": "Peanut butter", "it": "Burro di arachidi"}, "modere", "modere",
  {"fr": "Seulement sans xylitol, sans sel ni sucre ajoutés, et en petite quantité (très gras). Inutile pour le chat.",
   "en": "Only xylitol-free, with no added salt or sugar, and in small amounts (very fatty). Pointless for cats.",
   "it": "Solo senza xilitolo, senza sale né zucchero aggiunti e in piccole quantità (molto grasso). Inutile per il gatto."}),
 ("pain", "🍞", {"fr": "Pain cuit", "en": "Baked bread", "it": "Pane cotto"}, "modere", "modere",
  {"fr": "Un petit morceau de pain nature ne pose pas de problème, mais il n'apporte rien. Jamais avec raisins, graines ou ail.",
   "en": "A small piece of plain bread is fine, but adds nothing. Never with raisins, seeds or garlic.",
   "it": "Un pezzetto di pane semplice non è un problema, ma non apporta nulla. Mai con uvetta, semi o aglio."}),
 ("pates", "🍝", {"fr": "Pâtes cuites", "en": "Cooked pasta", "it": "Pasta cotta"}, "modere", "modere",
  {"fr": "Nature, sans sauce, en petite quantité.",
   "en": "Plain, without sauce, in small amounts.",
   "it": "Scondita, in piccole quantità."}),
 ("pomme-de-terre", "🥔", {"fr": "Pomme de terre", "en": "Potato", "it": "Patata"}, "modere", "modere",
  {"fr": "Cuite et nature uniquement. Jamais crue, ni verte, ni germée.",
   "en": "Cooked and plain only. Never raw, green or sprouted.",
   "it": "Solo cotta e al naturale. Mai cruda, verde o germogliata."}),
 ("mais", "🌽", {"fr": "Maïs", "en": "Corn", "it": "Mais"}, "modere", "modere",
  {"fr": "Quelques grains nature. Jamais l'épi : il peut boucher l'intestin.",
   "en": "A few plain kernels. Never the cob: it can block the intestine.",
   "it": "Qualche chicco al naturale. Mai la pannocchia: può ostruire l'intestino."}),
 ("thon", "🥫", {"fr": "Thon en conserve", "en": "Canned tuna", "it": "Tonno in scatola"}, "modere", "modere",
  {"fr": "De temps en temps, au naturel (pas à l'huile ni salé). Pas comme repas habituel.",
   "en": "Occasionally, in water (not oil or brine). Not as a regular meal.",
   "it": "Ogni tanto, al naturale (non sott'olio né salato). Non come pasto abituale."}),
 ("autre-espece", "🥣", {"fr": "Croquettes de l'autre espèce", "en": "The other species' food", "it": "Cibo dell'altra specie"}, "modere", "non",
  {"fr": "Les croquettes pour chat sont trop riches pour un chien. La nourriture pour chien ne couvre pas les besoins du chat (taurine notamment).",
   "en": "Cat food is too rich for a dog. Dog food doesn't meet a cat's needs (taurine in particular).",
   "it": "Le crocchette per gatti sono troppo ricche per il cane. Il cibo per cani non copre i bisogni del gatto (in particolare la taurina)."}),
 ("poulet", "🍗", {"fr": "Poulet ou dinde cuits", "en": "Cooked chicken or turkey", "it": "Pollo o tacchino cotti"}, "oui", "oui",
  {"fr": "Une excellente friandise : cuit, nature, sans os, sans peau ni assaisonnement.",
   "en": "An excellent treat: cooked, plain, boneless, skinless and unseasoned.",
   "it": "Un ottimo premio: cotto, al naturale, senza ossa, pelle né condimenti."}),
 ("poisson", "🐟", {"fr": "Poisson cuit", "en": "Cooked fish", "it": "Pesce cotto"}, "oui", "oui",
  {"fr": "Saumon, cabillaud… cuit, nature et sans arêtes.",
   "en": "Salmon, cod… cooked, plain and boneless.",
   "it": "Salmone, merluzzo… cotto, al naturale e senza lische."}),
 ("oeuf", "🥚", {"fr": "Œuf cuit", "en": "Cooked egg", "it": "Uovo cotto"}, "oui", "oui",
  {"fr": "Dur ou brouillé sans matière grasse ni sel. Pas cru.",
   "en": "Hard-boiled or scrambled without fat or salt. Not raw.",
   "it": "Sodo o strapazzato senza grassi né sale. Non crudo."}),
 ("potiron", "🎃", {"fr": "Potiron et courge cuits", "en": "Cooked pumpkin and squash", "it": "Zucca cotta"}, "oui", "oui",
  {"fr": "Cuit, nature, sans sucre ni épices : en petite quantité.",
   "en": "Cooked, plain, without sugar or spices: in small amounts.",
   "it": "Cotta, al naturale, senza zucchero né spezie: in piccole quantità."}),
 ("riz", "🍚", {"fr": "Riz cuit", "en": "Cooked rice", "it": "Riso cotto"}, "oui", "modere",
  {"fr": "Nature, bien cuit. Le chat, carnivore, n'en a pas vraiment besoin.",
   "en": "Plain and well cooked. Cats, as carnivores, don't really need it.",
   "it": "Al naturale e ben cotto. Il gatto, carnivoro, non ne ha davvero bisogno."}),
 ("carotte", "🥕", {"fr": "Carotte", "en": "Carrot", "it": "Carota"}, "oui", "modere",
  {"fr": "Crue ou cuite pour le chien, en morceaux adaptés à sa taille. Pour le chat, cuite et en tout petits morceaux.",
   "en": "Raw or cooked for dogs, in pieces suited to their size. For cats, cooked and in tiny pieces.",
   "it": "Cruda o cotta per il cane, a pezzi adatti alla sua taglia. Per il gatto, cotta e a pezzettini."}),
 ("haricots-verts", "🫛", {"fr": "Haricots verts", "en": "Green beans", "it": "Fagiolini"}, "oui", "modere",
  {"fr": "Nature, sans sel ni beurre.",
   "en": "Plain, without salt or butter.",
   "it": "Al naturale, senza sale né burro."}),
 ("courgette", "🥒", {"fr": "Courgette et concombre", "en": "Courgette and cucumber", "it": "Zucchina e cetriolo"}, "oui", "modere",
  {"fr": "Peu caloriques et pleins d'eau : une friandise légère pour le chien.",
   "en": "Low in calories and full of water: a light treat for dogs.",
   "it": "Poco calorici e ricchi d'acqua: un premio leggero per il cane."}),
 ("pomme", "🍎", {"fr": "Pomme et poire", "en": "Apple and pear", "it": "Mela e pera"}, "oui", "modere",
  {"fr": "En petits morceaux, sans trognon ni pépins.",
   "en": "In small pieces, without core or seeds.",
   "it": "A pezzetti, senza torsolo né semi."}),
 ("banane", "🍌", {"fr": "Banane", "en": "Banana", "it": "Banana"}, "oui", "modere",
  {"fr": "Quelques rondelles : elle est sucrée, donc avec modération.",
   "en": "A few slices: it's sugary, so in moderation.",
   "it": "Qualche rondella: è zuccherina, quindi con moderazione."}),
 ("pasteque", "🍉", {"fr": "Pastèque et melon", "en": "Watermelon and melon", "it": "Anguria e melone"}, "oui", "modere",
  {"fr": "La chair seulement, sans pépins ni écorce.",
   "en": "The flesh only, without seeds or rind.",
   "it": "Solo la polpa, senza semi né buccia."}),
 ("myrtilles", "🫐", {"fr": "Myrtilles et fraises", "en": "Blueberries and strawberries", "it": "Mirtilli e fragole"}, "oui", "modere",
  {"fr": "Quelques fruits, lavés, en friandise.",
   "en": "A few berries, washed, as a treat.",
   "it": "Qualche frutto, lavato, come premio."}),
]
VERDICT = {
 "fr": {"oui": "✅ Oui", "modere": "⚠️ Avec modération", "non": "❌ À éviter"},
 "en": {"oui": "✅ Yes", "modere": "⚠️ In moderation", "non": "❌ Avoid"},
 "it": {"oui": "✅ Sì", "modere": "⚠️ Con moderazione", "non": "❌ Da evitare"},
}
T = {
"fr": {"slug_titre": "Mon chien ou mon chat peut-il manger… ? 37 aliments",
       "desc": "Chocolat, raisin, banane, fromage, œuf… Ce que votre chien ou votre chat peut manger, avec modération ou jamais : la liste claire, aliment par aliment.",
       "fil": "Accueil", "court": "Peut-il manger… ?", "h1": "🍎 Mon chien ou mon chat peut-il manger… ?",
       "lead": "Une banane, un morceau de fromage, un reste de poulet ? Voici, aliment par aliment, ce que votre chien et votre chat peuvent manger, avec modération ou jamais. Tapez un aliment pour le trouver tout de suite.",
       "urgence": "<strong>Urgence :</strong> si votre animal a mangé un aliment toxique (chocolat, raisin, oignon, xylitol…), appelez <strong>immédiatement</strong> votre vétérinaire ou un centre antipoison vétérinaire, même s'il semble aller bien. N'essayez pas de le faire vomir sans avis vétérinaire.",
       "chercher": "Chercher un aliment (ex. : banane)", "filtres": ["Tous", "✅ Oui", "⚠️ Avec modération", "❌ À éviter"], "aucun": "Aucun aliment trouvé.",
       "chien": "Chien", "chat": "Chat",
       "regles_t": "Les règles d'or", "regles": [
         "<strong>Toujours nature</strong> : sans sel, sucre, beurre, sauce, épices, oignon ni ail.",
         "<strong>En petite quantité</strong> : les vétérinaires conseillent généralement que les friandises ne dépassent pas environ 10&nbsp;% de ce que l'animal mange dans la journée.",
         "<strong>Une nouveauté à la fois</strong>, en petite quantité, pour vérifier qu'il la digère bien.",
         "<strong>Le chat est un carnivore strict</strong> : fruits et légumes ne lui sont pas utiles. Mieux vaut lui donner un peu de viande ou de poisson cuits.",
         "<strong>Allergie, maladie, régime</strong> : demandez toujours l'avis de votre vétérinaire avant de donner de la nourriture humaine."],
       "liens": "Pour aller plus loin : <a href=\"meilleures-friandises-education-chien.html\">quelles friandises d'éducation choisir ?</a> · <a href=\"chien.html\">le guide du chien</a> · <a href=\"chat.html\">le guide du chat</a> · <a href=\"apropos.html#sources\">nos sources</a>.",
       "source": "Sources : listes d'aliments toxiques de l'ASPCA Animal Poison Control Center et recommandations des associations vétérinaires. Cette page ne remplace pas l'avis d'un vétérinaire.",
       "menu": "🍎 Peut-il manger… ?"},
"en": {"slug_titre": "Can my dog or cat eat…? 37 foods checked",
       "desc": "Chocolate, grapes, banana, cheese, egg… What your dog or cat can eat, in moderation or never: a clear list, food by food.",
       "fil": "Home", "court": "Can they eat…?", "h1": "🍎 Can my dog or cat eat…?",
       "lead": "A banana, a piece of cheese, leftover chicken? Here, food by food, is what your dog and cat can eat, in moderation or never. Type a food to find it straight away.",
       "urgence": "<strong>Emergency:</strong> if your pet has eaten something toxic (chocolate, grapes, onion, xylitol…), call your vet or a pet poison helpline <strong>immediately</strong>, even if they seem fine. Don't try to make them vomit without veterinary advice.",
       "chercher": "Search for a food (e.g. banana)", "filtres": ["All", "✅ Yes", "⚠️ In moderation", "❌ Avoid"], "aucun": "No food found.",
       "chien": "Dog", "chat": "Cat",
       "regles_t": "The golden rules", "regles": [
         "<strong>Always plain</strong>: no salt, sugar, butter, sauce, spices, onion or garlic.",
         "<strong>In small amounts</strong>: vets generally advise that treats should not exceed about 10% of what the animal eats in a day.",
         "<strong>One new food at a time</strong>, in a small amount, to check they digest it well.",
         "<strong>Cats are strict carnivores</strong>: fruit and vegetables are of no use to them. A little cooked meat or fish is better.",
         "<strong>Allergy, illness, special diet</strong>: always ask your vet before giving human food."],
       "liens": "Read more: <a href=\"meilleures-friandises-education-chien.html\">which training treats to choose?</a> · <a href=\"chien.html\">the dog guide</a> · <a href=\"chat.html\">the cat guide</a> · <a href=\"apropos.html#sources\">our sources</a>.",
       "source": "Sources: toxic food lists from the ASPCA Animal Poison Control Center and veterinary association guidance. This page does not replace your vet's advice.",
       "menu": "🍎 Can they eat…?"},
"it": {"slug_titre": "Il mio cane o gatto può mangiare…? 37 alimenti",
       "desc": "Cioccolato, uva, banana, formaggio, uovo… Cosa può mangiare il tuo cane o il tuo gatto, con moderazione o mai: la lista chiara, alimento per alimento.",
       "fil": "Home", "court": "Può mangiare…?", "h1": "🍎 Il mio cane o il mio gatto può mangiare…?",
       "lead": "Una banana, un pezzo di formaggio, un avanzo di pollo? Ecco, alimento per alimento, cosa possono mangiare il tuo cane e il tuo gatto, con moderazione o mai. Scrivi un alimento per trovarlo subito.",
       "urgence": "<strong>Urgenza:</strong> se il tuo animale ha mangiato un alimento tossico (cioccolato, uva, cipolla, xilitolo…), chiama <strong>subito</strong> il veterinario o un centro antiveleni veterinario, anche se sembra stare bene. Non cercare di farlo vomitare senza il parere del veterinario.",
       "chercher": "Cerca un alimento (es.: banana)", "filtres": ["Tutti", "✅ Sì", "⚠️ Con moderazione", "❌ Da evitare"], "aucun": "Nessun alimento trovato.",
       "chien": "Cane", "chat": "Gatto",
       "regles_t": "Le regole d'oro", "regles": [
         "<strong>Sempre al naturale</strong>: senza sale, zucchero, burro, sughi, spezie, cipolla né aglio.",
         "<strong>In piccole quantità</strong>: i veterinari consigliano in genere che gli snack non superino circa il 10% di ciò che l'animale mangia in un giorno.",
         "<strong>Una novità alla volta</strong>, in piccola quantità, per controllare che la digerisca bene.",
         "<strong>Il gatto è un carnivoro stretto</strong>: frutta e verdura non gli servono. Meglio un po' di carne o pesce cotti.",
         "<strong>Allergie, malattie, diete</strong>: chiedi sempre il parere del veterinario prima di dare cibo umano."],
       "liens": "Per saperne di più: <a href=\"meilleures-friandises-education-chien.html\">quali bocconcini scegliere?</a> · <a href=\"chien.html\">la guida al cane</a> · <a href=\"chat.html\">la guida al gatto</a> · <a href=\"apropos.html#sources\">le nostre fonti</a>.",
       "source": "Fonti: elenchi di alimenti tossici dell'ASPCA Animal Poison Control Center e raccomandazioni delle associazioni veterinarie. Questa pagina non sostituisce il parere del veterinario.",
       "menu": "🍎 Può mangiare…?"},
}


# Vidéo TikTok (version française uniquement), comme dans les articles
VIDEO = ('        <!-- video --><figure class="video-tiktok"><video controls preload="none" playsinline poster="videos/aliments-chien-chat.jpg" width="270" height="480">'
         '<source src="videos/aliments-chien-chat.mp4" type="video/mp4"></video><figcaption>🎬 L\'essentiel en 30 secondes · '
         '<a href="https://www.tiktok.com/@educanimauxx" target="_blank" rel="noopener">Suivez-nous sur TikTok</a></figcaption></figure><!-- /video -->\n')


def corps(code):
    t, v, e = T[code], VERDICT[code], html.escape
    cartes = "".join(
        f'          <article class="card aliment" id="{i}" data-verdicts="{c} {g}" data-nom="{e(n[code].lower())}">\n'
        f'            <h3><span aria-hidden="true">{emo}</span> {e(n[code])}</h3>\n'
        f'            <p class="verdicts"><span class="v v-{c}">🐕 {t["chien"]} : {v[c]}</span> <span class="v v-{g}">🐈 {t["chat"]} : {v[g]}</span></p>\n'
        f'            <p>{e(d[code])}</p>\n          </article>\n'
        for i, emo, n, c, g, d in A)
    filtres = "".join(f'<button type="button" class="chip{" actif" if k == 0 else ""}" data-filtre="{f}">{e(lab)}</button>'
                      for k, (f, lab) in enumerate(zip(["", "oui", "modere", "non"], t["filtres"])))
    regles = "".join(f"<li>{r}</li>" for r in t["regles"])
    return f"""    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">{t["fil"]}</a> › {t["court"]}</p>
        <h1>{t["h1"]}</h1>
        <p class="lead">{t["lead"]}</p>
{VIDEO if code == "fr" else ""}        <div class="callout warn">{t["urgence"]}</div>
        <div class="filtre-aliments">
          <input type="search" id="cherche-aliment" placeholder="{e(t["chercher"])}" aria-label="{e(t["chercher"])}" autocomplete="off">
          <div class="chips" role="group">{filtres}</div>
        </div>
        <div class="grid grid-2 aliments">
{cartes}        </div>
        <p class="aucun-aliment" hidden>{t["aucun"]}</p>
        <h2>{t["regles_t"]}</h2>
        <ul>{regles}</ul>
        <p class="muted small">{t["source"]}</p>
        <p>{t["liens"]}</p>
      </div>
    </section>"""


if __name__ == "__main__":
    for code in ("fr", "en", "it"):
        creer_page.creer(code, "aliments-chien-chat", T[code]["slug_titre"], T[code]["desc"], corps(code),
                         scripts=["js/aliments.js"], menu=T[code]["menu"])
    creer_page.finir()
    print(len(A), "aliments")
