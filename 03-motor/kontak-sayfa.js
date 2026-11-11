/** Kare kontrolu (yerel, md. 9 serbest): bir motor sayfasindan verilen saniyelerdeki kareleri alir, kontak sayfasi yapar.
 *  node kontak-sayfa.js --sayfa sahne21.html --bolum /bolumler/tetris-mode-24.json --t "1,2.8,4.7" --sutun 3 --w 1280 --h 720 --cikti x.jpg
 *  HUMAN TETRIS 24 (11 Kas 2026): motor 21'in acilis / duvar / OUT / kart karelerini render oncesi gormek icin. */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const KOK = path.resolve(__dirname, '..');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.ttf': 'font/ttf' };
const arg = (a, d) => { const i = process.argv.indexOf('--' + a); return i > -1 ? process.argv[i + 1] : d; };

(async () => {
  const W = +arg('w', 1280), H = +arg('h', 720), SUTUN = +arg('sutun', 3), OLC = +arg('olcek', 0.5);
  const T = arg('t', '1').split(',').map(Number);
  const CIKTI = path.resolve(arg('cikti', 'kontak.jpg'));
  const s = http.createServer((q, r) => {
    const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
    if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(r);
  });
  await new Promise(r => s.listen(0, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const pg = await b.newPage();
  await pg.setViewport({ width: W, height: H });
  pg.on('pageerror', e => console.log('HATA:', e.message));
  const KOK_URL = arg('url', `http://127.0.0.1:${s.address().port}`);   // --url http://127.0.0.1:8765 : calisan statik sunucu (cok dosyada node sunucusu fetch hatasi verdi)
  await pg.goto(`${KOK_URL}/03-motor/${arg('sayfa', 'sahne21.html')}?w=${W}&h=${H}&bolum=${encodeURIComponent(arg('bolum', ''))}`);
  await pg.waitForFunction('window.HAZIR === true', { timeout: 180000 });
  const veri = await pg.evaluate((T, SUTUN, OLC) => {
    const c = document.getElementById('cikti'), cw = c.width * OLC, ch = c.height * OLC, sat = Math.ceil(T.length / SUTUN);
    const k = Object.assign(document.createElement('canvas'), { width: cw * SUTUN, height: ch * sat }), g = k.getContext('2d');
    T.forEach((t, i) => {
      window.kareKur(Math.round(t * 30));
      const x = (i % SUTUN) * cw, y = Math.floor(i / SUTUN) * ch;
      g.drawImage(c, x, y, cw, ch);
      g.fillStyle = '#000'; g.fillRect(x, y, 70, 22); g.fillStyle = '#ff0'; g.font = '16px sans-serif'; g.fillText(t.toFixed(2), x + 4, y + 16);
    });
    return k.toDataURL('image/jpeg', 0.88);
  }, T, SUTUN, OLC);
  fs.writeFileSync(CIKTI, Buffer.from(veri.split(',')[1], 'base64'));
  console.log('->', CIKTI, T.length, 'kare');
  await b.close(); s.close();
})();
