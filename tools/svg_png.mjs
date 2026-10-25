// SVG -> saydam zeminli PNG (Chrome ile, kenar yumuşatmalı, büyük ölçekte).
//   node tools/svg_png.mjs ÖLÇEK GİRİŞ_KLASÖRÜ ÇIKIŞ_KLASÖRÜ
// Örn. ölçek 1.5: 720x960 SVG -> 1080x1440 PNG.
import { spawn } from 'node:child_process';
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync, mkdtempSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const [, , olcekS, giris, cikis] = process.argv;
const olcek = parseFloat(olcekS);
mkdirSync(cikis, { recursive: true });
const C = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profil = mkdtempSync(join(tmpdir(), 'svgpng-'));
const port = 9400 + Math.floor(Math.random() * 400);
const ch = spawn(C, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`, '--hide-scrollbars', 'about:blank']);
const bekle = ms => new Promise(r => setTimeout(r, ms));
await bekle(2500);
const sekme = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page');
const ws = new WebSocket(sekme.webSocketDebuggerUrl);
await new Promise(r => (ws.onopen = r));
let id = 0;
const bek = {};
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && bek[m.id]) { bek[m.id](m); delete bek[m.id]; } };
const gonder = (method, params = {}) => new Promise(r => { const i = ++id; bek[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await gonder('Page.enable');
await gonder('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
for (const f of readdirSync(giris).filter(f => f.endsWith('.svg')).sort()) {
  const svg = readFileSync(join(giris, f), 'utf8');
  const w = +svg.match(/width="(\d+)"/)[1], h = +svg.match(/height="(\d+)"/)[1];
  await gonder('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: olcek, mobile: false });
  await gonder('Page.navigate', { url: 'file://' + resolve(giris, f) });
  await bekle(700);
  const r = await gonder('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  writeFileSync(join(cikis, f.replace(/\.svg$/, '.png')), Buffer.from(r.result.data, 'base64'));
  console.log(f, '->', Math.round(w * olcek) + 'x' + Math.round(h * olcek));
}
await new Promise(r => { ch.on('exit', r); ch.kill(); });
try { rmSync(profil, { recursive: true, force: true }); } catch { /* Chrome geç kapanırsa geçici klasör kalır */ }
process.exit(0);
