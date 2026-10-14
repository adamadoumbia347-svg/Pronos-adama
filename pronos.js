// ============================================================
//  TES PRONOS : c'est le seul fichier à modifier au quotidien.
// ============================================================
//
// Chaque prono est un objet avec :
//   date      : "AAAA-MM-JJ"
//   sport     : "Football", "Basket", "Tennis"...
//   match     : "Équipe A - Équipe B"
//   prono     : ce que tu conseilles ("Victoire Équipe A", "+2,5 buts"...)
//   cote      : la cote (nombre, ex. 1.85)
//   confiance : 1 à 5 étoiles
//   extra     : true pour l'« Entrée Extra » (le prono phare du jour)
//   resultat  : "en_cours", "gagne", "perdu" ou "rembourse"
//   analyse   : (optionnel) 1 à 3 phrases pour expliquer ton choix
//
// Les statistiques (réussite, rentabilité) sont calculées automatiquement
// à partir des pronos terminés. NE SUPPRIME JAMAIS les pronos perdus :
// un historique honnête est ce qui donne confiance aux visiteurs.
//
// ⚠️ Les entrées ci-dessous sont des EXEMPLES : remplace-les par les tiennes.

window.PRONOS = [
  {
    date: "2026-10-14",
    sport: "Football",
    match: "Équipe A - Équipe B",
    prono: "Victoire Équipe A",
    cote: 1.85,
    confiance: 5,
    extra: true,
    resultat: "en_cours",
    analyse: "Exemple d'analyse : Équipe A invaincue à domicile depuis 8 matchs, Équipe B privée de deux titulaires en défense."
  },
  {
    date: "2026-10-14",
    sport: "Football",
    match: "Équipe C - Équipe D",
    prono: "Les deux équipes marquent",
    cote: 1.70,
    confiance: 3,
    extra: false,
    resultat: "en_cours",
    analyse: ""
  },
  {
    date: "2026-10-13",
    sport: "Basket",
    match: "Équipe E - Équipe F",
    prono: "Plus de 210,5 points",
    cote: 1.90,
    confiance: 4,
    extra: true,
    resultat: "gagne",
    analyse: ""
  },
  {
    date: "2026-10-13",
    sport: "Tennis",
    match: "Joueur G - Joueur H",
    prono: "Victoire Joueur G",
    cote: 1.55,
    confiance: 3,
    extra: false,
    resultat: "perdu",
    analyse: ""
  }
];

// Tes liens (laisse "" pour masquer un bouton)
window.LIENS = {
  telegram: "",   // ex. "https://t.me/tonCanal"
  whatsapp: "",   // ex. "https://whatsapp.com/channel/..."
  affiliation: "" // lien d'affiliation d'un bookmaker AGRÉÉ dans ton pays
};
