// ------------------------------------------------------------ REF-068 YARDIMCILARI (motor 14, galaksi temasi)
// Gok hareketi: Blender bulutsusunun ustunde goz kirpan yildizlar + ara ara kayan yildiz + yavas bulutsu nabzi (ekran dolu, hareketli gok)
function galaksiGok(t) {
  cx.save(); cx.globalCompositeOperation = 'lighter';
  const nab = 0.5 + 0.5 * Math.sin(t * 0.6);
  for (const [x, y, r, c] of [[0.22, 0.18, 0.35, '#7a3ee0'], [0.78, 0.24, 0.3, '#2a6aff'], [0.5, 0.08, 0.28, '#ff5ad8']]) {
    const g = cx.createRadialGradient(W * x, H * y, 0, W * x, H * y, W * r);
    g.addColorStop(0, hex(c, 0.10 + 0.08 * nab)); g.addColorStop(1, hex(c, 0));
    cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  }
  for (let i = 0; i < 140; i++) {                         // goz kirpan yildizlar (ufkun ustu)
    const r = rng(7100 + i * 37), x = W * r(), y = H * 0.56 * r(), f = r() * 6.28, h = 0.8 + r() * 2.6;
    const a = 0.2 + 0.8 * Math.max(0, Math.sin(t * h + f)) ** 2, R = (0.8 + r() * 2.2) * k;
    cx.fillStyle = hex(i % 7 ? '#ffffff' : '#9fe8ff', a); cx.beginPath(); cx.arc(x, y, R, 0, 6.283); cx.fill();
    if (i % 9 === 0) parilti4(x, y, (10 + 10 * r()) * k, a * 0.8);
  }
  const n = Math.floor(t / 2.7), q = t / 2.7 - n;          // kayan yildiz: ~2,7 sn'de bir, 0,6 sn
  if (q < 0.22) {
    const r = rng(8300 + n * 13), x0 = W * (0.1 + 0.8 * r()), y0 = H * (0.04 + 0.22 * r()), ang = 0.35 + 0.3 * r(), p = q / 0.22;
    const L = 260 * k, x = x0 + Math.cos(ang) * 520 * k * p, y = y0 + Math.sin(ang) * 520 * k * p;
    const g = cx.createLinearGradient(x, y, x - Math.cos(ang) * L, y - Math.sin(ang) * L);
    g.addColorStop(0, `rgba(255,255,255,${0.95 * (1 - p)})`); g.addColorStop(1, 'rgba(120,200,255,0)');
    cx.strokeStyle = g; cx.lineWidth = 4 * k; cx.lineCap = 'round';
    cx.beginPath(); cx.moveTo(x, y); cx.lineTo(x - Math.cos(ang) * L, y - Math.sin(ang) * L); cx.stroke();
  }
  cx.restore();
}
// REF-068 duvari: pembe (sol-alt) -> sari (sag-ust) degrade
function duvarDegrade(c, x, y, w, h) {
  const g = c.createLinearGradient(x, y + h, x + w, y);
  (TEMA.duvarDegrade || ['#ff7ae6', '#ffb0c8', '#ffe86a']).forEach((r, i, a) => g.addColorStop(i / (a.length - 1), r));
  return g;
}
// REF-068: kapida sari "START!" karti (yazi bizim cizimimiz), sonra asagi kayip kaybolur
function startKart(t, kay = 0, alfa = 1) {
  const A = aciklik(), tw = A.w * 0.82, th = A.h * 0.72, x = A.x + A.w / 2 - tw / 2, y = A.y + A.h * 0.16 + kay * A.h * 1.1;
  cx.save(); cx.globalAlpha = alfa;
  const g = cx.createLinearGradient(x, y, x + tw, y + th); g.addColorStop(0, '#ffe23a'); g.addColorStop(1, '#ffc21a');
  cx.fillStyle = g; cx.shadowColor = 'rgba(255,220,60,0.7)'; cx.shadowBlur = 24 * k;
  cx.beginPath(); cx.roundRect(x, y, tw, th, 10 * k); cx.fill(); cx.shadowBlur = 0;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, tw, th, 10 * k); cx.clip();       // karta konfeti serpintisi
  const r = rng(515);
  for (let j = 0; j < 22; j++) {
    cx.fillStyle = ['#ff4fb0', '#3fd8ff', '#7dff6a', '#ffffff'][j % 4];
    cx.save(); cx.translate(x + tw * r(), y + th * r()); cx.rotate(r() * 6.28 + t * (r() - 0.5) * 2);
    cx.fillRect(-7 * k, -2.5 * k, 14 * k, 5 * k); cx.restore();
  }
  cx.restore();
  cx.lineWidth = 5 * k; cx.strokeStyle = '#ffffff'; cx.beginPath(); cx.roundRect(x + 6 * k, y + 6 * k, tw - 12 * k, th - 12 * k, 8 * k); cx.stroke();
  const zip = 1 + 0.06 * Math.sin(t * 9);
  cx.save(); cx.translate(x + tw / 2, y + th * 0.44); cx.rotate(-0.06); cx.scale(zip, zip);
  yazi('START!', 0, 0, th * 0.42, ['#ff6ac8', '#ff2f8e', '#c4106a'], '#ffffff', 1, null);
  cx.restore();
  yazi('GET READY', x + tw / 2, y + th * 0.8, th * 0.16, '#ffffff', '#c4106a', 1);
  cx.restore();
}
// REF-068 HUD: ust ortada "MISSIONS : n/N" (level icinde), beyaz dolgu + pembe kalin kontur
function galaksiHud(t) {
  const d0 = [...DUVARLAR].reverse().find(x => t >= x.t0) || DUVARLAR[0]; if (!d0) return;
  const L = DUVARLAR.filter(x => x.tur === d0.tur), n = L.indexOf(d0) + 1;
  yazi(`${TEMA.sayac || 'MISSIONS'} : ${n}/${L.length}`, W / 2, 58 * k, 52 * k, ['#ffffff', '#ffe6f6'], '#ff2f9e', 1, '#ff5ac8');
}
// REF-068 tam ekran ovgu: sahnenin ustunde beyaz hiz cizgisi patlamasi + egik dev beyaz yazi, pembe kontur, mor golge
function galaksiOvgu(kart, u, t) {
  const g = ease(kisit(u / 0.22, 0, 1)), zip = 1 + 0.25 * Math.sin(Math.min(1, u / 0.25) * Math.PI);
  cx.save(); cx.fillStyle = `rgba(20,8,60,${0.45 * g})`; cx.fillRect(0, 0, W, H);
  cx.globalCompositeOperation = 'lighter';
  const r = rng(Math.floor(u * 14) + 610);
  for (let j = 0; j < 70; j++) {
    const a = r() * 6.283, r0 = (0.18 + 0.25 * r()) * W, L = (0.25 + 0.4 * r()) * W;
    cx.fillStyle = `rgba(255,255,255,${(0.25 + 0.5 * r()) * g})`;
    cx.beginPath(); cx.moveTo(W / 2 + Math.cos(a) * r0, H / 2 + Math.sin(a) * r0 * 0.62);
    cx.lineTo(W / 2 + Math.cos(a + 0.01) * (r0 + L), H / 2 + Math.sin(a + 0.01) * (r0 + L) * 0.62);
    cx.lineTo(W / 2 + Math.cos(a - 0.01) * (r0 + L), H / 2 + Math.sin(a - 0.01) * (r0 + L) * 0.62); cx.closePath(); cx.fill();
  }
  cx.restore();
  const satir = kart.metin.split('|');
  cx.save(); cx.translate(W / 2, H * 0.48); cx.rotate(-0.12); cx.scale(zip, zip);
  satir.forEach((m, j) => {
    const y = (j - (satir.length - 1) / 2) * 210 * k;
    yazi(m, 10 * k, y + 16 * k, 220 * k, '#7a2ad0', '#7a2ad0', g * 0.9);               // mor derinlik
    yazi(m, 0, y, 220 * k, ['#ffffff', '#fff4fb'], '#ff3fae', g, '#ff7ad8');
  });
  cx.restore();
}
// REF-068 LEVEL secim ekrani: "LEVEL :" + uc buton (EASY sari, NORMAL yesil, HARD kirmizi), imlec sec;len butona gelip tiklar.
// Buton ikonu bizim: 1-2-3 yildiz (referanstaki robot yuzu yerine).
function levelKart(kart, u, t) {
  cx.fillStyle = '#05030e'; cx.fillRect(0, 0, W, H);
  galaksiGok(t);
  cx.fillStyle = 'rgba(5,3,14,0.55)'; cx.fillRect(0, 0, W, H);
  const gir = ease(kisit(u / 0.3, 0, 1));
  yazi('LEVEL :', W / 2, H * 0.2, 150 * k * (0.8 + 0.2 * gir), ['#ffffff', '#ffe6f6'], '#ff2f9e', gir, '#ff5ac8');
  const B = [['EASY', '#ffd23a', '#c48a00', 1], ['NORMAL', '#4fe06a', '#1a9a34', 2], ['HARD', '#ff3a4a', '#b0101e', 3]];
  const sec = (kart.tur || 1) - 1, TIK = kart.sure * 0.55;
  const bx = i => W * (0.28 + 0.22 * i), by = H * 0.58, bw = 300 * k, bh = 330 * k;
  B.forEach(([ad, c1, c2, yld], i) => {
    const secili = i === sec && u >= TIK, gec = i < sec;
    let s = (0.6 + 0.4 * ease(kisit((u - 0.1 * i) / 0.35, 0, 1))) * (secili ? 1.12 + 0.05 * Math.sin((u - TIK) * 14) : 1);
    if (secili && u - TIK < 0.12) s *= 0.9;
    cx.save(); cx.translate(bx(i), by); cx.scale(s, s); cx.globalAlpha = gec ? 0.45 : 1;
    if (secili) { cx.shadowColor = c1; cx.shadowBlur = 60 * k; }
    cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(-bw / 2 - 10 * k, -bh / 2 - 10 * k, bw + 20 * k, bh + 20 * k, 40 * k); cx.fill();
    cx.shadowBlur = 0;
    const g = cx.createLinearGradient(0, -bh / 2, 0, bh / 2); g.addColorStop(0, c1); g.addColorStop(1, c2);
    cx.fillStyle = g; cx.beginPath(); cx.roundRect(-bw / 2, -bh / 2, bw, bh, 32 * k); cx.fill();
    yazi(ad, 0, -bh * 0.32, (ad.length > 4 ? 58 : 70) * k, '#ffffff', '#1a0630', 1);
    for (let j = 0; j < yld; j++) {                                          // zorluk yildizlari
      const xx = (j - (yld - 1) / 2) * 78 * k;
      cx.save(); cx.translate(xx, bh * 0.12); cx.rotate(Math.sin(t * 3 + j) * 0.1);
      cx.beginPath();
      for (let q = 0; q <= 10; q++) { const a = -Math.PI / 2 + q * Math.PI / 5, rr = q % 2 ? 18 * k : 40 * k; q ? cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : cx.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
      cx.closePath(); cx.fillStyle = '#ffffff'; cx.fill(); cx.lineWidth = 5 * k; cx.strokeStyle = '#1a0630'; cx.stroke();
      cx.restore();
    }
    if (gec) {                                                               // gecilmis level: tik isareti
      cx.strokeStyle = '#ffffff'; cx.lineWidth = 16 * k; cx.lineCap = 'round';
      cx.beginPath(); cx.moveTo(-50 * k, bh * 0.34); cx.lineTo(-10 * k, bh * 0.44); cx.lineTo(60 * k, bh * 0.24); cx.stroke();
    }
    cx.restore();
  });
  if (u > 0.3) {                                                             // el imleci secilen butona gelir ve tiklar
    const q = ease(kisit((u - 0.3) / (TIK - 0.3), 0, 1));
    const hx = lerp(W * 0.5, bx(sec) + 40 * k, q), hy = lerp(H * 0.95, by + 70 * k, q), sc = (u >= TIK && u < TIK + 0.15) ? 0.85 : 1;
    cx.save(); cx.translate(hx, hy); cx.scale(sc * 1.4, sc * 1.4);
    cx.fillStyle = '#ffffff'; cx.strokeStyle = '#111827'; cx.lineWidth = 3.5 * k; cx.beginPath();
    cx.moveTo(0, 0); cx.lineTo(0, 54 * k); cx.lineTo(13 * k, 41 * k); cx.lineTo(23 * k, 63 * k); cx.lineTo(32 * k, 59 * k); cx.lineTo(22 * k, 37 * k); cx.lineTo(40 * k, 37 * k); cx.closePath();
    cx.fill(); cx.stroke();
    if (u >= TIK && u < TIK + 0.4) { const r2 = (u - TIK) / 0.4; cx.strokeStyle = `rgba(255,255,255,${(1 - r2).toFixed(3)})`; cx.lineWidth = 5 * k; cx.beginPath(); cx.arc(0, 0, 16 * k + 50 * k * r2, 0, 6.283); cx.stroke(); }
    cx.restore();
  }
}
// REF-068 acilis geri sayimi: tam ekran THREE / TWO / ONE / GO GO GO (beyaz harf, pembe kalin kontur, hiz cizgili koyu zemin)
function galaksiBasla(kart, u, t) {
  const ad = kart.sure / 4, adim = Math.min(3, Math.floor(u / ad)), q = (u - adim * ad) / ad;
  cx.fillStyle = '#0a0418'; cx.fillRect(0, 0, W, H);
  cx.save(); cx.globalCompositeOperation = 'lighter';
  const r = rng(Math.floor(u * 12) + 720);
  for (let j = 0; j < 60; j++) {
    const a = r() * 6.283, r0 = (0.3 + 0.3 * r()) * W, L = (0.2 + 0.4 * r()) * W;
    cx.fillStyle = `rgba(255,255,255,${0.15 + 0.35 * r()})`;
    cx.beginPath(); cx.moveTo(W / 2 + Math.cos(a) * r0, H / 2 + Math.sin(a) * r0 * 0.6);
    cx.lineTo(W / 2 + Math.cos(a + 0.012) * (r0 + L), H / 2 + Math.sin(a + 0.012) * (r0 + L) * 0.6);
    cx.lineTo(W / 2 + Math.cos(a - 0.012) * (r0 + L), H / 2 + Math.sin(a - 0.012) * (r0 + L) * 0.6); cx.closePath(); cx.fill();
  }
  cx.restore();
  const s = 1.3 - 0.3 * ease(Math.min(1, q / 0.25));
  cx.save(); cx.translate(W / 2, H * 0.5); cx.rotate(-0.05); cx.scale(s, s);
  if (adim < 3) yazi(['THREE', 'TWO', 'ONE'][adim], 0, 0, 260 * k, ['#ffffff', '#fff4fb'], '#ff3fae', 1, '#ff7ad8');
  else { yazi('GO GO', 0, -120 * k, 230 * k, ['#ffffff', '#fff4fb'], '#ff3fae', 1, '#ff7ad8'); yazi('GO!', 0, 130 * k, 260 * k, ['#ffffff', '#fff4fb'], '#ff3fae', 1, '#ff7ad8'); }
  cx.restore();
}
// KENDI maskotumuz (16. videodan, seri ogesi): yuz ve govde ayni; bu videoda synthwave kiyafeti = camgobegi neon vizor gozluk + kulaklik
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
  for (const sx of [-1, 1]) {                                   // kollar
    cx.fillStyle = '#ffc6ea'; cx.beginPath(); cx.ellipse(sx * 58, -6 + Math.sin(t * 6 + sx) * 4, 13, 17, sx * 0.4, 0, 6.283); cx.fill(); cx.stroke();
  }
  // synthwave vizor: gozlerin ustunde camgobegi-pembe degrade neon bant
  const vz = cx.createLinearGradient(-48, 0, 48, 0); vz.addColorStop(0, '#3fe8ff'); vz.addColorStop(1, '#ff5ad8');
  cx.save(); cx.shadowColor = '#3fe8ff'; cx.shadowBlur = 14;
  cx.fillStyle = vz; cx.beginPath(); cx.roundRect(-48, -20, 96, 26, 13); cx.fill(); cx.stroke(); cx.restore();
  cx.fillStyle = 'rgba(255,255,255,0.7)'; cx.beginPath(); cx.roundRect(-38, -16, 30, 6, 3); cx.fill();
  for (const sx of [-1, 1]) {
    cx.fillStyle = 'rgba(255,90,170,0.45)'; cx.beginPath(); cx.ellipse(sx * 38, 18, 10, 6, 0, 0, 6.283); cx.fill();     // yanak
  }
  cx.strokeStyle = KON; cx.lineWidth = 4; cx.beginPath(); cx.arc(0, 16, 9, 0.2, Math.PI - 0.2); cx.stroke();          // gulumseme
  cx.save(); cx.translate(0, -58);                              // basta cicek (seri tanirligi)
  for (let i = 0; i < 5; i++) { cx.save(); cx.rotate(i * 1.2566 + t * 0.6); cx.fillStyle = '#ffffff'; cx.beginPath(); cx.ellipse(0, -11, 7, 11, 0, 0, 6.283); cx.fill(); cx.lineWidth = 2.5; cx.stroke(); cx.restore(); }
  cx.fillStyle = '#ffd94a'; cx.beginPath(); cx.arc(0, 0, 6, 0, 6.283); cx.fill(); cx.restore();
  cx.restore();
}
// maskot video boyunca: sol altta izgaranin ustunde vurusa ziplar (TALIMATLAR §4 maskot kurali); tam ekran kartlarda da ayni kosede
function maskotKose(t) {
  const v = (t * BPM / 60) % 1, zip = Math.abs(Math.sin(v * Math.PI)) * 16 * k;
  maskotCiz(W * 0.075, H * 0.86 - zip, 1.05, t);
}
