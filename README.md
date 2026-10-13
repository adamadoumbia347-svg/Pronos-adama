# Pronos-adama

Page statique qui affiche les matchs à venir avec leurs cotes 1 / N / 2.

Ouvrez `index.html` dans un navigateur. Aucun outil de build n'est nécessaire, et le site peut être déployé tel quel (par exemple sur Netlify).

## Ajouter ou modifier des cotes

Modifiez le tableau `MATCHS` dans `matches.js` :

```js
{
  competition: "Ligue 1",
  date: "2026-10-17T21:00",
  domicile: "Paris SG",
  exterieur: "Olympique de Marseille",
  cotes: { domicile: 1.55, nul: 4.2, exterieur: 5.5 }, // cotes décimales 1 / N / 2
  prono: "1", // facultatif : "1", "N" ou "2"
}
```

Pour chaque match, la page affiche :
- la probabilité implicite de chaque cote ;
- la cote favorite, en vert ;
- le prono choisi, avec un contour orange ;
- la marge du bookmaker.
