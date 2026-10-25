// node rendu.js <fichier.html> <dossier> [preview]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [,, fichier, out, mode] = process.argv;
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(__dirname, fichier));
  await p.evaluate(() => document.fonts.ready);
  // Modèles 3D : attendre que les textures soient prêtes (window.PRET)
  await p.waitForFunction(() => window.PRET !== false, null, { timeout: 120000 });
  const { D, sons } = await p.evaluate(() => ({ D: window.DUREE, sons: window.SONS }));
  fs.writeFileSync(path.join(out, 'sons.json'), JSON.stringify({ duree: D, sons }));
  const times = mode === 'preview' ? [0.2, D*0.2, D*0.4, D*0.6, D*0.8, D-0.3] : Array.from({length: Math.round(D*30)}, (_, i) => i / 30);
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => render(t), times[i]);
    await p.screenshot({ path: `${out}/${mode === 'preview' ? 'p' : 'f'}${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
