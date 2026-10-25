// Interface : chargement des données, routes (#pronostics, #analyse/…, #classement, #fiabilite, #methode).
(() => {
  const SOURCE = 'https://raw.githubusercontent.com/openfootball/football.json/master';
  const PAR_PAGE = 24;
  const D = window.PRONOS_DONNEES;
  const vue = document.getElementById('vue');
  const auj = new Date().toISOString().slice(0, 10);

  const etat = { code: null, matchs: [], saison: null, fit: null, elo: null, enLigne: false, eval: {}, nbAffiches: PAR_PAGE };

  // ---------- utilitaires ----------
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const pct = p => `${Math.round(p * 100)}\u00a0%`;
  const cote = p => (p > 0 ? (1 / p).toFixed(2).replace('.', ',') : '—');
  const nb = (x, d = 2) => x.toFixed(d).replace('.', ',');
  const court = Noms.court;
  const dateLongue = iso => new Date(iso + 'T12:00:00Z').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const dateCourte = iso => new Date(iso + 'T12:00:00Z').toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' });
  const lien = (...parties) => '#' + parties.map(encodeURIComponent).join('/');
  const lire = k => { try { return localStorage.getItem(k); } catch { return null; } };
  const ecrire = (k, v) => { try { localStorage.setItem(k, v); } catch { /* stockage indisponible */ } };
  const etoiles = n => `<span class="etoiles" title="Confiance ${n}/3">${'★'.repeat(n)}${'☆'.repeat(3 - n)}</span>`;

  // ---------- données ----------
  function chargerScript(src) {
    return new Promise((ok, ko) => {
      const s = document.createElement('script');
      s.src = src; s.onload = ok; s.onerror = ko;
      document.head.appendChild(s);
    });
  }

  function versObjets(lignes) {
    return lignes.map(([saison, date, heure, dom, ext, bd, be]) => ({ saison, date, heure, dom, ext, bd, be }));
  }

  // Récupère la saison en cours directement chez openfootball pour avoir les tout derniers scores.
  async function saisonEnLigne(code, saison) {
    const ctrl = new AbortController();
    const minuterie = setTimeout(() => ctrl.abort(), 6000);
    try {
      const r = await fetch(`${SOURCE}/${saison}/${code}.json`, { signal: ctrl.signal, cache: 'no-cache' });
      if (!r.ok) return null;
      const brut = (await r.json()).matches;
      return brut.map(m => {
        const s = m.score;
        const ft = Array.isArray(s) ? s : s && Array.isArray(s.ft) ? s.ft : null;
        return { saison, date: m.date, heure: m.time || '', dom: m.team1, ext: m.team2, bd: ft ? ft[0] : null, be: ft ? ft[1] : null };
      });
    } catch { return null; } finally { clearTimeout(minuterie); }
  }

  // Matchs d'une ligue (copie locale + saison en cours en direct), mémorisés pour la session.
  const ligues = {};
  function preparerLigue(code) {
    return ligues[code] ||= (async () => {
      if (!D[code]) await chargerScript(`data/${code}.js`);
      let matchs = versObjets(D[code].matchs), enLigne = false;
      const saison = D.saisons[D.saisons.length - 1];
      const frais = await saisonEnLigne(code, saison);
      if (frais && frais.length) {
        const avant = matchs.filter(m => m.bd !== null).length;
        const fusion = matchs.filter(m => m.saison !== saison).concat(frais);
        if (fusion.filter(m => m.bd !== null).length >= avant) { matchs = fusion; enLigne = true; }
      }
      matchs.sort((a, b) => (a.date + a.heure).localeCompare(b.date + b.heure));
      return { code, matchs, saison, enLigne, fits: {} };
    })();
  }

  // Forces ajustées sur les matchs joués avant la date (pas de triche sur les jours passés).
  function fitAu(l, date) {
    return l.fits[date] ||= Modele.ajuster(l.matchs, date);
  }

  async function chargerLigue(code) {
    etat.code = code;
    ecrire('pronos-ligue', code);
    dessinerLigues();
    vue.innerHTML = '<p class="chargement">Chargement des résultats…</p>';
    const l = await preparerLigue(code);
    if (etat.code !== code) return; // l'utilisateur a changé de ligue entre-temps
    const { matchs, saison } = l;
    etat.enLigne = l.enLigne;
    etat.matchs = matchs;
    etat.saison = saison;
    etat.fit = fitAu(l, auj);
    etat.elo = Modele.elo(matchs);
    etat.nbAffiches = PAR_PAGE;
    const joues = matchs.filter(m => m.bd !== null);
    etat.dernier = joues.length ? joues[joues.length - 1].date : null;
    document.getElementById('source').innerHTML =
      `Données : <a href="https://github.com/openfootball/football.json" rel="noopener">openfootball</a> (domaine public) · ` +
      `${joues.length} matchs analysés · dernier résultat le ${etat.dernier ? dateLongue(etat.dernier) : '—'}` +
      (etat.enLigne ? ' · mis à jour en direct' : ' · copie locale');
    router();
  }

  function equipesSaison() {
    return [...new Set(etat.matchs.filter(m => m.saison === etat.saison).flatMap(m => [m.dom, m.ext]))]
      .sort((a, b) => court(a).localeCompare(court(b), 'fr'));
  }

  // Derniers matchs joués d'une équipe (lieu : 'dom', 'ext' ou rien).
  function historique(equipe, n, lieu) {
    const liste = [];
    for (let i = etat.matchs.length - 1; i >= 0 && liste.length < n; i--) {
      const m = etat.matchs[i];
      if (m.bd === null) continue;
      const dom = m.dom === equipe, ext = m.ext === equipe;
      if (!(dom || ext) || (lieu === 'dom' && !dom) || (lieu === 'ext' && !ext)) continue;
      const bp = dom ? m.bd : m.be, bc = dom ? m.be : m.bd;
      liste.push({ m, dom, adv: dom ? m.ext : m.dom, bp, bc, res: bp > bc ? 'V' : bp === bc ? 'N' : 'D' });
    }
    return liste;
  }

  function resume(liste) {
    const n = liste.length || 1;
    const s = { n: liste.length, V: 0, N: 0, D: 0, bp: 0, bc: 0, plus25: 0, btts: 0, cleanSheet: 0, pts: 0 };
    for (const h of liste) {
      s[h.res]++; s.bp += h.bp; s.bc += h.bc;
      if (h.bp + h.bc > 2.5) s.plus25++;
      if (h.bp > 0 && h.bc > 0) s.btts++;
      if (h.bc === 0) s.cleanSheet++;
    }
    s.pts = s.V * 3 + s.N;
    s.mbp = s.bp / n; s.mbc = s.bc / n;
    return s;
  }

  const pastilles = liste => `<span class="forme">${liste.slice().reverse()
    .map(h => `<i class="${h.res}" title="${esc(dateCourte(h.m.date))} ${h.dom ? 'vs' : '@'} ${esc(court(h.adv))} ${h.bp}-${h.bc}">${h.res}</i>`).join('')}</span>`;

  function classement() {
    const t = {};
    for (const e of equipesSaison()) t[e] = { e, J: 0, V: 0, N: 0, D: 0, bp: 0, bc: 0, pts: 0 };
    for (const m of etat.matchs) {
      if (m.saison !== etat.saison || m.bd === null) continue;
      for (const [e, bp, bc] of [[m.dom, m.bd, m.be], [m.ext, m.be, m.bd]]) {
        const l = t[e]; l.J++; l.bp += bp; l.bc += bc;
        if (bp > bc) { l.V++; l.pts += 3; } else if (bp === bc) { l.N++; l.pts++; } else l.D++;
      }
    }
    return Object.values(t).sort((a, b) => b.pts - a.pts || (b.bp - b.bc) - (a.bp - a.bc) || b.bp - a.bp || court(a.e).localeCompare(court(b.e)));
  }

  // ---------- composants ----------
  function barre1N2(p) {
    const seg = (cls, v, lbl) => `<div class="${cls}" style="flex:${v}" title="${lbl} : ${pct(v)}">${v >= 0.12 ? pct(v) : ''}</div>`;
    return `<div class="barre" role="img" aria-label="Domicile ${pct(p.p1)}, nul ${pct(p.pN)}, extérieur ${pct(p.p2)}">
      ${seg('b1', p.p1, '1 · ' + court(p.dom))}${seg('bn', p.pN, 'N · Nul')}${seg('b2', p.p2, '2 · ' + court(p.ext))}</div>
      <div class="legende-barre"><span>1 · ${esc(court(p.dom))}</span><span>N · Nul</span><span>2 · ${esc(court(p.ext))}</span></div>`;
  }

  function puces(p) {
    return `<div class="conseils">${Modele.conseil(p).map(c =>
      `<span class="puce">${esc(c.libelle)} <span class="pct">${pct(c.proba)}</span> ${etoiles(Modele.confiance(c.proba))}</span>`).join('')}</div>`;
  }

  // Score le plus probable parmi ceux qui donnent l'issue favorite (évite un « 1-1 » affiché pour un favori à 60 %).
  function scoreProbable(p) {
    const mx = Math.max(p.p1, p.pN, p.p2);
    const ok = mx === p.p1 ? s => s.x > s.y : mx === p.p2 ? s => s.x < s.y : s => s.x === s.y;
    return p.scores.find(ok);
  }

  function carteMatch(m, fit = etat.fit, code = etat.code) {
    const p = Modele.predire(fit, m.dom, m.ext);
    const s = scoreProbable(p);
    let reel = '';
    if (m.bd !== null) {
      const mx = Math.max(p.p1, p.pN, p.p2), choix = mx === p.p1 ? '1' : mx === p.pN ? 'N' : '2';
      const ok = choix === (m.bd > m.be ? '1' : m.bd === m.be ? 'N' : '2');
      reel = `<span class="${ok ? 'resultat-ok' : 'resultat-ko'}">Score final ${m.bd}-${m.be} ${ok ? '✔' : '✘'}</span>`;
    }
    return `<a class="carte match" href="${lien('analyse', code, m.dom, m.ext)}">
      <div class="heure"><span>${esc(m.heure || '')}</span>${reel || `<span>Buts attendus ${nb(p.ld, 1)} – ${nb(p.le, 1)}</span>`}</div>
      <div class="match-equipes">
        <span class="eq">${esc(court(m.dom))}</span>
        <span class="score-prevu num">${s.x} - ${s.y}<small>score probable</small></span>
        <span class="eq">${esc(court(m.ext))}</span>
      </div>
      ${barre1N2(p)}
      ${puces(p)}
    </a>`;
  }

  // ---------- vues ----------
  const decaler = (iso, j) => new Date(Date.parse(iso) + j * 864e5).toISOString().slice(0, 10);

  async function vueJour(date) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date || '')) date = auj;
    vue.innerHTML = '<p class="chargement">Chargement des 7 championnats…</p>';
    const toutes = await Promise.all(D.index.map(l => preparerLigue(l.code)));
    if (location.hash.slice(1).split('/')[0] !== 'jour') return; // l'utilisateur est parti ailleurs
    const jours = [...new Set(toutes.flatMap(l => l.matchs.map(m => m.date)))].sort();
    const avant = jours.filter(j => j < date).pop(), apres = jours.find(j => j > date);
    const blocs = [], tops = [];
    let total = 0;
    for (const l of toutes) {
      const duJour = l.matchs.filter(m => m.date === date);
      if (!duJour.length) continue;
      const fit = fitAu(l, date);
      total += duJour.length;
      for (const m of duJour) {
        if (m.bd !== null) continue;
        const c = Modele.conseil(Modele.predire(fit, m.dom, m.ext))[0];
        tops.push({ c, m, code: l.code });
      }
      blocs.push(`<h2 class="jour">${esc(D[l.code].ligue)} <span class="discret">· ${duJour.length} match${duJour.length > 1 ? 's' : ''}</span></h2>
        <div class="matchs">${duJour.map(m => carteMatch(m, fit, l.code)).join('')}</div>`);
    }
    tops.sort((a, b) => b.c.proba - a.c.proba);
    const nav = (j, txt, titre) => j ? `<a class="bouton secondaire" href="${lien('jour', j)}" title="${titre}" aria-label="${titre}">${txt}</a>`
      : `<span class="bouton secondaire inactif" aria-hidden="true">${txt}</span>`;
    vue.innerHTML = `<div class="titre-section"><h1>Matchs du ${date === auj ? 'jour' : dateLongue(date)}</h1>
        <span class="discret">${date === auj ? dateLongue(date) + ' · ' : ''}${total} match${total > 1 ? 's' : ''} dans les 7 championnats</span></div>
      <div class="nav-jour">
        ${nav(avant, '◀', 'Jour de match précédent')}
        <input type="date" id="choix-date" value="${date}" aria-label="Choisir une date">
        ${date !== auj ? `<a class="bouton secondaire" href="#jour">Aujourd'hui</a>` : ''}
        ${nav(apres, '▶', 'Jour de match suivant')}
      </div>
      ${tops.length >= 3 ? `<div class="carte top-jour"><h2>Les 3 pronos les plus sûrs du jour</h2><ol>${tops.slice(0, 3).map(({ c, m, code }) =>
        `<li><a href="${lien('analyse', code, m.dom, m.ext)}">${esc(court(m.dom))} – ${esc(court(m.ext))}</a> :
          <b>${esc(c.libelle)}</b> <span class="discret">${pct(c.proba)} · cote juste ${cote(c.proba)}</span></li>`).join('')}</ol></div>` : ''}
      ${blocs.length ? blocs.join('') : `<p class="carte">Aucun match ce jour-là dans les 7 championnats.
        ${apres ? `Prochains matchs : <a href="${lien('jour', apres)}">${dateLongue(apres)}</a>.` : ''}</p>`}
      ${date < auj && blocs.length ? '<p class="discret">Pour les jours passés, les pronostics sont recalculés sans connaître les résultats du jour, pour comparer honnêtement.</p>' : ''}`;
    document.getElementById('choix-date').onchange = ev => { if (ev.target.value) location.hash = lien('jour', ev.target.value); };
  }

  function vuePronostics() {
    const aVenir = etat.matchs.filter(m => m.saison === etat.saison && m.bd === null && m.date >= auj);
    const retard = etat.dernier && (Date.parse(auj) - Date.parse(etat.dernier)) / 864e5 > 10;
    let html = `<div class="titre-section"><h1>Pronostics ${esc(D[etat.code].ligue)}</h1>
      <span class="discret">Saison ${esc(etat.saison.replace('-', '/'))}</span></div>`;
    if (retard) html += `<p class="alerte">Les derniers résultats publiés datent du ${dateLongue(etat.dernier)}. Les matchs joués depuis
      ne sont pas encore pris en compte : relancez <code>tools/maj_donnees.py</code> ou revenez plus tard.</p>`;
    if (!aVenir.length) {
      html += `<p class="carte">Aucun match à venir dans le calendrier. Utilisez <a href="${lien('analyse', etat.code)}">Analyser un match</a>
        pour simuler n'importe quelle affiche.</p>`;
      vue.innerHTML = html; return;
    }
    let jour = null, bloc = '';
    for (const m of aVenir.slice(0, etat.nbAffiches)) {
      if (m.date !== jour) {
        if (jour) bloc += '</div>';
        jour = m.date;
        bloc += `<h2 class="jour">${dateLongue(m.date)}</h2><div class="matchs">`;
      }
      bloc += carteMatch(m);
    }
    html += bloc + '</div>';
    if (aVenir.length > etat.nbAffiches) html += `<div class="centre"><button class="bouton secondaire" id="plus">Voir plus de matchs (${aVenir.length - etat.nbAffiches})</button></div>`;
    vue.innerHTML = html;
    const plus = document.getElementById('plus');
    if (plus) plus.onclick = () => { etat.nbAffiches += PAR_PAGE; const y = scrollY; vuePronostics(); scrollTo(0, y); };
  }

  function options(equipes, choisie) {
    return equipes.map(e => `<option value="${esc(e)}"${e === choisie ? ' selected' : ''}>${esc(court(e))}</option>`).join('');
  }

  function vueAnalyse(dom, ext) {
    const equipes = equipesSaison();
    if (!equipes.includes(dom)) dom = equipes[0];
    if (!equipes.includes(ext) || ext === dom) ext = equipes.find(e => e !== dom);
    const p = Modele.predire(etat.fit, dom, ext);
    const notes = etat.elo.notes;
    const fd = etat.fit.forces[dom], fe = etat.fit.forces[ext];
    const top = p.scores.slice(0, 6);
    const pasMarque = { dom: p.grille.reduce((s, l) => s + l[0], 0), ext: p.grille[0].reduce((s, x) => s + x, 0) };

    const marche = (lbl, v) => `<div class="marche"><span>${lbl}</span><span class="n num"><b>${pct(v)}</b></span><span class="n num discret">${cote(v)}</span>
      <div class="jauge"><i style="width:${(v * 100).toFixed(1)}%"></i></div></div>`;

    const heat = (() => {
      let max = 0;
      for (let x = 0; x <= 5; x++) for (let y = 0; y <= 5; y++) max = Math.max(max, p.grille[x][y]);
      let h = `<div class="ent" title="${esc(court(dom))} en ligne, ${esc(court(ext))} en colonne">↓→</div>`;
      for (let y = 0; y <= 5; y++) h += `<div class="ent">${y}</div>`;
      for (let x = 0; x <= 5; x++) {
        h += `<div class="ent">${x}</div>`;
        for (let y = 0; y <= 5; y++) {
          const v = p.grille[x][y], a = v / max;
          h += `<div style="background:color-mix(in srgb, var(--accent) ${Math.round(a * 85)}%, var(--carte-2));color:${a > 0.55 ? '#fff' : 'var(--texte)'}"
            title="${x}-${y} : ${(v * 100).toFixed(1)} %">${v >= 0.005 ? (v * 100).toFixed(0) : ''}</div>`;
        }
      }
      return h;
    })();

    const blocForme = (equipe, lieu, libLieu) => {
      const tout = historique(equipe, 10), place = historique(equipe, 10, lieu);
      const st = resume(tout), sp = resume(place);
      return `<div class="carte"><h2>${esc(court(equipe))}</h2>
        <p>Forme (5 derniers) ${pastilles(tout.slice(0, 5))}</p>
        <table><thead><tr><th></th><th class="n">10 derniers</th><th class="n">${libLieu}</th></tr></thead><tbody>
          <tr><td>Bilan V-N-D</td><td class="n">${st.V}-${st.N}-${st.D}</td><td class="n">${sp.V}-${sp.N}-${sp.D}</td></tr>
          <tr><td>Points / match</td><td class="n">${nb(st.pts / (st.n || 1))}</td><td class="n">${nb(sp.pts / (sp.n || 1))}</td></tr>
          <tr><td>Buts marqués / match</td><td class="n">${nb(st.mbp)}</td><td class="n">${nb(sp.mbp)}</td></tr>
          <tr><td>Buts encaissés / match</td><td class="n">${nb(st.mbc)}</td><td class="n">${nb(sp.mbc)}</td></tr>
          <tr><td>Matchs à +2,5 buts</td><td class="n">${st.plus25}/${st.n}</td><td class="n">${sp.plus25}/${sp.n}</td></tr>
          <tr><td>Les deux marquent</td><td class="n">${st.btts}/${st.n}</td><td class="n">${sp.btts}/${sp.n}</td></tr>
          <tr><td>Sans encaisser</td><td class="n">${st.cleanSheet}/${st.n}</td><td class="n">${sp.cleanSheet}/${sp.n}</td></tr>
        </tbody></table>
        <h3 style="margin-top:14px">Derniers résultats</h3>
        <table><tbody>${tout.slice(0, 6).map(h => `<tr><td class="num discret">${dateCourte(h.m.date)}</td>
          <td>${h.dom ? 'vs' : '@'} ${esc(court(h.adv))}</td><td class="n num"><b>${h.bp}-${h.bc}</b></td>
          <td class="n"><span class="forme"><i class="${h.res}">${h.res}</i></span></td></tr>`).join('')}</tbody></table>
      </div>`;
    };

    const h2h = etat.matchs.filter(m => m.bd !== null && ((m.dom === dom && m.ext === ext) || (m.dom === ext && m.ext === dom))).reverse();
    const bilanH2h = h2h.reduce((b, m) => {
      const bd = m.dom === dom ? m.bd : m.be, be = m.dom === dom ? m.be : m.bd;
      b[bd > be ? 0 : bd === be ? 1 : 2]++; b[3] += bd + be; return b;
    }, [0, 0, 0, 0]);

    const ligneForce = (lbl, v, inverse) => {
      // v = 1 : moyenne du championnat. Barre centrée, vers la droite = meilleur.
      const score = Math.max(-1, Math.min(1, Math.log(inverse ? 1 / v : v) / Math.log(2)));
      const g = score >= 0 ? 50 : 50 + score * 50, l = Math.abs(score) * 50;
      return `<div class="force-ligne"><span>${lbl}</span><div class="force-barre"><i style="left:${g}%;width:${l}%;background:${score >= 0 ? 'var(--bon)' : 'var(--mauvais)'}"></i></div>
        <span class="n num">${score >= 0 ? '+' : ''}${Math.round((inverse ? 1 / v - 1 : v - 1) * 100)} %</span></div>`;
    };

    const marchesValue = [
      ['1', `Victoire ${court(dom)}`, p.p1], ['N', 'Match nul', p.pN], ['2', `Victoire ${court(ext)}`, p.p2],
      ['1N', `${court(dom)} ou nul`, p.p1 + p.pN], ['N2', `${court(ext)} ou nul`, p.p2 + p.pN],
      ['+2.5', 'Plus de 2,5 buts', p.plus[2.5]], ['-2.5', 'Moins de 2,5 buts', 1 - p.plus[2.5]],
      ['btts', 'Les deux marquent : oui', p.btts], ['nbtts', 'Les deux marquent : non', 1 - p.btts],
    ];

    vue.innerHTML = `
      <div class="titre-section"><h1>Analyser un match</h1><span class="discret">${esc(D[etat.code].ligue)}</span></div>
      <div class="carte selecteurs">
        <label>Domicile<select id="sel-dom">${options(equipes, dom)}</select></label>
        <button class="inverser" id="inverser" type="button" title="Inverser domicile / extérieur" aria-label="Inverser">⇄</button>
        <label>Extérieur<select id="sel-ext">${options(equipes, ext)}</select></label>
      </div>

      <div class="pile" style="margin-top:14px">
        <div class="carte">
          <div class="affiche">
            <div><div class="nom">${esc(court(dom))}</div><div class="elo">Elo ${Math.round(notes[dom] ?? 1450)}</div></div>
            <div><div class="gros-score num">${scoreProbable(p).x} - ${scoreProbable(p).y}</div><div class="xg">Buts attendus ${nb(p.ld, 2)} – ${nb(p.le, 2)}</div></div>
            <div><div class="nom">${esc(court(ext))}</div><div class="elo">Elo ${Math.round(notes[ext] ?? 1450)}</div></div>
          </div>
          ${barre1N2(p)}
          ${puces(p)}
        </div>

        <div class="grille-2">
          <div class="carte">
            <h2>Résultat (1N2) et cotes justes</h2>
            <div class="cotes">
              <div><div class="lbl">1 · ${esc(court(dom))}</div><div class="val num">${pct(p.p1)}</div><div class="cote">cote juste ${cote(p.p1)}</div></div>
              <div><div class="lbl">N · Nul</div><div class="val num">${pct(p.pN)}</div><div class="cote">cote juste ${cote(p.pN)}</div></div>
              <div><div class="lbl">2 · ${esc(court(ext))}</div><div class="val num">${pct(p.p2)}</div><div class="cote">cote juste ${cote(p.p2)}</div></div>
            </div>
            <p class="discret">Une « cote juste » est la cote sans marge : si un bookmaker propose plus, le pari a une valeur positive selon le modèle.</p>
            <h3>Scores les plus probables</h3>
            <table><tbody>${top.map(s => `<tr><td><b class="num">${s.x} - ${s.y}</b></td><td class="n num">${(s.p * 100).toFixed(1).replace('.', ',')} %</td><td class="n num discret">${cote(s.p)}</td></tr>`).join('')}</tbody></table>
          </div>

          <div class="carte">
            <h2>Marchés</h2>
            <div class="marche discret"><span>Pari</span><span class="n">Proba</span><span class="n">Cote juste</span></div>
            ${marche('Double chance 1N', p.p1 + p.pN)}
            ${marche('Double chance N2', p.p2 + p.pN)}
            ${marche('Double chance 12', p.p1 + p.p2)}
            ${marche('Plus de 1,5 but', p.plus[1.5])}
            ${marche('Plus de 2,5 buts', p.plus[2.5])}
            ${marche('Plus de 3,5 buts', p.plus[3.5])}
            ${marche('Moins de 2,5 buts', 1 - p.plus[2.5])}
            ${marche('Les deux équipes marquent', p.btts)}
            ${marche(`${esc(court(dom))} marque`, 1 - pasMarque.dom)}
            ${marche(`${esc(court(ext))} marque`, 1 - pasMarque.ext)}
          </div>
        </div>

        <div class="grille-2">
          <div class="carte">
            <h2>Probabilité de chaque score (%)</h2>
            <p class="discret">Lignes : buts de ${esc(court(dom))} · colonnes : buts de ${esc(court(ext))}.</p>
            <div class="heatmap">${heat}</div>
          </div>
          <div class="carte">
            <h2>Forces estimées</h2>
            <p class="discret">Comparées à la moyenne du championnat (0&nbsp;%), calculées sur les résultats passés, les plus récents comptant davantage.</p>
            <div class="forces">
              <b>${esc(court(dom))}</b>
              ${fd ? ligneForce('Attaque', fd.attaque) + ligneForce('Défense', fd.defense, true) : '<p class="discret">Pas assez de matchs.</p>'}
              <b>${esc(court(ext))}</b>
              ${fe ? ligneForce('Attaque', fe.attaque) + ligneForce('Défense', fe.defense, true) : '<p class="discret">Pas assez de matchs.</p>'}
            </div>
            <p class="discret">Avantage du terrain dans ce championnat : +${Math.round((etat.fit.H - 1) * 100)} % de buts à domicile.</p>
          </div>
        </div>

        <div class="grille-2">
          ${blocForme(dom, 'dom', 'à domicile')}
          ${blocForme(ext, 'ext', 'à l\'extérieur')}
        </div>

        <div class="carte">
          <h2>Confrontations directes</h2>
          ${h2h.length ? `<p>${h2h.length} match(s) depuis 2024 : <b>${bilanH2h[0]}</b> victoire(s) ${esc(court(dom))}, <b>${bilanH2h[1]}</b> nul(s),
            <b>${bilanH2h[2]}</b> victoire(s) ${esc(court(ext))} · ${nb(bilanH2h[3] / h2h.length, 1)} buts par match.</p>
            <table><tbody>${h2h.map(m => `<tr><td class="num discret">${dateCourte(m.date)}</td><td>${esc(court(m.dom))}</td>
              <td class="n num"><b>${m.bd}-${m.be}</b></td><td>${esc(court(m.ext))}</td></tr>`).join('')}</tbody></table>`
            : '<p class="discret">Aucune confrontation dans les données (depuis 2024).</p>'}
        </div>

        <div class="carte">
          <h2>Détecteur de value bet</h2>
          <p class="discret">Entrez les cotes de votre bookmaker. Un pari a de la valeur quand probabilité × cote &gt; 1.
          La mise conseillée suit le quart de Kelly, en % de votre bankroll.</p>
          <div class="value-grille">${marchesValue.map(([k, lbl, pr]) => `<label>${esc(lbl)}
            <input type="number" min="1.01" step="0.01" inputmode="decimal" placeholder="cote" data-proba="${pr}" data-cle="${k}">
            <span class="value-res"></span></label>`).join('')}</div>
        </div>
      </div>`;

    const aller = (d, e) => { location.hash = lien('analyse', etat.code, d, e); };
    document.getElementById('sel-dom').onchange = ev => aller(ev.target.value, ext === ev.target.value ? dom : ext);
    document.getElementById('sel-ext').onchange = ev => aller(dom === ev.target.value ? ext : dom, ev.target.value);
    document.getElementById('inverser').onclick = () => aller(ext, dom);
    vue.querySelectorAll('input[data-proba]').forEach(inp => {
      inp.oninput = () => {
        const res = inp.nextElementSibling;
        const c = parseFloat(inp.value.replace(',', '.')), pr = +inp.dataset.proba;
        if (!(c > 1)) { res.textContent = ''; res.className = 'value-res'; return; }
        const valeur = pr * c - 1;
        const kelly = Math.max(0, valeur / (c - 1)) / 4;
        res.className = 'value-res ' + (valeur > 0 ? 'ok' : 'ko');
        res.textContent = valeur > 0
          ? `✔ Valeur +${nb(valeur * 100, 1)}\u00a0% · mise ${nb(kelly * 100, 1)}\u00a0%`
          : `✘ Pas de valeur (${nb(valeur * 100, 1)}\u00a0%)`;
      };
    });
  }

  function vueClassement() {
    const t = classement();
    const forces = etat.fit.forces, notes = etat.elo.notes;
    vue.innerHTML = `<div class="titre-section"><h1>Classement ${esc(D[etat.code].ligue)}</h1>
      <span class="discret">Saison ${esc(etat.saison.replace('-', '/'))} · calculé sur les résultats disponibles</span></div>
      <div class="carte defile"><table>
        <thead><tr><th class="n">#</th><th>Équipe</th><th class="n">Pts</th><th class="n">J</th><th class="n">V</th><th class="n">N</th><th class="n">D</th>
          <th class="n">BP</th><th class="n">BC</th><th class="n">Diff</th><th>Forme</th><th class="n" title="Classement Elo">Elo</th>
          <th class="n" title="Attaque par rapport à la moyenne">Att.</th><th class="n" title="Défense par rapport à la moyenne">Déf.</th></tr></thead>
        <tbody>${t.map((l, i) => {
          const f = forces[l.e];
          return `<tr><td class="n">${i + 1}</td>
            <td class="equipe"><a href="${lien('analyse', etat.code, l.e, t[i === 0 ? 1 : 0].e)}">${esc(court(l.e))}</a></td>
            <td class="n"><b>${l.pts}</b></td><td class="n">${l.J}</td><td class="n">${l.V}</td><td class="n">${l.N}</td><td class="n">${l.D}</td>
            <td class="n">${l.bp}</td><td class="n">${l.bc}</td><td class="n">${l.bp - l.bc > 0 ? '+' : ''}${l.bp - l.bc}</td>
            <td>${pastilles(historique(l.e, 5))}</td>
            <td class="n">${Math.round(notes[l.e] ?? 1450)}</td>
            <td class="n">${f ? nb(f.attaque) : '—'}</td><td class="n">${f ? nb(1 / f.defense) : '—'}</td></tr>`;
        }).join('')}</tbody></table></div>
      <p class="discret">Att. et Déf. : 1,00 = moyenne du championnat ; au-dessus de 1, l'équipe marque plus (Att.) ou encaisse moins (Déf.) que la moyenne.</p>`;
  }

  function graphiqueCalibration(calib) {
    const pts = calib.filter(b => b.n >= 15).map(b => ({ x: b.prevu / b.n, y: b.reel / b.n, n: b.n }));
    const W = 320, H = 240, m = { g: 40, d: 12, h: 12, b: 34 };
    const sx = v => m.g + v * (W - m.g - m.d), sy = v => H - m.b - v * (H - m.h - m.b);
    const graduations = [0, 0.2, 0.4, 0.6, 0.8, 1];
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Calibration : probabilité annoncée contre fréquence observée" style="width:100%;max-width:460px;display:block">
      ${graduations.map(v => `<line x1="${sx(0)}" x2="${sx(1)}" y1="${sy(v)}" y2="${sy(v)}" stroke="var(--bord)"/>
        <text x="${sx(0) - 6}" y="${sy(v) + 4}" text-anchor="end" font-size="10" fill="var(--texte-2)">${v * 100}%</text>
        <text x="${sx(v)}" y="${H - m.b + 15}" text-anchor="middle" font-size="10" fill="var(--texte-2)">${v * 100}%</text>`).join('')}
      <line x1="${sx(0)}" y1="${sy(0)}" x2="${sx(1)}" y2="${sy(1)}" stroke="var(--texte-2)" stroke-dasharray="4 4"/>
      <polyline fill="none" stroke="var(--accent)" stroke-width="2" points="${pts.map(p => `${sx(p.x)},${sy(p.y)}`).join(' ')}"/>
      ${pts.map(p => `<circle cx="${sx(p.x)}" cy="${sy(p.y)}" r="5" fill="var(--accent)" stroke="var(--carte)" stroke-width="2">
        <title>Annoncé ${Math.round(p.x * 100)} % → arrivé ${Math.round(p.y * 100)} % (${p.n} cas)</title></circle>`).join('')}
      <text x="${(sx(0) + sx(1)) / 2}" y="${H - 4}" text-anchor="middle" font-size="10" fill="var(--texte-2)">Probabilité annoncée par le modèle</text>
    </svg>`;
  }

  function vueFiabilite() {
    const debut = etat.matchs.find(m => m.saison === D.saisons[1])?.date;
    vue.innerHTML = '<p class="chargement">Calcul : le modèle rejoue chaque semaine depuis le début de la saison 2025/26…</p>';
    setTimeout(() => {
      const ev = etat.eval[etat.code] ||= Modele.evaluer(etat.matchs, debut);
      if (!ev.n) { vue.innerHTML = '<p class="carte">Pas assez de matchs pour évaluer le modèle.</p>'; return; }
      const parConfiance = [[0, 0.45], [0.45, 0.55], [0.55, 0.65], [0.65, 1.01]].map(([a, b]) => {
        const l = ev.details.filter(({ p }) => { const mx = Math.max(p.p1, p.pN, p.p2); return mx >= a && mx < b; });
        const ok = l.filter(({ m, p }) => {
          const mx = Math.max(p.p1, p.pN, p.p2);
          const choix = mx === p.p1 ? '1' : mx === p.pN ? 'N' : '2';
          return choix === (m.bd > m.be ? '1' : m.bd === m.be ? 'N' : '2');
        }).length;
        return { a, b, n: l.length, ok };
      });
      const recents = ev.details.slice(-30).reverse();
      vue.innerHTML = `<div class="titre-section"><h1>Fiabilité du modèle · ${esc(D[etat.code].ligue)}</h1>
        <span class="discret">${ev.n} matchs prédits sans connaître leur résultat (depuis le ${dateLongue(debut)})</span></div>
        <div class="stats">
          <div class="stat"><div class="val num">${pct(ev.precision)}</div><div class="lbl">Bon résultat 1N2 (issue la plus probable)</div></div>
          <div class="stat"><div class="val num">${pct(ev.toujoursDomicile)}</div><div class="lbl">Référence : toujours parier sur le domicile</div></div>
          <div class="stat"><div class="val num">${ev.conseils ? pct(ev.conseilsBons / ev.conseils) : '—'}</div><div class="lbl">Conseils principaux ≥ 62 % gagnants (${ev.conseils} conseils)</div></div>
          <div class="stat"><div class="val num">${pct(ev.plus25)}</div><div class="lbl">Bonne prédiction ± 2,5 buts</div></div>
          <div class="stat"><div class="val num">${pct(ev.btts)}</div><div class="lbl">Bonne prédiction « les deux marquent »</div></div>
          <div class="stat"><div class="val num">${nb(ev.brier, 3)}</div><div class="lbl">Score de Brier (0 = parfait, 0,667 = au hasard)</div></div>
        </div>
        <div class="grille-2" style="margin-top:14px">
          <div class="carte"><h2>Calibration</h2>
            <p class="discret">Quand le modèle annonce 60 %, l'événement arrive-t-il vraiment 6 fois sur 10 ? Plus les points suivent la diagonale, plus les probabilités sont fiables.</p>
            ${graphiqueCalibration(ev.calib)}
            <details><summary class="discret">Voir le tableau</summary><table><thead><tr><th>Tranche</th><th class="n">Cas</th><th class="n">Annoncé</th><th class="n">Observé</th></tr></thead>
              <tbody>${ev.calib.filter(b => b.n).map((b, i) => `<tr><td>${i * 10}–${i * 10 + 10} %</td><td class="n">${b.n}</td><td class="n">${pct(b.prevu / b.n)}</td><td class="n">${pct(b.reel / b.n)}</td></tr>`).join('')}</tbody></table></details>
          </div>
          <div class="carte"><h2>Réussite selon la confiance</h2>
            <p class="discret">Plus l'issue favorite est probable, plus le pronostic 1N2 est sûr.</p>
            <table><thead><tr><th>Proba du favori</th><th class="n">Matchs</th><th class="n">Réussite</th></tr></thead>
              <tbody>${parConfiance.map(c => `<tr><td>${c.b > 1 ? `≥ ${Math.round(c.a * 100)} %` : `${Math.round(c.a * 100)}–${Math.round(c.b * 100)} %`}</td><td class="n">${c.n}</td>
                <td class="n"><b>${c.n ? pct(c.ok / c.n) : '—'}</b></td></tr>`).join('')}</tbody></table>
            <p class="discret">Répartition réelle : ${pct(ev.freq['1'] / ev.n)} victoires à domicile, ${pct(ev.freq.N / ev.n)} nuls, ${pct(ev.freq['2'] / ev.n)} à l'extérieur.</p>
          </div>
        </div>
        <div class="carte defile" style="margin-top:14px"><h2>30 derniers pronostics contrôlés</h2>
          <table><thead><tr><th>Date</th><th>Match</th><th class="n">1 / N / 2</th><th class="n">Prévu</th><th class="n">Réel</th><th></th></tr></thead><tbody>
          ${recents.map(({ m, p }) => {
            const mx = Math.max(p.p1, p.pN, p.p2), choix = mx === p.p1 ? '1' : mx === p.pN ? 'N' : '2';
            const reel = m.bd > m.be ? '1' : m.bd === m.be ? 'N' : '2';
            return `<tr><td class="num discret">${dateCourte(m.date)}</td><td>${esc(court(m.dom))} – ${esc(court(m.ext))}</td>
              <td class="n num">${Math.round(p.p1 * 100)} / ${Math.round(p.pN * 100)} / ${Math.round(p.p2 * 100)}</td>
              <td class="n">${choix} <span class="discret">(${scoreProbable(p).x}-${scoreProbable(p).y})</span></td><td class="n"><b>${m.bd}-${m.be}</b></td>
              <td class="${choix === reel ? 'resultat-ok' : 'resultat-ko'}">${choix === reel ? '✔' : '✘'}</td></tr>`;
          }).join('')}</tbody></table></div>`;
    }, 30);
  }

  function vueMethode() {
    vue.innerHTML = `<div class="carte texte"><h1>Comment sont calculés les pronostics ?</h1>
      <p>Les pronostics s'appuient uniquement sur les <b>résultats passés</b> des saisons ${D.saisons.map(s => s.replace('-', '/')).join(', ')}
      (${D.index.map(l => esc(l.nom)).join(', ')}).</p>
      <h2>1. Force d'attaque et de défense</h2>
      <p>Pour chaque équipe, le modèle estime combien elle marque et encaisse par rapport à la moyenne du championnat, en tenant compte
      de la qualité des adversaires rencontrés. Les matchs récents pèsent plus lourd : un match d'il y a 200 jours compte moitié moins
      qu'un match d'hier. Les équipes promues (peu de matchs connus) partent légèrement sous la moyenne.</p>
      <h2>2. Buts attendus</h2>
      <p>Buts attendus du club qui reçoit = moyenne du championnat × avantage du terrain × attaque du club × faiblesse défensive de l'adversaire.
      Même calcul pour l'équipe visiteuse, sans l'avantage du terrain.</p>
      <h2>3. Probabilité de chaque score</h2>
      <p>Les buts suivent une loi de Poisson, corrigée (méthode Dixon-Coles) pour les petits scores 0-0, 1-0, 0-1 et 1-1, plus fréquents en réalité.
      En additionnant les scores, on obtient les probabilités 1N2, plus/moins de buts, « les deux équipes marquent », etc.</p>
      <h2>4. Forme et Elo</h2>
      <p>Le classement Elo évolue après chaque match selon le résultat et l'écart de buts ; il complète l'analyse de forme
      (5 et 10 derniers matchs, bilan à domicile / à l'extérieur, confrontations directes).</p>
      <h2>5. Contrôle</h2>
      <p>L'onglet <a href="#fiabilite">Fiabilité</a> rejoue le modèle semaine après semaine, sans jamais lui montrer le résultat à prédire,
      pour mesurer honnêtement son taux de réussite.</p>
      <h2>Limites</h2>
      <ul><li>Le modèle ne connaît ni les blessures, ni les suspensions, ni les compositions d'équipe, ni la météo, ni les enjeux du match.</li>
      <li>Aucun modèle ne bat durablement les bookmakers sans discipline : cherchez la <i>valeur</i> (cote supérieure à la cote juste), pas le « pari sûr ».</li>
      <li>Les résultats dépendent de la mise à jour des données (openfootball).</li></ul>
      <h2>Jeu responsable</h2>
      <p>Fixez-vous un budget, ne cherchez jamais à « vous refaire » après une perte et faites des pauses.
      Aide gratuite : <b>09 74 75 13 13</b> (Joueurs Info Service) · <a href="https://www.joueurs-info-service.fr" rel="noopener">joueurs-info-service.fr</a>.</p>
    </div>`;
  }

  // ---------- navigation ----------
  function dessinerLigues() {
    document.getElementById('ligues').innerHTML = D.index.map(l =>
      `<button type="button" data-code="${l.code}" aria-pressed="${l.code === etat.code}">${esc(l.nom)}</button>`).join('');
  }
  document.getElementById('ligues').addEventListener('click', ev => {
    const b = ev.target.closest('button[data-code]');
    if (!b || b.dataset.code === etat.code) return;
    const onglet = (location.hash.slice(1).split('/')[0]) || 'pronostics';
    if (onglet === 'analyse') history.replaceState(null, '', '#analyse');
    chargerLigue(b.dataset.code);
  });

  function router() {
    const [onglet = 'pronostics', ...args] = location.hash.slice(1).split('/').map(decodeURIComponent);
    if (args[0] && args[0] !== etat.code && D.index.some(l => l.code === args[0])) { chargerLigue(args[0]); return; }
    if (!etat.fit) return;
    document.getElementById('ligues').hidden = onglet === 'jour';
    document.querySelectorAll('.onglets a').forEach(a => a.classList.toggle('actif', a.dataset.onglet === (onglet || 'pronostics')));
    if (onglet === 'jour') vueJour(args[0]);
    else if (onglet === 'analyse') vueAnalyse(args[1], args[2]);
    else if (onglet === 'classement') vueClassement();
    else if (onglet === 'fiabilite') vueFiabilite();
    else if (onglet === 'methode') vueMethode();
    else vuePronostics();
    if (onglet !== 'pronostics') scrollTo(0, 0);
  }
  addEventListener('hashchange', router);

  // Thème clair / sombre (préférence mémorisée si possible).
  const racine = document.documentElement;
  const themeMemo = lire('pronos-theme');
  if (themeMemo) racine.dataset.theme = themeMemo;
  document.getElementById('theme').onclick = () => {
    const sombre = racine.dataset.theme ? racine.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    racine.dataset.theme = sombre ? 'light' : 'dark';
    ecrire('pronos-theme', racine.dataset.theme);
  };

  const depuisHash = location.hash.slice(1).split('/').map(decodeURIComponent)[1];
  const memo = lire('pronos-ligue');
  const depart = [depuisHash, memo, 'fr.1'].find(c => D.index.some(l => l.code === c));
  chargerLigue(depart);
})();
