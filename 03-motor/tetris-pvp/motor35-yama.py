"""MOTOR 35 (HUMAN TETRIS 38) = sahne33.html (motor 33, 36. video: 1P SOLO dev mantar ormani) + yama -> 03-motor/sahne35.html.
sahne33 degismez.

    python motor35-yama.py

38: REF-090 yapi (1P SOLO Christmas), alacakaranlik kurabiye koyu koprusu (varlik-kurabiye.py), ozel tur FREEZE (motor 32 tut evresi,
bolumde d.freeze + z.tut), yarisan karakter TEK sporcu (RED, karakter.py --sporcu 1 --renk FF2A3A), hakem maskot ren geyigi yavrusu PIP -
TAMAMI 2B (kullanici 25 Kas: 3B govde reddedildi): govde, uzuvlar, bas, boynuz cizgi-film dilinde; hareket karakter.py --eklem 1 verisinden
(her karede 20 eklemin ekran yeri; gercek poz acilari). Cizim maskot-ornek-38b.py ile birebir.
OUT = krema kapli kar yiginina gomulur: kar pufu + seker serpintisi. Gokte yagan kar taneleri + pariltilar.
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (koprunun ortasinda dev hediye
kutusu, kurdele cozulur, kapak firlar, kar + konfeti fiskirir, Pip ziplar) -> CAN YOU EARN THE GOLD STAR? ; ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne33.html")
HEDEF = os.path.join(BURA, "..", "sahne35.html")
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
t = t[:m.start()] + "<title>HUMAN TETRIS 38 - motor 35 (Christmas kurabiye koyu, 1P SOLO, FREEZE, 2B ren geyigi Pip, hediye kutusu girisi)</title>" + t[m.end():]
degis("// MOTOR 33 — HUMAN TETRIS 36", "// MOTOR 35 — HUMAN TETRIS 38 (REF-090 yapi, 25 Kas 2026; motor 33'ten, tetris-pvp/motor35-yama.py):\n"
      "//   - 1P SOLO Christmas: tek sporcu (RED); FREEZE ROUND (d.freeze, z.tut 3,2 sn)\n"
      "//   - sahne: tetris-pvp/varlik-kurabiye.py (alacakaranlik kurabiye koyu); gokte yagan kar + pariltilar\n"
      "//   - hakem ren geyigi PIP, TAMAMI 2B: eklem verisinden govde + uzuv + bas (maskot-ornek-38b.py ile ayni); kurabiye kursu + kar tumsegi\n"
      "//   - OUT krema kapli kar yigini (kar pufu + seker serpintisi); giris kanca -> dev hediye kutusu acilir -> CAN YOU EARN THE GOLD STAR?\n"
      "// --- motor 33 aciklamasi ---\n"
      "// MOTOR 33 — HUMAN TETRIS 36")

# ------------------------------------------------------------------ mini Noel topu (topCiz yerine) + kar tumsegi (simitCiz yerine)
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#ff2a3a', c2 = '#ffd23a') {   // motor 35: mini Noel topu (parlak top + altin kapak + kanca)
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.12);
  cx.lineWidth = Math.max(1.5, r * 0.08); cx.strokeStyle = '#2a1004'; cx.lineJoin = 'round';
  const g = cx.createRadialGradient(-r * 0.35, -r * 0.35, r * 0.05, 0, 0, r * 1.05); g.addColorStop(0, '#ffffff'); g.addColorStop(0.2, c1); g.addColorStop(1, c1);
  cx.fillStyle = g; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.fill(); cx.stroke();
  cx.strokeStyle = c2; cx.lineWidth = r * 0.14; cx.beginPath(); cx.ellipse(0, 0, r * 0.98, r * 0.28, 0, 0, 6.283); cx.stroke();   // altin serit
  cx.fillStyle = c2; cx.strokeStyle = '#2a1004'; cx.lineWidth = Math.max(1.2, r * 0.06);
  cx.beginPath(); cx.roundRect(-r * 0.26, -r * 1.18, r * 0.52, r * 0.26, r * 0.06); cx.fill(); cx.stroke();
  cx.beginPath(); cx.arc(0, -r * 1.3, r * 0.14, 0, 6.283); cx.stroke();
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 35: kar tumsegi + iki Noel topu (hakemin ayak alti)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.4); g.addColorStop(0, '#e8ecff'); g.addColorStop(1, '#8a96ff');
  cx.fillStyle = g; cx.strokeStyle = '#3a2a8a'; cx.lineWidth = Math.max(1.5, r * 0.06);
  cx.beginPath(); cx.moveTo(-r * 1.5, r * 0.2);
  for (const [px, py, pr] of [[-0.95, -0.05, 0.55], [-0.2, -0.3, 0.6], [0.6, -0.2, 0.55], [1.15, 0.0, 0.4]]) cx.arc(px * r, py * r, pr * r, Math.PI, 0);
  cx.lineTo(r * 1.5, r * 0.2); cx.quadraticCurveTo(0, r * 0.5, -r * 1.5, r * 0.2); cx.closePath(); cx.fill(); cx.stroke();
  cx.restore();
  topCiz(x - r * 1.15, y - r * 0.15, r * 0.24, 0, '#ff2a3a');
  topCiz(x + r * 1.2, y - r * 0.1, r * 0.2, 0, '#20c850');
}
""")

# ------------------------------------------------------------------ PIP (tamami 2B): maskot-ornek-38.py (bas) + 38b (govde) ile ayni
fonk("olliBas", r"""
function pipBas(u, duygu, t) {                                  // motor 35: Pip'in basi (maskot-ornek-38.bas, on gorunum), merkez (0,0), birim u
  const KN = '#2a1004', KURK = '#b8621e', AGIZ = '#ffc880', BOYNUZ = '#e8b060', BURUN = '#4a1e08', KULAK_IC = '#ff8aa8', LEKE = '#ffe0a8';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const pol = (pts, f, w = 1.6) => { cx.beginPath(); pts.forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.closePath(); cx.fillStyle = f; cx.fill(); if (w) { cx.strokeStyle = KN; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  for (const sx of [-1, 1]) {                                   // iki dalli tombul boynuz (once koyu kalin, sonra dolgu)
    const p0 = [sx * 9, -15], p1 = [sx * 15, -29], p2 = [sx * 13, -38], q1 = [sx * 22, -31];
    for (const [w, c] of [[7.6, KN], [5.2, BOYNUZ]]) {
      cx.strokeStyle = c; cx.lineWidth = w * u;
      for (const [a, b] of [[p0, p1], [p1, p2], [p1, q1]]) { cx.beginPath(); cx.moveTo(a[0] * u, a[1] * u); cx.lineTo(b[0] * u, b[1] * u); cx.stroke(); }
    }
    for (const c of [p2, q1]) el(c[0], c[1], 2.9, 2.9, BOYNUZ, KN, 1.1);
    if (sx < 0) { for (const d of [-1, 1]) el(-12 + d * 4, -23, 3.4, 2.2, '#e8102c', KN, 0.9); el(-12, -23, 1.6, 1.6, '#ffc21a', KN, 0.8); }   // kurdele
  }
  for (const sx of [-1, 1]) {                                   // yana acik kulaklar (pembe ic), hafif oynar
    cx.save(); cx.rotate(sx * 0.05 * Math.sin(t * 5));
    pol([[sx * 15, -10], [sx * 32, -15], [sx * 27, -4]], KURK); pol([[sx * 18, -9], [sx * 29, -13], [sx * 26, -6]], KULAK_IC, 0);
    cx.restore();
  }
  el(0, 0, 22, 20, KURK, KN, 1.6);
  el(0, -11, 4, 3, LEKE); el(-6, -14, 2, 1.6, LEKE); el(6, -14, 2, 1.6, LEKE);
  el(0, 9, 13, 9, AGIZ, KN, 1.2);
  el(0, 4.5, 4.6, 3.4, BURUN); el(-1.4, 3.6, 1.3, 0.9, '#a86a4a');
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') { cx.strokeStyle = KN; cx.lineWidth = 2.6 * u; cx.beginPath(); cx.arc(sx * 9 * u, -3 * u, 5.5 * u, Math.PI * 1.11, Math.PI * 1.89); cx.stroke(); }
    else if (duygu === 'sasirma') { el(sx * 9, -4, 6.5, 7.5, '#ffffff', KN, 1.4); el(sx * 9, -4, 2.6, 2.8, KN); }
    else { el(sx * 9, -3, 6, 7, '#ffffff', KN, 1.4); el(sx * 9 + 0.7, -2.4, 4.0, 4.8, KN); el(sx * 9 - 0.8, -4.6, 1.5, 1.5, '#ffffff'); }
    el(sx * 15, 5, 3.4, 2.1, '#ff7a8a');
  }
  if (duygu === 'sasirma') el(0, 13.5, 3.0, 2.6, '#7a1020', KN, 1.0);
  else { cx.strokeStyle = KN; cx.lineWidth = 1.4 * u; cx.beginPath(); cx.arc(0, 11.5 * u, 5 * u, 0.35, Math.PI - 0.35); cx.stroke(); }
}
""")
degis("let pipDuygu = 'mutlu';\nconst OLLI_U = Number(TEMA.olliU || 70 / 22 * 0.95);           // kafa birimi (onizleme kontaginda ayarlanir)\n",
      "let pipDuygu = 'mutlu';\n"
      "const PIP_OLCEK = Number(TEMA.pipOlcek || 2.6), PIP_DY = Number(TEMA.pipDy || -9);   // maskot-ornek-38b.py OLCEK / DY\n")
fonk("maskotCiz", r"""
function pipGovde(E, P, boy) {                                  // motor 35: Pip govdesi 2B - E: eklemler (kare px), P: kare px -> ekran, boy: govde boyu (ekran px)
  const KN = '#2a1004', KURK = '#b8621e', KURK_K = '#9a4e14', KARIN = '#ffc880', TOYNAK = '#3a1a0a', ATKI = '#e8102c', ATKI_K = '#b00820', CAN = '#ffc21a';
  const KON = Math.max(2, boy * 0.018);
  const g = a => P(E[a]);
  function kapsul(a, b, ra, rb, renk) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    cx.fillStyle = renk; cx.beginPath();
    cx.moveTo(a[0] + nx * ra, a[1] + ny * ra); cx.lineTo(b[0] + nx * rb, b[1] + ny * rb); cx.lineTo(b[0] - nx * rb, b[1] - ny * rb); cx.lineTo(a[0] - nx * ra, a[1] - ny * ra); cx.closePath(); cx.fill();
    cx.beginPath(); cx.arc(a[0], a[1], ra, 0, 6.283); cx.fill(); cx.beginPath(); cx.arc(b[0], b[1], rb, 0, 6.283); cx.fill();
  }
  function uzuv(segs, renk) {                                   // tek parca uzuv: once hepsinin konturu, sonra dolgular (eklemde cizgi yok)
    for (const [a, b, r1, r2] of segs) kapsul(a, b, r1 + KON, r2 + KON, KN);
    for (const [a, b, r1, r2, c] of segs) kapsul(a, b, r1, r2, c || renk);
  }
  function elips(m, rx, ry, aci, renk, kontur = true) {
    cx.save(); cx.translate(m[0], m[1]); cx.rotate(aci);
    if (kontur) { cx.fillStyle = KN; cx.beginPath(); cx.ellipse(0, 0, rx + KON, ry + KON, 0, 0, 6.283); cx.fill(); }
    cx.fillStyle = renk; cx.beginPath(); cx.ellipse(0, 0, rx, ry, 0, 0, 6.283); cx.fill(); cx.restore();
  }
  const ru = boy * 0.062, rl = boy * 0.042, rt = boy * 0.048, ra = boy * 0.05, rf = boy * 0.04;
  const bacak = (t_, renk) => uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.1], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 1.1, rl], [g(t_ + 'Foot'), g(t_ + 'Foot_uc'), rt, rt * 0.8, TOYNAK]], renk);
  const kol = (t_, renk) => uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra, rf * 1.05], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 1.05, rf], [g(t_ + 'Hand'), g(t_ + 'Hand_uc'), rf, rf * 0.8, TOYNAK]], renk);
  bacak('Left', KURK_K); kol('Left', KURK_K);                   // arka uzuvlar bir ton koyu
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.6 + nx_ * 0.4, my = hy * 0.6 + ny_ * 0.4, genis = boy * 0.17;
  elips([mx, my], genis, L * 0.62, aci, KURK);                  // armut govde
  elips([mx, my + L * 0.06], genis * 0.64, L * 0.44, aci, KARIN, false);
  cx.fillStyle = KARIN;
  for (let i = 0; i < 3; i++) { const tx = nx_ + (i - 1) * boy * 0.035, ty = ny_ + boy * 0.07; cx.beginPath(); cx.moveTo(tx - boy * 0.03, ty); cx.lineTo(tx, ty + boy * 0.06); cx.lineTo(tx + boy * 0.03, ty); cx.fill(); }
  bacak('Right', KURK); kol('Right', KURK);
  elips([nx_, ny_ + boy * 0.005], boy * 0.14, boy * 0.04, aci, ATKI);   // atki + sarkan uc + altin can
  uzuv([[[nx_ - boy * 0.07, ny_ + boy * 0.02], [nx_ - boy * 0.09, ny_ + boy * 0.1], boy * 0.03 - KON, boy * 0.026 - KON]], ATKI_K);
  elips([nx_, ny_ + boy * 0.05], boy * 0.03, boy * 0.03, 0, CAN);
}
let PIP_DURUS = null;                                            // durus karesi (ilk pozun 0. karesi = ayakta)
function pipTam(E, kafa, P, sc, boy, t) {                       // govde + bas; kafa = [x, y, r] kare px; sc = kare px -> ekran
  cx.save(); cx.lineJoin = 'round'; pipGovde(E, P, boy);
  const u = kafa[2] / 30 * PIP_OLCEK * sc, [bx, by] = P([kafa[0], kafa[1] - kafa[2] * 0.25]);
  cx.translate(bx, by + PIP_DY * u); pipBas(u, pipDuygu, t); cx.restore();
}
function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {   // motor 35: Pip (ayakta duran kare) - koseler, kartlar, abone; (x, y) govde ortasi
  if (alfa <= 0.01) return;
  const Y = KY.maskot; if (!PIP_DURUS) { const a = POZ_ADLAR[0]; PIP_DURUS = { E: Y.poz[a].eklem[0], kafa: Y.poz[a].kafa[0] }; }
  const sc = 230 * s * k / Y.boy_px, [hx, hy] = PIP_DURUS.E.Hips;
  const P = p => [x + (p[0] - hx) * sc, y + (p[1] - hy) * sc + 20 * s * k];
  cx.save(); cx.globalAlpha *= alfa;
  pipTam(PIP_DURUS.E, PIP_DURUS.kafa, P, sc, Y.boy_px * sc, t);
  cx.restore();
}
""")
# hakem: 3B kare yerine eklem verisinden 2B govde + bas
degis("  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];\n  if (!im) { maskotCiz(xm, ay - 80 * k - bob, 1.0, t); return; }",
      "  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];\n  if (!im || !Y.poz[ad] || !Y.poz[ad].eklem) { maskotCiz(xm, ay - 80 * k - bob, 1.0, t); return; }")
degis("  cx.save(); cx.shadowColor = '#ffd23a'; cx.shadowBlur = 24 * k;\n  cx.drawImage(im, x0, y0, px, px); cx.restore();\n"
      "  const kf = Y.poz[ad].kafa[Math.round(j)], kx = x0 + kf[0] * sc;\n  maskotCiz(kx, y0 + kf[1] * sc, kf[2] * sc * 1.25 / (62 * k), t, 1, true);",
      "  const jj = Math.round(j), E = Y.poz[ad].eklem[jj], kf = Y.poz[ad].kafa[jj];   // motor 35: Pip tamami 2B (eklem verisi)\n"
      "  cx.save(); cx.shadowColor = '#ffd23a'; cx.shadowBlur = 18 * k;\n"
      "  pipTam(E, kf, p => [x0 + p[0] * sc, y0 + p[1] * sc], sc, Y.boy_px * sc, t); cx.restore();")

# ------------------------------------------------------------------ yagan kar taneleri + pariltilar (spor/yaprak yerine)
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 35: yagan kar taneleri (yavas, salinarak) + yer yer parlayan yildizciklar
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j++) {
    const p = KAR_T[j];
    const x = ((p.x + Math.sin(t * 0.7 + p.f) * 0.015) % 1) * W, y = ((p.y + t * p.v * 0.4) % 1.1) * H * 0.95;
    if (j % 7 === 0) {                                          // parilti: 4 kollu yildizcik, nabiz
      const r = (p.r * 2 + 6) * k * (0.6 + 0.5 * Math.abs(Math.sin(t * 3 + p.f)));
      cx.save(); cx.translate(x, y * 0.6); cx.shadowColor = '#fff6c0'; cx.shadowBlur = 12 * k; cx.fillStyle = '#fff6d0';
      cx.beginPath(); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, rr = i % 2 ? r * 0.25 : r; cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } cx.closePath(); cx.fill(); cx.restore();
    } else {                                                    // kar tanesi: yumusak beyaz-leylak nokta
      const r = (p.r * 0.8 + 1.5) * k;
      cx.fillStyle = 'rgba(245,240,255,' + (0.6 + 0.4 * p.a) + ')'; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
    }
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ OUT: kar pufu + seker serpintisi
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 35: krema kapli kar yigini - kar pufu + seker serpintisi
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(3838 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 20; j++) {
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (160 + 260 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.6, r = (22 + 28 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.addColorStop(0, '#ffffff'); g.addColorStop(0.6, '#e6e8ff'); g.addColorStop(1, 'rgba(170,160,255,0.5)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  const SR = ['#ff2a4a', '#20c850', '#ffc21a', '#1e8cff', '#ff3aa8'];
  for (let j = 0; j < 22; j++) {                                // ucusan seker serpintisi
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (300 + 400 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 700 * k * u * u;
    cx.save(); cx.translate(x, y); cx.rotate(u * 8 + j); cx.fillStyle = SR[j % 5];
    cx.beginPath(); cx.roundRect(-11 * k, -4 * k, 22 * k, 8 * k, 4 * k); cx.fill(); cx.restore();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: kurabiye blok + krema + seker
fonk("kule", r"""
function kule(t) {                                             // motor 35: hakem kursusu zencefilli kurabiye blok, ustte damlayan krema, onde Noel topu
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#8a3a10'); g.addColorStop(0.5, '#d8761e'); g.addColorStop(1, '#7a3410');
  cx.fillStyle = g; cx.strokeStyle = '#2a1004'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd0e8'; cx.beginPath(); cx.moveTo(xm - w / 2, y0 + 4 * k);       // damlayan krema
  for (let i = 0; i <= 8; i++) { const x = xm - w / 2 + i * w / 8; cx.lineTo(x, y0 + (i % 2 ? 22 : 10) * k); }
  cx.lineTo(xm + w / 2, y0 - 4 * k); cx.lineTo(xm - w / 2, y0 - 4 * k); cx.closePath(); cx.fill(); cx.stroke();
  const SR = ['#ff2a4a', '#20c850', '#ffc21a', '#1e8cff'];
  for (let i = 0; i < 5; i++) { cx.fillStyle = SR[i % 4]; cx.beginPath(); cx.arc(xm - w * 0.36 + i * w * 0.18, y0 + h * 0.55, 7 * k, 0, 6.283); cx.fill(); cx.stroke(); }
  topCiz(xm + w * 0.5, y0 + h * 0.15, 20 * k, t, '#ff2a3a');
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 33: hakem yosun tumseginin ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 35: hakem kar tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + dev hediye kutusu acilisi
fonk("devMantar", r"""
function devHediye(x, yTaban, boy, acil, t) {                  // acilis: koprude dev hediye kutusu; acil = kapagin firlama orani (0-1)
  const w = boy * 0.62, h = boy * 0.5, y0 = yTaban - h;
  cx.save(); cx.lineJoin = 'round'; cx.strokeStyle = '#2a1004'; cx.lineWidth = 8 * k;
  const g = cx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); g.addColorStop(0, '#c80818'); g.addColorStop(0.45, '#ff2a3a'); g.addColorStop(1, '#a00614');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x - w / 2, y0, w, h, 18 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd23a'; cx.fillRect(x - w * 0.07, y0, w * 0.14, h); cx.strokeRect(x - w * 0.07, y0, w * 0.14, h);   // altin kurdele (dikey)
  const ky = y0 - h * 0.16 - acil * boy * 0.9, kr = acil * 0.9;                         // kapak yukari firlar ve doner
  cx.save(); cx.translate(x + acil * w * 0.35, ky); cx.rotate(kr);
  const g2 = cx.createLinearGradient(-w * 0.56, 0, w * 0.56, 0); g2.addColorStop(0, '#e01020'); g2.addColorStop(0.5, '#ff4a5a'); g2.addColorStop(1, '#b00818');
  cx.fillStyle = g2; cx.beginPath(); cx.roundRect(-w * 0.56, -h * 0.1, w * 1.12, h * 0.22, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd23a'; cx.fillRect(-w * 0.07, -h * 0.1, w * 0.14, h * 0.22); cx.strokeRect(-w * 0.07, -h * 0.1, w * 0.14, h * 0.22);
  const fc = 1 - acil * 0.6;                                     // fiyonk (kapakla gider, cozulurken kuculur)
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(sx * w * 0.13 * fc, -h * 0.2, w * 0.14 * fc, h * 0.12 * fc, sx * 0.5, 0, 6.283); cx.fill(); cx.stroke(); }
  cx.beginPath(); cx.arc(0, -h * 0.16, w * 0.05, 0, 6.283); cx.fill(); cx.stroke();
  cx.restore();
  cx.restore();
}
""")
degis("  // mekan acilisi (36: dev mantar ormani) - sahne kareKur'da zaten cizili\n", "  // mekan acilisi (38: kurabiye koyu) - sahne kareKur'da zaten cizili\n")
a = t.index("  const gb = ease(kisit(ua / 0.7, 0, 1)), ac = ease(kisit((ua - 0.45) / 0.35, 0, 1));")
b = t.index("  const R3 = rng(3131);")
t = t[:a] + r"""  const gb = ease(kisit(ua / 0.5, 0, 1)), ac = ease(kisit((ua - 0.4) / 0.4, 0, 1));    // dev hediye kutusu kayarak gelir, kapagi firlar
  const cik = ease(kisit((ua - 1.05) / 0.35, 0, 1));
  if (cik < 1) { cx.save(); cx.globalAlpha = 1 - cik; devHediye(W / 2, H * 1.0 + H * 0.5 * (1 - gb) + H * 0.4 * cik, H * 0.9, ac, t); cx.restore(); }
  const R2 = rng(3838);                                         // kutudan fiskiran kar ve yildizciklar (yukari, yana acilarak)
  for (let j = 0; j < 46; j++) {
    const t0 = 0.45 + 0.01 * j, q = ua - t0; if (q <= 0) continue;
    const a = -Math.PI / 2 + (R2() - 0.5) * 2.4, v = (650 + 700 * R2()) * k;
    const x = W / 2 + Math.cos(a) * v * q, y = H * 0.55 + Math.sin(a) * v * q * 0.8 + 260 * k * q * q, r = (10 + 16 * R2()) * k * (1 + q);
    if (y < -60 * k || q > 1.6) continue;
    cx.save(); cx.globalAlpha = kisit(1.4 - q, 0, 1); cx.shadowColor = '#fff6d0'; cx.shadowBlur = 18 * k;
    cx.fillStyle = j % 4 ? 'rgba(248,246,255,0.95)' : 'rgba(255,230,120,0.95)'; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill(); cx.restore();
  }
""" + t[b:]
degis("    const a = R3() * 6.283, hz = 0.6 + 0.9 * R3(), c = ['#20c850', '#7ae83a', '#ffc21a', '#ff7a10', '#ff3aa8', '#10c8d0'][Math.floor(R3() * 6)], r = (10 + 18 * R3()) * k;",
      "    const a = R3() * 6.283, hz = 0.6 + 0.9 * R3(), c = ['#ff2a3a', '#20c850', '#ffd23a', '#ffffff', '#ff3aa8', '#1e8cff'][Math.floor(R3() * 6)], r = (10 + 18 * R3()) * k;")
degis("  if (pa > 0.01) pYazi('YOU', W * 0.22, H * 0.6, 130 * k, RENK[0], pa);                       // motor 33: solo (BLUE oyuncu)",
      "  if (pa > 0.01) pYazi('YOU', W * 0.22, H * 0.6, 130 * k, RENK[0], pa);                       // motor 35: solo (RED oyuncu)")

# ------------------------------------------------------------------ kepenk: Pip neon yuzu (boynuz + kulak + goz + burun)
degis("    cx.beginPath(); cx.moveTo(mx + sx * r * 0.45, my - r * 0.72); cx.lineTo(mx + sx * r * 1.12, my - r * 1.2); cx.lineTo(mx + sx * r * 0.9, my - r * 0.86); cx.lineTo(mx + sx * r * 1.2, my - r * 0.84); cx.lineTo(mx + sx * r * 0.85, my - r * 0.5); cx.stroke();   // motor 33: Olli kulak tuyu\n"
      "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.02, r * 0.36, r * 0.38, 0, 0, 6.283); cx.stroke();          // yuz diski / iri goz\n"
      "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my, r * 0.13, r * 0.14, 0, 0, 6.283); cx.stroke();          // gozbebegi",
      "    cx.beginPath(); cx.moveTo(mx + sx * r * 0.4, my - r * 0.75); cx.lineTo(mx + sx * r * 0.7, my - r * 1.35); cx.lineTo(mx + sx * r * 0.62, my - r * 1.75);\n"
      "    cx.moveTo(mx + sx * r * 0.7, my - r * 1.35); cx.lineTo(mx + sx * r * 1.05, my - r * 1.45); cx.stroke();   // motor 35: Pip boynuz\n"
      "    cx.beginPath(); cx.moveTo(mx + sx * r * 0.7, my - r * 0.45); cx.lineTo(mx + sx * r * 1.45, my - r * 0.7); cx.lineTo(mx + sx * r * 1.2, my - r * 0.2); cx.closePath(); cx.stroke();   // kulak\n"
      "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.12, r * 0.18, r * 0.22, 0, 0, 6.283); cx.stroke();          // goz")
degis("  cx.beginPath(); cx.moveTo(mx - r * 0.14, my + r * 0.36); cx.lineTo(mx + r * 0.14, my + r * 0.36); cx.lineTo(mx, my + r * 0.62); cx.closePath(); cx.stroke();   // motor 33: gaga\n",
      "  cx.beginPath(); cx.ellipse(mx, my + r * 0.4, r * 0.5, r * 0.34, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.ellipse(mx, my + r * 0.22, r * 0.16, r * 0.12, 0, 0, 6.283); cx.stroke();   // motor 35: agiz-burun\n")

# ------------------------------------------------------------------ yazilar
degis("  satir([['1. WATCH OLLI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));", "  satir([['1. WATCH PIP SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));")
degis("satir([['CAN YOU GET ', KART_DOLGU], ['GOLD', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 96 * k * acilisSoru, acilisSoru);   // motor 33: yukleme notu sorusu",
      "satir([['CAN YOU EARN THE ', KART_DOLGU], ['GOLD STAR', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 35: yukleme notu sorusu")
degis("  yaziK(kart.rutbe + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);", "  yaziK((kart.rutbe === 'GOLD' ? 'GOLD STAR' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 35: Christmas altin yildiz")
degis("  [['GOLD', '24 WALLS',", "  [['GOLD STAR', '24 WALLS',")

# on kontak 1 (25 Kas): kapi ustunde boynuzlar ekranin ustunden tasiyor, sari parlama 2B cizimi bulaniklastiriyor, OUT'ta "BLUE LATE!"
degis("const MAS_BOY = 0.24; ", "const MAS_BOY = 0.20; ")      # motor 35: Pip boynuzlu, biraz kucuk ki boynuzlar kadraja sigsin
degis("  cx.save(); cx.shadowColor = '#ffd23a'; cx.shadowBlur = 18 * k;\n  pipTam(", "  cx.save();\n  pipTam(")
degis("satir([[outlar[0] === 'p1' ? 'BLUE' : 'PINK', ['#ffffff', RENK[outlar[0] === 'p1' ? 0 : 1]]]",
      "satir([[(TEMA.ad || ['BLUE', 'PINK'])[outlar[0] === 'p1' ? 0 : 1], ['#ffffff', RENK[outlar[0] === 'p1' ? 0 : 1]]]")   # motor 35: RED LATE!
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
