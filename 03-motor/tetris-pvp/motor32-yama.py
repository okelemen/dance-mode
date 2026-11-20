"""MOTOR 32 (HUMAN TETRIS 35) = sahne25.html (motor 25, 28. video: tek serit 2P CO-OP ikili poz + FREEZE) + yama -> 03-motor/sahne32.html.
sahne25 degismez.

    python motor32-yama.py

35: REF-087 yapi (2P CO-OP es poz), gunduz sicak hava balonu festivali (varlik-balon.py), ozel tur FREEZE (motor 22 freezeCiz),
yarisan karakterler sporcu (30'dan beri), hakem maskot ucan sincap PIP (2B bas: sivri kulak, alinda pilot gozlugu, krem yuz,
iki on dis; 3B govde karakter.py --sincap 1), OUT = pembe bulut yiginina duser (bulut pufu), gokte yukselen mini balonlar + konfeti.
Giris 30'dan beri (TALIMATLAR §4, 17 Kas): kanca (BOSS WALL onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis
(dev sicak hava balonu buluttan yukselir, sepetten mini balon + konfeti salinir) -> CAN YOU TWO CLEAR ALL 24? ; ilk duvar <= 5 sn.
Boksor VS karti yok (17 Kas kullanici karari).
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne25.html")
HEDEF = os.path.join(BURA, "..", "sahne32.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def fonk(ad, yeni):
    """'function ad(' satir basindan, satir basindaki ilk '}' satirina kadar olan fonksiyonu degistirir"""
    global t
    m = re.search(r"^function %s\(" % re.escape(ad), t, re.M)
    assert m, ad
    s = m.start()
    e = t.index("\n}\n", s) + 3
    t = t[:s] + yeni.strip("\n") + "\n" + t[e:]


m = re.search(r"<title>.*?</title>", t)
t = t[:m.start()] + "<title>HUMAN TETRIS 35 - motor 32 (tek serit balon festivali, 2P CO-OP es poz, FREEZE, ucan sincap Pip, kanca girisi)</title>" + t[m.end():]
degis("// MOTOR 25 — HUMAN TETRIS 28", "// MOTOR 32 — HUMAN TETRIS 35 (REF-087 yapi, 20 Kas 2026; motor 25'ten, tetris-pvp/motor32-yama.py):\n"
      "//   - sahne: tetris-pvp/varlik-balon.py (gunduz sicak hava balonu festivali, bulut denizi); gokte yukselen mini balonlar + konfeti\n"
      "//   - hakem ucan sincap PIP (2B bas: kulak, pilot gozlugu, krem yuz, iki on dis); bulut kursu; OUT pembe bulut yiginina (bulut pufu)\n"
      "//   - giris kanca (motor 27'den): BOSS onizleme -> geri sarma -> dev balon buluttan yukselir, mini balon + konfeti -> CAN YOU TWO CLEAR ALL 24?\n"
      "// --- motor 25 aciklamasi ---\n"
      "// MOTOR 25 — HUMAN TETRIS 28")

# ------------------------------------------------------------------ kucuk balon (maskotun elinde, gokte) + bulut tepecigi
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#ff2a3a', c2 = '#ffc21a') {   // motor 32: mini sicak hava balonu (dilimli zarf + sepet)
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.08);
  cx.lineWidth = Math.max(1.5, r * 0.07); cx.strokeStyle = '#3a1606';
  cx.beginPath(); cx.moveTo(-r * 0.62, r * 0.55); cx.quadraticCurveTo(-r * 1.05, -r * 0.2, -r * 0.55, -r * 0.9);
  cx.quadraticCurveTo(0, -r * 1.35, r * 0.55, -r * 0.9); cx.quadraticCurveTo(r * 1.05, -r * 0.2, r * 0.62, r * 0.55);
  cx.quadraticCurveTo(r * 0.3, r * 0.95, 0, r * 0.98); cx.quadraticCurveTo(-r * 0.3, r * 0.95, -r * 0.62, r * 0.55); cx.closePath();
  cx.save(); cx.clip();
  for (let j = -3; j <= 3; j++) { cx.fillStyle = (j + 3) % 2 ? c1 : c2; cx.fillRect(j * r * 0.32 - r * 0.16, -r * 1.4, r * 0.32, r * 2.6); }
  const g = cx.createRadialGradient(-r * 0.35, -r * 0.5, r * 0.05, 0, 0, r * 1.2); g.addColorStop(0, 'rgba(255,255,255,0.55)'); g.addColorStop(0.5, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,0,0.25)');
  cx.fillStyle = g; cx.fillRect(-r * 1.2, -r * 1.4, r * 2.4, r * 2.6);
  cx.restore(); cx.stroke();
  cx.strokeStyle = '#6a3a10'; cx.lineWidth = Math.max(1, r * 0.04);
  for (const s of [-1, 1]) { cx.beginPath(); cx.moveTo(s * r * 0.28, r * 0.96); cx.lineTo(s * r * 0.2, r * 1.3); cx.stroke(); }
  cx.fillStyle = '#d88a2a'; cx.strokeStyle = '#5a2a08'; cx.lineWidth = Math.max(1, r * 0.05);
  cx.beginPath(); cx.roundRect(-r * 0.24, r * 1.28, r * 0.48, r * 0.34, r * 0.06); cx.fill(); cx.stroke();
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 32: pembe-seftali bulut tepecigi (lila golge)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.8, 0, r * 0.4); g.addColorStop(0, '#ffe2ef'); g.addColorStop(0.6, '#ffb6d4'); g.addColorStop(1, '#b89aff');
  cx.fillStyle = g; cx.strokeStyle = '#8a4ab8'; cx.lineWidth = Math.max(1.5, r * 0.07);
  cx.beginPath();
  cx.moveTo(-r * 1.55, r * 0.15);
  for (const [px, py, pr] of [[-1.05, -0.15, 0.5], [-0.35, -0.5, 0.62], [0.4, -0.42, 0.58], [1.1, -0.1, 0.48]]) cx.arc(px * r, py * r, pr * r, Math.PI, 0);
  cx.lineTo(r * 1.55, r * 0.15); cx.quadraticCurveTo(0, r * 0.45, -r * 1.55, r * 0.15); cx.closePath(); cx.fill(); cx.stroke();
  cx.restore();
}
""")

# ------------------------------------------------------------------ PIP (2B): yuzSadece = yalniz bas (3B govdenin ustune), yoksa tam figur
fonk("maskotCiz", r"""
function pipBas(u, duygu, t) {                                  // motor 32: Pip'in basi, merkez (0,0), birim u (maskot-ornek-35.py ile ayni olcu)
  const KN = '#3a1606', TUR = '#d8702e', KREM = '#ffe6c0';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round';
  for (const sx of [-1, 1]) {                                   // sivri kulaklar (pembe ic), hafif oynar
    cx.save(); cx.translate(sx * 15 * u, -14 * u); cx.rotate(sx * 0.06 * Math.sin(t * 5));
    cx.fillStyle = TUR; cx.strokeStyle = KN; cx.lineWidth = 1.6 * u;
    cx.beginPath(); cx.moveTo(-8 * u, 0); cx.lineTo(sx * 3 * u, -20 * u); cx.lineTo(8 * u, 2 * u); cx.closePath(); cx.fill(); cx.stroke();
    cx.fillStyle = '#ff9ab0'; cx.beginPath(); cx.moveTo(-4 * u, -1 * u); cx.lineTo(sx * 2 * u, -14 * u); cx.lineTo(4 * u, 0); cx.closePath(); cx.fill();
    cx.restore();
  }
  const g = cx.createRadialGradient(-7 * u, -8 * u, 2 * u, 0, 0, 24 * u); g.addColorStop(0, '#f39a5a'); g.addColorStop(1, '#c45a1e');
  el(0, 0, 22, 20, g, KN, 1.6);
  el(0, 8, 15, 11, KREM);
  cx.fillStyle = '#5a2a10'; cx.beginPath(); cx.roundRect(-22 * u, -17 * u, 44 * u, 5 * u, 2 * u); cx.fill();   // gozluk kayisi
  for (const sx of [-1, 1]) { el(sx * 8, -15, 6.5, 5.5, '#22d0c8', '#5a2a10', 2.2); el(sx * 8 - 2, -17, 1.8, 1.4, '#e8fffd'); }
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') { cx.strokeStyle = KN; cx.lineWidth = 2.4 * u; cx.beginPath(); cx.arc(sx * 8 * u, -1 * u, 5 * u, Math.PI * 1.14, Math.PI * 1.86); cx.stroke(); }
    else if (duygu === 'sasirma') { el(sx * 8, -2, 5.5, 5.5, '#ffffff', KN, 1.4); el(sx * 8, -1, 2, 2, KN); }
    else { el(sx * 8, -2, 4.8, 5.8, '#ffffff', KN, 1.4); el(sx * 8 + 0.8, -1, 3, 3, KN); el(sx * 8 - 0.4, -2.8, 1.1, 1.1, '#ffffff'); }
    el(sx * 15, 7, 3.6, 2.2, '#ff7a8a');
  }
  el(0, 5, 2.6, 2, KN);
  if (duygu === 'sasirma') el(0, 12, 3, 4, '#7a1020', KN, 1.4);
  else {
    cx.fillStyle = '#7a1020'; cx.strokeStyle = KN; cx.lineWidth = 1.4 * u; cx.beginPath(); cx.moveTo(-6 * u, 9 * u); cx.quadraticCurveTo(0, 18 * u, 6 * u, 9 * u); cx.closePath(); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffffff'; cx.fillRect(-2 * u, 9.5 * u, 4 * u, 3 * u); cx.strokeStyle = KN; cx.lineWidth = 0.6 * u; cx.strokeRect(-2 * u, 9.5 * u, 4 * u, 3 * u);
    cx.beginPath(); cx.moveTo(0, 9.5 * u); cx.lineTo(0, 12.5 * u); cx.stroke();
  }
}
let pipDuygu = 'mutlu';
function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {   // motor 32: ucan sincap Pip (TALIMATLAR §4 maskot; yuz ve govde video boyunca ayni)
  if (alfa <= 0.01) return;
  cx.save(); cx.globalAlpha *= alfa; cx.translate(x, y); cx.scale(s * k, s * k);
  if (yuzSadece) { cx.translate(0, -32); pipBas(70 / 22, pipDuygu, t); cx.restore(); return; }
  const KN = '#3a1606';
  cx.lineJoin = 'round'; cx.lineWidth = 5; cx.strokeStyle = KN;
  const sal = Math.sin(t * 3) * 0.08;
  cx.save(); cx.translate(40, 40); cx.rotate(sal);                // kabarik kuyruk (arkada, saga ve yukari kivrik)
  const gk = cx.createLinearGradient(0, -120, 0, 40); gk.addColorStop(0, '#f0a060'); gk.addColorStop(1, '#c45a1e');
  cx.fillStyle = gk; cx.beginPath(); cx.moveTo(-10, 30); cx.bezierCurveTo(70, 40, 90, -60, 40, -110); cx.bezierCurveTo(20, -135, -15, -110, 5, -85);
  cx.bezierCurveTo(35, -60, 30, -10, -20, 0); cx.closePath(); cx.fill(); cx.stroke(); cx.restore();
  const gv = cx.createRadialGradient(-10, 20, 6, 0, 40, 60); gv.addColorStop(0, '#f39a5a'); gv.addColorStop(1, '#c45a1e');
  cx.fillStyle = gv; cx.beginPath(); cx.ellipse(0, 45, 44, 50, 0, 0, 6.283); cx.fill(); cx.stroke();   // govde
  cx.fillStyle = '#ffe6c0'; cx.beginPath(); cx.ellipse(0, 52, 28, 36, 0, 0, 6.283); cx.fill();
  for (const sx of [-1, 1]) {                                   // kollar + ayaklar
    cx.fillStyle = '#d8702e'; cx.beginPath(); cx.ellipse(sx * 46, 40 + Math.sin(t * 6 + sx) * 4, 12, 20, sx * 0.4, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffe6c0'; cx.beginPath(); cx.ellipse(sx * 22, 94, 18, 9, 0, 0, 6.283); cx.fill(); cx.stroke();
  }
  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(-34, -4, 68, 14, 7); cx.fill(); cx.stroke();      // kirmizi atki
  cx.beginPath(); cx.roundRect(10, 4, 14, 30, 6); cx.fill(); cx.stroke();
  cx.translate(0, -36); pipBas(48 / 22, pipDuygu, t);
  cx.restore();
  cx.save(); cx.globalAlpha *= alfa;                             // elinde ipli mini balon
  const bs = Math.sin(t * 2.2) * 4;
  cx.strokeStyle = '#ffffff'; cx.lineWidth = 2.5 * s * k; cx.beginPath(); cx.moveTo(x - 50 * s * k, y + 40 * s * k);
  cx.quadraticCurveTo(x - 80 * s * k, y - 20 * s * k, x - (90 + bs) * s * k, y - 70 * s * k); cx.stroke();
  cx.restore();
  topCiz(x - (90 + bs) * s * k, y - 110 * s * k, 30 * s * k, t, '#1e8cff', '#ffc21a');
}
""")

# ------------------------------------------------------------------ gokte yukselen mini balonlar (sabun kopukleri yerine)
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 32: gokte yukselen mini sicak hava balonlari (hareketli ust bosluk)
  const C = [['#ff2a3a', '#ffc21a'], ['#1e8cff', '#ffffff'], ['#20c850', '#ffc21a'], ['#ff3aa8', '#ffffff'], ['#8a3aff', '#10c8d0'], ['#ff7a10', '#1e8cff']];
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j += 6) {
    const p = KAR_T[j];
    const y = (1.08 - ((p.y + t * p.v * 0.45) % 1.15)) * H * 0.6, x = ((p.x + Math.sin(t * 0.5 + p.f) * 0.01) % 1) * W;
    if (Math.abs(x - W / 2) < W * 0.22 && y > H * 0.2) continue;
    topCiz(x, y, (p.r * 4 + 12) * k, t, C[j % 6][0], C[j % 6][1]);
  }
  cx.restore();
}
""")
degis("  karYagisi(t);\n", "  karYagisi(t);\n  konfeti(t, 0.45, 26, 0.8);\n")

# ------------------------------------------------------------------ OUT: pembe bulut yigini pufu
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 32: pembe bulut pufu (karakter bulut yiginina duser)
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(4711 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 16; j++) {
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (160 + 260 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.6, r = (26 + 30 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.addColorStop(0, '#fff2f8'); g.addColorStop(0.7, '#ffbcd8'); g.addColorStop(1, 'rgba(184,154,255,0.6)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  for (let j = 0; j < 14; j++) {                                // kucuk renkli konfeti
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (300 + 400 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 700 * k * u * u;
    cx.fillStyle = KONF_R[j % 6]; cx.fillRect(x - 6 * k, y - 3 * k, 12 * k, 6 * k);
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: hasir sepet + bulut; hakemin ayak alti bulut
fonk("kule", r"""
function kule(t) {                                             // motor 32: hakem kursusu hasir balon sepeti + kenarinda bulut
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#e8a030'); g.addColorStop(1, '#a8601a');
  cx.fillStyle = g; cx.strokeStyle = '#5a2a08'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(90,42,8,0.5)'; cx.lineWidth = 3 * k;
  for (let q = 1; q < 6; q++) { cx.beginPath(); cx.moveTo(xm - w / 2 + q * w / 6, y0 + 4 * k); cx.lineTo(xm - w / 2 + q * w / 6, H); cx.stroke(); }
  cx.fillStyle = '#e8102c'; cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 9 * k);
  simitCiz(xm + w * 0.42, y0 + h * 0.2, 22 * k);
  cx.restore();
}
""")
degis("  const pg = cx.createLinearGradient(0, ay - 20 * k, 0, ay + 30 * k); pg.addColorStop(0, '#ffd0ec'); pg.addColorStop(1, '#ff5fc0');\n"
      "  cx.fillStyle = pg; cx.strokeStyle = '#a0186a'; cx.lineWidth = 4 * k;\n"
      "  cx.beginPath(); cx.ellipse(xm, ay + 4 * k, 120 * k, 26 * k, 0, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 32: hakem pembe bulutun ustunde")
degis("cx.save(); cx.shadowColor = 'rgba(255,120,200,0.8)'; cx.shadowBlur = 14 * k;   // motor 25: pembe kremali pasta tabakasi (ayak alti)",
      "cx.save();                                                    // motor 32: ayak alti bulut (asagida)")
# hakem duygusu: PERFECT -> sevinc, OUT -> sasirma
degis("  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];\n  if (!im) {",
      "  pipDuygu = 'mutlu';\n"
      "  if (d) { const Z = ZD(d), b = Z.kart + Z.say; if (u >= b + Z.buyu * 0.5) pipDuygu = (d.out && (d.out.p1 || d.out.p2)) ? 'sasirma' : 'sevinc'; }\n"
      "  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];\n  if (!im) {")

# ------------------------------------------------------------------ GIRIS: kanca + balon acilisi (motor 27/31 kancaCiz'den)
fonk("acilisCiz", r"""
const KH = 1.6, KR_ = 0.4;                                      // motor 27 kanca: onizleme / geri sarma sureleri
function kancaBoss(ub) {                                        // BOSS WALL'un gercek karesi (karakterler + hakem dahil)
  const d = DUVARLAR[DUVARLAR.length - 1], tb = d.t0 + ub;
  AYNA = false; sahneCiz(tb); hakemCiz(tb, d, ub); duvarCiz(d, ub, tb);
}
function devBalon(x, y, r, t) {                                 // acilis: dev sicak hava balonu (kirmizi-sari dilim, mavi bant)
  topCiz(x, y, r, t, '#ff2a3a', '#ffc21a');
  cx.save(); cx.fillStyle = 'rgba(30,140,255,0.92)'; cx.beginPath(); cx.ellipse(x, y - r * 0.05, r * 0.98, r * 0.12, 0, 0, 6.283); cx.fill(); cx.restore();
}
function acilisCiz(kart, u, t) {
  acilisSoru = 0;
  if (u < KH + KR_) {
    const d = DUVARLAR[DUVARLAR.length - 1], Z = ZD(d), u0 = Z.kart + Z.say * 0.55, u1 = Z.kart + Z.say + Z.buyu * 0.4;
    const ub = u < KH ? lerp(u0, u1, ease(u / KH)) : lerp(u1, Z.kart * 0.5, ease((u - KH) / KR_));
    kancaBoss(ub);
    if (u < KH) {
      cx.save(); cx.globalAlpha = 0.25 + 0.2 * Math.sin(u * 14); cx.strokeStyle = '#ff1a2a'; cx.lineWidth = 60 * k; cx.strokeRect(0, 0, W, H); cx.restore();
      const g = ease(kisit((u - 0.1) / 0.25, 0, 1)), p = 1 + 0.12 * Math.max(0, 1 - (u - 0.1) * 5) + 0.03 * Math.sin(u * 9);
      if (g > 0.01) {
        cx.save(); cx.globalAlpha = g * 0.82; cx.fillStyle = '#1a0408'; cx.beginPath(); cx.roundRect(W / 2 - 680 * k, H * 0.13 - 74 * k, 1360 * k, 148 * k, 74 * k); cx.fill(); cx.restore();
        yaziK('CAN YOU PASS THIS?', W / 2, H * 0.13, 110 * k * g * p, ['#ffffff', '#fff27a', '#ffc21a'], g, '#3a0a00', '#ffffff');
      }
    } else {                                                    // geri sarma: VHS seritleri + << isareti
      const q = (u - KH) / KR_;
      cx.save(); cx.globalCompositeOperation = 'lighter';
      for (let j = 0; j < 7; j++) { const yy = ((j * 0.31 + q * 3.7) % 1) * H; cx.fillStyle = 'rgba(255,255,255,0.18)'; cx.fillRect(0, yy, W, (10 + 22 * ((j * 7) % 3)) * k); }
      cx.restore();
      cx.save(); cx.fillStyle = 'rgba(20,10,40,0.18)'; cx.fillRect(0, 0, W, H); cx.restore();
      cx.save(); cx.fillStyle = '#ffffff'; cx.strokeStyle = '#1a0630'; cx.lineWidth = 8 * k; cx.translate(150 * k, 140 * k);
      for (const dx of [0, 70 * k]) { cx.beginPath(); cx.moveTo(dx, 0); cx.lineTo(dx + 70 * k, -48 * k); cx.lineTo(dx + 70 * k, 48 * k); cx.closePath(); cx.stroke(); cx.fill(); }
      cx.restore();
    }
    return;
  }
  // mekan acilisi (35: balon festivali) - sahne kareKur'da zaten cizili
  const ua = u - KH - KR_;
  hakemCiz(t, null, 0);
  const R = H * 0.24, yb = lerp(H * 1.35, -H * 0.45, ease(kisit(ua / 1.3, 0, 1)));   // dev balon bulut denizinden yukselir, kadrajdan cikar
  if (ua < 1.3) devBalon(W / 2, yb, R, t);
  const R2 = rng(3535);                                         // sepetten salinan mini balonlar (yukari, yana acilarak)
  const MC = [['#1e8cff', '#ffffff'], ['#ff3aa8', '#ffffff'], ['#20c850', '#ffc21a'], ['#8a3aff', '#10c8d0'], ['#ff7a10', '#1e8cff'], ['#ffc21a', '#ff2a3a']];
  for (let j = 0; j < 18; j++) {
    const t0 = 0.35 + 0.03 * j, q = ua - t0; if (q <= 0) continue;
    const a = -Math.PI / 2 + (R2() - 0.5) * 2.4, v = (500 + 500 * R2()) * k;
    const x = W / 2 + Math.cos(a) * v * q, y = yb + R * 1.4 + Math.sin(a) * v * q - 120 * k * q;
    if (y < -80 * k) continue;
    topCiz(x, y, (26 + 20 * R2()) * k, t, MC[j % 6][0], MC[j % 6][1]);
  }
  const R3 = rng(3131);                                         // konfeti firtinasi ortadan disa
  for (let j = 0; j < 110; j++) {
    const a = R3() * 6.283, hz = 0.6 + 0.9 * R3(), c = KONF_R[Math.floor(R3() * 6)], r = (10 + 18 * R3()) * k;
    const d0 = kisit((ua - 0.45) * hz * 1.4, 0, 2) * W * 0.6;
    if (d0 <= 0) continue;
    const x = W / 2 + Math.cos(a) * d0, y = H * 0.5 + Math.sin(a) * d0 * 0.6 + 200 * k * (ua - 0.45) ** 2;
    if (x < -60 * k || x > W + 60 * k || y > H + 60 * k) continue;
    cx.save(); cx.translate(x, y); cx.rotate(a + ua * 6 * hz); cx.scale(1, 0.4 + 0.6 * Math.abs(Math.sin(ua * 7 * hz + a * 5)));
    cx.fillStyle = c; cx.fillRect(-r, -r * 0.4, 2 * r, r * 0.8);
    cx.restore();
  }
  acilisSoru = kart.soru ? ease(kisit((ua - 0.7) / 0.25, 0, 1)) : 0;
  const pa = ease(kisit((ua - 0.85) / 0.25, 0, 1));
  if (pa > 0.01) for (let i = 0; i < 2; i++) pYazi(['P1', 'P2'][i], i ? W * 0.75 : W * 0.25, H * 0.6, 130 * k, RENK[i], pa);
}
""")
degis("satir([['CAN YOU CLEAR ALL ', KART_DOLGU], [String(TOPLAM_DUVAR), ['#fff6a0', '#ffd23a', '#ff9a1a']], [' WALLS?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 24 CO-OP sorusu",
      "satir([['CAN YOU TWO CLEAR ALL ', KART_DOLGU], [String(TOPLAM_DUVAR), ['#fff6a0', '#ffd23a', '#ff9a1a']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 32: yukleme notu sorusu")
# acilista maskot alt ortada 2B ziplar; kancada (ilk 2 sn) ciz
degis("    if (kart.tip === 'acilis') {                                 // TALIMATLAR §4: maskot video boyunca; VS kartinda alt ortada (P1/P2 ve can barlarina degmez)\n"
      "      const v = (t * BPM / 60) % 1; maskotCiz(W / 2, H * 0.9 - Math.abs(Math.sin(v * Math.PI)) * 10 * k, 0.55, t);",
      "    if (kart.tip === 'acilis') {                                 // motor 32: kancada BOSS karesinde, acilista kursude hakem (3B) zaten cizili\n"
      "      const v = (t * BPM / 60) % 1;")


# tam render 1 (20 Kas): FREEZE turundaki OUT duvarinda (15) BLUE LATE! cikarken FREEZE! HOLD IT sayaci da suruyordu -> OUT duvarinda tut evresi cizilmez
degis("  if (T && u >= c) freezeCiz(u - c, T, t);", "  if (T && u >= c && !(d.out && (d.out.p1 || d.out.p2))) freezeCiz(u - c, T, t);   // motor 32: OUT duvarinda HOLD yok")
# tam render 1: kepenkte motor 25'ten kalan eski maskotun (yaprak kulak) neon yuzu -> Pip (sivri kulak + pilot gozlugu + iki on dis)
KUL_ESKI = ("    cx.beginPath(); cx.ellipse(mx + sx * r * 0.55, my - r * 0.95, r * 0.24, r * 0.42, sx * 0.5, 0, 6.283); cx.stroke();   // yaprak kulak\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.33, my - r * 0.12, r * 0.1, r * 0.15, 0, 0, 6.283); cx.stroke();          // goz")
KUL_YENI = ("    cx.beginPath(); cx.moveTo(mx + sx * r * 0.3, my - r * 0.78); cx.lineTo(mx + sx * r * 0.62, my - r * 1.45); cx.lineTo(mx + sx * r * 0.82, my - r * 0.55); cx.stroke();   // motor 32: Pip sivri kulak\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.62, r * 0.28, r * 0.22, 0, 0, 6.283); cx.stroke();          // pilot gozlugu\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.08, r * 0.1, r * 0.15, 0, 0, 6.283); cx.stroke();          // goz")
degis(KUL_ESKI, KUL_YENI)
degis("  cx.beginPath(); cx.arc(mx, my + r * 0.2, r * 0.16, 0.2, Math.PI - 0.2); cx.stroke();\n  cx.shadowBlur = 0;",
      "  cx.beginPath(); cx.moveTo(mx - r * 0.64, my - r * 0.62); cx.lineTo(mx - r * 0.9, my - r * 0.6); cx.moveTo(mx + r * 0.64, my - r * 0.62); cx.lineTo(mx + r * 0.9, my - r * 0.6); cx.stroke();   // gozluk kayisi\n"
      "  cx.beginPath(); cx.arc(mx, my + r * 0.2, r * 0.16, 0.2, Math.PI - 0.2); cx.stroke(); cx.strokeRect(mx - r * 0.07, my + r * 0.36, r * 0.14, r * 0.12);   // gulus + iki on dis\n  cx.shadowBlur = 0;")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
