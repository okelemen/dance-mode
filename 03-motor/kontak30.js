// HT30 yerel kare kontrolu: kontak-sayfa.js headless'ta HAZIR'a ulasmiyordu -> python http.server + headless:false (pencere disi) + elle yoklama
const fs = require('fs'), path = require('path'); const puppeteer = require('puppeteer-core');
const arg = (a, d) => { const i = process.argv.indexOf('--' + a); return i > -1 ? process.argv[i + 1] : d; };
(async () => {
  const T = arg('t', '1').split(',').map(Number), SUTUN = +arg('sutun', 3), OLC = +arg('olcek', 0.5);
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: false,
    args: ['--window-position=-3000,0', '--window-size=1300,800', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'], protocolTimeout: 900000 });
  const pg = await b.newPage(); await pg.setViewport({ width: 1280, height: 720 });
  pg.on('pageerror', e => console.log('HATA:', e.message)); pg.on('requestfailed', q => console.log('DUSTU:', q.url(), q.failure() && q.failure().errorText)); pg.on('response', r => { if (r.status() >= 400) console.log('YANIT', r.status(), r.url()); });
  await pg.goto(`http://127.0.0.1:8765/03-motor/${arg('sayfa')}?w=1280&h=720&bolum=${encodeURIComponent(arg('bolum'))}`);
  for (let i = 0; i < 300; i++) { if (await pg.evaluate('window.HAZIR === true')) break; await new Promise(r => setTimeout(r, 1000)); }
  const veri = await pg.evaluate((T, SUTUN, OLC) => {
    const c = document.getElementById('cikti'), cw = c.width * OLC, ch = c.height * OLC, sat = Math.ceil(T.length / SUTUN);
    const k = Object.assign(document.createElement('canvas'), { width: cw * SUTUN, height: ch * sat }), g = k.getContext('2d');
    T.forEach((t, i) => { window.kareKur(Math.round(t * 30)); const x = (i % SUTUN) * cw, y = Math.floor(i / SUTUN) * ch;
      g.drawImage(c, x, y, cw, ch); g.fillStyle = '#000'; g.fillRect(x, y, 70, 22); g.fillStyle = '#ff0'; g.font = '16px sans-serif'; g.fillText(t.toFixed(2), x + 4, y + 16); });
    return k.toDataURL('image/jpeg', 0.88);
  }, T, SUTUN, OLC);
  fs.writeFileSync(path.resolve(arg('cikti')), Buffer.from(veri.split(',')[1], 'base64')); console.log('->', arg('cikti'), T.length); await b.close();
})();
