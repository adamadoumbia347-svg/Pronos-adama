// node captures.js : captures pleine page du site (largeur téléphone) pour la vidéo de pub
const { chromium } = require('playwright');
const fs = require('fs');
const PAGES = { accueil: '/', chien: '/chien.html', rappel: '/rappel-chien.html', chat: '/chat.html',
  harnais: '/meilleur-harnais-chien.html', quiz: '/quiz.html', age: '/age-humain.html', nac: '/nac.html' };
(async () => {
  fs.mkdirSync(__dirname + '/captures', { recursive: true });
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2 });
  await p.route(/goatcounter|zgo\.at/, r => r.abort());
  for (const [nom, url] of Object.entries(PAGES)) {
    await p.goto('http://localhost:8766' + url, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `${__dirname}/captures/${nom}.jpg`, fullPage: true, quality: 85 });
  }
  // recherche ouverte avec « rappel »
  await p.goto('http://localhost:8766/', { waitUntil: 'networkidle' });
  await p.keyboard.press('/'); await p.waitForTimeout(400);
  await p.keyboard.type('rappel'); await p.waitForTimeout(800);
  await p.screenshot({ path: `${__dirname}/captures/recherche.jpg`, quality: 85 });
  await b.close();
})();
