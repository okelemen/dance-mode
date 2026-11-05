// ------------------------------------------------------------ REF-069 YARDIMCILARI (motor 15, neon yildiz sahnesi, CO-OP cift)
// sahne14 (galaksi) uzerine TEMA.yildiz bayragi: gok parlamasi, kapi ekraninda sonuk neon cift tabelasi, renkli DAMALI duvar karti + siyah
// cift silueti (yaklasinca P1/P2 renginde neon kontur), sarı 3-2-1, ust ilerleme cubugu (Start -> kupa) + kapi ustunde level etiketi,
// pastel izgarali tam ekran kartlar, SUBSCRIBE altinda LIKE / COMMENT / SHARE (Masaustu md. 27), kendi maskotumuz yildiz kiyafetiyle.
const KARE_RENK = TEMA.kareRenk || [['#ffc06a', '#ff8a1a'], ['#a8ff8a', '#2ad84a'], ['#ffa8ec', '#ff2ad0'], ['#fff27a', '#ffc21a'],
  ['#a8f6ff', '#1ad0ff'], ['#ffa0a0', '#ff3a4a'], ['#dcaaff', '#9a3aff']];

function yildiz5(x, y, r, renk, t = 0, kontur = null) {
  cx.save(); cx.translate(x, y); cx.rotate(0.15 * Math.sin(t * 3 + x));
  cx.beginPath();
  for (let q = 0; q <= 10; q++) { const a = -Math.PI / 2 + q * Math.PI / 5, rr = q % 2 ? r * 0.45 : r; q ? cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : cx.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  cx.closePath(); cx.fillStyle = renk; cx.fill();
  if (kontur) { cx.lineWidth = Math.max(2, r * 0.18); cx.strokeStyle = kontur; cx.lineJoin = 'round'; cx.stroke(); }
  cx.restore();
}

// gok: Blender gogunun ustunde goz kirpan kare (piksel) yildizlar + arti isiltilar + ara ara kayan yildiz (ekran dolu, hareketli gok)
function yildizGok(t) {
  cx.save(); cx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 120; i++) {
    const r = rng(9100 + i * 41), x = W * r(), y = H * 0.5 * r(), f = r() * 6.28, h = 0.8 + r() * 2.4;
    const a = 0.15 + 0.85 * Math.max(0, Math.sin(t * h + f)) ** 3, R = (2 + r() * 3) * k;
    cx.fillStyle = hex(['#ffffff', '#ff9ae8', '#9af4ff', '#fff27a'][i % 4], a); cx.fillRect(x - R / 2, y - R / 2, R, R);
    if (i % 8 === 0) parilti4(x, y, (12 + 10 * r()) * k, a * 0.9);
  }
  const n = Math.floor(t / 3.1), q = t / 3.1 - n;
  if (q < 0.2) {
    const r = rng(8800 + n * 11), x0 = W * (0.15 + 0.7 * r()), y0 = H * (0.03 + 0.18 * r()), ang = 0.3 + 0.3 * r(), p = q / 0.2;
    const L = 240 * k, x = x0 + Math.cos(ang) * 480 * k * p, y = y0 + Math.sin(ang) * 480 * k * p;
    const g = cx.createLinearGradient(x, y, x - Math.cos(ang) * L, y - Math.sin(ang) * L);
    g.addColorStop(0, `rgba(255,255,255,${0.95 * (1 - p)})`); g.addColorStop(1, 'rgba(255,150,230,0)');
    cx.strokeStyle = g; cx.lineWidth = 4 * k; cx.lineCap = 'round';
    cx.beginPath(); cx.moveTo(x, y); cx.lineTo(x - Math.cos(ang) * L, y - Math.sin(ang) * L); cx.stroke();
  }
  cx.restore();
}

function duvarEvre(t) {
  const d = DUVARLAR.find(x => t >= x.t0 && t < x.t0 + Z.sure);
  return d ? evre(t - d.t0).ad : 'yok';
}
// REF-069: kapinin ekrani; duvar gelmeden sonuk, titreyen neon cift tabelasi (bizim cizimimiz: el ele iki figur + kalp, P1 solda P2 sagda)
function kapiEkran(t) {
  const A = aciklik();
  cx.save();
  const g = cx.createLinearGradient(0, A.y, 0, A.y + A.h); g.addColorStop(0, '#1a1258'); g.addColorStop(1, '#0a0828');
  cx.fillStyle = g; cx.fillRect(A.x, A.y, A.w, A.h);
  cx.strokeStyle = 'rgba(140,150,255,0.14)'; cx.lineWidth = 1.5 * k;
  for (let x = A.x; x < A.x + A.w; x += A.w / 18) { cx.beginPath(); cx.moveTo(x, A.y); cx.lineTo(x, A.y + A.h); cx.stroke(); }
  for (let y = A.y; y < A.y + A.h; y += A.w / 18) { cx.beginPath(); cx.moveTo(A.x, y); cx.lineTo(A.x + A.w, y); cx.stroke(); }
  const ev = duvarEvre(t);
  if (ev === 'kart' || ev === 'bos' || ev === 'yok') {
    const tit = 0.35 + 0.4 * Math.abs(Math.sin(t * 7) * Math.sin(t * 2.3)), xm = A.x + A.w / 2, ym = A.y + A.h * 0.56, R = A.h * 0.17;
    cx.lineCap = 'round'; cx.lineJoin = 'round'; cx.lineWidth = 5 * k;
    [[-1, P1], [1, P2]].forEach(([s, c]) => {
      cx.strokeStyle = hex(c, tit); cx.shadowColor = c; cx.shadowBlur = 16 * k;
      const x = xm + s * R * 1.5;
      cx.beginPath(); cx.arc(x, ym - R * 1.35, R * 0.42, 0, 6.283); cx.stroke();
      cx.beginPath(); cx.moveTo(x, ym - R * 0.85); cx.lineTo(x, ym + R * 0.6);
      cx.moveTo(x, ym + R * 0.6); cx.lineTo(x - R * 0.5, ym + R * 1.5); cx.moveTo(x, ym + R * 0.6); cx.lineTo(x + R * 0.5, ym + R * 1.5);
      cx.moveTo(x, ym - R * 0.55); cx.lineTo(x + s * R * 0.9, ym - R * 1.2);
      cx.moveTo(x, ym - R * 0.55); cx.lineTo(xm, ym - R * 0.05);
      cx.stroke();
    });
    const hr = R * 0.42, hy = ym - R * 1.25;
    cx.strokeStyle = hex('#ff5ad8', tit + 0.2); cx.shadowColor = '#ff5ad8';
    cx.beginPath(); cx.moveTo(xm, hy + hr * 0.9);
    cx.bezierCurveTo(xm - hr * 1.6, hy - hr * 0.2, xm - hr * 0.7, hy - hr * 1.3, xm, hy - hr * 0.45);
    cx.bezierCurveTo(xm + hr * 0.7, hy - hr * 1.3, xm + hr * 1.6, hy - hr * 0.2, xm, hy + hr * 0.9); cx.stroke();
  }
  cx.restore();
}

// REF-069 duvari: her turda baska renk DAMALI kart, ortada SIYAH cift silueti (oyuk degil); kart yaklasinca siluete oyuncu renginde neon
// kontur (sol figur P1, sag figur P2 - referanstaki gokkusagi neonu yerine bizim takim renklerimiz)
function yildizDuvar(i, x, y, w, h, maske, alfa) {
  const [ac, ko] = KARE_RENK[i % KARE_RENK.length], n = 16, s = w / n;
  cx.save(); cx.globalAlpha = alfa;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.025); cx.clip();
  cx.fillStyle = ko; cx.fillRect(x, y, w, h); cx.fillStyle = ac;
  for (let j = 0; j * s < h; j++) for (let q = 0; q < n; q++) if ((q + j) % 2) cx.fillRect(x + q * s, y + j * s, s + 0.5, s + 0.5);
  cx.globalCompositeOperation = 'lighter';
  const r = rng(300 + i);
  for (let j = 0; j < 16; j++) parilti4(x + w * r(), y + h * r(), w * 0.012, 0.55);
  cx.restore();
  cx.lineWidth = Math.max(3, w * 0.005); cx.strokeStyle = '#ffffff';
  cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.025); cx.stroke();
  if (maske) {
    const MK = maskeKutu(maske, x, y, w, h), yak = kisit((w / W - 0.4) / 0.35, 0, 1);
    if (yak > 0) {
      kc.clearRect(0, 0, W, H); kc.drawImage(maske, ...MK); kc.globalCompositeOperation = 'source-in';
      const g = kc.createLinearGradient(MK[0], 0, MK[0] + MK[2], 0);
      g.addColorStop(0, P1); g.addColorStop(0.5, P1); g.addColorStop(0.5, P2); g.addColorStop(1, P2);
      kc.fillStyle = g; kc.fillRect(0, 0, W, H); kc.globalCompositeOperation = 'source-over';
      const d = Math.max(2, w * 0.006);
      cx.save(); cx.globalAlpha = alfa * yak;
      for (const [ox, oy] of [[d, 0], [-d, 0], [0, d], [0, -d], [d * 0.7, d * 0.7], [-d * 0.7, d * 0.7], [d * 0.7, -d * 0.7], [-d * 0.7, -d * 0.7]]) cx.drawImage(KAT, ox, oy);
      cx.restore();
    }
    kc.clearRect(0, 0, W, H); kc.drawImage(maske, ...MK); kc.globalCompositeOperation = 'source-in';
    kc.fillStyle = '#07040f'; kc.fillRect(0, 0, W, H); kc.globalCompositeOperation = 'source-over';
    cx.drawImage(KAT, 0, 0);
  }
  cx.restore();
}

function kupa(x, y, t) {
  cx.save(); cx.translate(x, y + 3 * k * Math.sin(t * 4));
  const g = cx.createLinearGradient(0, -30 * k, 0, 30 * k); g.addColorStop(0, '#fff3a0'); g.addColorStop(1, '#e0a000');
  cx.fillStyle = g; cx.strokeStyle = '#8a4a00'; cx.lineWidth = 3 * k; cx.lineJoin = 'round';
  cx.beginPath(); cx.moveTo(-22 * k, -28 * k); cx.lineTo(22 * k, -28 * k); cx.quadraticCurveTo(22 * k, 8 * k, 0, 12 * k); cx.quadraticCurveTo(-22 * k, 8 * k, -22 * k, -28 * k);
  cx.closePath(); cx.fill(); cx.stroke();
  for (const s of [-1, 1]) { cx.beginPath(); cx.arc(s * 24 * k, -16 * k, 9 * k, s > 0 ? -1.6 : 1.6, s > 0 ? 1.6 : 4.7); cx.stroke(); }
  cx.fillRect(-5 * k, 12 * k, 10 * k, 10 * k); cx.strokeRect(-5 * k, 12 * k, 10 * k, 10 * k);
  cx.beginPath(); cx.roundRect(-16 * k, 22 * k, 32 * k, 9 * k, 3 * k); cx.fill(); cx.stroke();
  yildiz5(0, -12 * k, 9 * k, '#ffffff', t);
  cx.restore();
}
// HUD: ustte Start -> kupa ilerleme cubugu, cubukta kosan mini maskot; kapinin ustunde level etiketi (SUBSCRIBE varken gizli, ust uste binmez)
function yildizHud(t, tur, il) {
  const x0 = W * 0.22, x1 = W * 0.78, y = 58 * k, h = 22 * k;
  cx.save();
  cx.fillStyle = 'rgba(255,255,255,0.92)'; cx.beginPath(); cx.roundRect(x0, y - h / 2, x1 - x0, h, h / 2); cx.fill();
  const g = cx.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, '#ffb0ec'); g.addColorStop(1, '#ff3fc0');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x0, y - h / 2, Math.max(h, (x1 - x0) * il), h, h / 2); cx.fill();
  cx.lineWidth = 3 * k; cx.strokeStyle = '#ff3fc0'; cx.beginPath(); cx.roundRect(x0, y - h / 2, x1 - x0, h, h / 2); cx.stroke();
  cx.fillStyle = '#ffd6f2'; cx.beginPath(); cx.roundRect(x0 - 150 * k, y - 26 * k, 136 * k, 52 * k, 14 * k); cx.fill(); cx.stroke();
  yazi('Start', x0 - 82 * k, y, 34 * k, '#c4106a', '#ffffff', 1);
  kupa(x1 + 48 * k, y, t);
  maskotYildiz(x0 + (x1 - x0) * il, y - 4 * k, 0.4, t);
  cx.restore();
}
// kapinin ustunde level etiketi: SAHNENIN parcasi (kesit kontrolu 1: HUD'da cizilince buyuyen kartin onunde kaliyordu), SUBSCRIBE varken gizli
function levelEtiket(t) {
  const ab = ABONE.some(x => t >= x - 0.3 && t < x + ABONE_SURE + 0.3), ad = (TEMA.levelAd || {})[turBul(t)];
  if (!ab && ad) { const A = aciklik(); yazi(ad, A.x + A.w / 2, A.y - 190 * k, 76 * k, ['#ffffff', '#c8f6ff', '#a890ff', '#ff9ae8'], '#4a1f86', 0.96, '#ff9ae8'); }
}

// ---- pastel tam ekran kartlar (REF-069 acilis / level / kapanis karti dili; metinler bizim)
function pastelZemin(t) {
  const g = cx.createLinearGradient(0, 0, W, H); g.addColorStop(0, '#ffd6f2'); g.addColorStop(0.5, '#efe2ff'); g.addColorStop(1, '#d4fbff');
  cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  const s = 54 * k, o = (t * 24 * k) % s;
  cx.strokeStyle = 'rgba(255,255,255,0.6)'; cx.lineWidth = 2 * k;
  for (let x = -s + o; x < W; x += s) { cx.beginPath(); cx.moveTo(x, 0); cx.lineTo(x, H); cx.stroke(); }
  for (let y = -s + o; y < H; y += s) { cx.beginPath(); cx.moveTo(0, y); cx.lineTo(W, y); cx.stroke(); }
  for (let i = 0; i < 24; i++) {
    const r = rng(5200 + i * 17), x = W * r(), y = ((H * r() - t * 50 * k * (0.4 + r())) % H + H) % H, R = (14 + 18 * r()) * k;
    if (i % 2) yildiz5(x, y, R, hex(['#ff9ae8', '#9af4ff', '#fff07a', '#c9a8ff'][i % 4], 0.7), t);
    else { cx.fillStyle = 'rgba(255,255,255,0.55)'; cx.beginPath(); cx.arc(x, y, R * 0.7, 0, 6.283); cx.fill(); }
  }
}
const PEMBE_YAZI = ['#ffc6f0', '#ff6ad6', '#e0209e'];
function pastelYazi(m, x, y, px, a, dolgu = PEMBE_YAZI) { yazi(m, x, y, px, dolgu, '#ffffff', a, '#ff9ae8'); }

function ikon(tur, x, y, r, renk) {
  cx.save(); cx.translate(x, y); cx.fillStyle = renk; cx.strokeStyle = renk; cx.lineWidth = r * 0.22; cx.lineJoin = 'round'; cx.lineCap = 'round';
  if (tur === 'begen') {                       // basparmak yukari (genel cizim)
    cx.beginPath(); cx.roundRect(-r * 0.95, -r * 0.1, r * 0.45, r * 1.05, r * 0.12); cx.fill();
    cx.beginPath(); cx.moveTo(-r * 0.35, r * 0.95); cx.lineTo(-r * 0.35, -r * 0.05); cx.lineTo(-r * 0.05, -r * 0.95);
    cx.quadraticCurveTo(r * 0.25, -r * 1.05, r * 0.2, -r * 0.55); cx.lineTo(r * 0.12, -r * 0.15); cx.lineTo(r * 0.8, -r * 0.15);
    cx.quadraticCurveTo(r * 1.05, -r * 0.1, r * 0.95, r * 0.2); cx.lineTo(r * 0.75, r * 0.85); cx.quadraticCurveTo(r * 0.68, r * 0.98, r * 0.5, r * 0.98); cx.closePath(); cx.fill();
  } else if (tur === 'yorum') {                // konusma balonu + uc nokta
    cx.beginPath(); cx.roundRect(-r, -r * 0.8, r * 2, r * 1.4, r * 0.35); cx.fill();
    cx.beginPath(); cx.moveTo(-r * 0.5, r * 0.5); cx.lineTo(-r * 0.75, r * 1.05); cx.lineTo(-r * 0.05, r * 0.55); cx.fill();
    cx.fillStyle = '#ffffff'; for (const q of [-0.5, 0, 0.5]) { cx.beginPath(); cx.arc(q * r, -r * 0.1, r * 0.15, 0, 6.283); cx.fill(); }
  } else {                                     // paylas: kivrik ok
    cx.lineWidth = r * 0.32; cx.beginPath(); cx.moveTo(-r * 0.9, r * 0.8); cx.quadraticCurveTo(-r * 0.8, -r * 0.3, r * 0.3, -r * 0.3); cx.stroke();
    cx.beginPath(); cx.moveTo(r * 0.15, -r * 0.95); cx.lineTo(r * 1.0, -r * 0.3); cx.lineTo(r * 0.15, r * 0.35); cx.closePath(); cx.fill();
  }
  cx.restore();
}
// Masaustu md. 27 (5 Kas 2026): SUBSCRIBE altinda LIKE / COMMENT / SHARE. Bu videoya uygun: beyaz-pastel hap butonlar, kendi neon renginde
// kenar + kosede sari yildiz; sirayla girer, sirayla "dokunulur" (dolar, pop) - abone tiklamasindan sonra
function begenSatiri(xm, y, s, u, t) {
  if (s <= 0.01) return;
  const B = [['LIKE', 'begen', '#ff3fc0'], ['COMMENT', 'yorum', '#16b8e8'], ['SHARE', 'paylas', '#f0a800']];
  const bw = 232 * k * s, bh = 62 * k * s, ara = 26 * k * s, top = 3 * bw + 2 * ara;   // kesit kontrolu 1: 74 px satir kapidaki kartin ust kenarina biniyordu
  B.forEach(([ad, ik, c], i) => {
    const gir = ease(kisit((u - 0.3 - i * 0.12) / 0.3, 0, 1)); if (gir <= 0) return;
    const tik = 1.75 + i * 0.32, dolu = u >= tik, bas = u >= tik && u < tik + 0.1 ? 0.88 : 1;
    const pop = dolu && u < tik + 0.35 ? 1 + 0.14 * Math.sin((u - tik) / 0.35 * Math.PI) : 1;
    const x = xm - top / 2 + i * (bw + ara) + bw / 2, ss = gir * bas * pop;
    cx.save(); cx.translate(x, y); cx.scale(ss, ss); cx.translate(-x, -y);
    cx.shadowColor = c; cx.shadowBlur = 22 * k;
    cx.fillStyle = dolu ? c : '#ffffff'; cx.beginPath(); cx.roundRect(x - bw / 2, y - bh / 2, bw, bh, bh / 2); cx.fill();
    cx.shadowBlur = 0; cx.lineWidth = 5 * k * s; cx.strokeStyle = dolu ? '#ffffff' : c; cx.stroke();
    ikon(ik, x - bw / 2 + bh * 0.62, y, bh * 0.3, dolu ? '#ffffff' : c);
    yazi(ad, x + bh * 0.3, y, (ad.length > 5 ? 32 : 38) * k * s, dolu ? '#ffffff' : '#3a1060', dolu ? '#3a1060' : '#ffffff', 1);
    yildiz5(x + bw / 2 - 12 * k * s, y - bh / 2 + 4 * k * s, 15 * k * s, '#ffe23a', t, '#ffffff');
    if (dolu && u < tik + 0.6) {
      const r3 = (u - tik) / 0.6;
      for (let j = 0; j < 8; j++) { const a = j / 8 * 6.283, d = (40 + 110 * r3) * k * s; yildiz5(x + Math.cos(a) * d * 1.4, y + Math.sin(a) * d * 0.7, 9 * k * s * (1 - r3), c, t); }
    }
    cx.restore();
  });
}

function yildizKart(kart, u, t) {
  pastelZemin(t);
  if (kart.tip === 'yazi') {
    const satir = kart.alt ? [kart.metin, kart.alt] : [kart.metin];
    satir.forEach((m, j) => {
      const g = ease(kisit((u - j * 0.18) / 0.35, 0, 1)), zip = 1 + 0.18 * Math.sin(Math.min(1, g) * Math.PI);
      pastelYazi(m, W / 2, H * (satir.length > 1 ? 0.40 + j * 0.22 : 0.5), (kart.px || (m.length > 13 ? 150 : 190)) * k * zip, g);
    });
  } else if (kart.tip === 'tur') {
    const g = ease(kisit(u / 0.3, 0, 1)), zip = 1 + 0.2 * Math.sin(Math.min(1, u / 0.35) * Math.PI);
    yazi('LEVEL ' + kart.tur, W / 2, H * 0.36, 80 * k, ['#e0fbff', '#5ae0ff', '#18a8d8'], '#ffffff', g, '#5ae0ff');
    const dolgu = { 1: ['#c8fbff', '#7ad8ff', '#b88aff'], 2: ['#fff6b0', '#ffc23a', '#ff7ab8'], 3: ['#ffd0a0', '#ff7a2a', '#e8203a'] }[kart.tur] || PEMBE_YAZI;
    yazi(kart.metin, W / 2, H * 0.56, 230 * k * zip, dolgu, '#ffffff', g, dolgu[1]);
  } else if (kart.tip === 'basla') {
    const ad = kart.sure / 4, adim = Math.min(3, Math.floor(u / ad)), q = (u - adim * ad) / ad;
    const s = 1.35 - 0.35 * ease(Math.min(1, q / 0.3));
    pastelYazi(['3', '2', '1', 'GO!'][adim], W / 2, H * 0.5, (adim === 3 ? 300 : 340) * k * s, Math.min(1, (1 - q) / 0.2 + 0.3),
      adim === 3 ? PEMBE_YAZI : ['#fff6b0', '#ffd23a', '#f09000']);
  } else if (kart.tip === 'nasil') {
    pastelYazi('HOW TO PLAY', W / 2, H * 0.11, 110 * k, ease(kisit(u / 0.3, 0, 1)));
    const ww = 980 * k, wh = ww * 9 / 16, wx = W / 2 - ww / 2, wy = H * 0.19;
    cx.save(); cx.shadowColor = '#ff9ae8'; cx.shadowBlur = 30 * k; cx.fillStyle = '#ffffff';
    cx.beginPath(); cx.roundRect(wx - 14 * k, wy - 14 * k, ww + 28 * k, wh + 28 * k, 28 * k); cx.fill(); cx.restore();
    cx.save(); cx.beginPath(); cx.roundRect(wx, wy, ww, wh, 18 * k); cx.clip();
    cx.drawImage(GOK, wx, wy, ww, wh); cx.drawImage(SERIT, wx, wy, ww, wh);
    const A = aciklik(), sc = ww / W, ad = DUVARLAR[0] && (DUVARLAR[0].grup || DUVARLAR[0].p1), m = MASKE[ad];
    const q = Math.pow((u % 2.4) / 2.4, 2.1), A2 = { x: wx + A.x * sc, y: wy + A.y * sc, w: A.w * sc, h: A.w * sc / PAR_ORAN };
    A2.y += A.h * sc - A2.h;
    const B2 = { x: wx - ww * 0.02, y: wy - wh * 0.02, w: ww * 1.04, h: ww * 1.04 / PAR_ORAN };
    const K = kutuLerp(A2, B2, q);
    yildizDuvar(0, K.x, K.y, K.w, K.h, m, 1);
    cx.restore();
    cx.lineWidth = 6 * k; cx.strokeStyle = '#ff6ad6'; cx.beginPath(); cx.roundRect(wx, wy, ww, wh, 18 * k); cx.stroke();
    for (let j = 0; j < 6; j++) yildiz5(wx + ww + 10 * k, wy + (j + 0.5) * wh / 6, 13 * k, ['#ff9ae8', '#9af4ff', '#fff07a'][j % 3], t, '#ffffff');
    pastelYazi(kart.metin || 'COPY THE SHAPE', W / 2, H * 0.83, 84 * k, kisit((u - 0.4) / 0.3, 0, 1));
    yazi(kart.alt || '', W / 2, H * 0.93, 54 * k, ['#5a2a9a', '#3a1070'], '#ffffff', kisit((u - 0.8) / 0.3, 0, 1));
  } else if (kart.tip === 'abone') {
    const g = ease(kisit(u / 0.4, 0, 1)), pul = 1 + 0.04 * Math.sin(u * 8);
    const bw = 760 * k * g * pul, bh = 170 * k * g * pul, y = H * 0.36;
    cx.save(); cx.shadowColor = '#ff1f3d'; cx.shadowBlur = 40 * k;
    cx.fillStyle = '#ffe23a'; cx.beginPath(); cx.roundRect(W / 2 - bw / 2 - 10 * k, y - bh / 2 - 10 * k, bw + 20 * k, bh + 20 * k, bh / 2 + 10 * k); cx.fill();
    cx.fillStyle = '#e11d2e'; cx.beginPath(); cx.roundRect(W / 2 - bw / 2, y - bh / 2, bw, bh, bh / 2); cx.fill(); cx.restore();
    if (g > 0.6) yazi('SUBSCRIBE', W / 2, y, 110 * k * pul, '#ffffff', '#5a0010');
    begenSatiri(W / 2, H * 0.6, 1.25, u, t);
    pastelYazi(TEMA.aboneAlt, W / 2, H * 0.82, 76 * k, kisit((u - 0.6) / 0.3, 0, 1));
  }
}

// KENDI maskotumuz (16. videodan, seri ogesi): yuz ve govde ayni; bu videoda yildiz sahnesi kiyafeti = sac tokasi yildiz + elde yildizli asa
function maskotYildiz(x, y, s, t, alfa = 1) {
  if (alfa <= 0.01) return;
  cx.save(); cx.globalAlpha *= alfa; cx.translate(x, y); cx.scale(s * k, s * k);
  const KON = '#5a1f86';
  cx.lineJoin = 'round'; cx.lineWidth = 5; cx.strokeStyle = KON;
  for (const sx of [-1, 1]) {
    cx.save(); cx.translate(sx * 34, -48); cx.rotate(sx * (0.5 + 0.06 * Math.sin(t * 5)));
    cx.fillStyle = '#ff9ad8'; cx.beginPath(); cx.ellipse(0, -18, 15, 26, 0, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffd6f2'; cx.beginPath(); cx.ellipse(0, -16, 6, 15, 0, 0, 6.283); cx.fill(); cx.restore();
  }
  const gv = cx.createRadialGradient(-14, -20, 6, 0, 0, 70); gv.addColorStop(0, '#fff0fa'); gv.addColorStop(1, '#ffb4e4');
  cx.fillStyle = gv; cx.beginPath(); cx.ellipse(0, 0, 62, 56, 0, 0, 6.283); cx.fill(); cx.stroke();
  // sag elde yildizli asa (vurusa sallanir)
  cx.save(); cx.translate(62, -4); cx.rotate(-0.5 + 0.25 * Math.sin(t * BPM / 60 * Math.PI));
  cx.strokeStyle = '#ffffff'; cx.lineWidth = 7; cx.beginPath(); cx.moveTo(0, 0); cx.lineTo(0, -62); cx.stroke();
  cx.strokeStyle = KON; cx.lineWidth = 2.5; cx.stroke();
  cx.restore();
  const ax = 62 + Math.sin(-0.5 + 0.25 * Math.sin(t * BPM / 60 * Math.PI)) * 62, ay = -4 - Math.cos(-0.5 + 0.25 * Math.sin(t * BPM / 60 * Math.PI)) * 62;
  cx.save(); cx.shadowColor = '#ffe23a'; cx.shadowBlur = 16; yildiz5(ax, ay, 20, '#ffe23a', t, KON); cx.restore();
  for (const sx of [-1, 1]) {
    cx.fillStyle = '#ffc6ea'; cx.beginPath(); cx.ellipse(sx * 58, -6 + Math.sin(t * 6 + sx) * 4, 13, 17, sx * 0.4, 0, 6.283); cx.fill(); cx.stroke();
  }
  const kirp = (t % 3.4) < 0.12 ? 0.15 : 1;
  for (const sx of [-1, 1]) {
    cx.fillStyle = '#2a0e4a'; cx.beginPath(); cx.ellipse(sx * 22, -6, 11, 15 * kirp, 0, 0, 6.283); cx.fill();
    if (kirp > 0.5) { cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 22 - 4, -12, 4.5, 0, 6.283); cx.fill(); cx.beginPath(); cx.arc(sx * 22 + 4, -1, 2, 0, 6.283); cx.fill(); }
    cx.fillStyle = 'rgba(255,90,170,0.45)'; cx.beginPath(); cx.ellipse(sx * 38, 14, 10, 6, 0, 0, 6.283); cx.fill();
  }
  cx.strokeStyle = KON; cx.lineWidth = 4; cx.beginPath(); cx.arc(0, 10, 9, 0.2, Math.PI - 0.2); cx.stroke();
  cx.save(); cx.translate(0, -58);
  for (let i = 0; i < 5; i++) { cx.save(); cx.rotate(i * 1.2566 + t * 0.6); cx.fillStyle = '#ffffff'; cx.beginPath(); cx.ellipse(0, -11, 7, 11, 0, 0, 6.283); cx.fill(); cx.lineWidth = 2.5; cx.stroke(); cx.restore(); }
  cx.fillStyle = '#ffd94a'; cx.beginPath(); cx.arc(0, 0, 6, 0, 6.283); cx.fill(); cx.restore();
  yildiz5(-40, -40, 13, '#9af4ff', t, KON);                  // sac tokasi yildiz
  cx.restore();
}
