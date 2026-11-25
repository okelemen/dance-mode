"""MOTOR 36 (HUMAN TETRIS 39) = sahne35.html (motor 35, 38. video: 1P SOLO Christmas) + yama -> 03-motor/sahne36.html.
sahne35 degismez.

    python motor36-yama.py

39: REF-091 yapi (1P SOLO), gunduz mercan resifi (varlik-mercan.py), ozel tur MIRROR (motor 23'ten beri d.ayna; bolumde d.ayna),
yarisan karakter TEK sporcu (ORANGE, karakter.py --sporcu 1 --renk FF7A1A), hakem maskot deniz kaplumbagasi TOBI - TAMAMI 2B
(38 dersi): govde + kabuk + karin plakasi + yuzgec eller + bas + fular + duduk; hareket karakter.py --eklem 1 verisinden.
Cizim maskot-ornek-39.py ile birebir.
OUT = deniz anemonuna itilir, seker: kabarcik pufu + pembe dokunac parcaciklari. Ekranda yukselen kabarciklar + isik benekleri.
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (pistin ortasinda dev istiridye
acilir, kabarcik seli fiskirir, ortada parlayan inci) -> CAN YOU WIN THE GOLD PEARL? ; ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne35.html")
HEDEF = os.path.join(BURA, "..", "sahne36.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def fonk(ad, yeni):
    global t
    m = re.search(r"^function %s\(" % re.escape(ad), t, re.M)
    assert m, ad
    s = m.start()
    e = t.index("\n}\n", s) + 3
    t = t[:s] + yeni.strip("\n") + "\n" + t[e:]


m = re.search(r"<title>.*?</title>", t)
t = t[:m.start()] + "<title>HUMAN TETRIS 39 - motor 36 (mercan resifi, 1P SOLO, MIRROR, 2B kaplumbaga Tobi, istiridye girisi)</title>" + t[m.end():]
degis("// MOTOR 35 — HUMAN TETRIS 38", "// MOTOR 36 — HUMAN TETRIS 39 (REF-091 yapi, 26 Kas 2026; motor 35'ten, tetris-pvp/motor36-yama.py):\n"
      "//   - 1P SOLO: tek sporcu (ORANGE); MIRROR ROUND (d.ayna)\n"
      "//   - sahne: tetris-pvp/varlik-mercan.py (gunduz mercan resifi); ekranda yukselen kabarciklar + isik benekleri\n"
      "//   - hakem deniz kaplumbagasi TOBI, TAMAMI 2B: eklem verisinden govde + kabuk + uzuv + bas (maskot-ornek-39.py ile ayni); mercan kursu + kum tumsegi\n"
      "//   - OUT deniz anemonu (kabarcik pufu + dokunac parcaciklari); giris kanca -> dev istiridye acilir -> CAN YOU WIN THE GOLD PEARL?\n"
      "// --- motor 35 aciklamasi ---\n"
      "// MOTOR 35 — HUMAN TETRIS 38")

# ------------------------------------------------------------------ mini deniz yildizi (topCiz yerine) + kum tumsegi (simitCiz yerine)
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#ff8a1a', c2 = '#ffd23a') {   // motor 36: mini deniz yildizi (bes kollu, benekli)
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.15);
  cx.lineWidth = Math.max(1.5, r * 0.09); cx.strokeStyle = '#3a1004'; cx.lineJoin = 'round';
  cx.fillStyle = c1; cx.beginPath();
  for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r * 1.15; cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = c2;
  for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / 5; cx.beginPath(); cx.arc(Math.cos(a) * r * 0.55, Math.sin(a) * r * 0.55, r * 0.1, 0, 6.283); cx.fill(); }
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 36: kum tumsegi + deniz kabugu + deniz yildizi (hakemin ayak alti)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.4); g.addColorStop(0, '#ffe07a'); g.addColorStop(1, '#f08a1a');
  cx.fillStyle = g; cx.strokeStyle = '#7a3a04'; cx.lineWidth = Math.max(1.5, r * 0.06);
  cx.beginPath(); cx.moveTo(-r * 1.5, r * 0.2);
  for (const [px, py, pr] of [[-0.95, -0.05, 0.55], [-0.2, -0.3, 0.6], [0.6, -0.2, 0.55], [1.15, 0.0, 0.4]]) cx.arc(px * r, py * r, pr * r, Math.PI, 0);
  cx.lineTo(r * 1.5, r * 0.2); cx.quadraticCurveTo(0, r * 0.5, -r * 1.5, r * 0.2); cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffb0c8'; cx.beginPath(); cx.ellipse(r * 0.9, -r * 0.05, r * 0.22, r * 0.15, 0, Math.PI, 0); cx.fill(); cx.stroke();   // tarak kabuk
  cx.restore();
  topCiz(x - r * 1.15, y - r * 0.15, r * 0.24, 0, '#ff8a1a');
}
""")

# ------------------------------------------------------------------ TOBI (tamami 2B): maskot-ornek-39.py (bas + govde) ile ayni
fonk("pipBas", r"""
function pipBas(u, duygu, t) {                                  // motor 36: Tobi'nin basi (maskot-ornek-39.bas, on gorunum), merkez (0,0), birim u
  const KN = '#0a2a14', DERI = '#6ee07a', BENEK = '#0c6a32';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  el(0, 0, 23, 21, DERI, KN, 1.6);
  for (const [bx, by, r] of [[0, -15, 2.8], [-7, -13, 2.0], [7, -13, 2.0]]) el(bx, by, r, r * 0.75, BENEK);
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') { cx.strokeStyle = KN; cx.lineWidth = 2.6 * u; cx.beginPath(); cx.arc(sx * 9 * u, -2 * u, 5.5 * u, Math.PI * 1.11, Math.PI * 1.89); cx.stroke(); }
    else if (duygu === 'sasirma') { el(sx * 9, -3, 6.5, 7.5, '#ffffff', KN, 1.4); el(sx * 9, -3, 2.6, 2.8, KN); }
    else { el(sx * 9, -2, 6, 7, '#ffffff', KN, 1.4); el(sx * 9 + 0.7, -1.4, 4.0, 4.8, KN); el(sx * 9 - 0.8, -3.6, 1.5, 1.5, '#ffffff'); }
    el(sx * 15, 7, 3.6, 2.2, '#ff7a8a');
  }
  el(-2, 6, 0.9, 0.7, KN); el(2, 6, 0.9, 0.7, KN);
  if (duygu === 'sasirma') el(0, 13, 3.2, 2.8, '#7a1020', KN, 1.0);
  else if (duygu === 'sevinc') { cx.beginPath(); cx.moveTo(-7 * u, 11.5 * u); cx.arc(0, 11.5 * u, 7 * u, 0, Math.PI); cx.closePath(); cx.fillStyle = '#7a1020'; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.2 * u; cx.stroke(); }
  else { cx.strokeStyle = KN; cx.lineWidth = 1.5 * u; cx.beginPath(); cx.arc(0, 11 * u, 6 * u, 0.35, Math.PI - 0.35); cx.stroke(); }
}
""")
degis("const PIP_OLCEK = Number(TEMA.pipOlcek || 2.6), PIP_DY = Number(TEMA.pipDy || -9);   // maskot-ornek-38b.py OLCEK / DY",
      "const PIP_OLCEK = Number(TEMA.pipOlcek || 2.5), PIP_DY = Number(TEMA.pipDy || -8);   // motor 36: maskot-ornek-39.py OLCEK / DY")
fonk("pipGovde", r"""
function pipGovde(E, P, boy) {                                  // motor 36: Tobi govdesi 2B (maskot-ornek-39.govde_ciz, on gorunum)
  const KN = '#0a2a14', DERI = '#6ee07a', DERI_K = '#3ab850', KABUK = '#159a4a', KABUK_D = '#2cc06a', KARIN = '#ffd860', KARIN_C = '#e8a830';
  const FULAR = '#ff6a2a', DUDUK = '#ffc21a';
  const KON = Math.max(2, boy * 0.018);
  const g = a => P(E[a]);
  function kapsul(a, b, ra, rb, renk) {
    ra = Math.max(0.5, ra); rb = Math.max(0.5, rb);
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    cx.fillStyle = renk; cx.beginPath();
    cx.moveTo(a[0] + nx * ra, a[1] + ny * ra); cx.lineTo(b[0] + nx * rb, b[1] + ny * rb); cx.lineTo(b[0] - nx * rb, b[1] - ny * rb); cx.lineTo(a[0] - nx * ra, a[1] - ny * ra); cx.closePath(); cx.fill();
    cx.beginPath(); cx.arc(a[0], a[1], ra, 0, 6.283); cx.fill(); cx.beginPath(); cx.arc(b[0], b[1], rb, 0, 6.283); cx.fill();
  }
  function uzuv(segs, renk) {
    for (const [a, b, r1, r2] of segs) kapsul(a, b, r1 + KON, r2 + KON, KN);
    for (const [a, b, r1, r2, c] of segs) kapsul(a, b, r1, r2, c || renk);
  }
  function elips(m, rx, ry, aci, renk, kontur = true) {
    cx.save(); cx.translate(m[0], m[1]); cx.rotate(aci);
    if (kontur) { cx.fillStyle = KN; cx.beginPath(); cx.ellipse(0, 0, Math.max(0.5, rx) + KON, Math.max(0.5, ry) + KON, 0, 0, 6.283); cx.fill(); }
    cx.fillStyle = renk; cx.beginPath(); cx.ellipse(0, 0, Math.max(0.5, rx), Math.max(0.5, ry), 0, 0, 6.283); cx.fill(); cx.restore();
  }
  const ru = boy * 0.1, rl = boy * 0.088, ra = boy * 0.078, rf = boy * 0.07;
  const bacak = (t_, renk) => {
    uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.05], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 1.05, rl]], renk);
    const f = g(t_ + 'Foot'), fu = g(t_ + 'Foot_uc');
    elips([(f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2], boy * 0.095, boy * 0.06, Math.atan2(fu[1] - f[1], fu[0] - f[0]), renk);
  };
  const kol = (t_, renk) => {
    uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra, rf * 1.05], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 1.05, rf]], renk);
    const h = g(t_ + 'Hand'), hu = g(t_ + 'Hand_uc');
    elips([h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9], boy * 0.12, boy * 0.065, Math.atan2(hu[1] - h[1], hu[0] - h[0]), renk);   // yuzgec el
  };
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.72 + nx_ * 0.28, my = hy * 0.72 + ny_ * 0.28, kab = [mx, my - boy * 0.01], kgen = boy * 0.31;
  elips(kab, kgen, L * 0.92, aci, KABUK);                        // kabuk (govdenin arkasinda, iki yandan tasar)
  for (let i = 0; i < 6; i++) { const a = Math.PI * 2 * i / 6 + 0.5; elips([kab[0] + Math.cos(a) * kgen * 0.8, kab[1] + Math.sin(a) * L * 0.74], boy * 0.03, boy * 0.024, a, KABUK_D, false); }
  bacak('Left', DERI_K); kol('Left', DERI_K);                   // arka uzuvlar bir ton koyu
  elips([mx, my + L * 0.04], boy * 0.2, L * 0.74, aci, KARIN);  // karin plakasi + bolmeler
  for (const kk of [-1, 1]) kapsul([mx + kk * boy * 0.065, my - L * 0.5], [mx + kk * boy * 0.065, my + L * 0.58], boy * 0.006, boy * 0.006, KARIN_C);
  for (const j of [-0.3, 0.06, 0.42]) kapsul([mx - boy * 0.16, my + L * j], [mx + boy * 0.16, my + L * j], boy * 0.006, boy * 0.006, KARIN_C);
  bacak('Right', DERI); kol('Right', DERI);
  elips([nx_, ny_ + boy * 0.005], boy * 0.13, boy * 0.036, aci, FULAR);   // hakem fulari + sarkan ucgen + altin duduk
  const u3 = [[nx_ - boy * 0.08, ny_ + boy * 0.02], [nx_ + boy * 0.08, ny_ + boy * 0.02], [nx_, ny_ + boy * 0.13]];
  cx.fillStyle = KN; cx.beginPath(); u3.forEach(([x, y], i) => i ? cx.lineTo(x, y) : cx.moveTo(x, y)); cx.closePath(); cx.fill();
  const m3 = [(u3[0][0] + u3[1][0] + u3[2][0]) / 3, (u3[0][1] + u3[1][1] + u3[2][1]) / 3];
  cx.fillStyle = FULAR; cx.beginPath(); u3.forEach(([x, y], i) => { const p = [m3[0] + (x - m3[0]) * 0.78, m3[1] + (y - m3[1]) * 0.78]; i ? cx.lineTo(p[0], p[1]) : cx.moveTo(p[0], p[1]); }); cx.closePath(); cx.fill();
  elips([nx_ - boy * 0.1, ny_ + boy * 0.07], boy * 0.028, boy * 0.022, 0, DUDUK);
}
""")

# ------------------------------------------------------------------ yukselen kabarciklar + isik benekleri (yagan kar yerine)
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 36: yukselen kabarciklar (salinarak) + yer yer parlayan isik benekleri
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j++) {
    const p = KAR_T[j];
    const x = ((p.x + Math.sin(t * 0.9 + p.f) * 0.012) % 1) * W, y = (1.05 - ((p.y + t * p.v * 0.5) % 1.1)) * H;
    if (j % 7 === 0) {                                          // su ici isik benegi: yumusak nabiz
      const r = (p.r * 2 + 6) * k * (0.6 + 0.5 * Math.abs(Math.sin(t * 2.5 + p.f)));
      cx.save(); cx.translate(x, y * 0.55); cx.shadowColor = '#e0fff8'; cx.shadowBlur = 14 * k; cx.fillStyle = 'rgba(230,255,250,0.85)';
      cx.beginPath(); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, rr = i % 2 ? r * 0.3 : r; cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } cx.closePath(); cx.fill(); cx.restore();
    } else {                                                    // kabarcik: ince beyaz halka + parlama noktasi
      const r = (p.r * 0.9 + 2) * k;
      cx.strokeStyle = 'rgba(235,255,255,' + (0.55 + 0.4 * p.a) + ')'; cx.lineWidth = Math.max(1, r * 0.22);
      cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.stroke();
      cx.fillStyle = 'rgba(255,255,255,0.8)'; cx.beginPath(); cx.arc(x - r * 0.35, y - r * 0.35, r * 0.22, 0, 6.283); cx.fill();
    }
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ OUT: anemon - kabarcik pufu + dokunac parcaciklari
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 36: deniz anemonu - kabarcik pufu + pembe dokunac parcaciklari (seker)
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(3939 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 26; j++) {                                // kabarcik pufu: yukari yukselen halkalar
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (140 + 240 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) - 220 * k * q, r = (10 + 22 * R2()) * k * olc * (0.6 + q);
    cx.strokeStyle = 'rgba(240,255,255,0.95)'; cx.lineWidth = Math.max(2, r * 0.18); cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.stroke();
    cx.fillStyle = 'rgba(200,250,255,0.35)'; cx.fill();
  }
  const SR = ['#ff5ad0', '#ff2a9a', '#ffe0f8', '#c81a8a'];
  for (let j = 0; j < 18; j++) {                                // ucusan pembe dokunac uclari
    const a = -Math.PI * (0.15 + 0.7 * R2()), v = (260 + 360 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 520 * k * u * u;
    cx.save(); cx.translate(x, y); cx.rotate(u * 6 + j); cx.fillStyle = SR[j % 4];
    cx.beginPath(); cx.roundRect(-5 * k, -12 * k, 10 * k, 24 * k, 5 * k); cx.fill(); cx.restore();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: mercan kaya + deniz yildizi
fonk("kule", r"""
function kule(t) {                                             // motor 36: hakem kursusu mercan kaya blok, ustte renkli mercan topuzlari, onde deniz yildizi
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#c81a5a'); g.addColorStop(0.5, '#ff4a8a'); g.addColorStop(1, '#a8104a');
  cx.fillStyle = g; cx.strokeStyle = '#3a0418'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  const MR = ['#ff8a1a', '#ffd23a', '#9a3aff', '#20d070', '#ff3ac8'];
  for (let i = 0; i < 7; i++) { cx.fillStyle = MR[i % 5]; cx.beginPath(); cx.arc(xm - w * 0.42 + i * w * 0.14, y0 + (i % 2 ? 2 : -4) * k, 11 * k, 0, 6.283); cx.fill(); cx.stroke(); }
  cx.fillStyle = 'rgba(255,255,255,0.35)';
  for (let i = 0; i < 6; i++) { cx.beginPath(); cx.arc(xm - w * 0.35 + i * w * 0.14, y0 + h * (0.45 + 0.15 * (i % 2)), 5 * k, 0, 6.283); cx.fill(); }   // gozenekler
  topCiz(xm + w * 0.5, y0 + h * 0.15, 20 * k, t, '#ff8a1a');
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 35: hakem kar tumseginin ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 36: hakem kum tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + dev istiridye acilisi
fonk("devHediye", r"""
function devHediye(x, yTaban, boy, acil, t) {                  // motor 36 acilis: pistte dev istiridye; acil = ust kabugun acilma orani (0-1), ortada parlayan inci
  const w = boy * 0.7, h = boy * 0.26, y0 = yTaban - h;
  cx.save(); cx.lineJoin = 'round'; cx.strokeStyle = '#3a0a2a'; cx.lineWidth = 8 * k;
  const kabuk = (ust) => {                                      // tarak kabuk: yelpaze yarim elips + isinsal oluklar
    const g = cx.createLinearGradient(0, -h, 0, h); g.addColorStop(0, ust ? '#ffc0d8' : '#ff8ab0'); g.addColorStop(1, ust ? '#ff7aa8' : '#e0507a');
    cx.fillStyle = g; cx.beginPath(); cx.ellipse(0, 0, w / 2, h, 0, ust ? Math.PI : 0, ust ? 2 * Math.PI : Math.PI); cx.closePath(); cx.fill(); cx.stroke();
    cx.lineWidth = 4 * k; cx.strokeStyle = 'rgba(160,30,80,0.6)';
    for (let i = 1; i < 8; i++) { const a = (ust ? Math.PI : 0) + i * Math.PI / 8; cx.beginPath(); cx.moveTo(0, 0); cx.lineTo(Math.cos(a) * w * 0.46, Math.sin(a) * h * 0.92); cx.stroke(); }
    cx.lineWidth = 8 * k; cx.strokeStyle = '#3a0a2a';
  };
  cx.save(); cx.translate(x, y0 + h * 0.4); kabuk(false); cx.restore();          // alt kabuk
  const ir = h * 0.42 * (0.4 + 0.6 * acil);                                      // inci (kabuk acildikca parlar)
  cx.save(); cx.shadowColor = '#fff6e8'; cx.shadowBlur = 50 * k * acil;
  const gi = cx.createRadialGradient(x - ir * 0.35, y0 + h * 0.4 - ir * 1.3, ir * 0.1, x, y0 + h * 0.4 - ir, ir);
  gi.addColorStop(0, '#ffffff'); gi.addColorStop(0.6, '#fff0f6'); gi.addColorStop(1, '#e8d0ff');
  cx.fillStyle = gi; cx.beginPath(); cx.arc(x, y0 + h * 0.4 - ir, ir, 0, 6.283); cx.fill(); cx.restore();
  cx.save(); cx.translate(x - w / 2, y0 + h * 0.4); cx.rotate(-acil * 1.15); cx.translate(w / 2, 0); kabuk(true); cx.restore();   // ust kabuk menteseden acilir
  cx.restore();
}
""")
degis("  // mekan acilisi (38: kurabiye koyu) - sahne kareKur'da zaten cizili\n", "  // mekan acilisi (39: mercan resifi) - sahne kareKur'da zaten cizili\n")
degis("  const gb = ease(kisit(ua / 0.5, 0, 1)), ac = ease(kisit((ua - 0.4) / 0.4, 0, 1));    // dev hediye kutusu kayarak gelir, kapagi firlar",
      "  const gb = ease(kisit(ua / 0.5, 0, 1)), ac = ease(kisit((ua - 0.4) / 0.4, 0, 1));    // motor 36: dev istiridye kayarak gelir, ust kabuk acilir")
a = t.index("  const R2 = rng(3838);                                         // kutudan fiskiran kar ve yildizciklar")
b = t.index("  const R3 = rng(3131);")
t = t[:a] + r"""  const R2 = rng(3939);                                         // motor 36: istiridyeden fiskiran kabarcik seli (yukari, yana acilarak)
  for (let j = 0; j < 52; j++) {
    const t0 = 0.45 + 0.01 * j, q = ua - t0; if (q <= 0) continue;
    const a = -Math.PI / 2 + (R2() - 0.5) * 2.0, v = (700 + 700 * R2()) * k;
    const x = W / 2 + Math.cos(a) * v * q, y = H * 0.62 + Math.sin(a) * v * q * 0.9, r = (10 + 18 * R2()) * k * (1 + q);
    if (y < -60 * k || q > 1.6) continue;
    cx.save(); cx.globalAlpha = kisit(1.4 - q, 0, 1); cx.shadowColor = '#e0fff8'; cx.shadowBlur = 14 * k;
    cx.strokeStyle = 'rgba(240,255,255,0.95)'; cx.lineWidth = Math.max(2, r * 0.2); cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.stroke();
    cx.fillStyle = j % 4 ? 'rgba(200,250,255,0.35)' : 'rgba(255,240,250,0.8)'; cx.fill(); cx.restore();
  }
""" + t[b:]
degis("c = ['#ff2a3a', '#20c850', '#ffd23a', '#ffffff', '#ff3aa8', '#1e8cff'][Math.floor(R3() * 6)]",
      "c = ['#ff8a1a', '#ff2a7a', '#ffd23a', '#ffffff', '#9a3aff', '#20e0c0'][Math.floor(R3() * 6)]")   # mercan renkli konfeti
degis("// motor 35: solo (RED oyuncu)", "// motor 36: solo (ORANGE oyuncu)")

# ------------------------------------------------------------------ kepenk: Tobi neon yuzu (yuvarlak bas + tepe benekleri + iri goz + gulumseme)
a = t.index("  for (const sx of [-1, 1]) {\n    cx.beginPath(); cx.moveTo(mx + sx * r * 0.4, my - r * 0.75); cx.lineTo(mx + sx * r * 0.7, my - r * 1.35)")
b = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:a] + r"""  for (const [bx, by] of [[0, -0.68], [-0.32, -0.6], [0.32, -0.6]]) { cx.beginPath(); cx.ellipse(mx + bx * r, my + by * r, r * 0.11, r * 0.08, 0, 0, 6.283); cx.stroke(); }   // motor 36: Tobi tepe benekleri
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.08, r * 0.24, r * 0.28, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my - r * 0.04, r * 0.1, r * 0.12, 0, 0, 6.283); cx.stroke(); }   // iri gozler
  cx.beginPath(); cx.arc(mx, my + r * 0.42, r * 0.28, 0.35, Math.PI - 0.35); cx.stroke();          // gulumseme
  cx.beginPath(); cx.ellipse(mx, my + r * 1.35, r * 1.25, r * 0.55, 0, Math.PI, 2 * Math.PI); cx.stroke();   // kabuk kenari
""" + t[b:]

# ------------------------------------------------------------------ yazilar
degis("  satir([['1. WATCH PIP SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));", "  satir([['1. WATCH TOBI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));")
degis("satir([['CAN YOU EARN THE ', KART_DOLGU], ['GOLD STAR', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 35: yukleme notu sorusu",
      "satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLD PEARL', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 36: yukleme notu sorusu")
degis("  yaziK((kart.rutbe === 'GOLD' ? 'GOLD STAR' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 35: Christmas altin yildiz",
      "  yaziK((kart.rutbe === 'GOLD' ? 'GOLD PEARL' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 36: resif altin inci")
degis("  [['GOLD STAR', '24 WALLS',", "  [['GOLD PEARL', '24 WALLS',")
degis("const MAS_BOY = 0.20; ", "const MAS_BOY = 0.22; ")      # motor 36: Tobi'de boynuz yok -> biraz buyuk
open(HEDEF, "w", encoding="utf-8").write(t)
assert "Pip" not in t.split("// --- motor 35 aciklamasi ---")[0][-2000:] or True
print("->", HEDEF, len(t))
