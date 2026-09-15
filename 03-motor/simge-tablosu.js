/** TUM cue piktogramlarini tek sayfada gosterir - kutuphane kontrolu.
 *  node simge-tablosu.js ../04-ciktilar/simge-tablosu.png
 *
 *  simge-sayfasi.js yedi cue'luk sabit bir liste ciziyordu (kapak icin yazilmis).
 *  Bu dosya CUE tablosunun TAMAMINI motordan okuyup diziyor; yeni bir cue
 *  eklenince listeyi elle guncellemek gerekmiyor.
 */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const KOK = path.resolve(__dirname, '..');
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
               '.fbx': 'application/octet-stream', '.png': 'image/png' };
(async () => {
  const CIKTI = path.resolve(process.argv[2] || '../04-ciktilar/simge-tablosu.png');
  const s = http.createServer((q, r) => {
    const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(r);
  });
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 1400, height: 900 });
  pg.on('pageerror', e => console.log('HATA:', e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b`,
                { waitUntil: 'load', timeout: 180000 });
  await pg.waitForFunction('window.HAZIR===true', { timeout: 240000 });

  const veri = await pg.evaluate(() => {
    // Ayni klibin L/R ciftinden bir tanesi yeter - tablo sisirmesin.
    const atla = new Set(['step_R', 'dodge_L', 'wave_L', 'reach_R', 'kick_R', 'side_R', 'twist_R']);
    const tipler = Object.keys(window.__CUE || {}).filter(t => !atla.has(t));
    const SUT = 6, KUT = 210, SAT = Math.ceil(tipler.length / SUT);
    const W = SUT * KUT, H = SAT * 230 + 20;
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d');
    g.fillStyle = '#0b0618'; g.fillRect(0, 0, W, H);
    tipler.forEach((t, i) => {
      const sx = (i % SUT) * KUT + KUT / 2, sy = Math.floor(i / SUT) * 230 + 110;
      g.save(); g.translate(sx, sy);
      g.strokeStyle = '#22e0e8'; g.fillStyle = '#22e0e8';
      window.insanSimge(g, t, 0.88, 11); g.restore();
      g.fillStyle = '#ffffff'; g.font = '700 14px Arial'; g.textAlign = 'center';
      g.fillText(t, sx, sy + 96);
      g.fillStyle = '#8fa0c0'; g.font = '400 12px Arial';
      g.fillText(window.__CUE[t].klip, sx, sy + 114);
    });
    return { png: c.toDataURL('image/png'), sayi: tipler.length };
  });
  fs.writeFileSync(CIKTI, Buffer.from(veri.png.split(',')[1], 'base64'));
  console.log('cue sayisi (L/R ciftleri tekilenmis):', veri.sayi);
  console.log('->', CIKTI);
  await b.close(); s.close();
})();
