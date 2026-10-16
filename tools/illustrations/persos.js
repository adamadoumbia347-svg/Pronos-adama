// Personnages vectoriels réutilisables (style plat). Chaque fonction renvoie un fragment SVG,
// dessiné dans un repère local ; on le place avec transform="translate(x,y) scale(s)".
const C = { pelage: "#d99a5b", fonce: "#a8692f", clair: "#f6dcbc", nez: "#2b2420", peau: "#f1c7a3", habit: "#2f7d6d", pantalon: "#3d4a63", cheveux: "#4a3426", chat: "#8a8f99", chatF: "#5d626b", chatC: "#d9dce2" };

// Tête de chien tournée vers la droite, centrée sur (0,0)
function teteChien(rot = 0) {
  return `<g transform="rotate(${rot})">
    <ellipse cx="-6" cy="-2" rx="34" ry="30" fill="${C.pelage}"/>
    <ellipse cx="26" cy="10" rx="24" ry="16" fill="${C.clair}"/>
    <ellipse cx="44" cy="4" rx="8" ry="6.5" fill="${C.nez}"/>
    <path d="M30 20 q8 6 16 0" stroke="${C.nez}" stroke-width="3" fill="none" stroke-linecap="round"/>
    <circle cx="8" cy="-10" r="5" fill="${C.nez}"/><circle cx="9.5" cy="-11.5" r="1.6" fill="#fff"/>
    <path d="M-24 -24 q-22 6 -18 44 q12 6 20 -10 z" fill="${C.fonce}"/>
  </g>`;
}
function queue(x, y, rot) {
  return `<path transform="translate(${x},${y}) rotate(${rot})" d="M0 0 q-10 -30 -34 -38" stroke="${C.pelage}" stroke-width="11" fill="none" stroke-linecap="round"/>`;
}
function patte(x, y, h, w = 15, rot = 0, col = C.pelage) {
  return `<rect transform="translate(${x},${y}) rotate(${rot})" x="${-w / 2}" y="0" width="${w}" height="${h}" rx="${w / 2}" fill="${col}"/>
          `;
}
// Chien debout (de profil, regarde à droite). Origine : sol, sous le milieu du corps.
function chienDebout(opts = {}) {
  const t = opts.tete || 0, q = opts.queue ?? -10;
  return `<g>
    ${queue(-62, -78, q)}
    ${patte(-48, -60, 60, 16, 0, C.fonce)}${patte(34, -60, 60, 16, 0, C.fonce)}
    <ellipse cx="0" cy="-78" rx="72" ry="34" fill="${C.pelage}"/>
    <ellipse cx="30" cy="-70" rx="34" ry="22" fill="${C.clair}" opacity=".55"/>
    ${patte(-32, -62, 62)}${patte(50, -62, 62)}
    <rect x="44" y="-128" width="30" height="50" rx="14" fill="${C.pelage}" transform="rotate(18 59 -103)"/>
    <g transform="translate(78,-128)">${teteChien(t)}</g>
  </g>`;
}
// Chien assis
function chienAssis(opts = {}) {
  const t = opts.tete ?? -8;
  return `<g>
    ${queue(-44, -14, 70)}
    <ellipse cx="-14" cy="-38" rx="42" ry="38" fill="${C.pelage}"/>
    <ellipse cx="-30" cy="-6" rx="30" ry="9" fill="${C.fonce}"/>
    <ellipse cx="18" cy="-86" rx="34" ry="58" fill="${C.pelage}" transform="rotate(16 18 -86)"/>
    <ellipse cx="32" cy="-92" rx="18" ry="36" fill="${C.clair}" opacity=".6" transform="rotate(16 32 -92)"/>
    ${patte(28, -70, 70)}${patte(48, -66, 66, 15, 0, C.fonce)}
    <g transform="translate(46,-150)">${teteChien(t)}</g>
  </g>`;
}
// Chien couché
function chienCouche(opts = {}) {
  const t = opts.tete ?? 0;
  return `<g>
    ${queue(-80, -22, 100)}
    <ellipse cx="-8" cy="-34" rx="80" ry="32" fill="${C.pelage}"/>
    <ellipse cx="-48" cy="-24" rx="36" ry="24" fill="${C.pelage}"/>
    <ellipse cx="-50" cy="-6" rx="34" ry="8" fill="${C.fonce}"/>
    ${patte(40, -16, 64, 15, -90)}${patte(46, -6, 62, 15, -90, C.fonce)}
    <ellipse cx="44" cy="-48" rx="26" ry="30" fill="${C.pelage}"/>
    <g transform="translate(70,-92)">${teteChien(t)}</g>
  </g>`;
}
// Humain debout (regarde à droite) ; brasD : angle du bras avant (0 = le long du corps, 90 = tendu devant)
function humain(opts = {}) {
  const b = opts.bras ?? 30, b2 = opts.bras2 ?? 10, pas = opts.pas ?? 0;
  return `<g>
    <rect x="-22" y="-120" width="18" height="120" rx="9" fill="${C.pantalon}" transform="rotate(${-pas} -13 -120)"/>
    <rect x="2" y="-120" width="18" height="120" rx="9" fill="${C.pantalon}" transform="rotate(${pas} 11 -120)"/>
    <ellipse cx="-14" cy="-2" rx="18" ry="7" fill="${C.nez}" transform="rotate(${-pas * 0.0} -14 -2)"/><ellipse cx="14" cy="-2" rx="18" ry="7" fill="${C.nez}"/>
    <rect x="-16" y="-218" width="16" height="78" rx="8" fill="${C.habit}" transform="rotate(${-b2} -8 -212)"/>
    <rect x="-30" y="-232" width="60" height="118" rx="26" fill="${C.habit}"/>
    <rect x="2" y="-218" width="16" height="80" rx="8" fill="${C.habit}" transform="rotate(${-b} 10 -212)"/>
    <circle cx="${10 + 76 * Math.sin(b * Math.PI / 180)}" cy="${-212 + 76 * Math.cos(b * Math.PI / 180)}" r="10" fill="${C.peau}"/>
    <rect x="-8" y="-250" width="16" height="22" rx="6" fill="${C.peau}"/>
    <circle cx="2" cy="-272" r="28" fill="${C.peau}"/>
    <path d="M-27 -276 q4 -32 34 -26 q20 4 20 22 q-14 -10 -34 -6 q-8 4 -20 10z" fill="${C.cheveux}"/>
    <circle cx="16" cy="-272" r="3.4" fill="${C.nez}"/>
    <path d="M14 -258 q8 4 14 -2" stroke="${C.nez}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  </g>`;
}
// position de la main avant d'un humain placé en (x,y) avec un bras à l'angle b
function main(x, y, b, s = 1) { return [x + s * (10 + 76 * Math.sin(b * Math.PI / 180)), y + s * (-212 + 76 * Math.cos(b * Math.PI / 180))]; }
module.exports = { C, chienDebout, chienAssis, chienCouche, humain, main, teteChien };
