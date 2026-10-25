// Modèle de pronostic : Poisson (forces d'attaque / défense pondérées dans le temps)
// avec correction Dixon-Coles des petits scores, plus un classement Elo pour la forme.
const Modele = (() => {
  const DEMI_VIE = 200;   // jours : un match d'il y a 200 jours compte moitié moins
  const PRIOR = 3;        // buts fictifs qui tirent une équipe peu connue vers la moyenne
  const RHO = -0.08;      // corrélation des petits scores (0-0, 1-1 plus fréquents)
  const MAX_BUTS = 10;
  const JOUR = 864e5;

  // Ajuste les forces sur les matchs joués avant dateRef (AAAA-MM-JJ).
  function ajuster(matchs, dateRef) {
    const xi = Math.log(2) / DEMI_VIE;
    const tRef = Date.parse(dateRef);
    const idx = new Map();
    const lignes = [];
    for (const m of matchs) {
      if (m.bd === null || m.date >= dateRef) continue;
      const w = Math.exp(-xi * (tRef - Date.parse(m.date)) / JOUR);
      if (w < 0.03) continue;
      for (const e of [m.dom, m.ext]) if (!idx.has(e)) idx.set(e, idx.size);
      lignes.push({ i: idx.get(m.dom), j: idx.get(m.ext), bd: m.bd, be: m.be, w });
    }
    const n = idx.size;
    const A = new Float64Array(n).fill(1), D = new Float64Array(n).fill(1);
    const poids = new Float64Array(n);
    for (const l of lignes) { poids[l.i] += l.w; poids[l.j] += l.w; }
    // Équipe quasi inconnue (promue) : on suppose qu'elle est un peu plus faible que la moyenne.
    const cibleA = Float64Array.from(poids, p => (p < 6 ? 0.85 : 1));
    const cibleD = Float64Array.from(poids, p => (p < 6 ? 1.15 : 1));
    let mu = 1.35, H = 1.2;

    for (let it = 0; it < 80; it++) {
      const butsP = new Float64Array(n), attP = new Float64Array(n);
      const butsC = new Float64Array(n), attC = new Float64Array(n);
      for (const l of lignes) {
        butsP[l.i] += l.w * l.bd; attP[l.i] += l.w * mu * H * D[l.j];
        butsP[l.j] += l.w * l.be; attP[l.j] += l.w * mu * D[l.i];
        butsC[l.i] += l.w * l.be; attC[l.i] += l.w * mu * A[l.j];
        butsC[l.j] += l.w * l.bd; attC[l.j] += l.w * mu * H * A[l.i];
      }
      for (let k = 0; k < n; k++) {
        A[k] = (butsP[k] + PRIOR * cibleA[k]) / (attP[k] + PRIOR);
        D[k] = (butsC[k] + PRIOR * cibleD[k]) / (attC[k] + PRIOR);
      }
      // Normalisation : moyenne géométrique des attaques et défenses = 1.
      const gA = Math.exp(A.reduce((s, x) => s + Math.log(x), 0) / n);
      const gD = Math.exp(D.reduce((s, x) => s + Math.log(x), 0) / n);
      for (let k = 0; k < n; k++) { A[k] /= gA; D[k] /= gD; }
      let bDom = 0, eDom = 0, bExt = 0, eExt = 0;
      for (const l of lignes) {
        bDom += l.w * l.bd; eDom += l.w * A[l.i] * D[l.j];
        bExt += l.w * l.be; eExt += l.w * A[l.j] * D[l.i];
      }
      mu = bExt / eExt;
      H = bDom / (mu * eDom);
    }
    const forces = {};
    for (const [e, k] of idx) forces[e] = { attaque: A[k], defense: D[k], poids: poids[k] };
    return { forces, mu, H, dateRef, nbMatchs: lignes.length };
  }

  function poisson(l, k) {
    let p = Math.exp(-l);
    for (let i = 1; i <= k; i++) p *= l / i;
    return p;
  }

  function tau(x, y, ld, le) {
    if (x === 0 && y === 0) return 1 - ld * le * RHO;
    if (x === 0 && y === 1) return 1 + ld * RHO;
    if (x === 1 && y === 0) return 1 + le * RHO;
    if (x === 1 && y === 1) return 1 - RHO;
    return 1;
  }

  const inconnue = { attaque: 0.85, defense: 1.15 };

  function predire(fit, dom, ext) {
    const fd = fit.forces[dom] || inconnue, fe = fit.forces[ext] || inconnue;
    const ld = fit.mu * fit.H * fd.attaque * fe.defense;
    const le = fit.mu * fe.attaque * fd.defense;
    const grille = [];
    let total = 0;
    for (let x = 0; x <= MAX_BUTS; x++) {
      grille.push([]);
      for (let y = 0; y <= MAX_BUTS; y++) {
        const p = poisson(ld, x) * poisson(le, y) * tau(x, y, ld, le);
        grille[x].push(p);
        total += p;
      }
    }
    let p1 = 0, pN = 0, p2 = 0, btts = 0;
    const plus = { 0.5: 0, 1.5: 0, 2.5: 0, 3.5: 0, 4.5: 0 };
    const scores = [];
    for (let x = 0; x <= MAX_BUTS; x++) for (let y = 0; y <= MAX_BUTS; y++) {
      const p = (grille[x][y] /= total);
      if (x > y) p1 += p; else if (x === y) pN += p; else p2 += p;
      if (x > 0 && y > 0) btts += p;
      for (const s in plus) if (x + y > s) plus[s] += p;
      scores.push({ x, y, p });
    }
    scores.sort((a, b) => b.p - a.p);
    return { dom, ext, ld, le, p1, pN, p2, btts, plus, grille, scores };
  }

  // Elo calculé match par match ; entre deux saisons on revient d'un tiers vers 1500.
  function elo(matchs) {
    const r = {}, histo = {};
    let saison = null;
    for (const m of matchs) {
      if (m.bd === null) continue;
      if (m.saison !== saison) {
        saison = m.saison;
        for (const e in r) r[e] = 1500 + (r[e] - 1500) * 2 / 3;
      }
      const rd = r[m.dom] ?? 1450, re = r[m.ext] ?? 1450;
      const attendu = 1 / (1 + 10 ** ((re - rd - 60) / 400));
      const res = m.bd > m.be ? 1 : m.bd === m.be ? 0.5 : 0;
      const ecart = Math.abs(m.bd - m.be);
      const k = 22 * (ecart <= 1 ? 1 : ecart === 2 ? 1.5 : (11 + ecart) / 8);
      r[m.dom] = rd + k * (res - attendu);
      r[m.ext] = re - k * (res - attendu);
      (histo[m.dom] ||= []).push([m.date, r[m.dom]]);
      (histo[m.ext] ||= []).push([m.date, r[m.ext]]);
    }
    return { notes: r, histo };
  }

  // Conseil de pari lisible à partir des probabilités.
  function conseil(p) {
    const liste = [];
    const max = Math.max(p.p1, p.pN, p.p2);
    if (p.p1 === max && p.p1 >= 0.55) liste.push({ pari: '1', libelle: `Victoire ${Noms.court(p.dom)}`, proba: p.p1 });
    else if (p.p2 === max && p.p2 >= 0.5) liste.push({ pari: '2', libelle: `Victoire ${Noms.court(p.ext)}`, proba: p.p2 });
    else if (p.p1 + p.pN >= 0.7 && p.p1 >= p.p2) liste.push({ pari: '1N', libelle: `${Noms.court(p.dom)} ou nul`, proba: p.p1 + p.pN });
    else if (p.p2 + p.pN >= 0.66) liste.push({ pari: 'N2', libelle: `${Noms.court(p.ext)} ou nul`, proba: p.p2 + p.pN });
    else liste.push({ pari: '12', libelle: 'Pas de nul', proba: p.p1 + p.p2 });
    if (p.plus[2.5] >= 0.58) liste.push({ pari: '+2.5', libelle: 'Plus de 2,5 buts', proba: p.plus[2.5] });
    else if (1 - p.plus[2.5] >= 0.58) liste.push({ pari: '-2.5', libelle: 'Moins de 2,5 buts', proba: 1 - p.plus[2.5] });
    if (p.btts >= 0.58) liste.push({ pari: 'BTTS', libelle: 'Les deux équipes marquent', proba: p.btts });
    else if (1 - p.btts >= 0.62) liste.push({ pari: 'BTTS-non', libelle: 'Une équipe ne marque pas', proba: 1 - p.btts });
    return liste;
  }

  function confiance(proba) {
    return proba >= 0.75 ? 3 : proba >= 0.62 ? 2 : 1;
  }

  // Validation « walk-forward » : chaque semaine, on réajuste sur le passé
  // puis on prédit les matchs de la semaine, sans jamais voir leur résultat.
  function evaluer(matchs, depuis) {
    const aTester = matchs.filter(m => m.bd !== null && m.date >= depuis);
    const semaines = new Map();
    for (const m of aTester) {
      const t = Date.parse(m.date);
      const lundi = new Date(t - ((new Date(t).getUTCDay() + 6) % 7) * JOUR).toISOString().slice(0, 10);
      if (!semaines.has(lundi)) semaines.set(lundi, []);
      semaines.get(lundi).push(m);
    }
    const res = [];
    for (const [lundi, liste] of semaines) {
      const fit = ajuster(matchs, lundi);
      for (const m of liste) res.push({ m, p: predire(fit, m.dom, m.ext) });
    }
    let bons = 0, brier = 0, logloss = 0, domicile = 0, bonsPlus = 0, bonsBtts = 0;
    let conseils = 0, conseilsBons = 0;
    const freq = { '1': 0, 'N': 0, '2': 0 };
    const calib = Array.from({ length: 10 }, () => ({ n: 0, prevu: 0, reel: 0 }));
    for (const { m, p } of res) {
      const reel = m.bd > m.be ? '1' : m.bd === m.be ? 'N' : '2';
      freq[reel]++;
      const probas = { '1': p.p1, 'N': p.pN, '2': p.p2 };
      const choix = Object.keys(probas).reduce((a, b) => (probas[a] >= probas[b] ? a : b));
      if (choix === reel) bons++;
      if (reel === '1') domicile++;
      for (const k in probas) brier += (probas[k] - (k === reel ? 1 : 0)) ** 2;
      logloss -= Math.log(Math.max(probas[reel], 1e-9));
      if ((p.plus[2.5] >= 0.5) === (m.bd + m.be > 2.5)) bonsPlus++;
      if ((p.btts >= 0.5) === (m.bd > 0 && m.be > 0)) bonsBtts++;
      for (const k in probas) {
        const b = calib[Math.min(9, Math.floor(probas[k] * 10))];
        b.n++; b.prevu += probas[k]; b.reel += k === reel ? 1 : 0;
      }
      const c = conseil(p)[0];
      if (c.proba >= 0.62) {
        conseils++;
        if (c.pari.split('').includes(reel) || (c.pari === '12' && reel !== 'N')) conseilsBons++;
      }
    }
    const n = res.length;
    return {
      n, precision: bons / n, brier: brier / n, logloss: logloss / n,
      toujoursDomicile: domicile / n, plus25: bonsPlus / n, btts: bonsBtts / n,
      conseils, conseilsBons, freq, calib, details: res,
    };
  }

  return { ajuster, predire, elo, conseil, confiance, evaluer };
})();

const Noms = (() => {
  const OTER = new Set(['FC', 'AFC', 'CF', 'SC', 'AC', 'AS', 'SSC', 'SV', 'VfB', 'VfL', 'TSG', 'FSV', 'RC', 'SL', 'CD',
    'UD', 'RCD', 'CFC', 'SD', 'CA', 'OGC', 'ACF', 'US', 'SS', 'BC', 'FK', 'SK', 'CP', 'GD', 'SBV', 'PSV', 'BV', 'Calcio']);
  const garder = new Set(['PSV']);
  function court(nom) {
    const mots = nom.split(' ').filter(m => garder.has(m) || (!OTER.has(m) && !/^\d+\.?$/.test(m)));
    return mots.length ? mots.join(' ') : nom;
  }
  return { court };
})();
