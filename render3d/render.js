// Rend des images 3D avec three.js dans un Chrome sans écran (SwiftShader, donc sans carte graphique).
//   node render.js états.json dossier_sortie [début] [fin] [largeur] [hauteur]
const fs = require('fs'), path = require('path'), http = require('http');
const puppeteer = require('puppeteer-core');

const [, , statesFile, outDir, a0, a1, wArg, hArg] = process.argv;
const W = +(wArg || 1080), H = +(hArg || 1920);
const states = JSON.parse(fs.readFileSync(statesFile, 'utf8'));
const from = +(a0 || 0), to = Math.min(+(a1 || states.length), states.length);
const www = path.join(__dirname, 'www'), three = path.join(__dirname, 'node_modules', 'three', 'build');

function serve() {
  return new Promise((res) => {
    const s = http.createServer((q, r) => {
      const u = decodeURIComponent(q.url.split('?')[0]);
      const f = u.startsWith('/three/') ? path.join(three, u.slice(7)) : path.join(www, u === '/' ? 'index.html' : u);
      fs.readFile(f, (e, d) => {
        if (e) { r.writeHead(404); r.end(); return; }
        r.writeHead(200, { 'Content-Type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); r.end(d);
      });
    }).listen(0, '127.0.0.1', () => res(s));
  });
}
function chrome() {
  for (const p of [process.env.CHROME_PATH, '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser']) if (p && fs.existsSync(p)) return p;
  throw new Error('Chrome introuvable');
}
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const srv = await serve();
  const browser = await puppeteer.launch({
    executablePath: chrome(), headless: 'new',
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl', '--disable-dev-shm-usage', '--allow-file-access-from-files'],
  });
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.error('ERREUR PAGE', e.message));
  page.on('console', (m) => { const t = m.text(); if (/error|Error|THREE/.test(t) && !/GPU stall|PCFSoft/.test(t)) console.error('PAGE', t); });
  await page.setViewport({ width: W, height: H });
  await page.goto(`http://127.0.0.1:${srv.address().port}/index.html`);
  await page.waitForFunction('window.ready === true', { timeout: 60000 });
  await page.evaluate((w, h) => window.sm.init(w, h), W, H);
  const t0 = Date.now();
  for (let i = from; i < to; i++) {
    const url = await page.evaluate((s) => window.sm.draw(s), states[i]);
    fs.writeFileSync(path.join(outDir, `f${String(i).padStart(6, '0')}.jpg`), Buffer.from(url.split(',')[1], 'base64'));
    if ((i - from) % 50 === 49) console.log(`rendu 3D : ${i - from + 1}/${to - from} images (${((Date.now() - t0) / 1000 / (i - from + 1)).toFixed(2)} s/image)`);
  }
  await browser.close(); srv.close();
})().catch((e) => { console.error(e); process.exit(1); });
