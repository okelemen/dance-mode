// ------------------------------------------------------------ REF-070 YARDIMCILARI (motor 16, neon yildiz koprusu, SOLO Easy Beginner)
let ZAMAN_T = 0;   // kareKur her karede yazar (hologram serit animasyonu)
// sahne15 (yildiz) uzerine TEMA.kopru bayragi: duvar karti DAMALI degil YANARDONER PASTEL HOLOGRAM, siyah siluet yaklasinca tek
// pembe->camgobegi neon kontur (P1/P2 ayrimi yok, solo); kapi ekraninda sonuk tek neon figur; pembe-beyaz 3-2-1; ustte "MISSIONS n/6".
// Siluetler Openclipart kamu mali cizimler (REF-071, Masaustu md. 21 5c). Bayrak yoksa motor 15 fonksiyonlari aynen calisir.

function holoZemin(x, y, w, h, i, t) {
  const g = cx.createLinearGradient(x, y, x + w, y + h);
  const kay = ((i * 0.37) % 1) * 0.2;
  [['#ffc6ee', 0], ['#dcc8ff', 0.28 + kay], ['#bdf3ff', 0.52 + kay], ['#fff2c6', 0.78], ['#ffc6ee', 1]]
    .forEach(([c, p]) => g.addColorStop(Math.min(1, p), c));
  cx.fillStyle = g; cx.fillRect(x, y, w, h);
  cx.save(); cx.globalCompositeOperation = 'lighter';
  const sx = x + w * (((t * 0.35 + i * 0.21) % 1.4) - 0.2);          // kayan parlak serit (hologram)
  const sg = cx.createLinearGradient(sx - w * 0.12, y, sx + w * 0.12, y + h);
  sg.addColorStop(0, 'rgba(255,255,255,0)'); sg.addColorStop(0.5, 'rgba(255,255,255,0.45)'); sg.addColorStop(1, 'rgba(255,255,255,0)');
  cx.fillStyle = sg; cx.fillRect(x, y, w, h);
  const r = rng(700 + i);
  for (let j = 0; j < 26; j++) parilti4(x + w * r(), y + h * r(), w * (0.006 + 0.01 * r()), 0.5 + 0.4 * Math.sin(t * 3 + j));
  cx.restore();
}

function yildizDuvar(i, x, y, w, h, maske, alfa) {
  if (!TEMA.kopru) return yildizDuvar18(i, x, y, w, h, maske, alfa);
  cx.save(); cx.globalAlpha = alfa;
  const rr = Math.min(w, h) * 0.06;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, w, h, rr); cx.clip(); holoZemin(x, y, w, h, i, ZAMAN_T); cx.restore();
  cx.lineWidth = Math.max(3, w * 0.006); cx.strokeStyle = '#ffffff';
  cx.beginPath(); cx.roundRect(x, y, w, h, rr); cx.stroke();
  if (maske) {
    const MK = maskeKutu(maske, x, y, w, h), yak = kisit((w / W - 0.4) / 0.35, 0, 1);
    if (yak > 0) {                                  // REF-070: yaklasinca siluetin cevresi neon (solo: tek degrade)
      kc.clearRect(0, 0, W, H); kc.drawImage(maske, ...MK); kc.globalCompositeOperation = 'source-in';
      const g = kc.createLinearGradient(MK[0], MK[1], MK[0] + MK[2], MK[1] + MK[3]);
      g.addColorStop(0, '#ff4ad0'); g.addColorStop(0.5, '#b07aff'); g.addColorStop(1, '#3fe8ff');
      kc.fillStyle = g; kc.fillRect(0, 0, W, H); kc.globalCompositeOperation = 'source-over';
      const d = Math.max(2, w * 0.006);
      cx.save(); cx.globalAlpha = alfa * yak; cx.shadowColor = '#ff7ae0'; cx.shadowBlur = 18 * k;
      for (const [ox, oy] of [[d, 0], [-d, 0], [0, d], [0, -d], [d * 0.7, d * 0.7], [-d * 0.7, d * 0.7], [d * 0.7, -d * 0.7], [-d * 0.7, -d * 0.7]]) cx.drawImage(KAT, ox, oy);
      cx.restore();
    }
    kc.clearRect(0, 0, W, H); kc.drawImage(maske, ...MK); kc.globalCompositeOperation = 'source-in';
    kc.fillStyle = '#07040f'; kc.fillRect(0, 0, W, H); kc.globalCompositeOperation = 'source-over';
    cx.drawImage(KAT, 0, 0);
  }
  cx.restore();
}

// kapi ekrani: duvar gelmeden sonuk, titreyen tek neon figur (kollar V, kendi cizimimiz) + iki yildiz
function kapiEkran(t) {
  if (!TEMA.kopru) return kapiEkran18(t);
  const A = aciklik();
  cx.save();
  const g = cx.createLinearGradient(0, A.y, 0, A.y + A.h); g.addColorStop(0, '#1a1258'); g.addColorStop(1, '#0a0828');
  cx.fillStyle = g; cx.fillRect(A.x, A.y, A.w, A.h);
  cx.strokeStyle = 'rgba(140,150,255,0.14)'; cx.lineWidth = 1.5 * k;
  for (let x = A.x; x < A.x + A.w; x += A.w / 18) { cx.beginPath(); cx.moveTo(x, A.y); cx.lineTo(x, A.y + A.h); cx.stroke(); }
  for (let y = A.y; y < A.y + A.h; y += A.w / 18) { cx.beginPath(); cx.moveTo(A.x, y); cx.lineTo(A.x + A.w, y); cx.stroke(); }
  const ev = duvarEvre(t);
  if (ev === 'kart' || ev === 'bos' || ev === 'yok') {
    const tit = 0.35 + 0.4 * Math.abs(Math.sin(t * 7) * Math.sin(t * 2.3)), xm = A.x + A.w / 2, ym = A.y + A.h * 0.58, R = A.h * 0.2;
    cx.lineCap = 'round'; cx.lineJoin = 'round'; cx.lineWidth = 5 * k;
    cx.strokeStyle = hex('#ff5ad8', tit); cx.shadowColor = '#ff5ad8'; cx.shadowBlur = 16 * k;
    cx.beginPath(); cx.arc(xm, ym - R * 1.35, R * 0.4, 0, 6.283); cx.stroke();
    cx.beginPath(); cx.moveTo(xm, ym - R * 0.9); cx.lineTo(xm, ym + R * 0.55);
    cx.moveTo(xm, ym + R * 0.55); cx.lineTo(xm - R * 0.55, ym + R * 1.5); cx.moveTo(xm, ym + R * 0.55); cx.lineTo(xm + R * 0.55, ym + R * 1.5);
    cx.moveTo(xm, ym - R * 0.6); cx.lineTo(xm - R * 0.95, ym - R * 1.65); cx.moveTo(xm, ym - R * 0.6); cx.lineTo(xm + R * 0.95, ym - R * 1.65);
    cx.stroke();
    cx.shadowBlur = 0;
    yildiz5(xm - R * 1.9, ym - R * 0.4, R * 0.28, hex('#3fe8ff', tit), t);
    yildiz5(xm + R * 1.9, ym - R * 0.4, R * 0.28, hex('#ffe23a', tit), t);
  }
  cx.restore();
}

// HUD: motor 15 cubugu + ustte "MISSIONS: n/6" (REF-070, level icindeki duvar sirasi)
function yildizHud(t, tur, il) {
  yildizHud18(t, tur, il);
  if (!TEMA.kopru) return;
  const liste = DUVARLAR.filter(d => d.tur === tur);
  if (!liste.length) return;
  const n = kisit(liste.filter(d => t >= d.t0).length, 1, liste.length);
  yazi(`MISSIONS: ${n}/${liste.length}`, W / 2, 22 * k, 34 * k, ['#ffffff', '#ffe6f6'], '#c4106a', 1);
}
