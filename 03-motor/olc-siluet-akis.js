/** SILUET AKIS PURUZU olcumu (15 Eyl 2026).
 *
 *  Kullanici: "siluetin hareketlerine cok dikkat et, garip hareketler
 *  yapmasin". Bu arac kare kare siluet kutusunu okur ve ARDISIK KARELER
 *  ARASINDAKI DEGISIMI olcer. Akiskan hareket kucuk ve duzgun degisir;
 *  SICRAMA (klip atlamasi, ani aynalama, harman kesilmesi) tek karede
 *  buyuk bir fark olarak gorunur.
 *
 *  Cikti: her karenin farki + en buyuk sicramalar, o andaki cue ile birlikte.
 *
 *  node olc-siluet-akis.js --bolum ../bolumler/onizleme-elma.json --toplam 64
 *                          --bas 2380 --son 2820
 */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const KOK = path.resolve(__dirname, '..');
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.fbx':'application/octet-stream' };
const arg = (a, d) => { const i = process.argv.indexOf('--' + a); return i > -1 ? process.argv[i + 1] : d; };

(async () => {
  const BOLUM = arg('bolum', ''), TOPLAM = +arg('toplam', 64);
  const BAS = +arg('bas', 2380), SON = +arg('son', 2820);
  const s = http.createServer((q, r) => {
    const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(r);
  });
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', protocolTimeout: 1800000,
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 640, height: 360 });
  pg.on('pageerror', e => console.log('HATA:', e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=${TOPLAM}`
    + (BOLUM ? `&bolum=${encodeURIComponent(BOLUM)}` : ''), { waitUntil: 'load', timeout: 240000 });
  await pg.waitForFunction('window.HAZIR===true', { timeout: 300000 });

  const rapor = await pg.evaluate((BAS, SON) => {
    const T = window.__T, FPS = 30;
    const kg = document.createElement('canvas'); kg.width = 96; kg.height = 128;
    const g2 = kg.getContext('2d', { willReadFrequently: true });
    const oku = () => {
      const cv = window.__CIKIS, W = cv.width, H = cv.height;
      g2.clearRect(0, 0, 96, 128);
      g2.drawImage(cv, Math.round(W * 0.035), Math.round(H * 0.28), Math.round(W * 0.19), Math.round(H * 0.54), 0, 0, 96, 128);
      const d = g2.getImageData(0, 0, 96, 128).data;
      const m = new Uint8Array(96 * 128);
      let sx = 0, say = 0;
      for (let i = 0; i < 96 * 128; i++) {
        const q = i * 4;
        const v = (d[q] + d[q+1] + d[q+2] > 300) ? 1 : 0;
        m[i] = v; if (v) { sx += i % 96; say++; }
      }
      return { m, com: say ? (sx / say - 48) / 48 : 0, say };
    };
    const farkHesap = (a, b) => {
      let f = 0, t = 0;
      for (let i = 0; i < a.length; i++) { if (a[i] || b[i]) { t++; if (a[i] !== b[i]) f++; } }
      return t ? f / t : 0;
    };
    const cueAd = (t) => {
      const NN = T.NOTALAR;
      let lo = 0, hi = NN.length - 1, k = -1;
      while (lo <= hi) { const m = (lo + hi) >> 1; if (NN[m].bas <= t) { k = m; lo = m + 1; } else hi = m - 1; }
      if (k < 0) return '-';
      const n = NN[k];
      return (t < n.bas + n.pencere) ? n.tip : '-';
    };
    const kayit = [];
    let onceki = null;
    for (let n = BAS; n <= SON; n++) {
      window.kareKur(n);
      try { window.kareAl('png'); } catch (e) {}
      const r = oku();
      const fark = onceki ? farkHesap(onceki, r.m) : 0;
      kayit.push({ n, fark: +fark.toFixed(4), com: +r.com.toFixed(3), alan: r.say, cue: cueAd(n / FPS) });
      onceki = r.m;
    }
    return kayit;
  }, BAS, SON);

  fs.writeFileSync(path.join(KOK, '04-ciktilar', 'siluet-akis.json'), JSON.stringify(rapor));
  const f = rapor.map(x => x.fark).filter(x => x > 0);
  const ort = f.reduce((a, c) => a + c, 0) / f.length;
  const sirali = [...rapor].sort((a, b) => b.fark - a.fark).slice(0, 12);
  console.log('kare araligi', BAS, '-', SON, '| ortalama kare farki', ort.toFixed(4));
  console.log('EN BUYUK SICRAMALAR:');
  for (const x of sirali) console.log(`  kare ${x.n}  fark ${x.fark.toFixed(3)}  (ortalamanin ${(x.fark/ort).toFixed(1)} kati)  cue=${x.cue}  com=${x.com}`);
  await b.close(); s.close();
})();
