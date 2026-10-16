const { chromium } = require('playwright');
const [,, idx, mode, out, fichier = 'serie.json'] = process.argv;
const cfg = require(require('path').resolve(__dirname, fichier))[+idx];
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/serie.html');
  await p.evaluate(c => setup(c), cfg);
  await p.evaluate(() => document.fonts.ready);
  const times = mode === 'preview' ? [0, 4.3, 7.5, 11.7, 15.9, 21] : Array.from({length: 660}, (_, i) => i / 30);
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => render(t), times[i]);
    await p.screenshot({ path: `${out}/${mode === 'preview' ? 'p' : 'f'}${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
