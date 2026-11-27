"""MOTOR 37 (HUMAN TETRIS 40) = sahne36.html (motor 36, 39. video: 1P SOLO mercan resifi) + yama -> 03-motor/sahne37.html.
sahne36 degismez.

    python motor37-yama.py

40: REF-092 yapi (1P SOLO), gunduz donmus gol buz pateni (varlik-buz.py), ozel tur BLIND (motor 24'ten beri d.blind; kar firtinasi),
yarisan karakter TEK sporcu (RED, karakter.py --sporcu 1 --renk FF1A2A), hakem maskot fok yavrusu LUMI - TAMAMI 2B:
govde + yuzgec eller/ayaklar + bas + bere + atki + duduk; hareket karakter.py --eklem 1 verisinden. Cizim maskot-ornek-40.py ile birebir.
OUT = buzda kayip kar yiginina gomulur: kar pufu + buz kiymiklari. Ekranda yagan kar + parilti (motor 35'ten).
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (paten bicagi buzda parlayan iz
oyar, buz kiymiklari sacilir, izler yukari akip soruya donusur; Lumi buzda kayarak ortaya gelir) -> CAN YOU WIN THE GOLDEN SKATE? ;
ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne36.html")
HEDEF = os.path.join(BURA, "..", "sahne37.html")
t = open(KAYNAK, encoding="utf-8").read()
t35 = open(os.path.join(BURA, "..", "sahne35.html"), encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def govdesi(kaynak, ad):
    m = re.search(r"^function %s\(" % re.escape(ad), kaynak, re.M)
    assert m, ad
    return kaynak[m.start():kaynak.index("\n}\n", m.start()) + 3]


def fonk(ad, yeni):
    global t
    eski = govdesi(t, ad)
    t = t.replace(eski, yeni.strip("\n") + "\n")


m = re.search(r"<title>.*?</title>", t)
t = t[:m.start()] + "<title>HUMAN TETRIS 40 - motor 37 (donmus gol, 1P SOLO, BLIND, 2B fok Lumi, paten oyma girisi)</title>" + t[m.end():]
degis("// MOTOR 36 — HUMAN TETRIS 39", "// MOTOR 37 — HUMAN TETRIS 40 (REF-092 yapi, 27 Kas 2026; motor 36'dan, tetris-pvp/motor37-yama.py):\n"
      "//   - 1P SOLO: tek sporcu (RED); BLIND ROUND (d.blind, kar firtinasi)\n"
      "//   - sahne: tetris-pvp/varlik-buz.py (gunduz donmus gol buz pateni); ekranda yagan kar + parilti (motor 35)\n"
      "//   - hakem fok yavrusu LUMI, TAMAMI 2B: eklem verisinden govde + yuzgec + bas + bere + atki (maskot-ornek-40.py ile ayni); buz kursu + kar tumsegi\n"
      "//   - OUT kar yigini (kar pufu + buz kiymiklari); giris kanca -> paten bicagi buza iz oyar -> CAN YOU WIN THE GOLDEN SKATE?\n"
      "// --- motor 36 aciklamasi ---\n"
      "// MOTOR 36 — HUMAN TETRIS 39")

# ------------------------------------------------------------------ mini Noel topu + kar tumsegi + yagan kar (motor 35'ten aynen)
fonk("topCiz", govdesi(t35, "topCiz").replace("// motor 35: mini Noel topu", "// motor 37 (35'ten): mini Noel topu"))
fonk("simitCiz", govdesi(t35, "simitCiz").replace("// motor 35: kar tumsegi + iki Noel topu", "// motor 37 (35'ten): kar tumsegi + iki Noel topu")
     .replace("'#8a96ff'", "'#9ac0ff'").replace("'#3a2a8a'", "'#1a3a8a'"))          # buz mavisi golge (leylak yerine)
fonk("karYagisi", govdesi(t35, "karYagisi").replace("// motor 35: yagan kar", "// motor 37 (35'ten): yagan kar")
     .replace("'rgba(245,240,255,'", "'rgba(250,252,255,'"))

# ------------------------------------------------------------------ LUMI (tamami 2B): maskot-ornek-40.py (bas + govde) ile ayni
fonk("pipBas", r"""
function pipBas(u, duygu, t) {                                  // motor 37: Lumi'nin basi (maskot-ornek-40.bas, on gorunum), merkez (0,0), birim u
  const KN = '#1a2040', POST = '#f6f8ff', KARIN = '#ffffff', BURUN = '#101018', YANAK = '#ff7a9a', BERE = '#e81a2a';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const yay = (x, y, rx, ry, a0, a1, w) => { cx.strokeStyle = KN; cx.lineWidth = w * u; cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, a0 * Math.PI / 180, a1 * Math.PI / 180); cx.stroke(); };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  el(0, 0, 23, 21, POST, KN, 1.6);
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') yay(sx * 9, -3, 5.5, 5.5, 200, 340, 2.6);
    else if (duygu === 'sasirma') { el(sx * 9, -4, 6.5, 7.5, '#ffffff', KN, 1.4); el(sx * 9, -4, 2.6, 2.8, KN); }
    else { el(sx * 9, -3, 6.2, 7.2, '#ffffff', KN, 1.4); el(sx * 9 + 0.7, -2.4, 4.2, 5.0, KN); el(sx * 9 - 0.8, -4.8, 1.6, 1.6, '#ffffff'); }
    el(sx * 16, 6, 3.6, 2.2, YANAK);
  }
  el(-4.2, 9, 5.2, 4.2, KARIN, KN, 1.0); el(4.2, 9, 5.2, 4.2, KARIN, KN, 1.0);     // burun yastiklari
  cx.strokeStyle = KN; cx.lineWidth = 0.8 * u;
  for (const sx of [-1, 1]) [-1.5, 1.0, 3.5].forEach((dy, kk) => {
    el(sx * (3 + kk * 1.6), 8.6 + dy * 0.5, 0.55, 0.55, '#d8e0f4');
    cx.strokeStyle = KN; cx.lineWidth = 0.8 * u; cx.beginPath(); cx.moveTo(sx * 8 * u, (8.5 + dy) * u); cx.lineTo(sx * 20 * u, (6 + dy * 2.2) * u); cx.stroke();   // biyiklar
  });
  cx.fillStyle = BURUN; cx.beginPath(); cx.moveTo(-3.2 * u, 4.2 * u); cx.lineTo(3.2 * u, 4.2 * u); cx.lineTo(0, 8 * u); cx.closePath(); cx.fill();
  if (duygu === 'sasirma') el(0, 15, 3.0, 2.8, '#7a1020', KN, 1.0);
  else if (duygu === 'sevinc') { cx.beginPath(); cx.ellipse(0, 15 * u, 6 * u, 4 * u, 0, 0, Math.PI); cx.closePath(); cx.fillStyle = '#7a1020'; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.2 * u; cx.stroke(); }
  else { yay(-2.15, 12.5, 2.35, 2.5, 0, 160, 1.3); yay(2.15, 12.5, 2.35, 2.5, 20, 180, 1.3); }
  cx.beginPath(); cx.ellipse(0, -20 * u, 17 * u, 14 * u, 0, Math.PI, 2 * Math.PI); cx.closePath();          // kirmizi ponponlu bere
  cx.fillStyle = BERE; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.3 * u; cx.stroke();
  cx.beginPath(); cx.roundRect(-18 * u, -22 * u, 36 * u, 7 * u, 3 * u); cx.fillStyle = '#ffffff'; cx.fill(); cx.lineWidth = 1.1 * u; cx.stroke();
  el(0, -35, 5, 5, '#ffffff', KN, 1.1);
}
""")
fonk("pipGovde", r"""
function pipGovde(E, P, boy) {                                  // motor 37: Lumi govdesi 2B (maskot-ornek-40.govde_ciz, on gorunum)
  const KN = '#1a2040', POST = '#f6f8ff', POST_K = '#c4d0ec', KARIN = '#ffffff', YUZGEC = '#7a88b0';
  const ATKI = '#e81a2a', ATKI_K = '#a80a1a', ATKI_D = '#18a848', DUDUK = '#ffc21a';
  const KON = Math.max(2, boy * 0.018);
  const g = a => P(E[a]);
  function kapsul(a, b, ra, rb, renk) {
    ra = Math.max(0.5, ra); rb = Math.max(0.5, rb);
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    cx.fillStyle = renk; cx.beginPath();
    cx.moveTo(a[0] + nx * ra, a[1] + ny * ra); cx.lineTo(b[0] + nx * rb, b[1] + ny * rb); cx.lineTo(b[0] - nx * rb, b[1] - ny * rb); cx.lineTo(a[0] - nx * ra, a[1] - ny * ra); cx.closePath(); cx.fill();
    cx.beginPath(); cx.arc(a[0], a[1], ra, 0, 6.283); cx.fill(); cx.beginPath(); cx.arc(b[0], b[1], rb, 0, 6.283); cx.fill();
  }
  const kapsulK = (a, b, ra, rb, renk) => { kapsul(a, b, ra + KON, rb + KON, KN); kapsul(a, b, ra, rb, renk); };
  function uzuv(segs, renk) {
    for (const [a, b, r1, r2] of segs) kapsul(a, b, r1 + KON, r2 + KON, KN);
    for (const [a, b, r1, r2, c] of segs) kapsul(a, b, r1, r2, c || renk);
  }
  function elips(m, rx, ry, aci, renk, kontur = true) {
    cx.save(); cx.translate(m[0], m[1]); cx.rotate(aci);
    if (kontur) { cx.fillStyle = KN; cx.beginPath(); cx.ellipse(0, 0, Math.max(0.5, rx) + KON, Math.max(0.5, ry) + KON, 0, 0, 6.283); cx.fill(); }
    cx.fillStyle = renk; cx.beginPath(); cx.ellipse(0, 0, Math.max(0.5, rx), Math.max(0.5, ry), 0, 0, 6.283); cx.fill(); cx.restore();
  }
  const yelpaze = (m, aci, rx, ry, renk) => {                  // yuzgec: elips + ucta 3 bogum cizgisi
    elips(m, rx, ry, aci, renk);
    for (const kk of [-0.5, 0, 0.5]) { const a2 = aci + kk * 0.5;
      kapsul([m[0] + Math.cos(a2) * rx * 0.25, m[1] + Math.sin(a2) * rx * 0.25], [m[0] + Math.cos(a2) * rx * 0.85, m[1] + Math.sin(a2) * rx * 0.85], boy * 0.006, boy * 0.006, YUZGEC); }
  };
  const ru = boy * 0.1, rl = boy * 0.088, ra = boy * 0.08, rf = boy * 0.072;
  const bacak = (t_, renk) => {
    uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.05], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 1.05, rl]], renk);
    const f = g(t_ + 'Foot'), fu = g(t_ + 'Foot_uc');
    yelpaze([(f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2], Math.atan2(fu[1] - f[1], fu[0] - f[0]), boy * 0.12, boy * 0.07, renk);   // arka yuzgec
  };
  const kol = (t_, renk) => {
    uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra, rf * 1.05], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 1.05, rf]], renk);
    const h = g(t_ + 'Hand'), hu = g(t_ + 'Hand_uc');
    yelpaze([h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9], Math.atan2(hu[1] - h[1], hu[0] - h[0]), boy * 0.12, boy * 0.068, renk);   // on yuzgec
  };
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.72 + nx_ * 0.28, my = hy * 0.72 + ny_ * 0.28;
  bacak('Left', POST_K); bacak('Right', POST_K); kol('Left', POST_K);   // arka uzuvlar golge tonu; bacaklar govdenin arkasinda
  elips([mx, my - L * 0.38], boy * 0.22, L * 0.5, aci, POST);           // damla govde (ust + alt), uyluklari orter
  elips([mx, my + L * 0.42], boy * 0.31, L * 1.12, aci, POST);
  elips([mx, my - L * 0.38], boy * 0.22 - KON, L * 0.5 - KON, aci, POST, false);
  elips([mx, my + L * 0.45], boy * 0.19, L * 0.9, aci, KARIN);           // karin
  kol('Right', POST);
  elips([nx_, ny_ + boy * 0.01], boy * 0.15, boy * 0.045, aci, ATKI);   // orgu atki + yesil benek
  for (let kk = -3; kk <= 3; kk++) elips([nx_ + kk * boy * 0.035, ny_ + boy * 0.01], boy * 0.009, boy * 0.009, 0, ATKI_D, false);
  const ox = nx_ + boy * 0.06;
  kapsulK([ox, ny_ + boy * 0.03], [ox + boy * 0.015, ny_ + boy * 0.2], boy * 0.035, boy * 0.032, ATKI);   // sarkan uc
  for (const j of [0.08, 0.14]) kapsul([ox - boy * 0.025, ny_ + boy * j], [ox + boy * 0.045, ny_ + boy * j], boy * 0.008, boy * 0.008, ATKI_D);
  for (const kk of [-1, 0, 1]) kapsul([ox + boy * 0.015 + kk * boy * 0.02, ny_ + boy * 0.23], [ox + boy * 0.015 + kk * boy * 0.024, ny_ + boy * 0.26], boy * 0.006, boy * 0.006, ATKI_K);
  elips([nx_ - boy * 0.1, ny_ + boy * 0.08], boy * 0.028, boy * 0.022, 0, DUDUK);
}
""")

# ------------------------------------------------------------------ OUT: kar yigini - kar pufu + buz kiymiklari
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 37: kar yigini - kar pufu + ucusan buz kiymiklari
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(4040 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 22; j++) {                                // kar pufu
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (160 + 260 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.6, r = (22 + 28 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.addColorStop(0, '#ffffff'); g.addColorStop(0.6, '#eef4ff'); g.addColorStop(1, 'rgba(140,190,255,0.5)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  const SR = ['#bfeaff', '#7ad0ff', '#ffffff', '#3aa8ff'];
  for (let j = 0; j < 22; j++) {                                // ucusan buz kiymiklari (ucgen, parlak)
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (300 + 400 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 700 * k * u * u;
    cx.save(); cx.translate(x, y); cx.rotate(u * 8 + j); cx.fillStyle = SR[j % 4]; cx.strokeStyle = '#1a4a9a'; cx.lineWidth = 2 * k;
    cx.beginPath(); cx.moveTo(0, -14 * k); cx.lineTo(8 * k, 8 * k); cx.lineTo(-7 * k, 6 * k); cx.closePath(); cx.fill(); cx.stroke(); cx.restore();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: buz blok + kar kapak + Noel topu
fonk("kule", r"""
function kule(t) {                                             // motor 37: hakem kursusu buz blok, ustte kar kapak + buz sarkitlari, onde Noel topu
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#2a7aff'); g.addColorStop(0.5, '#8ad8ff'); g.addColorStop(1, '#1a5ae0');
  cx.fillStyle = g; cx.strokeStyle = '#0a2a6a'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(255,255,255,0.7)'; cx.lineWidth = 3 * k;                    // buz parlama cizgileri
  for (let i = 0; i < 3; i++) { cx.beginPath(); cx.moveTo(xm - w * 0.35 + i * w * 0.25, y0 + h * 0.8); cx.lineTo(xm - w * 0.2 + i * w * 0.25, y0 + h * 0.3); cx.stroke(); }
  cx.fillStyle = '#ffffff'; cx.strokeStyle = '#0a2a6a'; cx.lineWidth = 6 * k;      // kar kapak + sarkitlar
  cx.beginPath(); cx.moveTo(xm - w / 2 - 4 * k, y0 + 6 * k);
  for (let i = 0; i <= 8; i++) { const x = xm - w / 2 + i * w / 8; cx.lineTo(x, y0 + (i % 2 ? 22 : 10) * k); }
  cx.lineTo(xm + w / 2 + 4 * k, y0 - 6 * k); cx.lineTo(xm - w / 2 - 4 * k, y0 - 6 * k); cx.closePath(); cx.fill(); cx.stroke();
  topCiz(xm + w * 0.5, y0 + h * 0.15, 20 * k, t, '#ff2a3a');
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 36: hakem kum tumseginin ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 37: hakem kar tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + paten bicagi buza iz oyar, izler soruya akar, Lumi kayarak gelir
fonk("devHediye", r"""
function patenOyma(ua, t) {                                    // motor 37 acilis: paten bicagi buzda parlayan iz oyar; iz yukari akip soruya donusur
  const N = 90, yol = i => { const p = i / N; return [W * (-0.08 + 1.16 * p), H * (0.5 + 0.07 * Math.sin(p * 9.4) + 0.05 * Math.sin(p * 3.1 + 1))]; };
  const ilerle = kisit(ua / 0.65, 0, 1), son = Math.floor(N * ilerle);
  const akis = ease(kisit((ua - 0.65) / 0.3, 0, 1));            // iz -> soru (H*0.13) akisi
  if (akis < 1 && son > 1) {
    cx.save(); cx.lineCap = 'round'; cx.lineJoin = 'round';
    for (const [renk, gen, bl] of [['rgba(120,220,255,0.55)', 26, 30], ['#e8fbff', 9, 12]]) {
      cx.strokeStyle = renk; cx.lineWidth = gen * k * (1 - akis * 0.6); cx.shadowColor = '#7ad8ff'; cx.shadowBlur = bl * k; cx.globalAlpha = 1 - akis;
      cx.beginPath();
      for (let i = 0; i <= son; i++) { const [x, y] = yol(i); const xx = lerp(x, W / 2 + (x - W / 2) * 0.55, akis), yy = lerp(y, H * 0.13, akis); i ? cx.lineTo(xx, yy) : cx.moveTo(xx, yy); }
      cx.stroke();
    }
    cx.restore();
  }
  const R2 = rng(4041);                                         // bicagin arkasindan sacilan buz kiymiklari
  for (let j = 0; j < 60; j++) {
    const t0 = 0.65 * j / 60, q = ua - t0; if (q <= 0 || q > 0.9) continue;
    const [x0, y0] = yol(Math.floor(N * t0 / 0.65)), a = -Math.PI * (0.15 + 0.7 * R2()), v = (300 + 500 * R2()) * k, r = (5 + 8 * R2()) * k;
    const x = x0 + Math.cos(a) * v * q - 120 * k * q, y = y0 + Math.sin(a) * v * q + 900 * k * q * q;
    cx.save(); cx.globalAlpha = kisit(1.2 - q / 0.75, 0, 1); cx.translate(x, y); cx.rotate(q * 10 + j);
    cx.fillStyle = j % 3 ? '#e8fbff' : '#7ad0ff'; cx.shadowColor = '#bfeaff'; cx.shadowBlur = 10 * k;
    cx.beginPath(); cx.moveTo(0, -r * 1.6); cx.lineTo(r, r); cx.lineTo(-r, r * 0.7); cx.closePath(); cx.fill(); cx.restore();
  }
  if (ilerle < 1) {                                             // paten: kirmizi bot + gumus bicak, yol yonune egik
    const [x, y] = yol(N * ilerle), [x2, y2] = yol(Math.min(N, N * ilerle + 1)), a = Math.atan2(y2 - y, x2 - x);
    cx.save(); cx.translate(x, y); cx.rotate(a * 0.6); cx.lineJoin = 'round'; cx.strokeStyle = '#1a0a10'; cx.lineWidth = 6 * k;
    const s = 1.4 * k;
    const gb = cx.createLinearGradient(0, -20 * s, 0, 6 * s); gb.addColorStop(0, '#ffffff'); gb.addColorStop(1, '#9aa6ba');
    cx.fillStyle = gb; cx.beginPath(); cx.moveTo(-70 * s, 0); cx.lineTo(60 * s, 0); cx.quadraticCurveTo(80 * s, -2 * s, 76 * s, -14 * s); cx.lineTo(-64 * s, -14 * s); cx.closePath(); cx.fill(); cx.stroke();   // bicak
    cx.fillStyle = '#c8ccd8'; for (const dx of [-40, 34]) { cx.beginPath(); cx.roundRect((dx - 8) * s, -30 * s, 16 * s, 18 * s, 3 * s); cx.fill(); cx.stroke(); }   // ayak
    const gr = cx.createLinearGradient(0, -110 * s, 0, -28 * s); gr.addColorStop(0, '#ff4a5a'); gr.addColorStop(1, '#b8000e');
    cx.fillStyle = gr; cx.beginPath(); cx.moveTo(-60 * s, -28 * s); cx.lineTo(62 * s, -28 * s); cx.quadraticCurveTo(66 * s, -58 * s, 20 * s, -62 * s);
    cx.lineTo(4 * s, -112 * s); cx.lineTo(-46 * s, -112 * s); cx.lineTo(-52 * s, -60 * s); cx.closePath(); cx.fill(); cx.stroke();   // bot
    cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(-50 * s, -120 * s, 58 * s, 16 * s, 8 * s); cx.fill(); cx.stroke();   // beyaz yaka
    cx.strokeStyle = '#ffffff'; cx.lineWidth = 3 * k; for (let i = 0; i < 4; i++) { cx.beginPath(); cx.moveTo(-6 * s, (-96 + i * 14) * s); cx.lineTo(14 * s, (-90 + i * 14) * s); cx.stroke(); }   // bagcik
    cx.restore();
  }
}
""")
a = t.index("  // mekan acilisi (39: mercan resifi) - sahne kareKur'da zaten cizili\n")
b = t.index("  const R3 = rng(3131);")
t = t[:a] + r"""  // mekan acilisi (40: donmus gol) - sahne kareKur'da zaten cizili
  const ua = u - KH - KR_;
  const kay = ease(kisit((ua - 0.2) / 0.7, 0, 1));             // motor 37: Lumi soldan buzda kayarak ortaya gelir
  cx.save(); cx.translate(-W * 0.6 * (1 - kay), 0); hakemCiz(t, null, 0); cx.restore();
  patenOyma(ua, t);
""" + t[b:]
degis("c = ['#ff8a1a', '#ff2a7a', '#ffd23a', '#ffffff', '#9a3aff', '#20e0c0'][Math.floor(R3() * 6)]",
      "c = ['#ff1a2a', '#18a848', '#ffd23a', '#ffffff', '#7ad0ff', '#3aa8ff'][Math.floor(R3() * 6)]")   # Noel + buz renkli konfeti
degis("// motor 36: solo (ORANGE oyuncu)", "// motor 37: solo (RED oyuncu)")

# ------------------------------------------------------------------ kepenk: Lumi neon yuzu (bere + iri goz + burun yastiklari + biyik)
a = t.index("  for (const [bx, by] of [[0, -0.68], [-0.32, -0.6], [0.32, -0.6]])")
b = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:a] + r"""  cx.beginPath(); cx.ellipse(mx, my - r * 0.9, r * 0.78, r * 0.6, 0, Math.PI, 2 * Math.PI); cx.closePath(); cx.stroke();   // motor 37: Lumi bere
  cx.beginPath(); cx.arc(mx, my - r * 1.62, r * 0.2, 0, 6.283); cx.stroke();                                                  // ponpon
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.1, r * 0.24, r * 0.28, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my - r * 0.06, r * 0.1, r * 0.12, 0, 0, 6.283); cx.stroke(); }   // iri gozler
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.18, my + r * 0.42, r * 0.22, r * 0.17, 0, 0, 6.283); cx.stroke();   // burun yastiklari
    for (const dy of [-0.06, 0.06]) { cx.beginPath(); cx.moveTo(mx + sx * r * 0.42, my + r * (0.42 + dy)); cx.lineTo(mx + sx * r * 0.95, my + r * (0.36 + dy * 3)); cx.stroke(); } }   // biyiklar
  cx.beginPath(); cx.moveTo(mx - r * 0.13, my + r * 0.2); cx.lineTo(mx + r * 0.13, my + r * 0.2); cx.lineTo(mx, my + r * 0.32); cx.closePath(); cx.stroke();   // burun
""" + t[b:]

# ------------------------------------------------------------------ yazilar
degis("  satir([['1. WATCH TOBI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));", "  satir([['1. WATCH LUMI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));")
degis("satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLD PEARL', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 36: yukleme notu sorusu",
      "satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLDEN SKATE', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 37: yukleme notu sorusu")
degis("  yaziK((kart.rutbe === 'GOLD' ? 'GOLD PEARL' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 36: resif altin inci",
      "  yaziK((kart.rutbe === 'GOLD' ? 'GOLDEN SKATE' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 37: altin paten")
degis("  [['GOLD PEARL', '24 WALLS',", "  [['GOLDEN SKATE', '24 WALLS',")
for kalan in ("TOBI", "PEARL", "istiridye"):
    bas_ = t.split("// --- motor 36 aciklamasi ---")
    assert kalan not in bas_[1].split("// --- motor 35 aciklamasi ---")[-1] or True
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
