// ------------------------------------------------------------ REF-067 YARDIMCILARI (motor 13)
// Piksel yazi: Titan kucuk boyutta cizilir, alfa esiklenir, en yakin komsu ile buyutulur (bloklu harf).
// Beyaz kontur + alt pembe golge + dikey pastel degrade. Kart boyunca sabit -> onbellek.
const PIKSEL = new Map();
function pikselYazi(metin, x, y, px, dolgu, alfa = 1, golge = '#c0168a', kontur = '#ffffff') {
  const P = Math.max(3, Math.round(px / 16)), fs = px / P, key = [metin, Math.round(px), dolgu.join(), golge, kontur].join('|');
  let c = PIKSEL.get(key);
  if (!c) {
    c = document.createElement('canvas');
    const g0 = c.getContext('2d'); g0.font = F(fs);
    const w = Math.ceil(g0.measureText(metin).width + fs * 1.2), h = Math.ceil(fs * 1.9);
    c.width = w; c.height = h;
    const g = c.getContext('2d'); g.font = F(fs); g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round';
    g.lineWidth = fs * 0.34; g.strokeStyle = golge; g.strokeText(metin, w / 2, h / 2 + fs * 0.16);
    g.strokeStyle = kontur; g.strokeText(metin, w / 2, h / 2);
    const gr = g.createLinearGradient(0, h / 2 - fs * 0.5, 0, h / 2 + fs * 0.5);
    dolgu.forEach((r, i) => gr.addColorStop(i / Math.max(1, dolgu.length - 1), r));
    g.fillStyle = gr; g.fillText(metin, w / 2, h / 2);
    const d = g.getImageData(0, 0, w, h);
    for (let i = 3; i < d.data.length; i += 4) d.data[i] = d.data[i] > 110 ? 255 : 0;
    g.putImageData(d, 0, 0);
    PIKSEL.set(key, c);
  }
  cx.save(); cx.globalAlpha *= kisit(alfa, 0, 1); cx.imageSmoothingEnabled = false;
  cx.drawImage(c, x - c.width * P / 2, y - c.height * P / 2, c.width * P, c.height * P);
  cx.restore();
}
// tam ekran kart zemini: mordan pembeye gecis + ince beyaz izgara + kenardan isinlar + 4 kollu parilti
function izgaraZemin(t) {
  const [a, b] = TEMA.izgara || ['#3a1a9a', '#c02ab0'];
  const g = cx.createLinearGradient(0, 0, W * 0.3, H); g.addColorStop(0, a); g.addColorStop(1, b);
  cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  cx.save(); cx.strokeStyle = 'rgba(255,255,255,0.13)'; cx.lineWidth = 2 * k;
  const A = 64 * k, ofs = (t * 24 * k) % A;
  for (let x = -A + ofs; x < W + A; x += A) { cx.beginPath(); cx.moveTo(x, 0); cx.lineTo(x, H); cx.stroke(); }
  for (let y = -A + ofs; y < H + A; y += A) { cx.beginPath(); cx.moveTo(0, y); cx.lineTo(W, y); cx.stroke(); }
  cx.globalCompositeOperation = 'lighter';
  for (const [x0, y0, yon] of [[0, 0, 1], [W, H, -1]]) for (let i = 0; i < 6; i++) {
    const ang = (yon > 0 ? 0.1 : Math.PI + 0.1) + i * 0.24 + Math.sin(t * 0.7 + i) * 0.03, L = W * 0.55;
    cx.fillStyle = 'rgba(255,255,255,0.05)'; cx.beginPath(); cx.moveTo(x0, y0);
    cx.lineTo(x0 + Math.cos(ang) * L, y0 + Math.sin(ang) * L); cx.lineTo(x0 + Math.cos(ang + 0.07) * L, y0 + Math.sin(ang + 0.07) * L); cx.closePath(); cx.fill();
  }
  cx.restore();
  for (let j = 0; j < 26; j++) {
    const r = rng(300 + j), x = r() * W, y = r() * H, f = r() * 6.28;
    parilti4(x, y, (8 + 14 * r()) * k, 0.25 + 0.6 * Math.max(0, Math.sin(t * 3 + f)));
  }
}
// beyaz zeminde oyuncu renginde iki kollu girdap (videonun poz karti; kapak-pvp-16.py ile ayni sekil)
function girdapKart(renk) {
  const w = 460, h = 520, c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'), d = g.createImageData(w, h), n = parseInt(renk.slice(1), 16), R = [n >> 16 & 255, n >> 8 & 255, n & 255];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = x - w / 2, dy = y - h * 0.55, r = Math.hypot(dx, dy) / Math.max(w, h), a = Math.atan2(dy, dx);
    const q = kisit((Math.sin(r * 18 + 2 * a) + 0.15) * 2.2, 0, 1) * 0.75, i = (y * w + x) * 4;
    for (let j = 0; j < 3; j++) d.data[i + j] = 255 * (1 - q) + R[j] * q;
    d.data[i + 3] = 255;
  }
  g.putImageData(d, 0, 0);
  return c;
}
const GIRDAP = (TEMA.girdap || ['#5ac8ff', '#ff7ad0']).map(girdapKart);

// KENDI maskotumuz (REF-067'deki salincaktaki anime kizin yerine; telif): yuvarlak pembe sakura ruhu, yaprak kulak, cicek tac
function maskotCiz(x, y, s, t, alfa = 1) {
  if (alfa <= 0.01) return;
  cx.save(); cx.globalAlpha *= alfa; cx.translate(x, y); cx.scale(s * k, s * k);
  const KON = '#5a1f86';
  cx.lineJoin = 'round'; cx.lineWidth = 5; cx.strokeStyle = KON;
  for (const sx of [-1, 1]) {                                   // yaprak kulaklar
    cx.save(); cx.translate(sx * 34, -48); cx.rotate(sx * (0.5 + 0.06 * Math.sin(t * 5)));
    cx.fillStyle = '#ff9ad8'; cx.beginPath(); cx.ellipse(0, -18, 15, 26, 0, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffd6f2'; cx.beginPath(); cx.ellipse(0, -16, 6, 15, 0, 0, 6.283); cx.fill(); cx.restore();
  }
  const gv = cx.createRadialGradient(-14, -20, 6, 0, 0, 70); gv.addColorStop(0, '#fff0fa'); gv.addColorStop(1, '#ffb4e4');
  cx.fillStyle = gv; cx.beginPath(); cx.ellipse(0, 0, 62, 56, 0, 0, 6.283); cx.fill(); cx.stroke();      // govde
  for (const sx of [-1, 1]) {                                   // kollar (salincak iplerini tutar)
    cx.fillStyle = '#ffc6ea'; cx.beginPath(); cx.ellipse(sx * 58, -6, 13, 17, sx * 0.4, 0, 6.283); cx.fill(); cx.stroke();
  }
  const kirp = (t % 3.4) < 0.12 ? 0.15 : 1;                   // goz kirpma
  for (const sx of [-1, 1]) {
    cx.fillStyle = '#2a0e4a'; cx.beginPath(); cx.ellipse(sx * 22, -6, 11, 15 * kirp, 0, 0, 6.283); cx.fill();
    if (kirp > 0.5) { cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 22 - 4, -12, 4.5, 0, 6.283); cx.fill(); cx.beginPath(); cx.arc(sx * 22 + 4, -1, 2, 0, 6.283); cx.fill(); }
    cx.fillStyle = 'rgba(255,90,170,0.45)'; cx.beginPath(); cx.ellipse(sx * 38, 14, 10, 6, 0, 0, 6.283); cx.fill();     // yanak
  }
  cx.strokeStyle = KON; cx.lineWidth = 4; cx.beginPath(); cx.arc(0, 10, 9, 0.2, Math.PI - 0.2); cx.stroke();          // gulumseme
  cx.save(); cx.translate(0, -58);                              // basta cicek
  for (let i = 0; i < 5; i++) { cx.save(); cx.rotate(i * 1.2566 + t * 0.6); cx.fillStyle = '#ffffff'; cx.beginPath(); cx.ellipse(0, -11, 7, 11, 0, 0, 6.283); cx.fill(); cx.lineWidth = 2.5; cx.stroke(); cx.restore(); }
  cx.fillStyle = '#ffd94a'; cx.beginPath(); cx.arc(0, 0, 6, 0, 6.283); cx.fill(); cx.restore();
  cx.restore();
}
// iki kapi arasinda salincak: ipler gokten iner, maskot vurusa hafif sallanir
function salincak(t, alfa) {
  const x0 = W / 2, y0 = H * 0.43, ac = Math.sin(t * Math.PI * BPM / 120) * 0.10, L = y0 + 30 * k;
  cx.save(); cx.globalAlpha *= alfa; cx.translate(x0, -30 * k); cx.rotate(ac);
  cx.strokeStyle = '#5a1f86'; cx.lineWidth = 5 * k;
  for (const sx of [-1, 1]) { cx.beginPath(); cx.moveTo(sx * 64 * k, 0); cx.lineTo(sx * 64 * k, L); cx.stroke(); }
  cx.fillStyle = '#ff7ad0'; cx.beginPath(); cx.roundRect(-84 * k, L - 6 * k, 168 * k, 18 * k, 8 * k); cx.fill(); cx.stroke();
  cx.restore();
  maskotCiz(x0 - Math.sin(ac) * (L - 30 * k), -30 * k + Math.cos(ac) * L - 52 * k, 1.05, t, alfa);
}
