// Génère les images de partage (1200×630, og:image) et les épingles Pinterest (1000×1500)
// pour chaque page, dans les 3 langues. Usage : node tools/partage/rendu.js
// Sorties : docs/img/partage/<lang>-<page>.jpg et docs/img/pinterest/<lang>-<page>.jpg
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const DOCS = path.join(__dirname, '../../docs');
const EXCLUES = new Set(['404.html', 'mentions-legales.html']);
const PAR_DEFAUT = { 'conseils.html': 'laisse', 'materiel.html': 'harnais', 'index.html': 'accueil' };
const DOMAINE = 'educanimaux.fr';
const ACCROCHE = { fr: 'Méthodes douces · pas à pas', en: 'Gentle methods · step by step', it: 'Metodi dolci · passo dopo passo' };
const sansEmoji = t => t.replace(/[\u{1F000}-\u{1FFFF}\u{2600}-\u{27BF}\u{FE0F}\u{200D}]/gu, '').replace(/\s+/g, ' ').trim();
const dec = t => t.replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/<[^>]+>/g, '');

function pages() {
  const r = [];
  for (const [lang, dossier] of [['fr', ''], ['en', 'en'], ['it', 'it']]) {
    for (const f of fs.readdirSync(path.join(DOCS, dossier)).filter(f => f.endsWith('.html') && !EXCLUES.has(f)).sort()) {
      const s = fs.readFileSync(path.join(DOCS, dossier, f), 'utf8');
      const titre = sansEmoji(dec(s.match(/<h1[^>]*>([\s\S]*?)<\/h1>/)[1]));
      const illu = (s.match(/data-illu="([^"]+)"/) || [])[1] || PAR_DEFAUT[f] || 'accueil';
      r.push({ lang, f, titre, illu });
    }
  }
  return r;
}

const police = ['nunito-latin.woff2', 'nunito-latin-ext.woff2'].map(f => `@font-face{font-family:N;src:url(file://${DOCS}/fonts/${f});font-weight:200 1000}`).join('');
const css = `${police}*{margin:0;box-sizing:border-box}body{font-family:N,sans-serif;background:#fff7ee;color:#2b2420}
  .logo{font-weight:900;color:#2b2420}.logo span{color:#b44c1c}.patte{display:inline-block;width:.9em;height:.9em;border-radius:50%;background:#b44c1c;margin-right:.3em;vertical-align:-.05em}
  .pied{color:#6b5d52;font-weight:700}`;

function og(p) {
  const taille = p.titre.length > 60 ? 52 : p.titre.length > 40 ? 60 : 68;
  return `<html><head><style>${css}
  .w{width:1200px;height:630px;display:flex;flex-direction:column;padding:48px 60px;background:linear-gradient(135deg,#fff7ee 0%,#ffe9d6 100%)}
  h1{font-size:${taille}px;line-height:1.12;font-weight:900;margin:22px 0 auto;max-width:1080px}
  .bas{display:flex;align-items:flex-end;justify-content:space-between;gap:30px}
  .bas img{width:560px;border-radius:22px;border:2px solid #f0dcc8}
  .logo{font-size:38px}.pied{font-size:26px;margin-top:8px}</style></head><body><div class="w">
  <div class="logo"><i class="patte"></i>Éduc'<span>Animaux</span></div>
  <h1>${p.titre}</h1>
  <div class="bas"><div><div class="pied">${ACCROCHE[p.lang]}</div><div class="pied" style="color:#b44c1c">${DOMAINE}</div></div>
  <img src="file://${DOCS}/img/illu/${p.illu}.svg"></div></div></body></html>`;
}
function pin(p) {
  const taille = p.titre.length > 60 ? 70 : p.titre.length > 40 ? 80 : 92;
  return `<html><head><style>${css}
  .w{width:1000px;height:1500px;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly;text-align:center;padding:80px 70px;background:linear-gradient(180deg,#fff7ee 0%,#ffe2c8 100%)}
  .logo{font-size:48px}h1{font-size:${taille}px;line-height:1.1;font-weight:900}
  img{width:860px;border-radius:30px;border:3px solid #f0dcc8;background:#fffaf3}
  .bandeau{background:#b44c1c;color:#fff;font-weight:900;font-size:40px;padding:22px 46px;border-radius:60px}
  .pied{font-size:34px;margin-top:-50px}</style></head><body><div class="w">
  <div class="logo"><i class="patte"></i>Éduc'<span>Animaux</span></div>
  <h1>${p.titre}</h1><img src="file://${DOCS}/img/illu/${p.illu}.svg">
  <div class="bandeau">${DOMAINE}</div><div class="pied">${ACCROCHE[p.lang]}</div></div></body></html>`;
}

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const tmp = path.join(require('os').tmpdir(), 'partage.html');
  for (const [dossier, rendu, w, h] of [['partage', og, 1200, 630], ['pinterest', pin, 1000, 1500]]) {
    fs.mkdirSync(path.join(DOCS, 'img', dossier), { recursive: true });
    const page = await b.newPage({ viewport: { width: w, height: h } });
    for (const p of pages()) {
      fs.writeFileSync(tmp, rendu(p));
      await page.goto('file://' + tmp); await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: path.join(DOCS, 'img', dossier, `${p.lang}-${p.f.replace('.html', '')}.jpg`), type: 'jpeg', quality: 88 });
    }
  }
  await b.close();
  console.log(pages().length + ' images de partage et épingles Pinterest générées.');
})();
