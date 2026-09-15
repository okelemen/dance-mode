/** ENGEL <-> SILUET ESLESMESI olcumu (15 Eyl 2026).
 *
 *  Kullanici: "engellerle siluetin hareketleri birbirini tutmuyor".
 *  Bu arac vurus aninda IKISINI birden okur:
 *    - engel nerede?  (nota kutusunun z'si; vurus cizgisi Z_VURUS = 4)
 *    - siluet hangi fazda? (calan aksiyonun klip zamani -> dongu ici faz)
 *  ve beklenen tepe faziyla karsilastirir.
 *
 *  node olc-eslesme.js --bolum ../bolumler/test-elma-cesit.json --toplam 32
 */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const KOK = path.resolve(__dirname, '..');
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.fbx':'application/octet-stream' };
const arg = (a, d) => { const i = process.argv.indexOf('--' + a); return i > -1 ? process.argv[i + 1] : d; };

(async () => {
  const BOLUM = arg('bolum', ''), TOPLAM = +arg('toplam', 32);
  const s = http.createServer((q, r) => {
    const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(r);
  });
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 640, height: 360 });
  pg.on('pageerror', e => console.log('HATA:', e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=${TOPLAM}`
    + (BOLUM ? `&bolum=${encodeURIComponent(BOLUM)}` : ''), { waitUntil: 'load', timeout: 240000 });
  await pg.waitForFunction('window.HAZIR===true', { timeout: 300000 });

  const rapor = await pg.evaluate(() => {
    const T = window.__T, NN = T.NOTALAR, FPS = 30;
    const cikti = [];
    for (let i = 0; i < NN.length; i++) {
      const n = NN[i];
      if (!n.klip || n.tip.startsWith('step')) continue;
      const kare = Math.round(n.t * FPS);
      window.kareKur(kare);
      // __CIKIS yalnizca kareAl cagrilinca boyaniyor; siluet kutusunu
      // okuyabilmek icin kareyi bir kez birlestiriyoruz.
      try { window.kareAl('png'); } catch (e) {}
      // Calan aksiyon: agirligi en yuksek olan
      let ad = null, enW = -1, zaman = 0, sure = 0;
      for (const [k, v] of Object.entries(T.aksiyon)) {
        const w = v.a.getEffectiveWeight ? v.a.getEffectiveWeight() : (v.a.weight || 0);
        if (v.a.enabled && w > enW) { enW = w; ad = k; zaman = v.a.time; sure = v.klip.duration; }
      }
      // Engelin z'si: nota kutusu
      let z = null;
      const m = T.notaMesh && T.notaMesh[i];
      if (m) z = +m.position.z.toFixed(2);
      // SILUET KUTUSUNDAKI FIGURUN YATAY MERKEZI: figur hangi yana gidiyor?
      // Kutu HUD'da sol ustte; __CIKIS uzerinden okunuyor.
      let com = null, en = null;
      try {
        const cv = window.__CIKIS, W = cv.width, H = cv.height;
        const kg = document.createElement('canvas'); kg.width = 200; kg.height = 320;
        const g2 = kg.getContext('2d', { willReadFrequently: true });
        // panel: kadrajin %2-%25 yatay, %24-%87 dikey (olc-mekan.py ile ayni)
        g2.drawImage(cv, Math.round(W*0.03), Math.round(H*0.27), Math.round(W*0.20), Math.round(H*0.56), 0, 0, 200, 320);
        const dd = g2.getImageData(0, 0, 200, 320).data;
        let sx = 0, say = 0, minx = 999, maxx = -1;
        for (let y = 0; y < 320; y++) for (let x = 0; x < 200; x++) {
          const q = (y * 200 + x) * 4;
          if (dd[q] + dd[q+1] + dd[q+2] > 300) { sx += x; say++; if (x < minx) minx = x; if (x > maxx) maxx = x; }
        }
        if (say > 50) { com = +((sx / say - 100) / 100).toFixed(3); en = maxx - minx; }
      } catch (e) {}
      cikti.push({
        i, tip: n.tip, klip: n.klip, t: +n.t.toFixed(2), kare, com, en,
        calan: ad, agirlik: +enW.toFixed(2),
        klipZaman: +zaman.toFixed(2), klipSure: +sure.toFixed(2),
        z,
      });
      if (cikti.length >= 40) break;
    }
    return { ZV: 4, cikti };
  });

  console.log(JSON.stringify(rapor, null, 1));
  fs.writeFileSync(path.join(KOK, '04-ciktilar', 'eslesme.json'), JSON.stringify(rapor, null, 1));
  await b.close(); s.close();
})();
