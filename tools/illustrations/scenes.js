// Génère les illustrations du site (SVG, sans texte) dans docs/img/illu/.
// Usage : node tools/illustrations/scenes.js
const fs = require('fs'), path = require('path');
const P = require('./persos.js'); const C = P.C;
const OUT = path.join(__dirname, '../../docs/img/illu'); fs.mkdirSync(OUT, { recursive: true });
const svg = (w, h, corps, fond = '#fffaf3') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img"><rect width="${w}" height="${h}" rx="28" fill="${fond}"/>${corps}</svg>`;
const sol = (y, w) => `<rect x="0" y="${y}" width="${w}" height="6" fill="#eadfd3"/>`;
const at = (x, y, s, contenu, flip = false) => `<g transform="translate(${x},${y}) scale(${flip ? -s : s},${s})">${contenu}</g>`;
const ok = (x, y) => `<g transform="translate(${x},${y})"><circle r="30" fill="#2f7d6d"/><path d="M-13 1 l9 10 l18 -20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
const ko = (x, y) => `<g transform="translate(${x},${y})"><circle r="30" fill="#c9442f"/><path d="M-11 -11 l22 22 M11 -11 l-22 22" stroke="#fff" stroke-width="7" stroke-linecap="round"/></g>`;
const friandise = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-14" y="-5" width="28" height="10" rx="5" fill="#b8763a"/><circle cx="-14" cy="-5" r="6" fill="#b8763a"/><circle cx="-14" cy="5" r="6" fill="#b8763a"/><circle cx="14" cy="-5" r="6" fill="#b8763a"/><circle cx="14" cy="5" r="6" fill="#b8763a"/></g>`;
const mainSeule = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-60" y="-11" width="70" height="22" rx="11" fill="${C.habit}"/><circle cx="14" cy="0" r="16" fill="${C.peau}"/></g>`;
const fleche = (x1, y1, x2, y2, col = '#b44c1c') => { const a = Math.atan2(y2 - y1, x2 - x1); const h = 14;
  return `<path d="M${x1} ${y1} L${x2} ${y2}" stroke="${col}" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 12"/><path d="M${x2} ${y2} l${-h * Math.cos(a - 0.5)} ${-h * Math.sin(a - 0.5)} M${x2} ${y2} l${-h * Math.cos(a + 0.5)} ${-h * Math.sin(a + 0.5)}" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`; };
const coeur = (x, y, s = 1, col = '#e0566b') => `<path transform="translate(${x},${y}) scale(${s})" d="M0 8 C -20 -8 -10 -24 0 -12 C 10 -24 20 -8 0 8 Z" fill="${col}"/>`;
const etoiles = (x, y) => `<g fill="#ffd23f"><path transform="translate(${x},${y})" d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4Z"/><path transform="translate(${x + 26},${y + 22}) scale(.6)" d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4Z"/></g>`;

// Chat assis (regarde à droite)
function chatAssis() {
  return `<g>
    <path d="M-40 -6 q-46 -10 -30 -70" stroke="${C.chat}" stroke-width="12" fill="none" stroke-linecap="round"/>
    <ellipse cx="-6" cy="-40" rx="40" ry="42" fill="${C.chat}"/>
    <ellipse cx="14" cy="-78" rx="26" ry="44" fill="${C.chat}" transform="rotate(10 14 -78)"/>
    <ellipse cx="22" cy="-74" rx="13" ry="30" fill="${C.chatC}" transform="rotate(10 22 -74)"/>
    <rect x="18" y="-60" width="13" height="60" rx="6.5" fill="${C.chatF}"/><rect x="32" y="-60" width="13" height="60" rx="6.5" fill="${C.chat}"/>
    <g transform="translate(28,-132)">
      <path d="M-26 -14 L-22 -46 L-4 -26 Z M12 -26 L28 -44 L28 -12 Z" fill="${C.chatF}"/>
      <ellipse cx="0" cy="0" rx="32" ry="28" fill="${C.chat}"/>
      <ellipse cx="14" cy="8" rx="13" ry="9" fill="${C.chatC}"/>
      <path d="M19 3 l6 0 l-3 4 z" fill="#e0566b"/>
      <ellipse cx="4" cy="-6" rx="4" ry="5.5" fill="#2b2420"/><ellipse cx="22" cy="-6" rx="3.5" ry="5" fill="#2b2420"/>
      <path d="M26 10 l22 -4 M26 13 l22 3" stroke="#2b2420" stroke-width="1.6"/>
    </g>
  </g>`;
}
// Chat dressé qui griffe un poteau à sa droite
function chatGriffe() {
  return `<g>
    <path d="M-34 -10 q-50 4 -50 -46" stroke="${C.chat}" stroke-width="12" fill="none" stroke-linecap="round"/>
    <rect x="-24" y="-40" width="14" height="40" rx="7" fill="${C.chatF}"/><rect x="-6" y="-40" width="14" height="40" rx="7" fill="${C.chat}"/>
    <ellipse cx="-4" cy="-82" rx="30" ry="62" fill="${C.chat}" transform="rotate(22 -4 -82)"/>
    <ellipse cx="6" cy="-90" rx="13" ry="40" fill="${C.chatC}" transform="rotate(22 6 -90)"/>
    <rect x="6" y="-176" width="13" height="70" rx="6.5" fill="${C.chat}" transform="rotate(38 12 -110)"/>
    <rect x="16" y="-160" width="13" height="64" rx="6.5" fill="${C.chatF}" transform="rotate(48 22 -100)"/>
    <g transform="translate(26,-156)">
      <path d="M-26 -14 L-22 -46 L-4 -26 Z M12 -26 L28 -44 L28 -12 Z" fill="${C.chatF}"/>
      <ellipse cx="0" cy="0" rx="30" ry="27" fill="${C.chat}"/>
      <path d="M-4 -6 q5 -5 10 0 M16 -6 q4 -5 9 0" stroke="#2b2420" stroke-width="3" fill="none" stroke-linecap="round"/>
      <ellipse cx="14" cy="8" rx="12" ry="8" fill="${C.chatC}"/><path d="M19 3 l6 0 l-3 4 z" fill="#e0566b"/>
    </g>
  </g>`;
}
const poteauSisal = (x, h) => { let r = `<rect x="${x - 70}" y="-14" width="140" height="14" rx="6" fill="#a86b3e"/><rect x="${x - 22}" y="${-h}" width="44" height="${h - 10}" fill="#d8c08f"/>`;
  for (let y = -h + 8; y < -16; y += 12) r += `<line x1="${x - 22}" y1="${y}" x2="${x + 22}" y2="${y + 6}" stroke="#b89a62" stroke-width="3"/>`;
  return r + `<rect x="${x - 40}" y="${-h - 14}" width="80" height="16" rx="6" fill="#a86b3e"/>`; };
const canape = (x) => `<g transform="translate(${x},0)"><rect x="-150" y="-120" width="300" height="90" rx="26" fill="#3d7bb3"/><rect x="-170" y="-80" width="60" height="70" rx="20" fill="#2f6496"/><rect x="110" y="-80" width="60" height="70" rx="20" fill="#2f6496"/><rect x="-120" y="-70" width="240" height="44" rx="14" fill="#5592c8"/><rect x="-150" y="-12" width="12" height="12" fill="#2b2420"/><rect x="138" y="-12" width="12" height="12" fill="#2b2420"/>
  <path d="M120 -110 l18 40 M132 -112 l18 40 M144 -110 l16 36" stroke="#fffaf3" stroke-width="4" stroke-linecap="round"/></g>`;

const S = {};
// 1. Laisse tendue (✗) / laisse souple (✓)
S['laisse'] = (() => { const w = 1200, h = 520, y = 460;
  const [mx, my] = P.main(170, y, 75, 0.9);
  const g = `${at(170, y, 0.9, P.humain({ bras: 75, pas: 6 }))}${at(430, y, 0.95, P.chienDebout({ tete: -6, queue: -20 }))}
    <path d="M${mx} ${my} L${430 + 0.95 * 62} ${y - 0.95 * 118}" stroke="#c9442f" stroke-width="6" stroke-linecap="round"/>
    ${ko(520, 70)}`;
  const [mx2, my2] = P.main(780, y, 30, 0.9);
  const d = `${at(780, y, 0.9, P.humain({ bras: 30 }))}${at(930, y, 0.95, P.chienDebout({ tete: -14, queue: -40 }))}
    <path d="M${mx2} ${my2} Q ${mx2 + 40} ${y - 20} ${930 + 0.95 * 62} ${y - 0.95 * 118}" stroke="#2f7d6d" stroke-width="6" fill="none" stroke-linecap="round"/>
    ${coeur(1010, 230, 1.4)}${ok(1110, 70)}`;
  return svg(w, h, `${sol(y, w)}<line x1="600" y1="40" x2="600" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>${g}${d}`); })();

// 2. Apprendre « assis » par le leurre
S['assis-leurre'] = (() => { const w = 1200, h = 480, y = 430;
  return svg(w, h, `${sol(y, w)}
    ${at(220, y, 1, P.chienDebout({ tete: -24 }))}${mainSeule(330, 200, 1)}${friandise(352, 178, 1)}${fleche(250, 150, 330, 150)}
    ${fleche(540, 260, 640, 260, '#eadfd3')}
    ${at(860, y, 1.05, P.chienAssis({ tete: -16 }))}${mainSeule(990, 190)}${friandise(1012, 168)}${etoiles(1060, 120)}${ok(1110, 70)}`); })();

// 3. Assis / couché / pas bouger
S['assis-couche-pasbouger'] = (() => { const w = 1200, h = 440, y = 400;
  const paume = (x, yy) => `<g transform="translate(${x},${yy})"><rect x="-10" y="-40" width="20" height="44" rx="10" fill="${C.peau}"/><rect x="-24" y="-30" width="12" height="30" rx="6" fill="${C.peau}"/><rect x="12" y="-30" width="12" height="30" rx="6" fill="${C.peau}"/><rect x="-14" y="2" width="28" height="40" rx="8" fill="${C.habit}"/></g>`;
  return svg(w, h, `${sol(y, w)}
    ${at(170, y, 0.95, P.chienAssis({ tete: -14 }))}${mainSeule(290, 150, 0.9)}${friandise(310, 130, 0.9)}
    <line x1="400" y1="60" x2="400" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>
    ${at(570, y, 0.95, P.chienCouche({ tete: 6 }))}${mainSeule(720, y - 30, 0.9)}${friandise(740, y - 50, 0.9)}${fleche(720, 250, 720, 330)}
    <line x1="800" y1="60" x2="800" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>
    ${at(920, y, 0.95, P.chienAssis({ tete: -6 }))}${paume(1110, 230)}${fleche(1040, 330, 1100, 330, '#2f7d6d')}`); })();

// 4. Rappel : le chien accourt vers son humain, longe qui traîne
S['rappel'] = (() => { const w = 1200, h = 500, y = 450;
  const [mx, my] = P.main(1010, y, 70, 0.95);
  return svg(w, h, `${sol(y, w)}
    <path d="M150 ${y - 4} q120 10 200 -2 q90 -12 160 -60" stroke="#2f7d6d" stroke-width="5" fill="none" stroke-linecap="round"/>
    <g stroke="#d99a5b" stroke-width="6" stroke-linecap="round" opacity=".7"><path d="M330 280 h-80"/><path d="M320 320 h-110"/><path d="M335 360 h-70"/></g>
    ${at(520, y, 1, P.chienDebout({ tete: -10, queue: -50 }))}
    ${at(1010, y, 0.95, P.humain({ bras: 70 }))}${friandise(mx + 16, my - 6)}${coeur(800, 230, 1.6)}${coeur(850, 190, 1)}`); })();

// 5. Harnais en Y (✓) / collier qui serre (✗)
S['harnais'] = (() => { const w = 1200, h = 470, y = 420;
  const harnais = (x) => `<g transform="translate(${x},${y})" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 -110 Q30 -78 22 -46" stroke="#2f7d6d" stroke-width="13"/>
      <path d="M52 -124 Q74 -112 84 -96" stroke="#2f7d6d" stroke-width="11"/>
      <path d="M84 -96 Q74 -74 56 -54" stroke="#2f7d6d" stroke-width="11"/>
      <path d="M22 -110 Q38 -122 52 -124" stroke="#2f7d6d" stroke-width="11"/>
      <circle cx="30" cy="-116" r="9" stroke="#ffd23f" stroke-width="5"/><circle cx="82" cy="-90" r="8" stroke="#ffd23f" stroke-width="5"/></g>`;
  return svg(w, h, `${sol(y, w)}
    <g transform="translate(220,${y})">${P.chienDebout({ tete: -4 })}</g>${harnais(220)}
    <path d="M244 ${y - 124} q-100 -60 -200 -40" stroke="#2b2420" stroke-width="5" fill="none"/>${ok(470, 70)}
    <line x1="600" y1="40" x2="600" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>
    <g transform="translate(860,${y})">${P.chienDebout({ tete: 10 })}</g>
    <g transform="translate(860,${y})"><path d="M48 -128 Q64 -118 70 -96" stroke="#c9442f" stroke-width="13" fill="none" stroke-linecap="round"/>
      <path d="M52 -124 q-110 -50 -210 -70" stroke="#2b2420" stroke-width="5" fill="none"/>
      <g stroke="#c9442f" stroke-width="5" stroke-linecap="round"><path d="M80 -112 l16 -6"/><path d="M82 -98 l18 2"/><path d="M78 -84 l14 10"/></g></g>${ko(1110, 70)}`); })();

// 6. Griffoir : canapé griffé (✗) → grand griffoir (✓)
S['griffoir'] = (() => { const w = 1200, h = 520, y = 470;
  return svg(w, h, `${sol(y, w)}
    <g transform="translate(250,${y})">${canape(0)}</g>${at(150, y, 0.8, P.chienAssis ? chatAssis() : '')}${ko(470, 70)}
    <line x1="600" y1="40" x2="600" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>
    <g transform="translate(0,${y})">${poteauSisal(940, 330)}</g>${at(830, y, 1.1, chatGriffe())}${coeur(760, 150, 1.3)}${ok(1110, 70)}`); })();

// 7. Chiot : jouet à mâcher (✓) plutôt que la main (✗)
S['chiot-jouet'] = (() => { const w = 1200, h = 440, y = 400;
  const os = (x, yy, s) => `<g transform="translate(${x},${yy}) scale(${s})"><rect x="-40" y="-9" width="80" height="18" rx="9" fill="#fff" stroke="#d0c3b3" stroke-width="3"/><circle cx="-40" cy="-10" r="13" fill="#fff" stroke="#d0c3b3" stroke-width="3"/><circle cx="-40" cy="10" r="13" fill="#fff" stroke="#d0c3b3" stroke-width="3"/><circle cx="40" cy="-10" r="13" fill="#fff" stroke="#d0c3b3" stroke-width="3"/><circle cx="40" cy="10" r="13" fill="#fff" stroke="#d0c3b3" stroke-width="3"/></g>`;
  return svg(w, h, `${sol(y, w)}
    ${at(250, y, 0.8, P.chienAssis({ tete: 4 }))}${mainSeule(400, 245, 1)}${ko(470, 70)}
    <line x1="600" y1="40" x2="600" y2="${y - 20}" stroke="#eadfd3" stroke-width="4" stroke-dasharray="10 12"/>
    ${at(820, y, 0.8, P.chienCouche({ tete: 14 }))}${os(940, y - 70, 0.9)}${etoiles(1000, 200)}${ok(1110, 70)}`); })();

// 8. Propreté : les moments clés pour sortir (icônes) → dehors + récompense
S['proprete-moments'] = (() => { const w = 1200, h = 400, y = 200;
  const rond = (x, contenu, col) => `<g transform="translate(${x},${y})"><circle r="70" fill="${col}"/>${contenu}</g>`;
  const soleil = `<circle r="26" fill="#ffd23f"/><g stroke="#ffd23f" stroke-width="7" stroke-linecap="round">${[0, 45, 90, 135, 180, 225, 270, 315].map(a => `<line x1="${36 * Math.cos(a * Math.PI / 180)}" y1="${36 * Math.sin(a * Math.PI / 180)}" x2="${48 * Math.cos(a * Math.PI / 180)}" y2="${48 * Math.sin(a * Math.PI / 180)}"/>`).join('')}</g>`;
  const gamelle = `<path d="M-40 0 h80 l-12 26 h-56 z" fill="#b44c1c"/><ellipse cx="0" cy="0" rx="40" ry="10" fill="#9a4016"/><circle cx="-10" cy="-6" r="7" fill="#b8763a"/><circle cx="8" cy="-8" r="7" fill="#b8763a"/><circle cx="0" cy="-14" r="6" fill="#b8763a"/>`;
  const balle = `<circle r="30" fill="#c6e23a"/><path d="M-28 -8 q28 12 56 0 M-28 10 q28 -12 56 0" stroke="#fff" stroke-width="5" fill="none"/>`;
  const lune = `<path d="M10 -32 a34 34 0 1 0 22 54 a28 28 0 1 1 -22 -54z" fill="#ffd23f"/><circle cx="26" cy="-20" r="4" fill="#fff"/>`;
  const arbre = `<rect x="-8" y="0" width="16" height="40" fill="#a86b3e"/><circle cx="0" cy="-12" r="34" fill="#2f7d6d"/><circle cx="-20" cy="6" r="20" fill="#3c9580"/><circle cx="22" cy="2" r="22" fill="#3c9580"/>`;
  return svg(w, h, `
    ${rond(110, soleil, '#fff1c7')}${rond(290, gamelle, '#ffe0c7')}${rond(470, balle, '#e5f3d5')}${rond(650, lune, '#e8e0ff')}
    ${fleche(735, y, 815, y)}
    ${rond(920, arbre, '#d6efe8')}<g transform="translate(1080,${y})"><circle r="70" fill="#fbefe2"/>${friandise(0, -6, 1.6)}${etoiles(24, -40)}</g>`); })();

// 9. Chat + clicker + baguette de ciblage
S['chat-clicker'] = (() => { const w = 1200, h = 460, y = 420;
  const clicker = (x, yy) => `<g transform="translate(${x},${yy}) rotate(-20)"><rect x="-30" y="-20" width="60" height="40" rx="14" fill="#ffd23f" stroke="#c99a00" stroke-width="3"/><circle cx="6" cy="0" r="11" fill="#b44c1c"/></g>`;
  return svg(w, h, `${sol(y, w)}
    ${at(420, y, 1.15, chatAssis())}
    <line x1="820" y1="250" x2="560" y2="${y - 210}" stroke="#2b2420" stroke-width="7" stroke-linecap="round"/><circle cx="555" cy="${y - 212}" r="16" fill="#c9442f"/>
    ${mainSeule(860, 252, 1)}${clicker(930, 150)}
    <g stroke="#b44c1c" stroke-width="5" stroke-linecap="round"><path d="M965 110 l20 -18"/><path d="M975 135 l28 -4"/><path d="M955 92 l6 -24"/></g>
    ${etoiles(560, 140)}`); })();

// 10. Illustration d'accueil : chien et chat assis, complices
S['accueil'] = (() => { const w = 600, h = 480, y = 430;
  return svg(w, h, `<circle cx="300" cy="250" r="200" fill="#ffe0c7"/><circle cx="430" cy="140" r="60" fill="#d6efe8"/>${sol(y, w)}
    ${at(250, y, 1.3, P.chienAssis({ tete: -6 }))}${at(462, y, 1.15, chatAssis(), true)}
    ${coeur(340, 110, 1.8)}${etoiles(120, 120)}${etoiles(470, 60)}`, 'transparent'); })();

for (const [nom, contenu] of Object.entries(S)) { fs.writeFileSync(path.join(OUT, nom + '.svg'), contenu); }
console.log(Object.keys(S).length + ' illustrations écrites dans docs/img/illu/');
