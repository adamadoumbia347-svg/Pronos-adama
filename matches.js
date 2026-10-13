// Liste des matchs et de leurs cotes (format décimal).
// Pour ajouter un match, copiez un bloc et modifiez les valeurs.
//   cotes.domicile  -> cote "1" (victoire de l'équipe à domicile)
//   cotes.nul       -> cote "N" (match nul)
//   cotes.exterieur -> cote "2" (victoire de l'équipe à l'extérieur)
// Les valeurs ci-dessous sont des exemples : remplacez-les par les cotes réelles.
const MATCHS = [
  {
    competition: "Ligue 1",
    date: "2026-10-17T21:00",
    domicile: "Paris SG",
    exterieur: "Olympique de Marseille",
    cotes: { domicile: 1.55, nul: 4.2, exterieur: 5.5 },
    prono: "1",
  },
  {
    competition: "Premier League",
    date: "2026-10-18T16:00",
    domicile: "Arsenal",
    exterieur: "Liverpool",
    cotes: { domicile: 2.3, nul: 3.4, exterieur: 3.0 },
    prono: "N",
  },
  {
    competition: "LaLiga",
    date: "2026-10-18T21:00",
    domicile: "Real Madrid",
    exterieur: "FC Barcelone",
    cotes: { domicile: 2.1, nul: 3.6, exterieur: 3.2 },
    prono: "1",
  },
  {
    competition: "Serie A",
    date: "2026-10-19T20:45",
    domicile: "Inter Milan",
    exterieur: "Juventus",
    cotes: { domicile: 1.95, nul: 3.3, exterieur: 4.0 },
    prono: "2",
  },
];
