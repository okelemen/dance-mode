"""MOTOR 38 (HUMAN TETRIS 41) = sahne37.html (motor 37, 40. video: 1P SOLO donmus gol) + yama -> 03-motor/sahne38.html.
sahne37 degismez.

    python motor38-yama.py

41: REF-093 yapi (1P SOLO), gunduz col vahasi (varlik-col.py), ozel tur SPEED (motor 33'ten beri d.hiz; FASTER!),
yarisan karakter TEK sporcu (BLUE, karakter.py --sporcu 1 --renk 2E9BFF), hakem maskot col tilkisi (fennek) yavrusu FINO - TAMAMI 2B:
govde + kuyruk + pati + bas (dev kulak) + turkuaz bandana + duduk; hareket karakter.py --eklem 1 verisinden. Cizim maskot-ornek-41.py ile birebir.
OUT = kum tepesinden asagi yuvarlanir: kum pufu + ucusan kum taneleri. Ekranda kar yerine suzulen altin kum pariltisi.
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (ruzgar dev kum tepesini yana
kaydirir, kum tanecikleri savrulur, altindan altin isik + soru; Fino once kulaklariyla tepenin arkasindan cikar) -> CAN YOU WIN THE
GOLDEN DUNE? ; ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne37.html")
HEDEF = os.path.join(BURA, "..", "sahne38.html")
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
t = t[:m.start()] + "<title>HUMAN TETRIS 41 - motor 38 (col vahasi, 1P SOLO, SPEED, 2B fennek Fino, kum tepesi girisi)</title>" + t[m.end():]
degis("// MOTOR 37 — HUMAN TETRIS 40", "// MOTOR 38 — HUMAN TETRIS 41 (REF-093 yapi, 27 Kas 2026; motor 37'den, tetris-pvp/motor38-yama.py):\n"
      "//   - 1P SOLO: tek sporcu (BLUE); SPEED ROUND (d.hiz, FASTER!)\n"
      "//   - sahne: tetris-pvp/varlik-col.py (gunduz col vahasi); ekranda suzulen altin kum pariltisi\n"
      "//   - hakem fennek FINO, TAMAMI 2B: eklem verisinden govde + kuyruk + pati + bas + bandana (maskot-ornek-41.py ile ayni); kumtasi kursu + kum tumsegi\n"
      "//   - OUT kum tepesi (kum pufu + kum taneleri); giris kanca -> ruzgar kum tepesini kaydirir -> CAN YOU WIN THE GOLDEN DUNE?\n"
      "// --- motor 37 aciklamasi ---\n"
      "// MOTOR 37 — HUMAN TETRIS 40")

# ------------------------------------------------------------------ mini kaktus (top yerine) + kum tumsegi + suzulen kum pariltisi
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#1aa84a', c2 = '#ff2a9a') {   // motor 38: mini kaktus (tombul yesil govde + iki kol + pembe cicek); imza 37 ile ayni
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.06);
  cx.lineWidth = Math.max(1.5, r * 0.1); cx.strokeStyle = '#0a3a14'; cx.lineJoin = 'round';
  const g = cx.createLinearGradient(-r, 0, r, 0); g.addColorStop(0, '#0a8a3a'); g.addColorStop(0.45, '#3ad86a'); g.addColorStop(1, '#0a8a3a');
  cx.fillStyle = g;
  cx.beginPath(); cx.roundRect(-r * 0.42, -r * 1.3, r * 0.84, r * 2.1, r * 0.42); cx.fill(); cx.stroke();          // govde
  for (const s of [-1, 1]) {                                      // kollar
    cx.beginPath(); cx.roundRect(s > 0 ? r * 0.3 : -r * 0.9, -r * 0.1, r * 0.6, r * 0.34, r * 0.17); cx.fill(); cx.stroke();
    cx.beginPath(); cx.roundRect(s > 0 ? r * 0.62 : -r * 0.9, -r * 0.75, r * 0.3, r * 0.8, r * 0.15); cx.fill(); cx.stroke();
  }
  cx.fillStyle = c2; cx.beginPath(); cx.arc(0, -r * 1.36, r * 0.22, 0, 6.283); cx.fill(); cx.stroke();          // cicek
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 38: altin kum tumsegi + iki mini kaktus (hakemin ayak alti)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.4); g.addColorStop(0, '#ffd87a'); g.addColorStop(1, '#f08a1a');
  cx.fillStyle = g; cx.strokeStyle = '#7a3a08'; cx.lineWidth = Math.max(1.5, r * 0.06);
  cx.beginPath(); cx.moveTo(-r * 1.5, r * 0.2);
  cx.quadraticCurveTo(-r * 0.7, -r * 0.55, 0, -r * 0.45); cx.quadraticCurveTo(r * 0.8, -r * 0.4, r * 1.5, r * 0.2);
  cx.quadraticCurveTo(0, r * 0.5, -r * 1.5, r * 0.2); cx.closePath(); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(200,100,10,0.6)'; cx.lineWidth = Math.max(1, r * 0.03);           // ruzgar dalgaciklari
  for (const dy of [-0.15, 0.05]) { cx.beginPath(); cx.moveTo(-r * 0.9, dy * r); cx.quadraticCurveTo(0, (dy - 0.12) * r, r * 0.9, dy * r); cx.stroke(); }
  cx.restore();
  topCiz(x - r * 1.15, y - r * 0.15, r * 0.24, 0);
  topCiz(x + r * 1.2, y - r * 0.1, r * 0.2, 0, '#1aa84a', '#ffd23a');
}
""")
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 38: suzulen altin kum pariltisi (yana ruzgarla) + yer yer parlayan yildizcik; imza 37 ile ayni
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j++) {
    const p = KAR_T[j];
    const x = ((p.x + t * p.v * 0.25 + 1) % 1) * W, y = ((p.y + Math.sin(t * 0.8 + p.f) * 0.02) % 1) * H * 0.95;
    if (j % 7 === 0) {
      const r = (p.r * 2 + 6) * k * (0.6 + 0.5 * Math.abs(Math.sin(t * 3 + p.f)));
      cx.save(); cx.translate(x, y * 0.6); cx.shadowColor = '#fff0a0'; cx.shadowBlur = 12 * k; cx.fillStyle = '#fff6c8';
      cx.beginPath(); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, rr = i % 2 ? r * 0.25 : r; cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } cx.closePath(); cx.fill(); cx.restore();
    } else if (j % 3 === 0) {                                   // kum taneleri: kucuk sicak altin nokta (seyrek; ekran kalabalik olmaz)
      const r = (p.r * 0.45 + 1) * k;
      cx.fillStyle = 'rgba(255,214,120,' + (0.45 + 0.4 * p.a) + ')'; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
    }
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ FINO (tamami 2B): maskot-ornek-41.py (bas + govde) ile ayni
fonk("pipBas", r"""
function pipBas(u, duygu, t) {                                  // motor 38: Fino'nun basi (maskot-ornek-41.bas, on gorunum), merkez (0,0), birim u
  const KN = '#3a1a08', POST = '#fff0d2', KARIN = '#ffffff', KULAK_I = '#ffa8b0', YANAK = '#ff7a9a', CIZGI = '#9a5a20';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const yay = (x, y, rx, ry, a0, a1, w) => { cx.strokeStyle = KN; cx.lineWidth = w * u; cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, a0 * Math.PI / 180, a1 * Math.PI / 180); cx.stroke(); };
  const cizgi = (x0, y0, x1, y1, renk, w) => { cx.strokeStyle = renk; cx.lineWidth = w * u; cx.beginPath(); cx.moveTo(x0 * u, y0 * u); cx.lineTo(x1 * u, y1 * u); cx.stroke(); };
  const poli = (pts, f, s, w) => { cx.beginPath(); pts.forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.closePath(); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  const oyna = Math.sin(t * 5) * 1.5;                           // kulaklar hafif oynar (imza: kulak oynatip el sallar)
  for (const sx of [-1, 1]) {                                   // dev sivri kulak: dis post + ic pembe
    const kx = sx * 12, ky = -9, ux = sx * 27 + oyna * sx, uy = -56, gen = 13;
    poli([[kx - gen, ky], [ux, uy], [kx + gen, ky]], POST, KN, 1.6);
    poli([[kx - gen * 0.55, ky - 1], [ux * 0.85 + kx * 0.15, uy * 0.85 + ky * 0.15], [kx + gen * 0.55, ky - 1]], KULAK_I);
  }
  el(0, 0, 23, 20, POST, KN, 1.6);                              // yuvarlak bas
  poli([[-14, 2], [0, -6], [14, 2], [9, 17], [0, 20], [-9, 17]], KARIN);   // beyaz yuz maskesi
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') yay(sx * 9, -3, 5.5, 5.5, 200, 340, 2.6);
    else if (duygu === 'sasirma') { el(sx * 9, -4, 6.5, 7.5, '#ffffff', KN, 1.4); el(sx * 9, -4, 2.6, 2.8, KN); }
    else { el(sx * 9, -3, 6.2, 7.2, '#ffffff', KN, 1.4); el(sx * 9 + 0.7, -2.4, 4.2, 5.0, KN); el(sx * 9 - 0.8, -4.8, 1.6, 1.6, '#ffffff'); }
    cizgi(sx * 5, 3, sx * 3.5, 9, CIZGI, 1.1);                    // fennek goz cizgisi
    el(sx * 16, 6, 3.6, 2.2, YANAK);
    for (const dy of [-1.0, 1.5]) cizgi(sx * 6, 12 + dy, sx * 21, 10 + dy * 2.4, KN, 0.7);   // biyiklar
  }
  el(0, 10.5, 3.4, 2.6, '#101018');                              // kucuk siyah burun
  if (duygu === 'sasirma') el(0, 16, 3.0, 2.8, '#7a1020', KN, 1.0);
  else if (duygu === 'sevinc') { cx.beginPath(); cx.ellipse(0, 16 * u, 6 * u, 4 * u, 0, 0, Math.PI); cx.closePath(); cx.fillStyle = '#7a1020'; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.2 * u; cx.stroke(); }
  else { yay(-2.15, 13.5, 2.35, 2.5, 0, 160, 1.3); yay(2.15, 13.5, 2.35, 2.5, 20, 180, 1.3); }
}
""")
fonk("pipGovde", r"""
function pipGovde(E, P, boy) {                                  // motor 38: Fino govdesi 2B (maskot-ornek-41.govde_ciz, on gorunum)
  const KN = '#3a1a08', POST = '#fff0d2', POST_K = '#f0b878', KARIN = '#ffffff', KUYRUK_U = '#4a2410';
  const ATKI = '#0ab8b0', ATKI_K = '#06807a', ATKI_D = '#ffd84a', DUDUK = '#ffc21a';
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
  const pati = (m, aci, rx, ry, renk) => elips(m, rx * 0.6, ry * 0.85, aci, renk);   // kucuk yuvarlak pati
  const ru = boy * 0.1, rl = boy * 0.088, ra = boy * 0.08, rf = boy * 0.072;
  const bacak = (t_, renk) => {
    uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.05], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 1.05, rl]], renk);
    const f = g(t_ + 'Foot'), fu = g(t_ + 'Foot_uc');
    pati([(f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2], Math.atan2(fu[1] - f[1], fu[0] - f[0]), boy * 0.12, boy * 0.07, renk);
  };
  const kol = (t_, renk) => {
    uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra, rf * 1.05], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 1.05, rf]], renk);
    const h = g(t_ + 'Hand'), hu = g(t_ + 'Hand_uc');
    pati([h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9], Math.atan2(hu[1] - h[1], hu[0] - h[0]), boy * 0.12, boy * 0.068, renk);
  };
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.72 + nx_ * 0.28, my = hy * 0.72 + ny_ * 0.28;
  const ka = Math.atan2(boy * 0.25, boy * 0.32), km = [hx + boy * 0.26, hy + boy * 0.16];   // gur kuyruk + koyu uc (fennek imzasi)
  elips(km, boy * 0.2, boy * 0.085, ka, POST);
  elips([km[0] + Math.cos(ka) * boy * 0.16, km[1] + Math.sin(ka) * boy * 0.16], boy * 0.065, boy * 0.06, ka, KUYRUK_U, false);
  bacak('Left', POST_K); bacak('Right', POST_K); kol('Left', POST_K);   // arka uzuvlar golge tonu
  elips([mx, my - L * 0.38], boy * 0.22, L * 0.5, aci, POST);           // tombul damla govde (foktan ince: bacaklar gorunur)
  elips([mx, my + L * 0.3], boy * 0.27, L * 0.95, aci, POST);
  elips([mx, my - L * 0.38], boy * 0.22 - KON, L * 0.5 - KON, aci, POST, false);
  elips([mx, my + L * 0.35], boy * 0.16, L * 0.75, aci, KARIN);          // karin
  kol('Right', POST);
  elips([nx_, ny_ + boy * 0.01], boy * 0.15, boy * 0.045, aci, ATKI);   // turkuaz bandana + altin benek
  for (let kk = -3; kk <= 3; kk++) elips([nx_ + kk * boy * 0.035, ny_ + boy * 0.01], boy * 0.009, boy * 0.009, 0, ATKI_D, false);
  const ox = nx_ + boy * 0.06;
  kapsulK([ox, ny_ + boy * 0.03], [ox + boy * 0.015, ny_ + boy * 0.2], boy * 0.035, boy * 0.032, ATKI);   // sarkan uc
  for (const j of [0.08, 0.14]) kapsul([ox - boy * 0.025, ny_ + boy * j], [ox + boy * 0.045, ny_ + boy * j], boy * 0.008, boy * 0.008, ATKI_D);
  for (const kk of [-1, 0, 1]) kapsul([ox + boy * 0.015 + kk * boy * 0.02, ny_ + boy * 0.23], [ox + boy * 0.015 + kk * boy * 0.024, ny_ + boy * 0.26], boy * 0.006, boy * 0.006, ATKI_K);
  elips([nx_ - boy * 0.1, ny_ + boy * 0.08], boy * 0.028, boy * 0.022, 0, DUDUK);
}
""")

# ------------------------------------------------------------------ OUT: kum tepesi - kum pufu + ucusan kum taneleri
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 38: kum tepesi - kum pufu + ucusan kum taneleri
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(4141 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 22; j++) {                                // kum pufu
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (160 + 260 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.6, r = (22 + 28 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.addColorStop(0, '#ffe8a8'); g.addColorStop(0.6, '#ffc860'); g.addColorStop(1, 'rgba(240,140,30,0.45)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  const SR = ['#ffd84a', '#ffb02a', '#fff0b0', '#f08a1a'];
  for (let j = 0; j < 28; j++) {                                // ucusan kum taneleri
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (300 + 400 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 700 * k * u * u, r = (4 + 6 * R2()) * k;
    cx.fillStyle = SR[j % 4]; cx.strokeStyle = '#7a3a08'; cx.lineWidth = 1.5 * k;
    cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill(); cx.stroke();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: kumtasi blok + turkuaz mozaik + mini kaktus
fonk("kule", r"""
function kule(t) {                                             // motor 38: hakem kursusu kumtasi blok, onde turkuaz mozaik serit, yaninda mini kaktus
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#d0602a'); g.addColorStop(0.5, '#f2a04a'); g.addColorStop(1, '#c0501a');
  cx.fillStyle = g; cx.strokeStyle = '#5a2008'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  for (let i = 0; i < 5; i++) {                                 // turkuaz / altin mozaik kareler
    cx.fillStyle = ['#0ac8c8', '#ffc81a'][i % 2]; cx.beginPath(); cx.roundRect(xm - w * 0.4 + i * w * 0.18, y0 + h * 0.3, w * 0.12, w * 0.12, 3 * k); cx.fill(); cx.lineWidth = 3 * k; cx.stroke();
  }
  topCiz(xm + w * 0.5, y0 + h * 0.15, 20 * k, t);
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 37: hakem kar tumseginin ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 38: hakem kum tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + ruzgar dev kum tepesini kaydirir, altindan isik; Fino kulaklariyla cikar
fonk("patenOyma", r"""
function patenOyma(ua, t) {                                    // motor 38 acilis (ad 37 ile ayni): ruzgar dev kum tepesini saga kaydirir, kum savrulur, altindan altin isik
  const kay = ease(kisit((ua - 0.15) / 0.6, 0, 1)), sil = kisit((ua - 0.7) / 0.25, 0, 1);
  if (sil >= 1) return;
  cx.save(); cx.globalAlpha = 1 - sil;
  const isik = kisit((ua - 0.3) / 0.4, 0, 1);                   // tepenin altindan yukselen altin isik huzmesi
  if (isik > 0) {
    const g = cx.createRadialGradient(W / 2, H * 0.62, 10 * k, W / 2, H * 0.62, W * 0.45 * isik);
    g.addColorStop(0, 'rgba(255,246,190,0.95)'); g.addColorStop(0.4, 'rgba(255,200,70,0.55)'); g.addColorStop(1, 'rgba(255,170,40,0)');
    cx.fillStyle = g; cx.fillRect(0, 0, W, H);
  }
  const dx = kay * W * 0.95;                                    // dev kum tepesi (ekranin alt yarisi), saga kayar
  const g2 = cx.createLinearGradient(0, H * 0.4, 0, H); g2.addColorStop(0, '#ffd27a'); g2.addColorStop(0.5, '#ffb03a'); g2.addColorStop(1, '#e0781a');
  cx.fillStyle = g2; cx.strokeStyle = '#7a3a08'; cx.lineWidth = 8 * k; cx.lineJoin = 'round';
  cx.beginPath(); cx.moveTo(-W * 0.1 + dx, H + 20 * k);
  cx.bezierCurveTo(W * 0.15 + dx, H * 0.45, W * 0.55 + dx, H * 0.35, W * 0.8 + dx, H * 0.55);
  cx.bezierCurveTo(W * 0.95 + dx, H * 0.65, W * 1.1 + dx, H * 0.8, W * 1.2 + dx, H + 20 * k);
  cx.closePath(); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(190,90,10,0.55)'; cx.lineWidth = 5 * k;            // ruzgar dalgaciklari
  for (let i = 0; i < 5; i++) { const y = H * (0.62 + i * 0.07); cx.beginPath(); cx.moveTo(W * 0.1 + dx, y); cx.quadraticCurveTo(W * 0.5 + dx, y - 30 * k, W * 0.95 + dx, y + 10 * k); cx.stroke(); }
  cx.restore();
  const R2 = rng(4142);                                         // ruzgarla savrulan kum tanecikleri + ruzgar cizgileri
  cx.save();
  for (let j = 0; j < 90; j++) {
    const t0 = 0.6 * R2(), q = ua - 0.1 - t0; if (q <= 0 || q > 0.8) continue;
    const x = W * (0.05 + 0.6 * R2()) + q * W * 1.3, y = H * (0.35 + 0.5 * R2()) - q * 120 * k * R2(), r = (3 + 6 * R2()) * k;
    cx.globalAlpha = kisit(1.1 - q / 0.7, 0, 1); cx.fillStyle = j % 3 ? '#ffd84a' : '#fff0b0';
    cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  cx.strokeStyle = 'rgba(255,255,255,0.75)'; cx.lineWidth = 5 * k; cx.lineCap = 'round';
  for (let j = 0; j < 8; j++) {
    const q = kisit((ua - 0.05 - j * 0.04) / 0.5, 0, 1); if (q <= 0 || q >= 1) continue;
    const y = H * (0.2 + j * 0.07), x = -W * 0.2 + q * W * 1.4;
    cx.globalAlpha = Math.sin(q * Math.PI) * 0.8; cx.beginPath(); cx.moveTo(x - 240 * k, y); cx.quadraticCurveTo(x - 80 * k, y - 18 * k, x, y); cx.stroke();
  }
  cx.restore();
}
""")
degis("""  const kay = ease(kisit((ua - 0.2) / 0.7, 0, 1));             // motor 37: Lumi soldan buzda kayarak ortaya gelir
  cx.save(); cx.translate(-W * 0.6 * (1 - kay), 0); hakemCiz(t, null, 0); cx.restore();
  patenOyma(ua, t);""",
      """  const cik = ease(kisit((ua - 0.25) / 0.6, 0, 1));             // motor 38: Fino tepenin arkasindan once kulaklariyla yukari cikar
  cx.save(); cx.translate(0, H * 0.45 * (1 - cik)); hakemCiz(t, null, 0); cx.restore();
  patenOyma(ua, t);""")
degis("c = ['#ff1a2a', '#18a848', '#ffd23a', '#ffffff', '#7ad0ff', '#3aa8ff'][Math.floor(R3() * 6)]",
      "c = ['#ffd23a', '#0ac8c8', '#ff2a8a', '#ffffff', '#ff7a1a', '#1a8aff'][Math.floor(R3() * 6)]")   # col vahasi renkli konfeti
degis("// motor 37: solo (RED oyuncu)", "// motor 38: solo (BLUE oyuncu)")
degis("  // mekan acilisi (40: donmus gol) - sahne kareKur'da zaten cizili", "  // mekan acilisi (41: col vahasi) - sahne kareKur'da zaten cizili")

# ------------------------------------------------------------------ kepenk: Fino neon yuzu (dev kulak + iri goz + burun + biyik)
a = t.index("  cx.beginPath(); cx.ellipse(mx, my - r * 0.9, r * 0.78, r * 0.6, 0, Math.PI, 2 * Math.PI); cx.closePath(); cx.stroke();   // motor 37: Lumi bere")
b = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:a] + r"""  for (const sx of [-1, 1]) { cx.beginPath(); cx.moveTo(mx + sx * r * 0.2, my - r * 0.75); cx.lineTo(mx + sx * r * 1.05, my - r * 2.1); cx.lineTo(mx + sx * r * 0.85, my - r * 0.45); cx.closePath(); cx.stroke(); }   // motor 38: Fino dev kulaklar
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.1, r * 0.24, r * 0.28, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my - r * 0.06, r * 0.1, r * 0.12, 0, 0, 6.283); cx.stroke(); }   // iri gozler
  for (const sx of [-1, 1]) for (const dy of [-0.06, 0.08]) { cx.beginPath(); cx.moveTo(mx + sx * r * 0.25, my + r * (0.5 + dy)); cx.lineTo(mx + sx * r * 0.92, my + r * (0.42 + dy * 3)); cx.stroke(); }   // biyiklar
  cx.beginPath(); cx.ellipse(mx, my + r * 0.45, r * 0.14, r * 0.1, 0, 0, 6.283); cx.stroke();   // burun
""" + t[b:]

# ------------------------------------------------------------------ yazilar
degis("  satir([['1. WATCH LUMI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));", "  satir([['1. WATCH FINO SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));")
degis("satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLDEN SKATE', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 37: yukleme notu sorusu",
      "satir([['CAN YOU WIN THE ', KART_DOLGU], ['GOLDEN DUNE', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 38: yukleme notu sorusu")
degis("  yaziK((kart.rutbe === 'GOLD' ? 'GOLDEN SKATE' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 37: altin paten",
      "  yaziK((kart.rutbe === 'GOLD' ? 'GOLDEN DUNE' : kart.rutbe) + '!', W / 2, H * 0.45, 110 * k * s, dol, 1);   // motor 38: altin kum tepesi")
degis("  [['GOLDEN SKATE', '24 WALLS',", "  [['GOLDEN DUNE', '24 WALLS',")
kod = t.split("// --- motor 37 aciklamasi ---")[1]
for kalan in ("LUMI", "SKATE"):
    gov = re.sub(r"//.*", "", kod)
    assert kalan not in gov, kalan
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
