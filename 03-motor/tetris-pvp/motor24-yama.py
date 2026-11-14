"""motor 24 (HUMAN TETRIS 27, CO-OP karli zirve) = sahne23.html + bu yamalar -> sahne24.html. Eski motorlar degismez (TALIMATLAR §6).

    python motor24-yama.py

CO-OP (tek serit, tek sari duvar, ikili siluet): varlik-dag.py (gok.png + serit.png 1920), karakter.py --ikili (p1/p2 ayni genis kare,
birlikte ikili poz), maskot <grup>-A / <grup>-B. Maskot ekranin ortasinda kapinin kirisi ustunde (TALIMATLAR §4: kenar yasak; abone ve
3-2-1 yanlara kayar). Ust: solda tur adi, sagda WALLS CLEARED n/24. BLIND ROUND: siluet tipinin arkasinda, son 1,5 sn'de belirir.
OUT: biri gec kalirsa duvar ikisini kar yiginlarina iter (P1 sola, P2 saga), kar patlamasi.
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(BURA, "..", "sahne23.html"), encoding="utf-8").read()


def r(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:80])
    t = t.replace(a, b)


r('<title>HUMAN TETRIS 26 - motor 23 (iki serit tropik plaj, MIRROR turu, yarisan karakterler, cankurtaran hakem maskot)</title>',
  '<title>HUMAN TETRIS 27 - motor 24 (CO-OP tek serit karli zirve, BLIND turu, ikili karakterler, kayakci hakem maskot)</title>')
r('html,body { margin:0; background:#3aa8ff; overflow:hidden; }', 'html,body { margin:0; background:#1a8cff; overflow:hidden; }')
r('''// =====================================================================
// MOTOR 23 — HUMAN TETRIS 26''', '''// =====================================================================
// MOTOR 24 — HUMAN TETRIS 27 (REFERANSSIZ, CO-OP 2 oyuncu, 14 Kas 2026; motor 23'ten, tetris-pvp/motor24-yama.py). TALIMATLAR §2b 4. mekan:
//   - sahne: tetris-pvp/varlik-dag.py (TEK serit: gok.png + serit.png; turkuaz buz pist, kar setleri, buz kristali kapi); gokte kar yagar
//   - tek sari CO-OP duvari, ikili siluet (d.grup); iki karakter (karakter.py --ikili) ayni yerde birlikte ikili pozu yapar
//   - OUT (CO-OP): biri gec kalirsa duvar ikisini birden kar yiginlarina iter (P1 sola, P2 saga), kar patlamasi; o duvar sayilmaz
//   - hakem maskot (kayakci bere + atki) ekranin ortasinda kapinin kirisi ustunde; once A sonra B figurunu gosterir
//   - ust: solda tur adi, sagda WALLS CLEARED n/24; abone solda, 3-2-1 sagda (maskot ortada kalir)
//   - BLIND ROUND (d.blind): duvar kar firtinasiyla ortulu (BLIND! + ?), siluet son 1,5 sn'de belirir; karakterler ve maskot ondan sonra poza girer
// =====================================================================
// MOTOR 23 — HUMAN TETRIS 26''')
# ---- varliklar: tek serit
r('''const [GOK, ...SERIT] = await Promise.all(['gok.png', ...OY.map(o => 'serit-' + o + '.png')].map(a => resim(VARLIK + a)));''',
  '''const [GOK, ...SERIT] = await Promise.all(['gok.png', 'serit.png'].map(a => resim(VARLIK + a)));   // motor 24: CO-OP tek serit''')
r('''  bg.drawImage(GOK, -40, -40, W + 80, H + 80); SERIT.forEach((im, i) => bg.drawImage(im, i * W / 2 - 20, -40, W / 2 + 40, H + 80)); bg.filter = 'none'; }''',
  '''  bg.drawImage(GOK, -40, -40, W + 80, H + 80); bg.drawImage(SERIT[0], -40, -40, W + 80, H + 80); bg.filter = 'none'; }''')
r('''const POZ_ADLAR = [...new Set(DUVARLAR.flatMap(d => OY.map(o => d[o])).filter(Boolean))];''',
  '''const POZ_ADLAR = [...new Set(DUVARLAR.map(d => d.grup).filter(Boolean))];          // motor 24: duvar basina tek ikili maske''')
r('''  const adlar = o === 'maskot' ? POZ_ADLAR : [...new Set(DUVARLAR.map(d => d[o]))];''',
  '''  const adlar = o === 'maskot' ? POZ_ADLAR.flatMap(a => [a + '-A', a + '-B']) : POZ_ADLAR;   // motor 24: ikili kareler''')
# ---- sahne: kar yagisi, tek serit
r('''function sahneCiz(t) {
  cx.drawImage(GOK, 0, 0, W, H);
  konfeti(t, 0.42, 40);                                        // tribun ustunde dusen konfeti (hareketli gok)
  SERIT.forEach((im, i) => cx.drawImage(im, i * SW, 0, SW, H));''', '''const KAR_R = rng(127);
const KAR_T = Array.from({ length: 150 }, () => ({ x: KAR_R(), y: KAR_R(), v: 0.05 + KAR_R() * 0.09, r: 2 + KAR_R() * 4.5, f: KAR_R() * 6.28, a: 0.55 + KAR_R() * 0.45 }));
function karYagisi(t, alfa = 1) {                              // motor 24: gokte ve sahnede yavas dusen kar taneleri (hareketli gok)
  cx.save();
  for (const p of KAR_T) {
    const y = ((p.y + t * p.v) % 1.05) * H - 0.02 * H, x = ((p.x + Math.sin(t * 0.8 + p.f) * 0.01) % 1) * W;
    cx.globalAlpha = p.a * alfa; cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(x, y, p.r * k, 0, 6.283); cx.fill();
  }
  cx.restore();
}
function sahneCiz(t) {
  cx.drawImage(GOK, 0, 0, W, H);
  cx.drawImage(SERIT[0], 0, 0, W, H);                          // motor 24: tek serit
  karYagisi(t);''')
r('''function aciklik(i) {                                          // kapi acikligi (serit koordinati -> ekran)
  const a = YER['aciklik_' + OY[i]], sx = SW / SERIT_W, sy = H / 1080;
  return { x: i * SW + a[0] * sx, y: a[1] * sy, w: (a[2] - a[0]) * sx, h: (a[3] - a[1]) * sy };
}''', '''function aciklik(i) {                                          // kapi acikligi (serit koordinati -> ekran); motor 24: tek kapi
  const a = YER['aciklik_p1'], sx = W / SERIT_W, sy = H / 1080;
  return { x: a[0] * sx, y: a[1] * sy, w: (a[2] - a[0]) * sx, h: (a[3] - a[1]) * sy };
}''')
# ---- duvar karti: sari CO-OP duvari
r('''  // motor 22: buzlu beyaz pano + oyuncu renginde kalin cerceve - pastel degrade yok
  const g = cx.createLinearGradient(0, y, 0, y + h);
  g.addColorStop(0, '#ffffff'); g.addColorStop(0.5, '#f3f5f9'); g.addColorStop(1, '#e4e8ef');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.fill();
  cx.strokeStyle = RENK[i]; cx.lineWidth = Math.max(6 * k, w * 0.025); cx.stroke();''', '''  // motor 24: CO-OP sari duvar (kapak ile ayni), cilali ust yansima + buz mavisi kalin cerceve
  const g = cx.createLinearGradient(0, y, 0, y + h);
  g.addColorStop(0, '#fff27a'); g.addColorStop(0.5, '#ffd21a'); g.addColorStop(1, '#ffb81a');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.fill();
  const yg = cx.createLinearGradient(0, y, 0, y + h * 0.3); yg.addColorStop(0, 'rgba(255,255,255,0.45)'); yg.addColorStop(1, 'rgba(255,255,255,0)');
  cx.fillStyle = yg; cx.fill();
  cx.strokeStyle = '#1a6ad8'; cx.lineWidth = Math.max(6 * k, w * 0.012); cx.stroke();''')
# ---- duvar + BLIND
a0 = t.index('function duvarCiz(d, u, t) {')
a1 = t.index('function freezeCiz(u, T, t) {')
t = t[:a0] + '''function tipi(x, y, w, h, t, alfa) {                          // motor 24 BLIND: kartin ustunde kar firtinasi (beyaz sis + capraz akan kar cizgileri)
  if (alfa <= 0.01) return;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.clip();
  cx.globalAlpha = alfa;
  const g = cx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(240,250,255,0.97)'); g.addColorStop(1, 'rgba(205,232,255,0.97)');
  cx.fillStyle = g; cx.fillRect(x, y, w, h);
  const R = rng(2727);
  cx.strokeStyle = 'rgba(150,200,240,0.75)'; cx.lineCap = 'round';
  for (let j = 0; j < 70; j++) {
    const px = x + ((R() + t * (0.35 + R() * 0.3)) % 1) * (w + 200 * k) - 100 * k, py = y + ((R() + t * (0.6 + R() * 0.4)) % 1) * h, L = (20 + R() * 40) * k;
    cx.lineWidth = (2 + R() * 3) * k; cx.beginPath(); cx.moveTo(px, py); cx.lineTo(px + L, py + L * 0.45); cx.stroke();
  }
  cx.restore();
}
function duvarCiz(d, u, t) {
  const Z = ZD(d), a = Z.kart, b = a + Z.say, c = b + Z.buyu, T = Z.tut || 0;
  if (u >= c + T) { tamEkran(d, u - c - T, t); return null; }
  const K = aciklik(0);
  let s = 1, alfa = 1, kar = 0, acik = 1;
  if (u < a) { const q = kisit(u / a, 0, 1); alfa = ease(kisit(q / 0.3, 0, 1)); acik = ease(kisit((q - 0.15) / 0.85, 0, 1)); }
  else if (u >= b) { const q = (u - b) / Z.buyu; s = 1 + 0.55 * ease(kisit(q / 0.75, 0, 1)); kar = kisit((q - 0.65) / 0.3, 0, 1); }
  else s = 1 + 0.015 * Math.sin((u - a) * 5);
  if (d.boss) s *= 1.12;                                     // BOSS WALL: buyuk duvar
  const w = K.w * s, h = K.h * s, x = K.x + K.w / 2 - w / 2, y = K.y + K.h / 2 - h / 2 - (s - 1) * K.h * 0.12;
  const ac = d.blind ? acilma(d, u) : 1;                     // BLIND: siluet son 1,5 sn'de belirir
  if (kar < 1) {
    kartZemin(0, x, y, w, h, t, alfa * (1 - kar));
    siluet(d.grup, x, y, w, h, alfa * (1 - kar) * ac);
    if (d.blind) {
      tipi(x, y, w, h, t, alfa * (1 - ac));
      const p = 1 + 0.05 * Math.sin(t * 5);
      if (ac < 0.98) {
        yaziK('BLIND!', x + w / 2, y + h * 0.36, 120 * k * p, ['#ffffff', '#bff0ff', '#3ac8ff'], alfa * (1 - ac), '#06306a', '#ffffff');
        yaziK('?', x + w / 2, y + h * 0.7, 150 * k * p, ['#ffffff', '#bff0ff', '#3ac8ff'], alfa * (1 - ac), '#06306a', '#ffffff');
      }
    }
  }
  if (d.boss && kar < 1) {                                   // BOSS WALL: kirmizi nabiz cerceve
    cx.save(); cx.globalAlpha = (0.6 + 0.4 * Math.sin(t * 12)) * (1 - kar); cx.strokeStyle = '#ff2a3a'; cx.lineWidth = 14 * k;
    cx.shadowColor = '#ff2a3a'; cx.shadowBlur = 30 * k; cx.strokeRect(x - 8 * k, y - 8 * k, w + 16 * k, h + 16 * k); cx.restore();
  }
  if (u < a) kepenk(0, K, acik, t);
  if (kar > 0) {                                             // kapi kararir: duvar gecti
    cx.save(); cx.globalAlpha = kar * 0.88; cx.fillStyle = '#0a0618'; cx.fillRect(K.x, K.y, K.w, K.h); cx.restore();
  }
  karakterCiz(d, u, t);
  return u >= a && u < b ? (u - a) / Z.say : null;
}
function acilma(d, u) {                                       // BLIND: 0 = gizli, 1 = acik (sayimin son 1,5 sn'si); BLIND olmayan duvarda 1
  if (!d.blind) return 1;
  const Z = ZD(d), b = Z.kart + Z.say;
  return ease(kisit((u - (b - 1.5)) / 0.3, 0, 1));
}
''' + t[a1:]
# ---- tam ekran: tek panel
a0 = t.index('// tam ekran acilis: iki pastel panel')
a1 = t.index('// iki kapinin arasinda 3-2-1')
t = t[:a0] + '''// tam ekran: tek panel (motor 24 CO-OP) - bulanik zirve + buz mavisi ton, ortada ikilinin dev silueti; OUT ise kar + OUT!
function tamEkran(d, u, t) {
  const Z = ZD(d);
  const gir = ease(kisit(u / 0.35, 0, 1)), cik = 1 - ease(kisit((u - (Z.gec - 0.35)) / 0.35, 0, 1)), a = gir * cik;
  const out = d.out && (d.out.p1 || d.out.p2);
  cx.save(); cx.globalAlpha = a;
  cx.drawImage(BULANIK, 0, 0, W, H);
  const g = cx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, out ? 'rgba(90,150,230,0.55)' : 'rgba(40,160,255,0.55)'); g.addColorStop(1, out ? 'rgba(20,40,110,0.8)' : 'rgba(10,70,180,0.75)');
  cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  const hl = cx.createRadialGradient(W / 2, H * 0.55, 0, W / 2, H * 0.55, W * 0.45);
  hl.addColorStop(0, 'rgba(255,255,255,0.85)'); hl.addColorStop(0.6, 'rgba(255,255,255,0.35)'); hl.addColorStop(1, 'rgba(255,255,255,0)');
  cx.fillStyle = hl; cx.fillRect(0, 0, W, H);
  cx.restore();
  karYagisi(t, a);
  const zip = 1 + 0.04 * Math.sin(kisit(u / 0.5, 0, 1) * Math.PI);
  const sw = W * 0.86 * zip, sh = H * 0.84 * zip;
  siluet(d.grup, W / 2 - sw / 2, H * 0.14 + (H * 0.84 - sh), sw, sh, a * (out ? 0.45 : 1), '#000000', 7 * k, '#7ad8ff');
  const pp = kisit((u - 0.2) / 0.3, 0, 1), ps = ease(pp) * (1 + 0.15 * Math.sin(pp * Math.PI));
  if (out) {
    sicrama(W * 0.3, H * 0.66, u, 1.4); sicrama(W * 0.7, H * 0.66, u - 0.1, 1.4);
    yaziK('OUT!', W / 2, H * 0.46, 170 * k * ps, ['#ffffff', '#ff8a8a', '#ff1a2a'], a * pp, '#3a0010', '#ff4a4a');
    return;
  }
  yaziK('+1', W * 0.86, H * 0.2, 120 * k * ps, ['#fff6a0', '#ffd23a', '#ff8a1a'], a * pp, KON, '#ffffff');
  const m = d.ovgu || TEMA.ovgu[(d.no - 1) % TEMA.ovgu.length];
  const pop = kisit((u - 0.25) / 0.3, 0, 1), s = ease(pop) * (1 + 0.12 * Math.sin(pop * Math.PI));
  yaziK(m, W / 2, H * 0.5, 150 * k * s, ['#fff6a0', '#ffd23a', '#ff8a1a'], a * pop, KON, '#ffffff');
}

''' + t[a1:]
# ---- 3-2-1 sagda (maskot ortada)
r('''  yaziK(String(n), W / 2, H * 0.37, 170 * k * s, ['#ffffff', '#ffd6f2', '#ff4ad0'], 1, '#24083e', '#ff6ad6');   // md. 28: alt uc 2,6 -> 6,1''',
  '''  yaziK(String(n), W * 0.84, H * 0.43, 190 * k * s, ['#ffffff', '#ffd6f2', '#ff4ad0'], 1, '#24083e', '#ff6ad6');   // motor 24: sagda (maskot ortada); md. 28''')
# ---- HUD
a0 = t.index('function skorBul(t) {')
a1 = t.index('// ilk iki duvarda ustte HOW TO PLAY seridi')
t = t[:a0] + '''function skorBul(t) {
  let s = 0, son = -1;
  for (const d of DUVARLAR) { const Z = ZD(d); const tt = d.t0 + Z.kart + Z.say + Z.buyu; if (t >= tt) { s = d.skor; son = d.skor !== (DUVARLAR[d.no - 2] || { skor: 0 }).skor ? tt : son; } }
  return [s, son];
}
// motor 24: sag ustte WALLS CLEARED n/24 (mobil paket md. 3, CO-OP); sol ustte tur adi; orta ust maskotun
function hudCiz(t, tur) {
  const [s, son] = skorBul(t), pop = son >= 0 && t - son < 0.5 ? 1 + 0.35 * Math.sin((t - son) / 0.5 * Math.PI) : 1;
  const w = 470 * k, h = 84 * k, xm = W - w / 2 - 30 * k, y = H * 0.06;
  cx.save(); cx.shadowColor = 'rgba(10,30,90,0.5)'; cx.shadowBlur = 18 * k;
  cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(xm - w / 2, y - h / 2, w, h, h / 2); cx.fill(); cx.shadowBlur = 0;
  cx.lineWidth = 6 * k; cx.strokeStyle = KON; cx.stroke();
  cx.fillStyle = '#1a6ad8'; cx.beginPath(); cx.roundRect(xm - w / 2 + 7 * k, y - h / 2 + 7 * k, 280 * k, h - 14 * k, (h - 14 * k) / 2); cx.fill();
  cx.restore();
  yaziK('WALLS CLEARED', xm - w / 2 + 147 * k, y, 34 * k, ['#ffffff', '#ffffff'], 1, '#06306e');
  yaziK(s + '/' + TOPLAM_DUVAR, xm + w / 2 - 92 * k, y, 54 * k * pop, ['#ffffff', '#d6f2ff', '#1a8cff'], 1, '#24083e');
  const ad = TEMA.turAd[tur] || ('ROUND ' + tur);
  cx.font = F(52 * k); const yw = cx.measureText(ad).width;
  yaziK(ad, Math.max(190 * k, yw / 2 + 34 * k), H * 0.06, 52 * k, ['#f0fff8', '#7affd0', '#1ac8a0'], 1);
}
''' + t[a1:]
r('''  cx.save(); cx.globalAlpha = a; cx.fillStyle = 'rgba(20,10,60,0.72)'; cx.beginPath(); cx.roundRect(W / 2 - 720 * k, H * 0.118 - 33 * k, 1440 * k, 66 * k, 33 * k); cx.fill(); cx.restore();
  satir([['COPY THE SHAPE ON YOUR SIDE  ·  ', '#ffffff'], ['BLUE', RENK[0]], [' LEFT  ', '#ffffff'], ['PINK', '#ff6ade'], [' RIGHT', '#ffffff']], W / 2, H * 0.118, 42 * k, a);   // md. 28: PINK #ff2ad2 mor konturla 4,2 -> 5,4''',
  '''  // motor 24: iki parca, kapinin iki yaninda (orta ust maskotun; sol ust abone, sag 3-2-1 ile cakismaz)
  cx.save(); cx.globalAlpha = a; cx.fillStyle = 'rgba(20,10,60,0.72)';
  cx.beginPath(); cx.roundRect(W * 0.15 - 260 * k, H * 0.56 - 31 * k, 520 * k, 62 * k, 31 * k); cx.fill();
  cx.beginPath(); cx.roundRect(W * 0.85 - 260 * k, H * 0.56 - 31 * k, 520 * k, 62 * k, 31 * k); cx.fill(); cx.restore();
  satir([['MAKE THE SHAPE TOGETHER', '#ffffff']], W * 0.15, H * 0.56, 32 * k, a);
  satir([['BLUE', RENK[0]], [' LEFT  ·  ', '#ffffff'], ['PINK', '#ff6ade'], [' RIGHT', '#ffffff']], W * 0.85, H * 0.56, 34 * k, a);   // md. 28: PINK #ff6ade''')
# ---- kar sicramasi
r('''    cx.fillStyle = ['#ffd27a', '#f3a53a', '#fff1c4'][j % 3]; cx.beginPath(); cx.arc(x, y, (5 + 8 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 23: kum tanesi''',
  '''    cx.fillStyle = ['#ffffff', '#dff2ff', '#b8e2ff'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 24: kar topagi''')
r('''  cx.strokeStyle = 'rgba(255,214,140,0.9)'; cx.lineWidth = 14 * k * (1 - q);''', '''  cx.strokeStyle = 'rgba(235,248,255,0.95)'; cx.lineWidth = 16 * k * (1 - q);''')
# ---- karakterler: ikili
a0 = t.index('function karakterCiz(d, u, t) {')
a1 = t.index('// ------------------------------------------------------------ HAKEM MASKOT')
t = t[:a0] + '''function karakterCiz(d, u, t) {                               // motor 24: iki karakter ayni genis karede, birlikte ikili poz
  const Z = ZD(d), a = Z.kart, b = a + Z.say, ad = d.grup;
  const out = !!(d.out && (d.out.p1 || d.out.p2));
  const bas = d.blind ? (b - 1.5 - a) / Z.say : 0.35, sure = d.blind ? 1.2 / Z.say : 0.4;    // BLIND: siluet acilinca poza girer
  for (let i = 0; i < 2; i++) {
    const o = OY[i], Y = KY[o], L = KR[o][ad]; if (!L) continue;
    const gec = out && d.out[o];                                // gec kalan oyuncu poza yarim girer
    const sc = H * KAR_BOY / Y.boy_px, pw = Y.w_px * sc, ph = Y.h_px * sc;
    let j = 0, dx = 0, dy = 0, don = 0, bob = 0;
    const sq = (u - a) / Z.say;
    if (u < a || sq < bas) bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI + i * 0.6)) * 8 * k;
    else j = (gec ? 0.5 : 1) * (KK - 1) * ease(kisit((sq - bas) / sure, 0, 1));
    if (u >= b) j = gec ? (KK - 1) * 0.5 : KK - 1;
    const kf = Y.poz[ad].kalca[kisit(Math.round(j), 0, KK - 1)];
    const x0 = W / 2 - pw / 2, y0 = H * 0.985 - Y.zemin_px * sc;
    const hx = x0 + kf[0] * sc, hy = y0 + kf[1] * sc;
    if (out && u >= b) {                                        // OUT: duvar ikisini iter -> kendi tarafindaki kar yiginina gomulur
      const q = kisit((u - b - Z.buyu * 0.45) / (Z.buyu * 0.55), 0, 1);
      const hedef = YER.dag ? (i ? YER.dag.yigin_sag_x : YER.dag.yigin_sol_x) * W / SERIT_W : (i ? W * 0.8 : W * 0.2);
      dx = (hedef - hx) * q; dy = 200 * k * q * q - 140 * k * Math.sin(q * Math.PI); don = (i ? 1 : -1) * 1.5 * q;
      if (q >= 0.85) sicrama(hedef, (YER.dag ? YER.dag.yigin_y * H / 1080 : H * 0.8), (q - 0.85) * Z.buyu * 0.55, 1);
      if (q >= 0.98) continue;
    }
    const im = karKare(o, ad, j); if (!im) continue;
    cx.save(); cx.translate(hx + dx, hy + dy - bob); cx.rotate(don); cx.translate(-hx, -hy);
    cx.shadowColor = RENK[i]; cx.shadowBlur = 22 * k;
    cx.drawImage(im, x0, y0, pw, ph);
    cx.restore();
  }
}

''' + t[a1:]
r('''const KAR_BOY = 0.34;                                          // ekranda karakter boyu (H orani)''',
  '''const KAR_BOY = 0.36;                                          // ekranda karakter boyu (H orani; motor 24 ikili: ayakta govde boyu)''')
# ---- hakem maskot: kapinin ustunde ortada
a0 = t.index('function hakemCiz(t, d, u) {')
a1 = t.index('function hakemBalon(d, u, t) {')
t = t[:a0] + '''function hakemCiz(t, d, u) {                                   // motor 24: kapinin kirisi ustunde ortada; once A sonra B figurunu gosterir
  const K = aciklik(0), xm = W / 2, ay = K.y - 6 * k, Y = KY.maskot;
  cx.save(); cx.fillStyle = '#ffffff'; cx.shadowColor = 'rgba(120,180,255,0.8)'; cx.shadowBlur = 14 * k;   // kar tepecigi (ayak alti)
  cx.beginPath(); cx.ellipse(xm, ay + 4 * k, 120 * k, 26 * k, 0, 0, 6.283); cx.fill(); cx.restore();
  let ad = (d ? d.grup : POZ_ADLAR[0]) + '-A', j = 0, bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 10 * k, isaret = 0, soru = false;
  if (d) {
    const Z = ZD(d), sq = (u - Z.kart) / Z.say;
    if (d.blind && acilma(d, u) < 0.5 && u < Z.kart + Z.say) soru = true;     // BLIND: maskot da goremiyor
    else if (u < Z.kart) isaret = -1;
    else if (sq < 1) {
      let yari, q;
      if (d.blind) { yari = 0; q = kisit((u - (Z.kart + Z.say - 1.5)) / 1.5, 0, 1); }
      else { yari = sq < 0.5 ? 0 : 1; q = (sq - yari * 0.5) / 0.5; }
      ad = d.grup + (yari ? '-B' : '-A'); isaret = yari ? 1 : -1;
      j = (KK - 1) * (q < 0.2 ? ease(q / 0.2) : q < 0.8 ? 1 : 1 - ease((q - 0.8) / 0.2));
      if (j > 0.5) bob = 0;
    } else ad = d.grup + '-B';
  }
  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];
  if (!im) { maskotCiz(xm, ay - 80 * k - bob, 1.0, t); return; }
  const sc = H * MAS_BOY / Y.boy_px, px = im.width * sc, x0 = xm - px / 2, y0 = ay - Y.zemin_px * sc - bob;
  cx.save(); cx.shadowColor = '#7ad8ff'; cx.shadowBlur = 24 * k;
  cx.drawImage(im, x0, y0, px, px); cx.restore();
  const kf = Y.poz[ad].kafa[Math.round(j)], kx = x0 + kf[0] * sc;
  maskotCiz(kx, y0 + kf[1] * sc, kf[2] * sc * 1.25 / (62 * k), t, 1, true);
  if (soru) {                                                    // BLIND: maskotun yaninda soru balonu
    const bx = xm + 150 * k, by = y0 + px * 0.25;
    cx.save(); cx.fillStyle = '#ffffff'; cx.strokeStyle = KON; cx.lineWidth = 6 * k;
    cx.beginPath(); cx.ellipse(bx, by, 56 * k, 50 * k, 0, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
    yaziK('?', bx, by + 2 * k, 70 * k * (1 + 0.08 * Math.sin(t * 6)), ['#ffffff', '#bff0ff', '#3ac8ff'], 1, '#06306a');
  }
  if (d && isaret && u < ZD(d).kart + ZD(d).say) {             // hangi figuru gosterdigini (sol mavi / sag pembe) ok ile isaret eder
    const i = isaret > 0 ? 1 : 0, ox = xm + isaret * 170 * k, oy = y0 + px * 0.45;
    cx.save(); cx.fillStyle = RENK[i]; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k; cx.translate(ox + Math.sin(t * 8) * 8 * k * isaret, oy);
    cx.scale(isaret, 1); cx.beginPath(); cx.moveTo(-30 * k, -26 * k); cx.lineTo(30 * k, 0); cx.lineTo(-30 * k, 26 * k); cx.closePath(); cx.fill(); cx.stroke(); cx.restore();
  }
}
''' + t[a1:]
r('''const MAS_BOY = 0.32;                                          // kullanici: maskot ortada ve gorunur''',
  '''const MAS_BOY = 0.24;                                          // kullanici: maskot ortada ve gorunur (motor 24: kapinin kirisi ustunde)''')
r('''  const y = H * 0.47;
  cx.save(); cx.globalAlpha = q; cx.fillStyle = '#ffffff'; cx.strokeStyle = KON; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(W / 2 - 230 * k * s, y - 50 * k * s, 460 * k * s, 100 * k * s, 50 * k * s); cx.fill(); cx.stroke(); cx.restore();
  if (!outlar.length) yaziK(d.ovgu || 'PERFECT!', W / 2, y, 64 * k * s, ['#fff6a0', '#ffd23a', '#ff8a1a'], q);
  else satir([[outlar[0] === 'p1' ? 'BLUE' : 'PINK', ['#ffffff', RENK[outlar[0] === 'p1' ? 0 : 1]]], [' OUT!', ['#ffffff', '#ff8a8a', '#ff1a2a']]], W / 2, y, 64 * k * s, q);''',
  '''  const y = H * 0.42, xb = W * 0.17;                            // motor 24: kapinin solunda (orta duvarin)
  cx.save(); cx.globalAlpha = q; cx.fillStyle = '#ffffff'; cx.strokeStyle = KON; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xb - 230 * k * s, y - 50 * k * s, 460 * k * s, 100 * k * s, 50 * k * s); cx.fill(); cx.stroke(); cx.restore();
  if (!outlar.length) yaziK(d.ovgu || 'PERFECT!', xb, y, 64 * k * s, ['#fff6a0', '#ffd23a', '#ff8a1a'], q);
  else satir([[outlar[0] === 'p1' ? 'BLUE' : 'PINK', ['#ffffff', RENK[outlar[0] === 'p1' ? 0 : 1]]], [' LATE!', ['#ffffff', '#ff8a8a', '#ff1a2a']]], xb, y, 64 * k * s, q);''')
# ---- acilis: VS yerine CO-OP
r('''    cx.font = F(px); const wV = cx.measureText('V').width, wS = cx.measureText('S').width;
    yazi('V', -wS / 2 + 4 * k, 0, px, ['#ffffff', ACIK[0], P1, KOYU[0]], '#1a0630', Math.min(1, q / 0.05), null);
    yazi('S', wV / 2 - 4 * k, 0, px, ['#ffffff', ACIK[1], P2, KOYU[1]], '#1a0630', Math.min(1, q / 0.05), null);''',
  '''    yazi('CO-OP', 0, 0, px * 0.6, ['#fff6a0', '#ffd23a', '#ff9a1a'], '#1a0630', Math.min(1, q / 0.05), null);   // motor 24: VS yerine CO-OP (TALIMATLAR §4)''')
r('''      satir([['WHO WILL WIN? ', KART_DOLGU], ['BLUE', ['#ffffff', ACIK[0], RENK[0]]], [' OR ', KART_DOLGU], ['PINK', ['#ffffff', ACIK[1], RENK[1]]], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);''',
  '''      satir([['CAN YOU CLEAR ALL ', KART_DOLGU], [String(TOPLAM_DUVAR), ['#fff6a0', '#ffd23a', '#ff9a1a']], [' WALLS?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 24 CO-OP sorusu''')
# ---- sonuc karti: takim skoru + rutbe
a0 = t.index('function sonucKart(kart, u, t) {')
a1 = t.index('// md. 28 (tam render 1): BRONZE alt tonu')
t = t[:a0] + '''function sonucKart(kart, u, t) {                              // motor 24: bastaki "CAN YOU CLEAR ALL 24 WALLS?" sorusunun cevabi (takim)
  kartZeminCiz(t);
  const gir = ease(kisit(u / 0.4, 0, 1)), s = gir * (1 + 0.12 * Math.sin(gir * Math.PI));
  konfeti(t, 1.0, 70);
  const ad = DUVARLAR[DUVARLAR.length - 1].grup;
  for (let i = 0; i < 2; i++) {
    const o = OY[i], Y = KY[o], im = karKare(o, ad, KK - 1); if (!im) continue;
    const sc = H * 0.42 / Y.boy_px, pw = Y.w_px * sc, ph = Y.h_px * sc;
    cx.save(); cx.shadowColor = RENK[i]; cx.shadowBlur = 40 * k; cx.drawImage(im, W / 2 - pw / 2, H * 0.98 - Y.zemin_px * sc - Math.abs(Math.sin(t * 5 + i)) * 16 * k, pw, ph); cx.restore();
  }
  const dol = { GOLD: ['#fff6c0', '#ffd23a', '#e09a00'], SILVER: ['#ffffff', '#dfe6f2', '#9aa6ba'], BRONZE: ['#ffe0c0', '#ec9a5a', '#d8843a'] }[kart.rutbe];
  yaziK('TEAM SCORE', W / 2, H * 0.13, 100 * k * s, KART_DOLGU, 1, KON, '#7ad8ff');
  yaziK(kart.skor + ' / ' + kart.toplam, W / 2, H * 0.29, 130 * k * s, ['#fff6a0', '#ffd23a', '#ff9a1a'], 1);
  yaziK(kart.rutbe + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);
}
''' + t[a1:]
# ---- abone: solda (maskot ortada)
r('''  aboneButon(W / 2, H * 0.18, ease(gir) * zip * cik * 0.62, u, t);
  begenSatiri(W / 2, H * 0.265, cik * 0.5, u, t);''', '''  aboneButon(W * 0.2 - 30 * k, H * 0.2, ease(gir) * zip * cik * 0.62, u, t);   // motor 24: solda (orta ust maskotun, TALIMATLAR §4)
  begenSatiri(W * 0.2, H * 0.285, cik * 0.5, u, t);''')
r('''window.KARAKTER_VAR = ['p1', 'p2', 'maskot'].every(o => Object.values(KR[o]).every(L => L.length === KK && L.every(Boolean)));''',
  '''window.KARAKTER_VAR = ['p1', 'p2', 'maskot'].every(o => Object.values(KR[o]).length > 0 && Object.values(KR[o]).every(L => L.length === KK && L.every(Boolean)));''')
r('''    if (!tam) hakemCiz(t, d, t - d.t0);                       // maskot kapilarin arasinda; karakterler duvarCiz icinde ustte''',
  '''    if (!tam) hakemCiz(t, d, t - d.t0);                       // motor 24: maskot kapinin ustunde ortada; karakterler duvarCiz icinde''')
# ---- plaj kalintilari: plaj topu -> kartopu, can simidi -> kar tepecigi (karli zirve dunyasi)
a0 = t.index('function topCiz(x, y, r, t) {')
a1 = t.index('// REF-077 lunaparkinda: elinde ipli sabun kabarcigi')
t = t[:a0] + '''function topCiz(x, y, r, t) {                                  // motor 24: kartopu (plaj topu yerine) - beyaz, buz mavisi golge, parilti
  cx.save(); cx.translate(x, y);
  const g = cx.createRadialGradient(-r * 0.35, -r * 0.35, r * 0.1, 0, 0, r); g.addColorStop(0, '#ffffff'); g.addColorStop(0.7, '#e6f4ff'); g.addColorStop(1, '#9fd0ff');
  cx.fillStyle = g; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.fill();
  cx.lineWidth = Math.max(2, r * 0.08); cx.strokeStyle = '#5a8ad8'; cx.stroke();
  cx.restore();
  parilti4(x + r * 0.5, y - r * 0.6, r * 0.5, 0.6 + 0.4 * Math.sin(t * 5));
}
function simitCiz(x, y, r) {                                    // motor 24: kar tepecigi (can simidi yerine)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.7, 0, r * 0.5); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#bfe0ff');
  cx.fillStyle = g; cx.strokeStyle = '#5a8ad8'; cx.lineWidth = Math.max(1.5, r * 0.08);
  cx.beginPath(); cx.ellipse(0, 0, r * 1.5, r * 0.62, 0, Math.PI, 0); cx.closePath(); cx.fill(); cx.stroke();
  cx.restore();
}
''' + t[a1:]
r('''const KAR_BOY = 0.36;                                          // ekranda karakter boyu (H orani; motor 24 ikili: ayakta govde boyu)''',
  '''const KAR_BOY = 0.30;                                          // ekranda karakter boyu (H orani; motor 24 onizleme 1: 0,36 duvar kartinin altina biniyordu)''')
open(os.path.join(BURA, "..", "sahne24.html"), "w", encoding="utf-8").write(t)
print("-> sahne24.html", len(t))
