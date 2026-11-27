"""MOTOR 39 (HUMAN TETRIS 42) = sahne34.html (motor 34, 37. video: 1v1 ucan gokyuzu adalari) + yama -> 03-motor/sahne39.html.
sahne34 degismez.

    python motor39-yama.py

42: REF-094 yapi (1v1), gunduz korsan gemisi guvertesi (varlik-gemi.py), ozel tur FREEZE (motor 22'den beri Z.tut; FREEZE! + tutma cubugu).
Yarisan karakterler iki sporcu (BLUE sol / PINK sag, karakter.py --sporcu 1). Hakem maskot papagan yavrusu PAKO - TAMAMI 2B
(38-41 yontemi): govde + kanat tuyleri + kuyruk tuyleri + pence + bas (tepelik, kanca gaga, uc koseli korsan sapkasi, kurukafa yok) + duduk;
hareket karakter.py --eklem 1 verisinden. Cizim maskot-ornek-42.py ile birebir.
OUT = tahtadan denize duser: turkuaz-beyaz su sicramasi + halka. Hakem kursusu ahsap sandik + altin sikkeler + iki fener; basamak can simidi.
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis: dev kirmizi-sari serit yelken
katman katman iner (prompts.chat "Black Sails" katmanli acilis fikri), iki yana aralanir; Pako direkten suzulup kursuye konar;
martilar + altin sikkeler ucusur -> WHO WILL WIN THE TREASURE? / BLUE OR PINK? ; ilk duvar <= 5 sn.
Sonuc kartinda kazananin yaninda hazine sandigi acilir (yukleme notu: "most points wins the treasure").
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne34.html")
HEDEF = os.path.join(BURA, "..", "sahne39.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def satir_degis(icerir, yeni):
    """'icerir' gecen TEK satiri tamamen 'yeni' ile degistirir"""
    global t
    L = t.split("\n"); idx = [i for i, s in enumerate(L) if icerir in s]
    assert len(idx) == 1, (len(idx), icerir[:80])
    L[idx[0]] = yeni; t = "\n".join(L)


def govdesi(kaynak, ad):
    m = re.search(r"^function %s\(" % re.escape(ad), kaynak, re.M)
    assert m, ad
    return kaynak[m.start():kaynak.index("\n}\n", m.start()) + 3]


def fonk(ad, yeni):
    global t
    eski = govdesi(t, ad)
    t = t.replace(eski, yeni.strip("\n") + "\n")


m = re.search(r"<title>.*?</title>", t)
t = t[:m.start()] + "<title>HUMAN TETRIS 42 - motor 39 (iki serit korsan gemisi guvertesi, FREEZE turu, 2B papagan Pako, yelken girisi)</title>" + t[m.end():]
degis("// MOTOR 34 — HUMAN TETRIS 37", "// MOTOR 39 — HUMAN TETRIS 42 (REF-094 yapi, 28 Kas 2026; motor 34'ten, tetris-pvp/motor39-yama.py):\n"
      "//   - 1v1: BLUE sol / PINK sag sporcu; FREEZE ROUND (Z.tut, FREEZE! + tutma cubugu)\n"
      "//   - sahne: tetris-pvp/varlik-gemi.py (gunduz korsan gemisi guvertesi); OUT tahtadan denize (su sicramasi)\n"
      "//   - hakem papagan PAKO, TAMAMI 2B: eklem verisinden govde + kanat + kuyruk + pence + bas + korsan sapkasi (maskot-ornek-42.py ile ayni)\n"
      "//   - hakem kursusu ahsap sandik + altin sikke + iki fener; giris kanca -> serit yelken katman katman iner, aralanir -> WHO WILL WIN THE TREASURE?\n"
      "//   - sonuc karti: kazananin yaninda hazine sandigi acilir\n"
      "// --- motor 34 aciklamasi ---\n"
      "// MOTOR 34 — HUMAN TETRIS 37")

# ------------------------------------------------------------------ renkler: ucusan altin sikke + bayrak kagitlari
satir_degis("const KONF_R = ['#ff3aa8', '#ffd21e', '#2fd04a', '#7ad0ff', '#a040ff', '#ff7a14'];",
            "const KONF_R = ['#ffd21e', '#ff1e3c', '#2fd04a', '#7ad0ff', '#ffb21a', '#ff7a14'];   // motor 39: altin sikke + bayrak kagitlari")

# ------------------------------------------------------------------ basamak: can simidi (kirmizi-beyaz)
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 39: kirmizi-beyaz can simidi (maskotun basamagi; korsan gemisi)
  cx.save(); cx.translate(x, y); cx.scale(1, 0.42);
  cx.lineWidth = r * 0.62; cx.strokeStyle = '#3a0a08'; cx.beginPath(); cx.arc(0, 0, r * 1.05, 0, 6.283); cx.stroke();
  cx.lineWidth = r * 0.5; cx.strokeStyle = '#ff1e2a'; cx.beginPath(); cx.arc(0, 0, r * 1.05, 0, 6.283); cx.stroke();
  cx.strokeStyle = '#fff2dc'; for (let q = 0; q < 4; q++) { const a = q * Math.PI / 2 + Math.PI / 4; cx.beginPath(); cx.arc(0, 0, r * 1.05, a - 0.3, a + 0.3); cx.stroke(); }
  cx.lineWidth = r * 0.1; cx.strokeStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.arc(0, 0, r * 1.2, 3.6, 4.6); cx.stroke();
  cx.restore();
}
""")

# ------------------------------------------------------------------ PAKO: tamami 2B (maskot-ornek-42.py bas / govde_ciz ile birebir)
PAKO = r"""
function pipBas(u, duygu, t) {                                  // motor 39: Pako'nun basi (maskot-ornek-42.bas, on gorunum), merkez (0,0), birim u
  const KN = '#1e2a10', POST = '#3fd14a', TEPE = '#ff6a1a', TEPE_K = '#e8361a', GAGA_U = '#ffb21a', GAGA_A = '#4a2a10', SAPKA = '#6a3a1a', SAPKA_S = '#ffd23a';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const poli = (pts, f, s, w) => { cx.beginPath(); pts.forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.closePath(); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  const oyna = Math.sin(t * 6) * 1.5;                           // tepelik hafif sallanir
  [[-9, -44, -17], [0, -50, -2], [9, -43, 13]].forEach(([dx, uy, ux], i) => poli([[dx - 5, -16], [ux + oyna, uy], [dx + 5, -16]], i === 1 ? TEPE_K : TEPE, KN, 1.2));
  el(0, 0, 22, 20, POST, KN, 1.6);                              // yuvarlak bas
  poli([[-28, -9], [-23, -25], [-11, -33], [0, -28], [11, -33], [23, -25], [28, -9], [14, -15], [0, -12], [-14, -15]], SAPKA, KN, 1.4);   // korsan sapkasi
  cx.strokeStyle = SAPKA_S; cx.lineWidth = 2.0 * u; cx.beginPath();
  [[-26, -11], [-14, -17], [0, -14.5], [14, -17], [26, -11]].forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.stroke();
  el(0, -22, 3.6, 3.6, SAPKA_S, KN, 0.9);                       // altin rozet
  for (const sx of [-1, 1]) {
    el(sx * 9, -4, 8.2, 8.6, '#ffffff', KN, 1.0);               // beyaz goz halkasi
    if (duygu === 'sevinc') { cx.strokeStyle = KN; cx.lineWidth = 2.6 * u; cx.beginPath(); cx.arc(sx * 9 * u, -4 * u, 5.2 * u, 200 * Math.PI / 180, 340 * Math.PI / 180); cx.stroke(); }
    else if (duygu === 'sasirma') el(sx * 9, -4, 2.4, 2.6, '#101018');
    else { el(sx * 9 + 0.6, -3.6, 4.6, 5.4, '#101018'); el(sx * 9 - 0.9, -6.0, 1.7, 1.7, '#ffffff'); }
    el(sx * 16, 6, 3.4, 2.1, '#ff7a6a');
  }
  if (duygu === 'sasirma' || duygu === 'sevinc') { cx.beginPath(); cx.ellipse(0, 16 * u, 6 * u, 7 * u, 0, 0, Math.PI); cx.closePath(); cx.fillStyle = GAGA_A; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = 1.1 * u; cx.stroke(); }
  poli([[-8, 4], [0, 1], [8, 4], [6, 12], [0, 19], [-6, 12]], GAGA_U, KN, 1.3);   // kalin kivrik kanca gaga
  cx.strokeStyle = '#d88a10'; cx.lineWidth = 0.9 * u; cx.beginPath(); cx.moveTo(0, 5 * u); cx.lineTo(0, 15 * u); cx.stroke();
}
const PIP_OLCEK = Number(TEMA.pipOlcek || 2.5), PIP_DY = Number(TEMA.pipDy || -8);   // maskot-ornek-42.py OLCEK / DY
function pipGovde(E, P, boy) {                                  // motor 39: Pako govdesi 2B (maskot-ornek-42.govde_ciz, on gorunum)
  const KN = '#1e2a10', POST = '#3fd14a', POST_K = '#22a83a', KARIN = '#ffe04a', KANAT_U = '#ffcc1a', GAGA_U = '#ffb21a', DUDUK = '#ffc21a';
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
  function yelpaze(m, aci, rx, ry, renk, uc = false) {          // kanat ucu tuy yelpazesi / pence
    elips(m, rx * 0.6, ry * 0.85, aci, renk);
    if (uc) for (const q of [-1, 0, 1]) elips([m[0] + Math.cos(aci + q * 0.35) * rx * 0.55, m[1] + Math.sin(aci + q * 0.35) * rx * 0.55], rx * 0.32, ry * 0.32, aci + q * 0.35, KANAT_U);
  }
  const ru = boy * 0.1, rl = boy * 0.088, ra = boy * 0.08, rf = boy * 0.072;
  const [hx, hy] = g('Hips'), [nx_, ny_] = g('Neck');
  const bacak = (t_, renk) => {
    uzuv([[g(t_ + 'UpLeg'), g(t_ + 'Leg'), ru, rl * 1.05], [g(t_ + 'Leg'), g(t_ + 'Foot'), rl * 0.6, rl * 0.5, GAGA_U]], renk);
    const f = g(t_ + 'Foot'), fu = g(t_ + 'Foot_uc');
    yelpaze([(f[0] + fu[0]) / 2, (f[1] + fu[1]) / 2], Math.atan2(fu[1] - f[1], fu[0] - f[0]), boy * 0.11, boy * 0.06, GAGA_U);
  };
  const kol = (t_, renk) => {
    const a_ = g(t_ + 'Arm'), h_ = g(t_ + 'Hand'), dx = h_[0] - a_[0], dy = h_[1] - a_[1], L_ = Math.hypot(dx, dy) || 1;
    let nx = -dy / L_, ny = dx / L_; const mx0 = (a_[0] + h_[0]) / 2 - hx;
    if (nx * mx0 + ny * 0.3 * Math.abs(mx0 || 1) < 0) { nx = -nx; ny = -ny; }   // kanat tuyleri govdeden DISA sarkar
    const fa = Math.atan2(ny, nx);
    for (const q of [0.3, 0.5, 0.7, 0.9]) {
      const fm = [a_[0] + dx * q + nx * boy * 0.1, a_[1] + dy * q + ny * boy * 0.1];
      elips(fm, boy * 0.11, boy * 0.04, fa, POST_K);
      elips([fm[0] + nx * boy * 0.085, fm[1] + ny * boy * 0.085], boy * 0.04, boy * 0.03, fa, KANAT_U, false);
    }
    uzuv([[g(t_ + 'Arm'), g(t_ + 'ForeArm'), ra, rf * 1.05], [g(t_ + 'ForeArm'), g(t_ + 'Hand'), rf * 1.05, rf]], renk);
    const h = g(t_ + 'Hand'), hu = g(t_ + 'Hand_uc');
    yelpaze([h[0] + (hu[0] - h[0]) * 0.9, h[1] + (hu[1] - h[1]) * 0.9], Math.atan2(hu[1] - h[1], hu[0] - h[0]), boy * 0.13, boy * 0.07, renk, true);
  };
  const aci = Math.atan2(ny_ - hy, nx_ - hx) + Math.PI / 2, L = Math.hypot(nx_ - hx, ny_ - hy);
  const mx = hx * 0.72 + nx_ * 0.28, my = hy * 0.72 + ny_ * 0.28;
  for (const [q, uz] of [[-0.35, 0.34], [0, 0.42], [0.35, 0.34]]) {   // uzun sivri kuyruk tuyleri (yesil, ucu sari)
    const ka = Math.PI / 2 + q * 0.5, km = [hx + Math.cos(ka) * boy * uz * 0.55, hy + Math.sin(ka) * boy * uz * 0.55];
    elips(km, boy * uz * 0.5, boy * 0.045, ka, POST_K);
    elips([km[0] + Math.cos(ka) * boy * uz * 0.38, km[1] + Math.sin(ka) * boy * uz * 0.38], boy * 0.07, boy * 0.03, ka, KANAT_U, false);
  }
  bacak('Left', POST_K); bacak('Right', POST_K); kol('Left', POST_K);
  elips([mx, my - L * 0.38], boy * 0.22, L * 0.5, aci, POST);           // tombul damla govde
  elips([mx, my + L * 0.3], boy * 0.27, L * 0.95, aci, POST);
  elips([mx, my - L * 0.38], boy * 0.22 - KON, L * 0.5 - KON, aci, POST, false);
  elips([mx, my + L * 0.35], boy * 0.16, L * 0.75, aci, KARIN);          // sari gogus
  kol('Right', POST);
  elips([nx_ - boy * 0.1, ny_ + boy * 0.08], boy * 0.028, boy * 0.022, 0, DUDUK);   // altin duduk
}
let PIP_DURUS = null;                                            // durus karesi (ilk pozun 0. karesi = ayakta)
function pipTam(E, kafa, P, sc, boy, t) {                       // govde + bas; kafa = [x, y, r] kare px; sc = kare px -> ekran
  cx.save(); cx.lineJoin = 'round'; pipGovde(E, P, boy);
  const u = kafa[2] / 30 * PIP_OLCEK * sc, [bx, by] = P([kafa[0], kafa[1] - kafa[2] * 0.25]);
  cx.translate(bx, by + PIP_DY * u); pipBas(u, MASKOT_DUYGU, t); cx.restore();
}
function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {   // motor 39: Pako (ayakta duran kare) - koseler, kartlar, abone; (x, y) govde ortasi
  if (alfa <= 0.01) return;
  const Y = KY.maskot; if (!PIP_DURUS) { const a = POZ_ADLAR[0]; PIP_DURUS = { E: Y.poz[a].eklem[0], kafa: Y.poz[a].kafa[0] }; }
  const sc = 230 * s * k / Y.boy_px, [hx, hy] = PIP_DURUS.E.Hips;
  const P = p => [x + (p[0] - hx) * sc, y + (p[1] - hy) * sc + 20 * s * k];
  cx.save(); cx.globalAlpha *= alfa;
  pipTam(PIP_DURUS.E, PIP_DURUS.kafa, P, sc, Y.boy_px * sc, t);
  cx.restore();
}
"""
fonk("maskotCiz", PAKO)

# ------------------------------------------------------------------ hakem: 3B kare + 2B kafa yerine tamami 2B (eklem verisi)
eski_h = t[t.index("  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];\n  if (!im) { maskotCiz(xm, ay - 80 * k - bob, 1.0, t); return; }"):]
eski_h = eski_h[:eski_h.index("// motor 34: Kiko buyuk kafa (olcek 2,1 = ornek sayfa)\n") + len("// motor 34: Kiko buyuk kafa (olcek 2,1 = ornek sayfa)\n")]
degis(eski_h, """  const im = KR.maskot[ad] && KR.maskot[ad][Math.round(j)];
  if (!im || !Y.poz[ad] || !Y.poz[ad].eklem) { maskotCiz(xm, ay - 80 * k - bob, 1.0, t); return; }
  const sc = H * MAS_BOY / Y.boy_px, px = im.width * sc, x0 = xm - px / 2, y0 = ay - Y.zemin_px * sc - bob;
  MASKOT_DUYGU = 'mutlu';                                      // motor 28: duvar gecince PERFECT -> sevinc, OUT -> sasirma
  if (d && u >= ZD(d).kart + ZD(d).say + ZD(d).buyu * 0.5) MASKOT_DUYGU = (d.out && (d.out.p1 || d.out.p2)) ? 'sasirma' : 'sevinc';
  const jj = Math.round(j), E = Y.poz[ad].eklem[jj], kf = Y.poz[ad].kafa[jj];   // motor 39: Pako tamami 2B (eklem verisi)
  cx.save(); pipTam(E, kf, p => [x0 + p[0] * sc, y0 + p[1] * sc], sc, Y.boy_px * sc, t); cx.restore();
""")

# ------------------------------------------------------------------ hakem kursusu: ahsap sandik + altin sikkeler + iki fener
satir_degis("// motor 34: ucan ada kursu",
            "  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#e8963a'); g.addColorStop(0.5, '#b8601a'); g.addColorStop(1, '#7a3a0a');   // motor 39: ahsap hazine sandigi kursu")
satir_degis("// cimende cicekler",
            "  for (let q = 0; q < 9; q++) { const xx = xm - w * 0.42 + q * w * 0.105, yy = y0 + (q % 2) * 5 * k; cx.fillStyle = '#ffd21e'; cx.strokeStyle = '#8a5200'; cx.lineWidth = 2.5 * k; cx.beginPath(); cx.ellipse(xx, yy, 9 * k, 6 * k, 0, 0, 6.283); cx.fill(); cx.stroke(); }   // motor 39: kapakta altin sikkeler")
satir_degis("// tas derzleri", "  cx.strokeStyle = '#ffc21a'; cx.lineWidth = 7 * k; for (const dx of [-0.36, 0.36]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 12 * k); cx.lineTo(xm + dx * w, H); cx.stroke(); }   // motor 39: altin kosebent")

# ------------------------------------------------------------------ OUT: tahtadan denize -> su sicramasi
satir_degis("function sicrama(xm, ym, u, olc = 1) {", "function sicrama(xm, ym, u, olc = 1) {                        // motor 39: su sicramasi: turkuaz-beyaz damlalar + kopuk halkasi (tahtadan denize dusus)")
satir_degis("// motor 34: bulut halkasi", "  cx.strokeStyle = 'rgba(220,250,255,0.95)'; cx.lineWidth = 18 * k * (1 - q);   // motor 39: kopuk halkasi")
satir_degis("// motor 34: bulut topu", "    cx.fillStyle = ['#e8fcff', '#5ae0ff', '#14b8e8'][j % 3]; cx.beginPath(); cx.arc(x, y, (10 + 14 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 39: su damlasi")

# ------------------------------------------------------------------ kepenkte Pako neon yuzu (bas + korsan sapkasi + tepelik + gozler + kanca gaga)
a = t.index("  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.88, 0, 0, 6.283); cx.stroke();                        // motor 34: Kiko neon yuzu - bas")
b = t.index("// kivrik gaga\n", a) + len("// kivrik gaga\n")
t = t[:a] + """  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.9, 0, 0, 6.283); cx.stroke();                         // motor 39: Pako neon yuzu - bas
  for (const [dx, h] of [[-0.4, 1.95], [0, 2.25], [0.42, 1.9]]) {                                      // tepelik (sapkanin arkasindan)
    cx.beginPath(); cx.moveTo(mx + (dx - 0.2) * r, my - 1.0 * r); cx.lineTo(mx + (dx * 1.6) * r, my - h * r); cx.lineTo(mx + (dx + 0.2) * r, my - 1.0 * r); cx.stroke();
  }
  cx.beginPath(); cx.moveTo(mx - 1.27 * r, my - 0.41 * r); cx.lineTo(mx - 1.05 * r, my - 1.14 * r); cx.lineTo(mx - 0.5 * r, my - 1.5 * r); cx.lineTo(mx, my - 1.27 * r);
  cx.lineTo(mx + 0.5 * r, my - 1.5 * r); cx.lineTo(mx + 1.05 * r, my - 1.14 * r); cx.lineTo(mx + 1.27 * r, my - 0.41 * r); cx.lineTo(mx, my - 0.55 * r); cx.closePath(); cx.stroke();   // korsan sapkasi
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.41, my - r * 0.18, r * 0.36, r * 0.38, 0, 0, 6.283); cx.stroke(); cx.beginPath(); cx.arc(mx + sx * r * 0.43, my - r * 0.16, r * 0.12, 0, 6.283); cx.stroke(); }   // goz halkasi
  cx.beginPath(); cx.moveTo(mx - r * 0.36, my + r * 0.18); cx.lineTo(mx, my + r * 0.05); cx.lineTo(mx + r * 0.36, my + r * 0.18); cx.lineTo(mx + r * 0.27, my + r * 0.55);
  cx.lineTo(mx, my + r * 0.86); cx.lineTo(mx - r * 0.27, my + r * 0.55); cx.closePath(); cx.stroke();   // kanca gaga
""" + t[b:]

# ------------------------------------------------------------------ giris: serit yelken katman katman iner, aralanir; Pako suzulur; marti + altin sikke
a = t.index("  hakemCiz(t, null, 0);", t.index("const ua = u - KH - KR_;")); assert "dev bulut perdesi" in t[a:a + 300]
b = t.index("  if (ua < 0.18) { cx.save(); cx.fillStyle = `rgba(255,255,255,", a)
t = t[:a] + r"""  const ac = ease(kisit((ua - 0.75) / 0.45, 0, 1));            // motor 39: dev serit yelken (3 katman) iki yana aralanir
  const ps = ease(kisit((ua - 0.55) / 0.45, 0, 1));             // Pako direkten suzulup kursuye konar
  if (ps >= 1) hakemCiz(t, null, 0);
  for (let j = 0; j < 3; j++) {                                 // katman katman iner (ustten asagi)
    const in_ = ease(kisit((ua - j * 0.12) / 0.35, 0, 1));
    if (in_ <= 0 || ac >= 1) continue;
    const y0 = -H * 0.04 + j * H * 0.34, h = H * 0.37 * in_;
    for (const s of [-1, 1]) {
      const xs = W / 2 + s * W * 0.52 * ac, x0 = s < 0 ? xs - W / 2 : xs, x1 = s < 0 ? xs : xs + W / 2;
      cx.save(); cx.beginPath(); cx.moveTo(x0, y0); cx.lineTo(x1, y0); cx.lineTo(x1, y0 + h);
      cx.quadraticCurveTo((x0 + x1) / 2, y0 + h + 46 * k * in_, x0, y0 + h); cx.closePath(); cx.clip();
      for (let q = 0; q < 6; q++) { cx.fillStyle = q % 2 ? '#ffd21e' : '#ff2a3a'; cx.fillRect(x0 + (x1 - x0) * q / 6 - 1, y0, (x1 - x0) / 6 + 2, h + 60 * k); }
      const g = cx.createLinearGradient(x0, 0, x1, 0); g.addColorStop(0, 'rgba(110,20,0,0.28)'); g.addColorStop(0.5, 'rgba(255,255,255,0.14)'); g.addColorStop(1, 'rgba(110,20,0,0.28)');
      cx.fillStyle = g; cx.fillRect(x0, y0, x1 - x0, h + 60 * k); cx.restore();
    }
    cx.save(); cx.globalAlpha = 1 - ac; cx.fillStyle = '#9a4a1a'; cx.strokeStyle = '#3a1406'; cx.lineWidth = 6 * k;   // seren (ahsap)
    cx.beginPath(); cx.roundRect(-20 * k, y0 - 16 * k, W + 40 * k, 32 * k, 16 * k); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffc21a'; for (const xx of [W * 0.02, W * 0.98]) { cx.beginPath(); cx.arc(xx, y0, 20 * k, 0, 6.283); cx.fill(); cx.stroke(); }
    cx.restore();
  }
  if (ps > 0 && ps < 1) {                                       // suzulme: sol ustten yay cizerek kursuye
    const xx = lerp(W * 0.12, W / 2, ps), yy = lerp(-H * 0.05, H * 0.8, ps) - Math.sin(ps * Math.PI) * H * 0.12;
    maskotCiz(xx, yy, lerp(0.7, 1.0, ps), t);
  }
  const R = rng(3333);                                          // motor 39: marti surusu + ucusan altin sikkeler soldan saga
  for (let j = 0; j < 80; j++) {
    const hz = 0.8 + 0.7 * R(), y0 = R() * H * 0.8, ph = R(), r = (16 + 22 * R()) * k;
    const x = (-0.25 + (ua * hz * 1.1 + ph * 0.6 - 0.2)) * W, y = y0 + Math.sin(ua * 5 + ph * 9) * 50 * k;
    if (x < -60 * k || x > W + 60 * k || ua < 0.7) continue;
    cx.save(); cx.translate(x, y);
    if (j % 3 === 0) {                                          // marti: govde + cirpan kanatlar
      const kn = Math.sin(ua * 26 * hz + ph * 9) * r * 0.7;
      cx.strokeStyle = '#ffffff'; cx.fillStyle = '#ffffff'; cx.lineWidth = 5 * k; cx.lineCap = 'round';
      cx.beginPath(); cx.moveTo(-r * 1.2, -kn); cx.quadraticCurveTo(-r * 0.5, -r * 0.3, 0, 0); cx.quadraticCurveTo(r * 0.5, -r * 0.3, r * 1.2, -kn); cx.stroke();
      cx.beginPath(); cx.ellipse(0, 0, r * 0.35, r * 0.2, 0, 0, 6.283); cx.fill();
      cx.fillStyle = '#ff8a10'; cx.beginPath(); cx.ellipse(r * 0.38, 0, r * 0.12, r * 0.06, 0, 0, 6.283); cx.fill();
    } else {                                                    // donen altin sikke
      cx.scale(Math.abs(Math.sin(ua * 7 * hz + ph * 5)) * 0.8 + 0.2, 1);
      cx.fillStyle = '#ffd21e'; cx.strokeStyle = '#8a5200'; cx.lineWidth = 3 * k; cx.beginPath(); cx.arc(0, 0, r * 0.45, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = 'rgba(255,255,255,0.6)'; cx.beginPath(); cx.arc(-r * 0.12, -r * 0.12, r * 0.12, 0, 6.283); cx.fill();
    }
    cx.restore();
  }
""" + t[b:]

# ------------------------------------------------------------------ acilis sorusu: WHO WILL WIN THE TREASURE? + BLUE OR PINK?
a = t.index("      cx.save(); cx.globalAlpha = acilisSoru * 0.8; cx.fillStyle = '#100630'; cx.beginPath(); cx.roundRect(W / 2 - 620 * k, H * 0.13 - 62 * k, 1240 * k, 124 * k, 62 * k); cx.fill(); cx.restore();")
b = t.index("\n", t.index("satir([['WHO WILL WIN? ', KART_DOLGU]", a)) + 1
t = t[:a] + """      cx.save(); cx.globalAlpha = acilisSoru * 0.82; cx.fillStyle = '#2a1006'; cx.beginPath(); cx.roundRect(W / 2 - 700 * k, H * 0.165 - 112 * k, 1400 * k, 224 * k, 70 * k); cx.fill();   // motor 39: ahsap tabela + halat
      cx.strokeStyle = '#e8b45a'; cx.lineWidth = 10 * k; cx.setLineDash([22 * k, 10 * k]); cx.stroke(); cx.setLineDash([]); cx.restore();
      yaziK('WHO WILL WIN THE TREASURE?', W / 2, H * 0.12, 80 * k * acilisSoru, ['#fff6a0', '#ffd23a', '#ff9a1a'], acilisSoru, '#3a1400');
      satir([['BLUE', ['#ffffff', ACIK[0], RENK[0]]], [' OR ', KART_DOLGU], ['PINK', ['#ffffff', ACIK[1], RENK[1]]], ['?', KART_DOLGU]], W / 2, H * 0.215, 80 * k * acilisSoru, acilisSoru);
""" + t[b:]

# ------------------------------------------------------------------ sonuc karti: hazine sandigi acilir
degis("function sonucKart(kart, u, t) {                              // bastaki \"WHO WILL WIN?\" sorusunun cevabi\n  kartZeminCiz(t);",
      """function hazineCiz(x, y, r, u, t) {                            // motor 39: hazine sandigi - kapak acilir, altin sikkeler sacilir, isilti
  const ac = ease(kisit((u - 0.5) / 0.5, 0, 1));
  cx.save(); cx.translate(x, y); cx.lineJoin = 'round';
  cx.shadowColor = '#ffd21e'; cx.shadowBlur = 60 * k * ac;
  const gg = cx.createLinearGradient(0, -r * 0.5, 0, r * 0.6); gg.addColorStop(0, '#c8402a'); gg.addColorStop(1, '#7a1a0a');
  cx.fillStyle = gg; cx.strokeStyle = '#3a0a04'; cx.lineWidth = 8 * k;
  cx.beginPath(); cx.roundRect(-r, -r * 0.4, 2 * r, r, 18 * k); cx.fill(); cx.stroke(); cx.shadowBlur = 0;
  cx.fillStyle = '#ffc21a'; for (const dx of [-0.82, 0.62]) { cx.beginPath(); cx.roundRect(dx * r, -r * 0.4, r * 0.2, r, 6 * k); cx.fill(); cx.stroke(); }
  cx.beginPath(); cx.roundRect(-r * 0.14, -r * 0.3, r * 0.28, r * 0.34, 6 * k); cx.fill(); cx.stroke();          // kilit
  for (let q = 0; q < 9; q++) { cx.fillStyle = '#ffd21e'; cx.beginPath(); cx.ellipse((-0.7 + q * 0.175) * r, -r * 0.42 - (q % 2) * 8 * k, 22 * k, 13 * k, 0, 0, 6.283); cx.fill(); cx.lineWidth = 3 * k; cx.stroke(); }   // ici altin dolu
  cx.save(); cx.translate(0, -r * 0.4); cx.scale(1, Math.cos(ac * 1.9)); cx.lineWidth = 8 * k;     // kapak geriye acilir
  const gk = cx.createLinearGradient(0, -r * 0.6, 0, 0); gk.addColorStop(0, '#d8503a'); gk.addColorStop(1, '#8a2a12'); cx.fillStyle = gk;
  cx.beginPath(); cx.moveTo(-r, 0); cx.quadraticCurveTo(0, -r * 0.9, r, 0); cx.closePath(); cx.fill(); cx.stroke(); cx.restore();
  const R3 = rng(777);
  if (ac > 0.2) for (let j = 0; j < 26; j++) {                  // sacilan sikkeler
    const a = -Math.PI * (0.15 + 0.7 * R3()), v = (260 + 420 * R3()) * k, tt = ((u - 0.6 + R3() * 1.2) % 1.6 + 1.6) % 1.6;
    const xx = Math.cos(a) * v * tt * 0.7, yy = -r * 0.5 + Math.sin(a) * v * tt + 700 * k * tt * tt;
    if (yy > r * 0.6) continue;
    cx.save(); cx.translate(xx, yy); cx.scale(Math.abs(Math.sin(t * 8 + j)) * 0.8 + 0.2, 1);
    cx.fillStyle = '#ffd21e'; cx.strokeStyle = '#8a5200'; cx.lineWidth = 3 * k; cx.beginPath(); cx.arc(0, 0, 16 * k, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
  }
  cx.restore();
}
function sonucKart(kart, u, t) {                              // bastaki "WHO WILL WIN THE TREASURE?" sorusunun cevabi
  kartZeminCiz(t);
  if (kart.hazine) hazineCiz(kart.kazanan === 'p1' ? W * 0.76 : W * 0.24, H * 0.8, 190 * k, u, t);""")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
