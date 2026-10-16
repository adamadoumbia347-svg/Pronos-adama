const P = require('./persos.js');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="1200" height="400"><rect width="1200" height="400" fill="#fffaf3"/>
<line x1="0" y1="350" x2="1200" y2="350" stroke="#eadfd3" stroke-width="4"/>
<g transform="translate(150,350)">${P.chienDebout()}</g>
<g transform="translate(420,350)">${P.chienAssis()}</g>
<g transform="translate(700,350)">${P.chienCouche()}</g>
<g transform="translate(1000,350)">${P.humain({bras:60})}</g></svg>`;
require('fs').writeFileSync(process.argv[2], svg);
