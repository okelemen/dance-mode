"""MOTOR 40 (HUMAN TETRIS 43) = sahne38.html (motor 38, 41. video: 1P SOLO col vahasi) + yama -> 03-motor/sahne40.html.
sahne38 degismez. (motor 39 = 42. video 1v1 korsan gemisi, iki serit; 43 solo oldugu icin tek serit motoru 38'den turer.)

    python motor40-yama.py

43: REF-095 yapi (1P SOLO), gunduz dinozor vadisi (varlik-dino.py), ozel tur MIRROR (motor 33'ten beri d.ayna; bolum JSON'unda),
yarisan karakter TEK sporcu (PURPLE, karakter.py --sporcu 1 --renk 9A3AFF), hakem maskot T-rex yavrusu BAKU - TAMAMI 2B:
bas (yumurta kabugu sapka, genis burun, dis) + turuncu govde + sari karin plakalari + kalin kuyruk + tirnakli ayak + ince kol + duduk;
hareket karakter.py --eklem 1 verisinden. Cizim maskot-ornek-43.py ile birebir (on gorunum).
OUT = camur birikintisine kayar: camur sicramasi + ucusan camur damlalari. Ekranda kum pariltisi yerine suzulen polen + dusen yaprak.
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (uzakta volkan "puf" duman atar,
ortada dev altin yumurta sallanir, catlar, iki yarisi ayrilir, icinden isik + Baku firlar) -> CAN YOU HATCH THE GOLDEN EGG? ; ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne38.html")
HEDEF = os.path.join(BURA, "..", "sahne40.html")
t = open(KAYNAK, encoding="utf-8").read()


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
t = t[:m.start()] + "<title>HUMAN TETRIS 43 - motor 40 (dinozor vadisi, 1P SOLO, MIRROR, 2B T-rex Baku, yumurta girisi)</title>" + t[m.end():]
degis("// MOTOR 38 — HUMAN TETRIS 41", "// MOTOR 40 — HUMAN TETRIS 43 (REF-095 yapi, 28 Kas 2026; motor 38'den, tetris-pvp/motor40-yama.py):\n"
      "//   - 1P SOLO: tek sporcu (PURPLE); MIRROR ROUND (d.ayna, bolum JSON'u)\n"
      "//   - sahne: tetris-pvp/varlik-dino.py (gunduz dinozor vadisi); ekranda suzulen polen + dusen yaprak\n"
      "//   - hakem T-rex BAKU, TAMAMI 2B: eklem verisinden govde + kuyruk + ayak + kol + bas + kabuk sapka (maskot-ornek-43.py ile ayni); yosunlu tas kursu + cim tumsegi\n"
      "//   - OUT camur (camur sicramasi + damlalar); giris kanca -> volkan pufu + altin yumurta catlar -> CAN YOU HATCH THE GOLDEN EGG?\n"
      "// --- motor 38 aciklamasi ---\n"
      "// MOTOR 38 — HUMAN TETRIS 41")

# ------------------------------------------------------------------ mini benekli yumurta (kaktus yerine) + cim tumsegi + polen/yaprak
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#2ad8c8', c2 = '#ffffff') {   // motor 40: mini benekli dinozor yumurtasi (hafif sallanir); imza 38 ile ayni
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.08);
  cx.lineWidth = Math.max(1.5, r * 0.1); cx.strokeStyle = '#2a1608'; cx.lineJoin = 'round';
  const g = cx.createRadialGradient(-r * 0.3, -r * 0.6, r * 0.1, 0, -r * 0.2, r * 1.3); g.addColorStop(0, '#ffffff'); g.addColorStop(0.35, c1); g.addColorStop(1, c1);
  cx.fillStyle = g;
  cx.beginPath(); cx.ellipse(0, -r * 0.55, r * 0.72, r * 0.95, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.fillStyle = c2;
  for (const [bx, by, br] of [[-0.25, -0.95, 0.14], [0.28, -0.6, 0.12], [-0.1, -0.25, 0.1], [0.3, -1.1, 0.08]]) { cx.beginPath(); cx.arc(bx * r, by * r, br * r, 0, 6.283); cx.fill(); }
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 40: canli yesil cim tumsegi + iki mini yumurta (hakemin ayak alti)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.4); g.addColorStop(0, '#7ae04a'); g.addColorStop(1, '#1a9a2a');
  cx.fillStyle = g; cx.strokeStyle = '#0a4a14'; cx.lineWidth = Math.max(1.5, r * 0.06);
  cx.beginPath(); cx.moveTo(-r * 1.5, r * 0.2);
  cx.quadraticCurveTo(-r * 0.7, -r * 0.55, 0, -r * 0.45); cx.quadraticCurveTo(r * 0.8, -r * 0.4, r * 1.5, r * 0.2);
  cx.quadraticCurveTo(0, r * 0.5, -r * 1.5, r * 0.2); cx.closePath(); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(10,90,20,0.7)'; cx.lineWidth = Math.max(1, r * 0.03);            // cim tutamlari
  for (let i = -5; i <= 5; i++) { const bx = i * r * 0.22; cx.beginPath(); cx.moveTo(bx, -r * 0.2); cx.lineTo(bx + r * 0.05, -r * 0.42 + Math.abs(i) * r * 0.02); cx.stroke(); }
  cx.restore();
  topCiz(x - r * 1.15, y - r * 0.05, r * 0.26, 0, '#ffd81a', '#ffffff');
  topCiz(x + r * 1.2, y, r * 0.22, 0, '#ff6a9a', '#ffffff');
}
""")
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 40: suzulen sari-yesil polen + yer yer dusen yaprak; imza 38 ile ayni
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j++) {
    const p = KAR_T[j];
    const x = ((p.x + t * p.v * 0.12 + Math.sin(t * 0.7 + p.f) * 0.02 + 1) % 1) * W, y = ((p.y + t * p.v * 0.05) % 1) * H * 0.95;
    if (j % 9 === 0) {                                          // dusen yaprak: yesil damla, doner
      const r = (p.r * 2 + 8) * k;
      cx.save(); cx.translate(x, y); cx.rotate(t * 1.5 + p.f); cx.scale(1, 0.45 + 0.35 * Math.sin(t * 3 + p.f));
      cx.fillStyle = ['#3ac81a', '#6ad81a', '#18b83a'][j % 3]; cx.strokeStyle = '#0a5a14'; cx.lineWidth = 2 * k;
      cx.beginPath(); cx.ellipse(0, 0, r, r * 0.45, 0, 0, 6.283); cx.fill(); cx.stroke();
      cx.beginPath(); cx.moveTo(-r, 0); cx.lineTo(r, 0); cx.stroke(); cx.restore();
    } else if (j % 3 === 0) {                                   // polen: kucuk sari-yesil isikli nokta (seyrek; ekran kalabalik olmaz)
      const r = (p.r * 0.5 + 1.5) * k;
      cx.shadowColor = '#e8ff6a'; cx.shadowBlur = 8 * k;
      cx.fillStyle = 'rgba(232,255,106,' + (0.5 + 0.4 * p.a) + ')'; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
      cx.shadowBlur = 0;
    }
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ BAKU (tamami 2B): maskot-ornek-43.py (bas + govde, on gorunum) ile ayni
fonk("pipBas", r"""
function pipBas(u, duygu, t) {                                  // motor 40: Baku'nun basi (maskot-ornek-43.bas, on gorunum), merkez (0,0), birim u
  const KN = '#2a1608', POST = '#ff8a2a', KABUK = '#fffaf0', KABUK_B = '#ffd84a', YANAK = '#ff5a3a';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const yay = (x, y, rx, ry, a0, a1, w) => { cx.strokeStyle = KN; cx.lineWidth = w * u; cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, a0 * Math.PI / 180, a1 * Math.PI / 180); cx.stroke(); };
  const poli = (pts, f, s, w) => { cx.beginPath(); pts.forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.closePath(); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  el(0, 0, 24, 21, POST, KN, 1.6);                              // iri yuvarlak bas
  cx.beginPath(); cx.roundRect(-15 * u, 2 * u, 30 * u, 17 * u, 8 * u); cx.fillStyle = POST; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.6 * u; cx.stroke();   // genis burun
  el(0, 2, 22.5, 18.5, POST);
  for (const sx of [-1, 1]) {
    el(sx * 5, 8, 1.6, 1.2, KN);                                // burun delikleri
    el(sx * 9.5, -6, 7.6, 8.0, '#ffffff', KN, 1.0);
    if (duygu === 'sevinc') yay(sx * 9.5, -6, 5, 5, 200, 340, 2.6);
    else if (duygu === 'sasirma') el(sx * 9.5, -6, 2.4, 2.6, '#101018');
    else { el(sx * 9.5 + 0.6, -5.6, 4.4, 5.2, '#101018'); el(sx * 9.5 - 0.9, -8.0, 1.6, 1.6, '#ffffff'); }
    el(sx * 18, 6, 3.4, 2.1, YANAK);
  }
  if (duygu === 'sasirma' || duygu === 'sevinc') {              // acik agiz + minik disler
    cx.beginPath(); cx.ellipse(0, 16.5 * u, 9 * u, 7.5 * u, 0, 0, Math.PI); cx.closePath(); cx.fillStyle = '#a8201a'; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.1 * u; cx.stroke();
    for (const tx of [-6, -2, 2, 6]) poli([[tx - 1.4, 16.2], [tx, 19], [tx + 1.4, 16.2]], '#ffffff', KN, 0.6);
  } else yay(0, 12, 9, 6, 20, 160, 1.4);                        // gulumseme
  const sal = Math.sin(t * 4) * 0.04;                           // kabuk sapka hafif sallanir
  cx.save(); cx.rotate(sal);
  const nok = [[-22, -16]];                                     // yumurta kabugu sapka: zikzak kirik kenar + kubbe + sari benek
  for (let i = 0; i < 9; i++) nok.push([-22 + (i + 0.5) * 44 / 9, -16 + (i % 2 === 0 ? 3 : -1)]);
  nok.push([22, -16]);
  for (let q = 0; q <= 16; q++) { const a = q * Math.PI / 16; nok.push([22 * Math.cos(a), -16 - 18 * Math.sin(a)]); }
  poli(nok, KABUK, KN, 1.4);
  for (const [bx, by, br] of [[-10, -24, 3.2], [6, -29, 2.6], [13, -20, 2.2], [-2, -20, 1.8]]) el(bx, by, br, br * 0.85, KABUK_B);
  cx.restore();
}
""")
fonk("pipGovde", r"""
function pipGovde(E, P, boy) {                                  // motor 40: Baku govdesi 2B (maskot-ornek-43.govde_ciz, on gorunum)
  const KN = '#2a1608', POST = '#ff8a2a', POST_K = '#e8601a', KARIN = '#ffe04a', KARIN_S = '#f0b81a', TIRNAK = '#fff6e0', DUDUK = '#ffc21a';
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
  const ru = boy * 0.1, rl = boy * 0.088, ra = boy * 0.08, rf = boy * 0.072;
  const bacak = (t_, renk) => {                                 // kalin bacak + uc beyaz tirnakli ayak
    uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.05], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 0.75, rl * 0.65]], renk);
    const f = g(t_ + 'Foot'), fu = g(t_ + 'Foot_uc'), fa = Math.atan2(fu[1] - f[1], fu[0] - f[0]);
    elips([(f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2], boy * 0.1, boy * 0.06, fa, renk);
    for (const kk of [-1, 0, 1]) elips([fu[0] + Math.cos(fa + kk * 0.4) * boy * 0.03, fu[1] + Math.sin(fa + kk * 0.4) * boy * 0.03], boy * 0.028, boy * 0.016, fa + kk * 0.4, TIRNAK);
  };
  const kol = (t_, renk) => {                                   // ince kol + uc tirnak (iskelet boyunda: pozu gostersin)
    uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra * 0.75, rf * 0.7], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 0.7, rf * 0.6]], renk);
    const h = g(t_ + 'Hand'), hu = g(t_ + 'Hand_uc'), aci = Math.atan2(hu[1] - h[1], hu[0] - h[0]);
    for (const kk of [-1, 0, 1]) elips([h[0] + Math.cos(aci + kk * 0.45) * boy * 0.05, h[1] + Math.sin(aci + kk * 0.45) * boy * 0.05], boy * 0.03, boy * 0.016, aci + kk * 0.45, TIRNAK);
  };
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.72 + nx_ * 0.28, my = hy * 0.72 + ny_ * 0.28;
  const ka = Math.PI / 2 + 0.55;                                // kalin, sivrilen T-rex kuyrugu (govdenin arkasinda)
  for (const [q, rr] of [[0.18, 0.15], [0.36, 0.11], [0.52, 0.075], [0.64, 0.045]]) elips([hx + Math.cos(ka) * boy * q, hy + Math.sin(ka) * boy * q], boy * rr * 1.25, boy * rr, ka, POST_K);
  bacak('Left', POST_K); bacak('Right', POST); kol('Left', POST_K);
  elips([mx, my - L * 0.38], boy * 0.22, L * 0.5, aci, POST);           // tombul armut govde
  elips([mx, my + L * 0.3], boy * 0.27, L * 0.95, aci, POST);
  elips([mx, my - L * 0.38], boy * 0.22 - KON, L * 0.5 - KON, aci, POST, false);
  elips([mx, my + L * 0.35], boy * 0.16, L * 0.75, aci, KARIN);          // sari karin
  const dx_ = Math.cos(aci), dy_ = Math.sin(aci), ux_ = -dy_, uy_ = dx_;
  for (const q of [0.0, 0.3, 0.6, 0.9]) {                       // yatay karin plakasi cizgileri
    const cxq = mx + ux_ * L * (q - 0.35), cyq = my + uy_ * L * (q - 0.35);
    kapsul([cxq - dx_ * boy * 0.11, cyq - dy_ * boy * 0.11], [cxq + dx_ * boy * 0.11, cyq + dy_ * boy * 0.11], boy * 0.006, boy * 0.006, KARIN_S);
  }
  kol('Right', POST);
  elips([nx_ - boy * 0.1, ny_ + boy * 0.08], boy * 0.028, boy * 0.022, 0, DUDUK);
}
""")

# ------------------------------------------------------------------ OUT: camur birikintisi - camur sicramasi + ucusan damlalar
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 40: camur birikintisi - parlak koyu kahve camur sicramasi + damlalar
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(4343 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 16; j++) {                                // camur kabarciklari (yayilan halka)
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (140 + 220 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.5, r = (18 + 24 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r); g.addColorStop(0, '#c8783a'); g.addColorStop(0.5, '#7a3a12'); g.addColorStop(1, 'rgba(90,40,10,0.6)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  const SR = ['#6a2a0a', '#8a4a1a', '#5a2208', '#a0582a'];
  for (let j = 0; j < 26; j++) {                                // ucusan camur damlalari (parlak benekli)
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (320 + 420 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 760 * k * u * u, r = (5 + 8 * R2()) * k;
    cx.fillStyle = SR[j % 4]; cx.strokeStyle = '#2a1004'; cx.lineWidth = 1.5 * k;
    cx.beginPath(); cx.ellipse(x, y, r, r * 1.25, a, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,230,200,0.7)'; cx.beginPath(); cx.arc(x - r * 0.3, y - r * 0.35, r * 0.25, 0, 6.283); cx.fill();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: yosunlu tas blok + fosil kemik + mini yumurta
fonk("kule", r"""
function kule(t) {                                             // motor 40: hakem kursusu yosunlu sicak tas blok, onde capraz fosil kemik, yaninda mini yumurta
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#a8582a'); g.addColorStop(0.5, '#e0a060'); g.addColorStop(1, '#a04a1a');
  cx.fillStyle = g; cx.strokeStyle = '#4a2008'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#3ac81a'; cx.strokeStyle = '#0a5a14'; cx.lineWidth = 3 * k;                 // ustte yosun kapagi
  cx.beginPath(); cx.ellipse(xm, y0 + 4 * k, w * 0.48, 9 * k, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.strokeStyle = '#4a2008'; cx.fillStyle = '#fff0d0'; cx.lineWidth = 3 * k;                 // fosil kemik
  cx.save(); cx.translate(xm, y0 + h * 0.45); cx.rotate(-0.25);
  cx.beginPath(); cx.roundRect(-w * 0.3, -6 * k, w * 0.6, 12 * k, 6 * k); cx.fill(); cx.stroke();
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) { cx.beginPath(); cx.arc(sx * w * 0.3, sy * 7 * k, 10 * k, 0, 6.283); cx.fill(); cx.stroke(); }
  cx.restore();
  topCiz(xm + w * 0.5, y0 + h * 0.15, 22 * k, t, '#9a5aff', '#ffffff');
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 38: hakem kum tumseginin ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 40: hakem cim tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + volkan pufu + dev altin yumurta catlar, Baku firlar
fonk("patenOyma", r"""
function patenOyma(ua, t) {                                    // motor 40 acilis (ad 37 ile ayni): volkan duman pufu + dev altin yumurta sallanir, catlar, ikiye ayrilir
  const sil = kisit((ua - 0.75) / 0.2, 0, 1);
  if (sil >= 1) return;
  cx.save(); cx.globalAlpha = 1 - sil;
  const puf = kisit((ua - 0.02) / 0.5, 0, 1);                   // sol ustte volkan duman pufu (beyaz tombul bulutlar yukari buyur)
  if (puf > 0 && puf < 1) {
    for (let j = 0; j < 6; j++) {
      const q = kisit(puf * 1.3 - j * 0.08, 0, 1); if (q <= 0) continue;
      const x = W * (0.16 + 0.03 * Math.sin(j * 2.1)), y = H * (0.42 - q * 0.32 - j * 0.03), r = (40 + 30 * j) * k * (0.4 + q);
      cx.globalAlpha = (1 - sil) * (1 - q * 0.6);
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#c8c8d8'; cx.lineWidth = 4 * k;
      cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill(); cx.stroke();
    }
    cx.globalAlpha = 1 - sil;
  }
  const isik = kisit((ua - 0.38) / 0.25, 0, 1);                 // yumurtanin icinden isik patlamasi
  if (isik > 0) {
    const g = cx.createRadialGradient(W / 2, H * 0.62, 10 * k, W / 2, H * 0.62, W * 0.5 * isik);
    g.addColorStop(0, 'rgba(255,250,200,0.95)'); g.addColorStop(0.4, 'rgba(255,210,70,0.55)'); g.addColorStop(1, 'rgba(255,170,40,0)');
    cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  }
  const sal = ua < 0.35 ? Math.sin(ua * 60) * 0.12 * kisit(ua / 0.1, 0, 1) : 0;   // yumurta sallanir
  const ayr = ease(kisit((ua - 0.4) / 0.35, 0, 1));            // iki yari ayrilir
  const ex = W / 2, ey = H * 0.66, rx = 230 * k, ry = 300 * k, cat = ua > 0.28;
  const yari = (ust) => {
    cx.save(); cx.translate(ex + (ust ? -1 : 1) * ayr * W * 0.55, ey + (ust ? -1 : 1) * ayr * H * 0.35); cx.rotate(sal + (ust ? -1 : 1) * ayr * 0.8);
    cx.beginPath();
    if (ust) { cx.moveTo(-rx, -10 * k); cx.ellipse(0, 0, rx, ry, 0, Math.PI, 2 * Math.PI); cx.lineTo(rx, -10 * k); }
    else { cx.moveTo(rx, -10 * k); cx.ellipse(0, 0, rx, ry, 0, 0, Math.PI); cx.lineTo(-rx, -10 * k); }
    for (let q = 0; q <= 8; q++) { const i = ust ? 8 - q : q; cx.lineTo(-rx + i * rx * 2 / 8, (i % 2 ? 22 : -22) * k - 10 * k); }   // zikzak kirik kenar (ust: sagdan sola, alt: soldan saga)
    cx.closePath();
    const g = cx.createRadialGradient(-rx * 0.3, -ry * 0.4, rx * 0.1, 0, 0, ry * 1.1); g.addColorStop(0, '#fff8c0'); g.addColorStop(0.45, '#ffd23a'); g.addColorStop(1, '#e09a00');
    cx.fillStyle = g; cx.strokeStyle = '#6a3a00'; cx.lineWidth = 8 * k; cx.lineJoin = 'round'; cx.fill(); cx.stroke();
    cx.fillStyle = '#ffffff';                                   // beyaz benekler
    for (const [bx, by, br] of (ust ? [[-0.4, -0.5, 0.12], [0.3, -0.7, 0.09], [0.45, -0.25, 0.07]] : [[-0.3, 0.45, 0.1], [0.35, 0.3, 0.08]])) { cx.beginPath(); cx.arc(bx * rx, by * ry, br * rx, 0, 6.283); cx.fill(); }
    cx.restore();
  };
  if (!cat) {                                                   // butun yumurta (henuz catlamadi)
    cx.save(); cx.translate(ex, ey); cx.rotate(sal);
    const g = cx.createRadialGradient(-rx * 0.3, -ry * 0.4, rx * 0.1, 0, 0, ry * 1.1); g.addColorStop(0, '#fff8c0'); g.addColorStop(0.45, '#ffd23a'); g.addColorStop(1, '#e09a00');
    cx.fillStyle = g; cx.strokeStyle = '#6a3a00'; cx.lineWidth = 8 * k;
    cx.beginPath(); cx.ellipse(0, 0, rx, ry, 0, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffffff';
    for (const [bx, by, br] of [[-0.4, -0.5, 0.12], [0.3, -0.7, 0.09], [0.45, -0.25, 0.07], [-0.3, 0.45, 0.1], [0.35, 0.3, 0.08]]) { cx.beginPath(); cx.arc(bx * rx, by * ry, br * rx, 0, 6.283); cx.fill(); }
    const c = kisit((ua - 0.18) / 0.1, 0, 1);                   // catlak cizgisi buyur
    if (c > 0) { cx.strokeStyle = '#4a2a00'; cx.lineWidth = 6 * k; cx.beginPath(); cx.moveTo(-rx * c, -10 * k); for (let i = 0; i <= 8 * c; i++) cx.lineTo(-rx * c + i * rx * 2 * c / (8 * c || 1), (i % 2 ? 22 : -22) * k - 10 * k); cx.stroke(); }
    cx.restore();
  } else { yari(true); yari(false); }
  cx.restore();
  const R2 = rng(4344);                                         // catlarken ucusan kabuk kiriklari
  cx.save();
  for (let j = 0; j < 40; j++) {
    const q = ua - 0.3; if (q <= 0 || q > 0.6) continue;
    const a = 6.283 * R2(), v = (300 + 700 * R2()) * k, x = W / 2 + Math.cos(a) * v * q, y = H * 0.62 + Math.sin(a) * v * q * 0.7 + 600 * k * q * q, r = (6 + 10 * R2()) * k;
    cx.globalAlpha = kisit(1 - q / 0.6, 0, 1); cx.fillStyle = j % 2 ? '#ffd23a' : '#fff8c0'; cx.strokeStyle = '#6a3a00'; cx.lineWidth = 2 * k;
    cx.beginPath(); cx.moveTo(x - r, y); cx.lineTo(x, y - r * 0.8); cx.lineTo(x + r, y + r * 0.3); cx.closePath(); cx.fill(); cx.stroke();
  }
  cx.restore();
}
""")
degis("""  const cik = ease(kisit((ua - 0.25) / 0.6, 0, 1));             // motor 38: Fino tepenin arkasindan once kulaklariyla yukari cikar
  cx.save(); cx.translate(0, H * 0.45 * (1 - cik)); hakemCiz(t, null, 0); cx.restore();
  patenOyma(ua, t);""",
      """  const cik = ease(kisit((ua - 0.38) / 0.3, 0, 1));             // motor 40: Baku yumurta catlayinca icinden yukari firlar
  cx.save(); cx.translate(0, H * 0.35 * (1 - cik)); hakemCiz(t, null, 0); cx.restore();
  patenOyma(ua, t);""")
degis("c = ['#ffd23a', '#0ac8c8', '#ff2a8a', '#ffffff', '#ff7a1a', '#1a8aff'][Math.floor(R3() * 6)]",
      "c = ['#ffd23a', '#3ac81a', '#9a3aff', '#ffffff', '#ff7a1a', '#2ad8c8'][Math.floor(R3() * 6)]")   # dinozor vadisi konfeti (yaprak yesili + mor)
degis("// motor 38: solo (BLUE oyuncu)", "// motor 40: solo (PURPLE oyuncu)")
degis("  // mekan acilisi (41: col vahasi) - sahne kareKur'da zaten cizili", "  // mekan acilisi (43: dinozor vadisi) - sahne kareKur'da zaten cizili")

# ------------------------------------------------------------------ kepenk: Baku neon yuzu (kabuk sapka + iri goz + burun delikleri + disli gulumseme)
a = t.index("  for (const sx of [-1, 1]) { cx.beginPath(); cx.moveTo(mx + sx * r * 0.2, my - r * 0.75); cx.lineTo(mx + sx * r * 1.05, my - r * 2.1)")
b = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:a] + r"""  cx.beginPath(); cx.moveTo(mx - r * 0.95, my - r * 0.55);                                        // motor 40: Baku yumurta kabugu sapka (zikzak kenar + kubbe)
  for (let i = 0; i < 9; i++) cx.lineTo(mx - r * 0.95 + (i + 0.5) * r * 1.9 / 9, my - r * (i % 2 ? 0.62 : 0.45));
  cx.lineTo(mx + r * 0.95, my - r * 0.55); cx.ellipse(mx, my - r * 0.55, r * 0.95, r * 0.8, 0, 0, Math.PI, true); cx.closePath(); cx.stroke();
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.12, r * 0.24, r * 0.26, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my - r * 0.1, r * 0.1, r * 0.12, 0, 0, 6.283); cx.stroke(); }   // iri gozler
  for (const sx of [-1, 1]) { cx.beginPath(); cx.arc(mx + sx * r * 0.2, my + r * 0.3, r * 0.05, 0, 6.283); cx.stroke(); }   // burun delikleri
  cx.beginPath(); cx.ellipse(mx, my + r * 0.48, r * 0.38, r * 0.2, 0, 0.2, Math.PI - 0.2); cx.stroke();   // gulumseme
  for (const sx of [-0.2, 0, 0.2]) { cx.beginPath(); cx.moveTo(mx + sx * r - r * 0.05, my + r * 0.62); cx.lineTo(mx + sx * r, my + r * 0.52); cx.lineTo(mx + sx * r + r * 0.05, my + r * 0.62); cx.stroke(); }   // disler
""" + t[b:]

# ------------------------------------------------------------------ yazilar
degis("  satir([['1. WATCH FINO SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));", "  satir([['1. WATCH BAKU SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));")
degis("satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLDEN DUNE', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 38: yukleme notu sorusu",
      "satir([['CAN YOU HATCH THE ', KART_DOLGU], ['GOLDEN EGG', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 40: yukleme notu sorusu")
degis("  yaziK((kart.rutbe === 'GOLD' ? 'GOLDEN DUNE' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 38: altin kum tepesi",
      "  yaziK((kart.rutbe === 'GOLD' ? 'GOLDEN EGG' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 40: altin yumurta")
degis("  [['GOLDEN DUNE', '24 WALLS',", "  [['GOLDEN EGG', '24 WALLS',")
degis("// motor 38: GOLDEN DUNE 24 WALLS'a yapisiyordu", "// motor 38: uzun rutbe adi (GOLDEN EGG) 24 WALLS'a yapismasin")
kod = t.split("// --- motor 38 aciklamasi ---")[1]
gov = re.sub(r"//.*", "", kod)
for kalan in ("FINO", "DUNE", "Fino"):
    assert kalan not in gov, kalan
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
