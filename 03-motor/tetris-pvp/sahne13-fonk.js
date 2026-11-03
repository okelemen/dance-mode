// sahne13-kur.py: her "//@@ ad" blogu sahne11.html'deki ayni adli fonksiyonu degistirir.
//@@ altinGok
function altinGok(t) {
  // REF-067 gogu sabit cizim; ustune vurusa hafif nabiz. Yapraklar ayri katmanda (yapraklar), t'den deterministik.
  cx.drawImage(GOK, 0, 0, W, H);
  const vurusF = (t * BPM / 60) % 1, nab = Math.pow(1 - vurusF, 3);
  cx.save(); cx.globalCompositeOperation = 'lighter'; cx.globalAlpha = 0.10 * nab; cx.drawImage(GOK, 0, 0, W, H); cx.restore();
}
function yapraklar(t) {
  for (let i = 0; i < 70; i++) {
    const r = rng(2600 + i * 31), hz = 40 + 70 * r(), x = ((r() * W + Math.sin(t * 0.9 + i) * 60 * k + t * 30 * k) % W + W) % W;
    const y = ((r() * H + t * hz * k) % (H + 40 * k)) - 20 * k, b = (7 + 8 * r()) * k, ac = t * (1 + 2 * r()) + i;
    cx.save(); cx.translate(x, y); cx.rotate(ac); cx.scale(1, 0.45 + 0.4 * Math.sin(t * 3 + i));
    cx.fillStyle = i % 3 ? 'rgba(255,200,236,0.92)' : 'rgba(255,255,255,0.9)';
    cx.beginPath(); cx.ellipse(0, 0, b, b * 0.6, 0, 0, 6.283); cx.fill(); cx.restore();
  }
}
//@@ sahneCiz
let MASKOT_ALFA = 1;
function sahneCiz(t) {
  altinGok(t);
  cx.drawImage(SERIT1, 0, 0, W / 2, H);
  cx.drawImage(SERIT2, W / 2, 0, W / 2, H);
  for (let i = 0; i < 2; i++) if (TEMA.oklar !== false) yolOklari(t, i);
  salincak(t, MASKOT_ALFA);
  yapraklar(t);
}
//@@ duvarCiz
// REF-067: duvar = beyaz girdapli kart (oyuncu renginde girdap) + ortada DUZ SIMSIYAH poz; ince beyaz kenar + renkli isilti
function kapiKart(i) {                                         // kapi acikliginda dik kart (oran acikliktan)
  const A = aciklik(i), w = A.w * 0.9, h = A.h * 0.92;
  return { x: A.x + (A.w - w) / 2, y: A.y + A.h - h - A.h * 0.02, w, h };
}
function duvarCiz(i, kutu, maske, alfa) {
  if (alfa <= 0 || !maske) return;
  const { x, y, w, h } = kutu, r = Math.min(w, h) * 0.06;
  cx.save(); cx.beginPath(); cx.rect(i * W / 2, 0, W / 2, H); cx.clip();
  cx.globalAlpha = alfa;
  cx.shadowColor = RENK[i]; cx.shadowBlur = Math.max(10, w * 0.06);
  cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(x, y, w, h, r); cx.fill(); cx.shadowBlur = 0;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, w, h, r); cx.clip(); cx.drawImage(GIRDAP[i], x, y, w, h); cx.restore();
  const mh = h * 0.86, mw = mh * maske.width / maske.height, s = Math.min(1, w * 0.92 / mw);
  cx.drawImage(maske, x + w / 2 - mw * s / 2, y + h * 0.96 - mh * s, mw * s, mh * s);
  cx.lineWidth = Math.max(2, w * 0.012); cx.strokeStyle = 'rgba(255,255,255,0.95)'; cx.beginPath(); cx.roundRect(x, y, w, h, r); cx.stroke();
  cx.restore();
}
//@@ oyuncuKarti
function oyuncuKarti(i, p, t = SON_T) {
  // REF-067 kapidaki "PLAYER" kafesi: koyu kart, oyuncu renginde parmakliklar, ustte piksel PLAYER N, ortada P1/P2
  const K = kapiKart(i), giris = ease(kisit(p, 0, 1));
  const s = 0.85 + 0.15 * giris, w = K.w * s, h = K.h * s, x = K.x + K.w / 2 - w / 2, y = K.y + K.h - h;
  cx.save(); cx.globalAlpha *= giris;
  cx.shadowColor = RENK[i]; cx.shadowBlur = 30 * k;
  const g = cx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, i ? '#3a0a3a' : '#0a1a4a'); g.addColorStop(1, i ? '#7a1068' : '#103a8a');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x, y, w, h, 20 * k); cx.fill(); cx.shadowBlur = 0;
  cx.lineWidth = 8 * k; cx.strokeStyle = RENK[i]; cx.stroke();
  yazi(i === 0 ? 'P1' : 'P2', x + w / 2, y + h * 0.56, h * 0.36 * (1 + 0.04 * Math.sin(t * 6)), i === 0 ? ['#ffffff', TEMA.p1acik, P1] : ['#ffffff', TEMA.p2acik, P2], '#2a0a4a', 1, RENK[i]);
  cx.lineWidth = 7 * k; cx.strokeStyle = hex(i ? TEMA.p2parlak : TEMA.p1parlak, 0.85);       // kafes parmakliklari
  for (let j = 1; j < 6; j++) { const bx = x + w * j / 6; cx.beginPath(); cx.moveTo(bx, y + h * 0.2); cx.lineTo(bx, y + h - 8 * k); cx.stroke(); }
  cx.beginPath(); cx.moveTo(x + 6 * k, y + h * 0.2); cx.lineTo(x + w - 6 * k, y + h * 0.2); cx.stroke();
  pikselYazi(i === 0 ? 'PLAYER 1' : 'PLAYER 2', x + w / 2, y + h * 0.1, h * 0.085, ['#ffffff', i ? TEMA.p2acik : TEMA.p1acik], 1, i ? TEMA.p2koyu : TEMA.p1koyu);
  cx.restore();
}
//@@ kapiKutusu
function kapiKutusu(i) { return kapiKart(i); }
//@@ tabela
function tabela(i, t, alfa) { oyuncuKarti(i, alfa, t); }
//@@ bosPaneller
function bosPaneller(alfa = 1) { for (let i = 0; i < 2; i++) oyuncuKarti(i, alfa); }
//@@ duvarlarCiz
function maskotAlfa(e) {                                     // sayim ve buyume sirasinda maskot iki kapi arasindan cekilir
  if (e.ad === 'kart') return 1;
  if (e.ad === 'say') return 1 - ease(Math.min(1, e.p * 4));
  if (e.ad === 'bos') return ease(Math.min(1, e.p * 2));
  return 0;
}
function duvarlarCiz(d, u) {
  const e = evre(u);
  AKTIF_NO = d.no;
  if (e.ad === 'kart') { bosPaneller(Math.min(1, e.p * 4)); return e; }
  if (e.ad === 'bos') bosPaneller(ease(Math.min(1, e.p * 2)));
  for (let i = 0; i < 2; i++) {
    const maske = MASKE[i === 0 ? d.p1 : d.p2];
    const A2 = kapiKart(i), B = { x: i * W / 2 + W * 0.02, y: H * 0.03, w: W / 2 - W * 0.04, h: H * 0.94 };
    if (e.ad === 'say') {
      const fl = kisit(1 - e.p * Z.say / 0.25, 0, 1);
      duvarCiz(i, olcekle(A2, 0.7 + 0.3 * ease(kisit(e.p * Z.say / 0.3, 0, 1))), maske, ease(kisit(e.p * Z.say / 0.2, 0, 1)));
      if (fl > 0) { cx.fillStyle = `rgba(255,255,255,${0.6 * fl})`; cx.fillRect(A2.x, A2.y, A2.w, A2.h); }
    } else if (e.ad === 'buyu') {
      duvarCiz(i, kutuLerp(A2, B, Math.pow(e.p, 2.1)), maske, 1);
    } else if (e.ad === 'gec') {
      const q = ease(e.p);
      duvarCiz(i, olcekle(B, 1 + 0.35 * q), maske, 1 - q);
    }
  }
  return e;
}
//@@ sayimCiz
function sayimCiz(e) {
  if (e.ad !== 'say') return;
  const n = 3 - Math.min(2, Math.floor(e.p * 3)), q = (e.p * 3) % 1;
  const A = aciklik(0), s = 1.3 - 0.3 * ease(Math.min(1, q / 0.25));
  yazi(String(n), W / 2, A.y + A.h * 0.45, 190 * k * s, ['#ffffff', '#fff0fa', '#ffd6f2'], '#c0168a', 1, '#ff7ad0');
}
//@@ ovguCiz
function ovguCiz(d, e) { }   // REF-067'de duvar basina ovgu yazisi yok; tezahurat tam ekran kartlarda (gecis)
//@@ hudCiz
function hudCiz(t) {
  // REF-067: sol ustte ROUND N; ustte iki avatarli cekisme cubugu (sol mavi, sag pembe), ortada kupa
  const tur = turBul(t);
  pikselYazi('ROUND ' + tur, 150 * k, 46 * k, 56 * k, ['#ffffff', '#f0e6ff'], 1, '#5a1f86');
  const x0 = 330 * k, x1 = W - 120 * k, y = 46 * k, h = 26 * k, xm = (x0 + x1) / 2;
  const turD = DUVARLAR.filter(x => x.tur === tur), n = turD.filter(x => t >= x.t0).length, oran = turD.length ? n / turD.length : 0;
  const orta = xm + (x1 - x0) * Math.sin(t * 1.3) * 0.04 * (1 - oran);
  cx.save();
  cx.fillStyle = 'rgba(255,255,255,0.85)'; cx.beginPath(); cx.roundRect(x0 - 6 * k, y - h / 2 - 6 * k, x1 - x0 + 12 * k, h + 12 * k, h); cx.fill();
  const g1 = cx.createLinearGradient(0, y - h / 2, 0, y + h / 2); g1.addColorStop(0, TEMA.p1acik); g1.addColorStop(1, P1);
  cx.fillStyle = g1; cx.beginPath(); cx.roundRect(x0, y - h / 2, orta - x0, h, h / 2); cx.fill();
  const g2 = cx.createLinearGradient(0, y - h / 2, 0, y + h / 2); g2.addColorStop(0, TEMA.p2acik); g2.addColorStop(1, P2);
  cx.fillStyle = g2; cx.beginPath(); cx.roundRect(orta, y - h / 2, x1 - orta, h, h / 2); cx.fill();
  cx.lineWidth = 3 * k; cx.strokeStyle = '#5a1f86'; cx.beginPath(); cx.roundRect(x0 - 6 * k, y - h / 2 - 6 * k, x1 - x0 + 12 * k, h + 12 * k, h); cx.stroke();
  cx.translate(orta, y); cx.fillStyle = '#ffd94a'; cx.strokeStyle = '#7a3a00'; cx.lineWidth = 3 * k;   // kupa
  cx.beginPath(); cx.moveTo(-20 * k, -26 * k); cx.lineTo(20 * k, -26 * k); cx.quadraticCurveTo(18 * k, 4 * k, 0, 8 * k); cx.quadraticCurveTo(-18 * k, 4 * k, -20 * k, -26 * k); cx.fill(); cx.stroke();
  cx.fillRect(-4 * k, 8 * k, 8 * k, 10 * k); cx.beginPath(); cx.roundRect(-14 * k, 16 * k, 28 * k, 8 * k, 3 * k); cx.fill(); cx.stroke();
  cx.restore();
  for (const [i, ax] of [[0, x0 + 30 * k], [1, x1 - 30 * k]]) {                     // avatarlar: oyuncu renginde rozet
    cx.save(); cx.fillStyle = RENK[i]; cx.strokeStyle = '#ffffff'; cx.lineWidth = 5 * k; cx.shadowColor = RENK[i]; cx.shadowBlur = 16 * k;
    cx.beginPath(); cx.arc(ax, y, 30 * k, 0, 6.283); cx.fill(); cx.shadowBlur = 0; cx.stroke(); cx.restore();
    yazi(i ? 'P2' : 'P1', ax, y + 2 * k, 30 * k, '#ffffff', '#2a0a4a');
  }
}
//@@ nasilCiz
function nasilCiz(kart, u, t) {
  // HOW TO PLAY (REF-067: mor izgara zemin + cerceveli sahne): kart gelir, siluet karta oturur, PERFECT!
  izgaraZemin(t);
  pikselYazi('HOW TO PLAY', W / 2, H * 0.11, 110 * k, ['#ffffff', '#ffd6f2', '#ff9ae0'], ease(kisit(u / 0.3, 0, 1)));
  const ad = kart.poz || (DUVARLAR[0] && DUVARLAR[0].p1), m = MASKE[ad];
  if (!m) return;
  const fw = W * 0.56, fh = fw * 9 / 16, fx = W / 2 - fw / 2, fy = H * 0.19;
  cx.save(); cx.shadowColor = '#ff7ad0'; cx.shadowBlur = 30 * k; cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(fx - 12 * k, fy - 12 * k, fw + 24 * k, fh + 24 * k, 24 * k); cx.fill(); cx.restore();
  cx.save(); cx.beginPath(); cx.roundRect(fx, fy, fw, fh, 16 * k); cx.clip();
  cx.drawImage(GOK, fx, fy, fw, fh); cx.drawImage(SERIT1, fx, fy, fw / 2, fh); cx.drawImage(SERIT2, fx + fw / 2, fy, fw / 2, fh);
  const K = { x: fx + fw * 0.06, y: fy + fh * 0.1, w: fw * 0.38, h: fh * 0.84 };
  cx.restore();
  duvarCiz(0, K, m, 1);
  const otur = kart.sure * 0.55, q = ease(kisit((u - 0.4) / (otur - 0.4), 0, 1));
  const mh = K.h * 0.86, mw = mh * m.width / m.height;
  cx.save(); cx.globalAlpha = kisit((u - 0.3) / 0.2, 0, 1) * 0.6;
  cx.drawImage(m, K.x + K.w / 2 - mw / 2 + lerp(fw * 0.5, 0, q), K.y + K.h * 0.96 - mh, mw, mh);
  cx.restore();
  pikselYazi(kart.metin || 'COPY YOUR SHAPE', W / 2, H * 0.82, 80 * k, ['#ffffff', '#ffd6f2'], kisit((u - 0.5) / 0.3, 0, 1));
  pikselYazi(kart.alt || 'BEFORE THE CARD REACHES YOU!', W / 2, H * 0.93, 52 * k, ['#ffffff', '#e6dcff'], kisit((u - 0.9) / 0.3, 0, 1), '#5a1f86');
  if (u >= otur) {
    const q2 = u - otur;
    pikselYazi('PERFECT!', W / 2 + fw * 0.12, fy + fh / 2, 140 * k * (1 + 0.3 * Math.exp(-q2 * 8)), ['#ffffff', '#fff27a', '#ffb000'], Math.min(1, q2 / 0.1));
  }
}
