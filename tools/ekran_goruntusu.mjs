// Web sürümünden telefon boyutunda (412x880) ekran görüntüsü alır (Chrome DevTools, gerçek zamanlı bekler).
//   node tools/ekran_goruntusu.mjs ÇIKIŞ_KLASÖRÜ "http://localhost:8765/?...|x,y|x,y" ...
// Her URL için ÇIKIŞ/shot_N.png yazar; '|x,y' ile sayfa yüklendikten sonra o noktalara dokunur.
// macOS'ta Google Chrome yolu sabittir; başka sistemde C değişkenini değiştir.
import { spawn } from 'node:child_process';
import { writeFileSync, rmSync } from 'node:fs';
const [,, out, ...urls] = process.argv;
const C = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
rmSync(out + '/prof', { recursive: true, force: true });
const ch = spawn(C, ['--headless=new', '--remote-debugging-port=9333', '--user-data-dir=' + out + '/prof', '--window-size=412,880', '--force-device-scale-factor=1', 'about:blank']);
const sleep = ms => new Promise(r => setTimeout(r, ms));
await sleep(2500);
const tabs = await (await fetch('http://127.0.0.1:9333/json')).json();
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = {};
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m.result); delete pend[m.id]; } };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send('Emulation.setDeviceMetricsOverride', { width: 412, height: 880, deviceScaleFactor: 1, mobile: true });
for (let k = 0; k < urls.length; k++) {
  const [u, ...tik] = urls[k].split("|"); await send("Page.navigate", { url: u });
  await sleep(14000); for (const t of tik) { const [x, y] = t.split(",").map(Number); for (const type of ["mousePressed", "mouseReleased"]) await send("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 }); await sleep(2500); }
  const r = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${out}/shot_${k}.png`, Buffer.from(r.data, 'base64'));
}
ch.kill();
process.exit(0);
