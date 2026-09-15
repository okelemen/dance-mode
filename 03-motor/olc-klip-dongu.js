/** Klibin DONGU uzunlugunu olcer: hareket kac saniyede bir tekrar ediyor?
 *
 *  Neden gerekli (15 Eyl 2026, kullanici: "siluette cok garip hareketlilikler
 *  var"): olc-tempo.js charleston klibinin 20,90 sn oldugunu ve 1,81 sn'lik
 *  cue penceresine sigdirildigini olctu - hareket 11,5 KAT hizlaniyor. Sebep
 *  klibin uzun olmasi degil, TEKRARLI olmasi: icinde ayni dans dongusu
 *  defalarca var. Pencereye klibin TAMAMI degil BIR DONGUSU sigdirilmali.
 *
 *  Yontem: klip N faza bolunur, her fazda siluet maskesi alinir (kucultulmus
 *  ikili maske), sonra faz kaymalari icin ortalama fark hesaplanir. Farkin en
 *  dusuk oldugu kayma = dongu uzunlugu. Goz karari yok.
 *
 *  node olc-klip-dongu.js --klipler charleston,side-to-side,raise-roof,jacks
 */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const KOK = path.resolve(__dirname, '..');
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.fbx':'application/octet-stream' };
const arg = (a, d) => { const i = process.argv.indexOf('--' + a); return i > -1 ? process.argv[i + 1] : d; };

(async () => {
  const KLIPLER = arg('klipler', 'charleston,side-to-side,raise-roof,jacks').split(',');
  const N = +arg('n', 96);
  const s = http.createServer((q, r) => {
    const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(r);
  });
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const pg = await b.newPage();
  await pg.setViewport({ width: 640, height: 360 });
  pg.on('pageerror', e => console.log('HATA:', e.message));
  await pg.goto(`http://127.0.0.1:${s.address().port}/03-motor/sahne.html?w=640&h=360&tema=b&toplam=64`,
    { waitUntil: 'load', timeout: 240000 });
  await pg.waitForFunction('window.HAZIR===true', { timeout: 300000 });

  const sonuc = await pg.evaluate(async (KLIPLER, N) => {
    const cv = document.createElement('canvas'); cv.width = 48; cv.height = 64;
    const g = cv.getContext('2d', { willReadFrequently: true });
    const maskeAl = (veri) => new Promise(res => {
      const im = new Image();
      im.onload = () => {
        g.clearRect(0, 0, 48, 64); g.drawImage(im, 0, 0, 48, 64);
        const d = g.getImageData(0, 0, 48, 64).data;
        // OZELLIK: satir bazli GENISLIK PROFILI (her satirda soldan saga
        // uzanim). Siluet KONTUR olarak ciziliyor, ici bos - piksel ortusmesi
        // olcmek butun ciftleri 0,8'in ustunde gosteriyordu (olc-iou.py'de
        // belgelenen ayni tuzak). Uzanim profili bosluktan etkilenmiyor.
        const prof = new Float32Array(64);
        for (let y = 0; y < 64; y++) {
          let sol = -1, sag = -1;
          for (let x = 0; x < 48; x++) {
            const i = (y * 48 + x) * 4;
            if (d[i + 3] > 90 && (d[i] + d[i+1] + d[i+2]) > 150) { if (sol < 0) sol = x; sag = x; }
          }
          prof[y] = sol < 0 ? 0 : (sag - sol + 1) / 48;
        }
        res(prof);
      };
      im.onerror = () => res(null);
      im.src = veri;
    });
    const out = {};
    for (const ad of KLIPLER) {
      const aks = window.__T.aksiyon[ad];
      if (!aks) { out[ad] = { hata: 'klip yok' }; continue; }
      const sure = aks.klip.duration;
      const maskeler = [];
      for (let i = 0; i < N; i++) {
        const veri = window.siluetKaresi(ad, i / N, 240, 320);
        maskeler.push(veri ? await maskeAl(veri) : null);
      }
      const fark = (a, b) => {
        if (!a || !b) return 1;
        let f = 0;
        for (let i = 0; i < a.length; i++) f += Math.abs(a[i] - b[i]);
        return f / a.length;
      };
      // Her kayma icin ortalama fark. Kayma 0 disarida; en dusuk fark = dongu.
      const skor = [];
      for (let k = 2; k <= Math.floor(N / 2); k++) {
        let toplam = 0, say = 0;
        for (let i = 0; i + k < N; i++) { toplam += fark(maskeler[i], maskeler[i + k]); say++; }
        skor.push({ kayma: k, fark: toplam / say });
      }
      // Egrinin TAMAMI disari veriliyor; dongu secimi disarida yapiliyor.
      // En dusuk fark HER ZAMAN en kucuk kaymadir (komsu kareler benzer) -
      // aranan sey ilk BELIRGIN YEREL MINIMUM.
      out[ad] = {
        sure: +sure.toFixed(2),
        egri: skor.map(x => +x.fark.toFixed(4)),
        k0: 2,
        N: N,
      };
    }
    return out;
  }, KLIPLER, N);

  console.log(JSON.stringify(sonuc, null, 1));
  fs.writeFileSync(path.join(KOK, '04-ciktilar', 'klip-dongu.json'), JSON.stringify(sonuc, null, 1));
  await b.close(); s.close();
})();
