"""MOTOR 33 (HUMAN TETRIS 36) = sahne32.html (motor 32, 35. video: tek serit 2P CO-OP) + yama -> 03-motor/sahne33.html.
sahne32 degismez.

    python motor33-yama.py

36: REF-088 yapi (1P SOLO), gunduz dev mantar ormani (varlik-mantar.py), ozel tur SPEED (motor 26/29: d.hiz duvarlarinda FASTER!),
yarisan karakter TEK sporcu (BLUE, karakter.py --sporcu 1, kare kare tek kisilik), hakem maskot baykus yavrusu OLLI
(2B bas: genis karamel bas, iki uclu kulak tuyu, krem yuz diski, amber gozler, turuncu gaga, basta yaprak; 3B govde karakter.py --baykus 1),
OUT = yumusak dev mantar sapkasina duser, seker, spor bulutu. Bolumde d.grup = tek kisilik poz adi (maske varlik-36s1/poz/).
Giris (TALIMATLAR §4): kanca (BOSS onizleme + CAN YOU PASS THIS? + geri sarma) -> mekana ozel acilis (yerden dev mantar
buyur, sapkasi acilir, spor bulutu + yapraklar) -> CAN YOU GET GOLD? ; ilk duvar <= 5 sn.
"""
import os, re

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne32.html")
HEDEF = os.path.join(BURA, "..", "sahne33.html")
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
t = t[:m.start()] + "<title>HUMAN TETRIS 36 - motor 33 (tek serit dev mantar ormani, 1P SOLO, SPEED, baykus Olli, kanca girisi)</title>" + t[m.end():]
degis("// MOTOR 32 — HUMAN TETRIS 35", "// MOTOR 33 — HUMAN TETRIS 36 (REF-088 yapi, 21 Kas 2026; motor 32'den, tetris-pvp/motor33-yama.py):\n"
      "//   - 1P SOLO: tek sporcu karakter (OY = ['p1']), d.grup = tek kisilik poz; hakem Olli ayni pozu tek seferde gosterir (A/B yok)\n"
      "//   - sahne: tetris-pvp/varlik-mantar.py (gunduz dev mantar ormani); gokte suzulen sporlar + yapraklar + kelebekler\n"
      "//   - hakem baykus yavrusu OLLI (2B bas), kutuk kursu + yosun tumsek; OUT dev mantar sapkasina (spor bulutu); SPEED ROUND FASTER!\n"
      "//   - giris kanca -> dev mantar yerden buyur, sapka acilir, spor bulutu -> CAN YOU GET GOLD?\n"
      "// --- motor 32 aciklamasi ---\n"
      "// MOTOR 32 — HUMAN TETRIS 35")

# ------------------------------------------------------------------ SOLO: tek oyuncu, tek kisilik kareler, maskot A/B yok
degis("const OY = ['p1', 'p2'];", "const OY = ['p1'];                                              // motor 33: 1P SOLO")
degis("const KR = { p1: {}, p2: {}, maskot: {} };", "const KR = { p1: {}, maskot: {} };")
degis("await Promise.all(['p1', 'p2', 'maskot'].flatMap(o => {\n  const adlar = o === 'maskot' ? POZ_ADLAR.flatMap(a => [a + '-A', a + '-B']) : POZ_ADLAR;   // motor 24: ikili kareler",
      "await Promise.all(['p1', 'maskot'].flatMap(o => {\n  const adlar = POZ_ADLAR;                                      // motor 33: solo - maskot da ayni tek kisilik poz")
degis("window.KARAKTER_VAR = ['p1', 'p2', 'maskot'].every(", "window.KARAKTER_VAR = ['p1', 'maskot'].every(")
degis("  for (let i = 0; i < 2; i++) {\n    const o = OY[i], Y = KY[o], L = KR[o][ad]; if (!L) continue;",
      "  for (let i = 0; i < OY.length; i++) {\n    const o = OY[i], Y = KY[o], L = KR[o][ad]; if (!L) continue;")
degis("    const kf = Y.poz[ad].kalca[kisit(Math.round(j), 0, KK - 1)];",           # solo kareler (karakter.py --ikili olmadan) kalca tasimiyor
      "    const kf = Y.poz[ad].kalca ? Y.poz[ad].kalca[kisit(Math.round(j), 0, KK - 1)] : [Y.w_px / 2, Y.zemin_px - Y.boy_px * 0.5];   // motor 33: solo karede kalca yok -> govde ortasi")
degis("  for (let i = 0; i < 2; i++) {\n    const o = OY[i], Y = KY[o], im = karKare(o, ad, KK - 1); if (!im) continue;",
      "  for (let i = 0; i < OY.length; i++) {\n    const o = OY[i], Y = KY[o], im = karKare(o, ad, KK - 1); if (!im) continue;")
degis("  for (let i = 0; i < 2; i++) {                                // iki mini kart (serit renkleri)",
      "  for (let i = 0; i < OY.length; i++) {                         // motor 33: tek mini kart")
# hakem: ayni pozu tek seferde gosterir (yarim A / yarim B yok), ok isareti yok
degis("let ad = (d ? d.grup : POZ_ADLAR[0]) + '-A', j = 0,", "let ad = (d ? d.grup : POZ_ADLAR[0]), j = 0,")
degis("    else if (u < Z.kart) isaret = -1;", "    else if (u < Z.kart) isaret = 0;")
degis("      else { yari = sq < 0.5 ? 0 : 1; q = (sq - yari * 0.5) / 0.5; }\n      ad = d.grup + (yari ? '-B' : '-A'); isaret = yari ? 1 : -1;",
      "      else { yari = 0; q = sq; }\n      ad = d.grup; isaret = 0;")
degis("    } else ad = d.grup + '-B';", "    } else ad = d.grup;")
# yazilar: CO-OP -> SOLO
degis("  satir([['MAKE THE SHAPE TOGETHER', '#ffffff']], W * 0.15, H * 0.56, 32 * k, a);\n"
      "  satir([['BLUE', RENK[0]], [' LEFT  ·  ', '#ffffff'], ['PINK', '#ff6ade'], [' RIGHT', '#ffffff']], W * 0.85, H * 0.56, 34 * k, a);   // md. 28: PINK #ff6ade",
      "  satir([['COPY THE SHAPE', '#ffffff']], W * 0.15, H * 0.56, 34 * k, a);                       // motor 33: solo\n"
      "  satir([['HOLD IT!', '#ffffff']], W * 0.85, H * 0.56, 34 * k, a);")
degis("  satir([['1. PICK A SIDE: ', '#ffffff'], ['BLUE', RENK[0]], [' LEFT · ', '#ffffff'], ['PINK', RENK[1]], [' RIGHT', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));\n"
      "  satir([['2. COPY THE SHAPE ON YOUR SIDE', '#ffffff']], W / 2, H * 0.52, 60 * k, g(1));",
      "  satir([['1. WATCH OLLI SHOW THE POSE', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));\n"
      "  satir([['2. COPY THE SHAPE', '#ffffff']], W / 2, H * 0.52, 60 * k, g(1));")
degis("  yaziK('TEAM SCORE', W / 2, H * 0.13, 100 * k * s, KART_DOLGU, 1, KON, '#7ad8ff');",
      "  yaziK('YOUR SCORE', W / 2, H * 0.13, 100 * k * s, KART_DOLGU, 1, KON, '#7ad8ff');")
degis("satir([['CAN YOU TWO CLEAR ALL ', KART_DOLGU], [String(TOPLAM_DUVAR), ['#fff6a0', '#ffd23a', '#ff9a1a']], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);   // motor 32: yukleme notu sorusu",
      "satir([['CAN YOU GET ', KART_DOLGU], ['GOLD', ['#fff6c0', '#ffd23a', '#e09a00']], ['?', KART_DOLGU]], W / 2, H * 0.13, 96 * k * acilisSoru, acilisSoru);   // motor 33: yukleme notu sorusu")
degis("  if (pa > 0.01) for (let i = 0; i < 2; i++) pYazi(['P1', 'P2'][i], i ? W * 0.75 : W * 0.25, H * 0.6, 130 * k, RENK[i], pa);",
      "  if (pa > 0.01) pYazi('YOU', W * 0.22, H * 0.6, 130 * k, RENK[0], pa);                       // motor 33: solo (BLUE oyuncu)")

# ------------------------------------------------------------------ SPEED ROUND: d.hiz duvarlarinda ustte FASTER! (motor 26/29)
degis("  karakterCiz(d, u, t);\n  if (T && u >= c && !(d.out && (d.out.p1 || d.out.p2))) freezeCiz(u - c, T, t);",
      "  karakterCiz(d, u, t);\n"
      "  if (d.hiz && u < b) {                                          // motor 33 (motor 26) SPEED ROUND: hizlanan duvarda ustte FASTER! (abone dugmesiyle ust uste binmez)\n"
      "    const ab = ABONE.reduce((m, x) => Math.max(m, kisit(1 - Math.max(x - t, t - x - ABONE_SURE, 0) / 0.3, 0, 1)), 0);\n"
      "    const gir = ease(kisit(u / 0.3, 0, 1)) * (1 - ab), p = 1 + 0.08 * Math.sin(t * 14);\n"
      "    if (gir > 0.01) yaziK('FASTER!', W / 2, H * 0.12, 104 * k * ease(kisit(u / 0.3, 0, 1)) * p, ['#fff6a0', '#ffd23a', '#ff6a1a'], gir, '#4a1400', '#ffffff');\n"
      "  }\n"
      "  if (T && u >= c && !(d.out && (d.out.p1 || d.out.p2))) freezeCiz(u - c, T, t);")

# ------------------------------------------------------------------ mini mantar (topCiz yerine) + yosun tumsegi (simitCiz yerine)
fonk("topCiz", r"""
function topCiz(x, y, r, t, c1 = '#ff2a3a', c2 = '#fff08a') {   // motor 33: mini mantar (sapka + krem-sari benek + sap); gokte suzen spor yerine
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2 + x * 0.01) * 0.12);
  cx.lineWidth = Math.max(1.5, r * 0.08); cx.strokeStyle = '#3a1606'; cx.lineJoin = 'round';
  cx.fillStyle = '#ffcf8a'; cx.beginPath(); cx.roundRect(-r * 0.22, -r * 0.1, r * 0.44, r * 0.9, r * 0.18); cx.fill(); cx.stroke();
  cx.beginPath(); cx.moveTo(-r, 0); cx.quadraticCurveTo(-r * 0.95, -r * 0.95, 0, -r * 0.95); cx.quadraticCurveTo(r * 0.95, -r * 0.95, r, 0);
  cx.quadraticCurveTo(0, r * 0.18, -r, 0); cx.closePath();
  const g = cx.createRadialGradient(-r * 0.35, -r * 0.6, r * 0.05, 0, -r * 0.3, r * 1.1); g.addColorStop(0, '#ffffff'); g.addColorStop(0.18, c1); g.addColorStop(1, c1);
  cx.fillStyle = g; cx.fill(); cx.stroke();
  cx.fillStyle = c2;
  for (const [px, py, pr] of [[-0.5, -0.4, 0.13], [0.1, -0.65, 0.15], [0.55, -0.32, 0.11], [-0.1, -0.25, 0.09]]) { cx.beginPath(); cx.arc(px * r, py * r, pr * r, 0, 6.283); cx.fill(); }
  cx.restore();
}
""")
fonk("simitCiz", r"""
function simitCiz(x, y, r) {                                    // motor 33: yosun tumsegi + iki mini mantar (hakemin ayak alti)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.4); g.addColorStop(0, '#5ae04a'); g.addColorStop(1, '#109a2a');
  cx.fillStyle = g; cx.strokeStyle = '#0a5a1a'; cx.lineWidth = Math.max(1.5, r * 0.06);
  cx.beginPath(); cx.moveTo(-r * 1.5, r * 0.2);
  for (const [px, py, pr] of [[-0.95, -0.05, 0.55], [-0.2, -0.3, 0.6], [0.6, -0.2, 0.55], [1.15, 0.0, 0.4]]) cx.arc(px * r, py * r, pr * r, Math.PI, 0);
  cx.lineTo(r * 1.5, r * 0.2); cx.quadraticCurveTo(0, r * 0.5, -r * 1.5, r * 0.2); cx.closePath(); cx.fill(); cx.stroke();
  cx.restore();
  topCiz(x - r * 1.15, y - r * 0.25, r * 0.32, 0, '#ff3aa8');
  topCiz(x + r * 1.2, y - r * 0.2, r * 0.26, 0, '#ffc21a');
}
""")

# ------------------------------------------------------------------ OLLI (2B): maskot-ornek-36.py ile ayni olcu
fonk("pipBas", "")                                              # Pip'in basi kalkar (olliBas maskotCiz blogunda)
degis("let pipDuygu = 'mutlu';\nfunction maskotCiz(", "function maskotCiz(")
fonk("maskotCiz", r"""
function olliBas(u, duygu, t) {                                 // motor 33: Olli'nin basi, merkez (0,0), birim u
  const KN = '#3a1606', KAR = '#c8782a', DISK = '#ffe2a8', AMBER = '#ffb01a', GAGA = '#ff8a10';
  const el = (x, y, rx, ry, f, s, w) => { cx.beginPath(); cx.ellipse(x * u, y * u, rx * u, ry * u, 0, 0, 6.283); if (f) { cx.fillStyle = f; cx.fill(); } if (s) { cx.strokeStyle = s; cx.lineWidth = w * u; cx.stroke(); } };
  const pol = (pts, f, w = 1.6) => { cx.beginPath(); pts.forEach(([x, y], i) => i ? cx.lineTo(x * u, y * u) : cx.moveTo(x * u, y * u)); cx.closePath(); cx.fillStyle = f; cx.fill(); cx.strokeStyle = KN; cx.lineWidth = w * u; cx.stroke(); };
  cx.lineJoin = 'round';
  for (const sx of [-1, 1]) {                                   // iki uclu kulak tuyleri (disa yatik), hafif oynar
    cx.save(); cx.rotate(sx * 0.04 * Math.sin(t * 5));
    pol([[sx * 11, -17], [sx * 27, -27], [sx * 22, -20], [sx * 29, -19], [sx * 21, -11]], '#8a4a1a');
    cx.restore();
  }
  const g = cx.createRadialGradient(-7 * u, -8 * u, 2 * u, 0, 0, 26 * u); g.addColorStop(0, '#e89a4a'); g.addColorStop(1, KAR);
  el(0, 0, 24, 21, g, KN, 1.6);
  pol([[-3, -19], [0, -31], [4, -19]], '#20c850', 1.0);         // basta yaprak
  for (const sx of [-1, 1]) el(sx * 9.5, 1, 11, 12, DISK);       // yuz diski
  for (const sx of [-1, 1]) {
    if (duygu === 'sevinc') { cx.strokeStyle = KN; cx.lineWidth = 2.6 * u; cx.beginPath(); cx.arc(sx * 9.5 * u, 1 * u, 6 * u, Math.PI * 1.11, Math.PI * 1.89); cx.stroke(); }
    else if (duygu === 'sasirma') { el(sx * 9.5, 0, 8, 8.5, '#ffffff', KN, 1.4); el(sx * 9.5, 0, 4.2, 4.4, AMBER); el(sx * 9.5, 0, 2.2, 2.2, KN); }
    else { el(sx * 9.5, 0, 7.5, 8, '#ffffff', KN, 1.4); el(sx * 9.5 + 0.8, 0.5, 5, 5.2, AMBER); el(sx * 9.5 + 1.2, 0.8, 3, 3.2, KN); el(sx * 9.5 - 1, -2.4, 1.4, 1.4, '#ffffff'); }
    el(sx * 17, 11, 3.6, 2.2, '#ff7a8a');
  }
  if (duygu === 'sasirma') { pol([[-3.5, 8], [3.5, 8], [0, 13]], GAGA, 1.0); el(0, 15.5, 2.6, 2.4, '#7a1020', KN, 1.0); }
  else pol([[-3.5, 8], [3.5, 8], [0, 15]], GAGA, 1.0);
}
let pipDuygu = 'mutlu';
function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {   // motor 33: baykus Olli (TALIMATLAR §4 maskot; yuz ve govde video boyunca ayni)
  if (alfa <= 0.01) return;
  cx.save(); cx.globalAlpha *= alfa; cx.translate(x, y); cx.scale(s * k, s * k);
  if (yuzSadece) { cx.translate(0, -32 - 7 * 2.1 * 70 / 22 / 2.1); olliBas(2.1 * 70 / 22 / 2.1 * 1.0 * 2.1 / 2.1 * 1.0, pipDuygu, t); cx.restore(); return; }
  const KN = '#3a1606';
  cx.lineJoin = 'round'; cx.lineWidth = 5; cx.strokeStyle = KN;
  const gv = cx.createRadialGradient(-10, 20, 6, 0, 40, 60); gv.addColorStop(0, '#e89a4a'); gv.addColorStop(1, '#c8782a');
  cx.fillStyle = gv; cx.beginPath(); cx.ellipse(0, 45, 48, 52, 0, 0, 6.283); cx.fill(); cx.stroke();   // tuy topu govde
  cx.fillStyle = '#ffc870'; cx.beginPath(); cx.ellipse(0, 54, 26, 32, 0, 0, 6.283); cx.fill();         // gogus
  for (const sx of [-1, 1]) {                                   // kanatlar + ayaklar
    cx.fillStyle = '#8a4a1a'; cx.beginPath(); cx.ellipse(sx * 48, 40 + Math.sin(t * 6 + sx) * 5, 14, 26, sx * 0.45, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ff8a10'; for (const dx of [-8, 0, 8]) { cx.beginPath(); cx.ellipse(sx * 22 + dx, 98, 5, 8, 0, 0, 6.283); cx.fill(); cx.stroke(); }
  }
  cx.fillStyle = '#18b83a'; cx.beginPath(); cx.roundRect(-36, -4, 72, 14, 7); cx.fill(); cx.stroke();      // yesil atki
  cx.beginPath(); cx.roundRect(10, 4, 14, 30, 6); cx.fill(); cx.stroke();
  cx.translate(0, -40); olliBas(52 / 24, pipDuygu, t);
  cx.restore();
}
""")
# yuzSadece olcusu: 3B govdenin ustunde bas; ornek sayfada OLCEK 2,1 / DY -7 (birim u = ks/30). Motor 32 Pip'te 70/22 idi.
degis("  if (yuzSadece) { cx.translate(0, -32 - 7 * 2.1 * 70 / 22 / 2.1); olliBas(2.1 * 70 / 22 / 2.1 * 1.0 * 2.1 / 2.1 * 1.0, pipDuygu, t); cx.restore(); return; }",
      "  if (yuzSadece) { cx.translate(0, -32 - 7 * OLLI_U); olliBas(OLLI_U, pipDuygu, t); cx.restore(); return; }")
degis("let pipDuygu = 'mutlu';", "let pipDuygu = 'mutlu';\nconst OLLI_U = Number(TEMA.olliU || 70 / 22 * 0.95);           // kafa birimi (onizleme kontaginda ayarlanir)")

# ------------------------------------------------------------------ gokte suzulen sporlar + yapraklar (mini balonlar yerine)
fonk("karYagisi", r"""
function karYagisi(t, alfa = 1) {                              // motor 33: suzulen parlak sporlar + duserek donen yapraklar (hareketli ust bosluk)
  cx.save(); cx.globalAlpha = alfa;
  for (let j = 0; j < KAR_T.length; j++) {
    const p = KAR_T[j];
    const x = ((p.x + Math.sin(t * 0.6 + p.f) * 0.02) % 1) * W;
    if (j % 5 === 0) {                                          // yaprak: yukaridan asagi, donerek
      const y = ((p.y + t * p.v * 0.35) % 1.1) * H * 0.75;
      if (Math.abs(x - W / 2) < W * 0.2 && y > H * 0.25) continue;
      cx.save(); cx.translate(x, y); cx.rotate(t * 1.5 + p.f); cx.scale(1, 0.5 + 0.5 * Math.abs(Math.sin(t * 2 + p.f)));
      cx.fillStyle = ['#20c850', '#7ae83a', '#ffc21a', '#ff7a10'][j % 4]; cx.strokeStyle = '#0a5a1a'; cx.lineWidth = 2 * k;
      cx.beginPath(); cx.ellipse(0, 0, (p.r * 3 + 8) * k, (p.r * 1.4 + 4) * k, 0, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
    } else {                                                    // spor: yukari suzulen, nabiz gibi parlayan sari nokta
      const y = (1.05 - ((p.y + t * p.v * 0.3) % 1.1)) * H * 0.7;
      const r = (p.r * 0.9 + 1.5) * k * (0.8 + 0.3 * Math.sin(t * 4 + p.f));
      cx.save(); cx.shadowColor = '#fff27a'; cx.shadowBlur = 12 * k; cx.fillStyle = 'rgba(255,248,170,0.95)';
      cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill(); cx.restore();
    }
  }
  cx.restore();
}
""")
degis("  karYagisi(t);\n  konfeti(t, 0.45, 26, 0.8);\n", "  karYagisi(t);\n")

# ------------------------------------------------------------------ OUT: dev mantar sapkasinda seker + spor bulutu
fonk("sicrama", r"""
function sicrama(xm, ym, u, olc = 1) {                        // motor 33: spor bulutu (karakter yumusak mantar sapkasina duser)
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(3636 + Math.round(xm));
  cx.save(); cx.globalAlpha = 1 - q;
  for (let j = 0; j < 18; j++) {
    const a = -Math.PI * (0.05 + 0.9 * R2()), v = (160 + 260 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * Math.sqrt(q), y = ym + Math.sin(a) * v * Math.sqrt(q) * 0.6, r = (22 + 28 * R2()) * k * olc * (0.6 + q);
    const g = cx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r); g.addColorStop(0, '#fffbd0'); g.addColorStop(0.65, '#f2e66a'); g.addColorStop(1, 'rgba(140,220,90,0.55)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill();
  }
  for (let j = 0; j < 12; j++) {                                // ucusan yapraklar
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (300 + 400 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * u * 0.6, y = ym + Math.sin(a) * v * u + 700 * k * u * u;
    cx.save(); cx.translate(x, y); cx.rotate(u * 8 + j); cx.fillStyle = ['#20c850', '#7ae83a', '#ffc21a'][j % 3];
    cx.beginPath(); cx.ellipse(0, 0, 14 * k, 6 * k, 0, 0, 6.283); cx.fill(); cx.restore();
  }
  cx.restore();
}
""")

# ------------------------------------------------------------------ hakem kursusu: kesik kutuk (yillik halkalar) + yosun
fonk("kule", r"""
function kule(t) {                                             // motor 33: hakem kursusu kesik kutuk + ustunde yosun, kenarda mini mantar
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(xm - w / 2, 0, xm + w / 2, 0); g.addColorStop(0, '#7a3e12'); g.addColorStop(0.5, '#b8682a'); g.addColorStop(1, '#6a3410');
  cx.fillStyle = g; cx.strokeStyle = '#3a1606'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(58,22,6,0.45)'; cx.lineWidth = 3 * k;
  for (let q = 1; q < 5; q++) { cx.beginPath(); cx.moveTo(xm - w / 2 + q * w / 5, y0 + 6 * k); cx.lineTo(xm - w / 2 + q * w / 5 + 6 * k, H); cx.stroke(); }
  cx.fillStyle = '#f0b060'; cx.strokeStyle = '#3a1606'; cx.lineWidth = 5 * k;
  cx.beginPath(); cx.ellipse(xm, y0 + 2 * k, w / 2, 16 * k, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(122,62,18,0.6)'; cx.lineWidth = 2.5 * k;
  for (const r of [0.3, 0.6]) { cx.beginPath(); cx.ellipse(xm, y0 + 2 * k, w / 2 * r, 16 * k * r, 0, 0, 6.283); cx.stroke(); }
  topCiz(xm + w * 0.5, y0 + h * 0.15, 22 * k, t, '#ff7a10');
  cx.restore();
}
""")
degis("  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 32: hakem pembe bulutun ustunde",
      "  cx.restore(); simitCiz(xm, ay + 14 * k, 80 * k);              // motor 33: hakem yosun tumseginin ustunde")

# ------------------------------------------------------------------ GIRIS: kanca + dev mantar acilisi
m = re.search(r"^function devBalon\(", t, re.M); s0 = m.start(); e0 = t.index("\n}\n", s0) + 3
t = t[:s0] + r"""function devMantar(x, yTaban, boy, acil, t) {                // acilis: yerden buyuyen dev mantar; acil = sapkanin acilma orani (0-1)
  const sw = boy * 0.16, sh = boy * (0.35 + 0.45 * acil);
  cx.save(); cx.lineJoin = 'round'; cx.strokeStyle = '#3a1606'; cx.lineWidth = 8 * k;
  const gs = cx.createLinearGradient(x - sw, 0, x + sw, 0); gs.addColorStop(0, '#e8a860'); gs.addColorStop(0.5, '#ffdca0'); gs.addColorStop(1, '#d89050');
  cx.fillStyle = gs; cx.beginPath(); cx.roundRect(x - sw / 2, yTaban - sh, sw, sh + 20 * k, sw * 0.3); cx.fill(); cx.stroke();
  const R = boy * (0.25 + 0.4 * acil), Rh = boy * (0.32 - 0.08 * acil), yc = yTaban - sh;
  cx.beginPath(); cx.moveTo(x - R, yc); cx.quadraticCurveTo(x - R * 0.95, yc - Rh * 1.4, x, yc - Rh * 1.4); cx.quadraticCurveTo(x + R * 0.95, yc - Rh * 1.4, x + R, yc);
  cx.quadraticCurveTo(x, yc + Rh * 0.3, x - R, yc); cx.closePath();
  const g = cx.createRadialGradient(x - R * 0.35, yc - Rh, R * 0.05, x, yc - Rh * 0.6, R * 1.1); g.addColorStop(0, '#ffffff'); g.addColorStop(0.15, '#ff3aa8'); g.addColorStop(1, '#c8106a');
  cx.fillStyle = g; cx.fill(); cx.stroke();
  cx.fillStyle = '#fff08a';
  for (const [px, py, pr] of [[-0.55, -0.55, 0.12], [-0.1, -0.95, 0.14], [0.45, -0.7, 0.11], [0.7, -0.25, 0.08], [-0.75, -0.2, 0.08], [0.1, -0.45, 0.09]]) {
    cx.beginPath(); cx.arc(x + px * R, yc + py * Rh, pr * R, 0, 6.283); cx.fill();
  }
  cx.restore();
}
""".lstrip("\n") + t[e0:]
degis("  // mekan acilisi (35: balon festivali) - sahne kareKur'da zaten cizili\n", "  // mekan acilisi (36: dev mantar ormani) - sahne kareKur'da zaten cizili\n")
a = t.index("  const R = H * 0.24, yb = lerp(H * 1.35, -H * 0.45, ease(kisit(ua / 1.3, 0, 1)));")
b = t.index("  const R3 = rng(3131);")
t = t[:a] + r"""  const gb = ease(kisit(ua / 0.7, 0, 1)), ac = ease(kisit((ua - 0.45) / 0.35, 0, 1));   // dev mantar yerden firlar, sapkasi acilir
  const cik = ease(kisit((ua - 1.05) / 0.35, 0, 1));
  if (cik < 1) { cx.save(); cx.globalAlpha = 1 - cik; devMantar(W / 2, H * 1.02 + H * 0.6 * (1 - gb) + H * 0.5 * cik, H * 0.95, ac, t); cx.restore(); }
  const R2 = rng(3636);                                         // sapkadan firlayan parlak spor bulutu (yukari, yana acilarak)
  for (let j = 0; j < 40; j++) {
    const t0 = 0.6 + 0.01 * j, q = ua - t0; if (q <= 0) continue;
    const a = -Math.PI / 2 + (R2() - 0.5) * 2.6, v = (600 + 700 * R2()) * k;
    const x = W / 2 + Math.cos(a) * v * q, y = H * 0.35 + Math.sin(a) * v * q * 0.8 + 160 * k * q * q, r = (10 + 18 * R2()) * k * (1 + q);
    if (y < -60 * k || q > 1.6) continue;
    cx.save(); cx.globalAlpha = kisit(1.4 - q, 0, 1); cx.shadowColor = '#fff27a'; cx.shadowBlur = 20 * k;
    cx.fillStyle = j % 3 ? 'rgba(255,248,170,0.95)' : 'rgba(170,240,110,0.9)'; cx.beginPath(); cx.arc(x, y, r, 0, 6.283); cx.fill(); cx.restore();
  }
""" + t[b:]
# acilis konfetisi -> yapraklar (renkler yesil/sari/turuncu)
degis("    const a = R3() * 6.283, hz = 0.6 + 0.9 * R3(), c = KONF_R[Math.floor(R3() * 6)], r = (10 + 18 * R3()) * k;",
      "    const a = R3() * 6.283, hz = 0.6 + 0.9 * R3(), c = ['#20c850', '#7ae83a', '#ffc21a', '#ff7a10', '#ff3aa8', '#10c8d0'][Math.floor(R3() * 6)], r = (10 + 18 * R3()) * k;")

# ------------------------------------------------------------------ kepenk: Olli neon yuzu
KUL_ESKI = ("    cx.beginPath(); cx.moveTo(mx + sx * r * 0.3, my - r * 0.78); cx.lineTo(mx + sx * r * 0.62, my - r * 1.45); cx.lineTo(mx + sx * r * 0.82, my - r * 0.55); cx.stroke();   // motor 32: Pip sivri kulak\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.62, r * 0.28, r * 0.22, 0, 0, 6.283); cx.stroke();          // pilot gozlugu\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.08, r * 0.1, r * 0.15, 0, 0, 6.283); cx.stroke();          // goz")
KUL_YENI = ("    cx.beginPath(); cx.moveTo(mx + sx * r * 0.45, my - r * 0.72); cx.lineTo(mx + sx * r * 1.12, my - r * 1.2); cx.lineTo(mx + sx * r * 0.9, my - r * 0.86); cx.lineTo(mx + sx * r * 1.2, my - r * 0.84); cx.lineTo(mx + sx * r * 0.85, my - r * 0.5); cx.stroke();   // motor 33: Olli kulak tuyu\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.4, my - r * 0.02, r * 0.36, r * 0.38, 0, 0, 6.283); cx.stroke();          // yuz diski / iri goz\n"
            "    cx.beginPath(); cx.ellipse(mx + sx * r * 0.42, my, r * 0.13, r * 0.14, 0, 0, 6.283); cx.stroke();          // gozbebegi")
degis(KUL_ESKI, KUL_YENI)
degis("  cx.beginPath(); cx.moveTo(mx - r * 0.64, my - r * 0.62); cx.lineTo(mx - r * 0.9, my - r * 0.6); cx.moveTo(mx + r * 0.64, my - r * 0.62); cx.lineTo(mx + r * 0.9, my - r * 0.6); cx.stroke();   // gozluk kayisi\n"
      "  cx.beginPath(); cx.arc(mx, my + r * 0.2, r * 0.16, 0.2, Math.PI - 0.2); cx.stroke(); cx.strokeRect(mx - r * 0.07, my + r * 0.36, r * 0.14, r * 0.12);   // gulus + iki on dis\n",
      "  cx.beginPath(); cx.moveTo(mx - r * 0.14, my + r * 0.36); cx.lineTo(mx + r * 0.14, my + r * 0.36); cx.lineTo(mx, my + r * 0.62); cx.closePath(); cx.stroke();   // motor 33: gaga\n")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
