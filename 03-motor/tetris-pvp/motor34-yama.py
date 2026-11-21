"""MOTOR 34 (HUMAN TETRIS 37) = sahne30.html (motor 30, 1v1 antik kum arenasi, BLIND) + yama -> 03-motor/sahne34.html. sahne30 degismez.

    python motor34-yama.py

37: REF-089 yapi, 1v1, gunduz ucan gokyuzu adalari (varlik-gokada.py), ozel tur BLIND (33'ten beri ilk; 34 MIRROR, 35 FREEZE, 36 SPEED).
BLIND: duvar bulut sisiyle ortulu, BLIND! + ?, siluet sayimin son 1,5 sn'sinde belirir (motor 30 mekanigi aynen).
OUT = karakter pistin disindaki bulut yatagina duser (bulut pufu: mavi-pembe puf + halka).
Hakem maskot KIKO (kartal yavrusu, kullanici 21 Kas): 2B kafa = kestane bas, krem yuz maskesi, uc tepe tuyu, kalin kas, iri amber goz,
iri kivrik sari gaga; govde 3B (karakter.py --kartal 1, kirmizi pilot atkisi). Elde kirmizi-sari hakem bayragi. Kepenkte Kiko neon yuzu.
Hakem kursusu: kucuk ucan ada (cimen ust + turuncu kaya) + iki fener. Giris KANCA (30'dan beri); mekan acilisi farkli: bulut perdesi
iki yana aralanir, bulut denizinden sellaleli bir ada yukselir, kus surusu yaziyi acar.
YENI - SUBSCRIBE WALL (kullanici 21 Kas, A: "abone cagrisini ilk bir dakikada daha gorunur ... istersen oyuna koy"): bolumde d.aboneDuvar
olan duvar (0:30-0:50 arasi, 24 yarisma duvarinin disinda, skora sayilmaz, OUT yok). Iki kapinin ustunde dev kirmizi SUBSCRIBE dugmesi
asili; iki serit ve Kiko yukari yumruk pozu (wide-stance-punch-up); duvar gecerken dugme basilir -> SUBSCRIBED! + zil; tam ekran
panelde yarim ekran SUBSCRIBE dugmesi + imlec tiklar + LIKE / COMMENT / SHARE buyuk. Bu duvarda kucuk 15 sn cagrisi yok (bolum-kur).
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne30.html")
HEDEF = os.path.join(BURA, "..", "sahne34.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def arasi(bas, son, yeni):
    """bas'tan son'a kadar (son haric) olan blogu degistirir; bas tek olmali"""
    global t
    assert t.count(bas) == 1, ("bas", t.count(bas), bas[:80])
    i = t.index(bas); j = t.index(son, i)
    t = t[:i] + yeni + t[j:]


degis("<title>HUMAN TETRIS 33 - motor 30 (iki serit antik kum arenasi, BLIND turu, ejderha hakem maskot)</title>",
      "<title>HUMAN TETRIS 37 - motor 34 (iki serit ucan gokyuzu adalari, BLIND turu, SUBSCRIBE WALL, kartal hakem Kiko)</title>")
degis("// MOTOR 30 — HUMAN TETRIS 33 (REF-085 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor30-yama.py):",
      "// MOTOR 34 — HUMAN TETRIS 37 (REF-089 yapi, 21 Kas 2026; motor 30'dan, tetris-pvp/motor34-yama.py):\n"
      "//   - sahne: tetris-pvp/varlik-gokada.py; gokte ucusan cicek yapraklari; OUT bulut yatagina duser (bulut pufu)\n"
      "//   - BLIND ROUND (motor 30 mekanigi): duvar bulut sisiyle ortulu, siluet son 1,5 sn'de; maskot o ana kadar soru balonu\n"
      "//   - hakem maskot KIKO kartal yavrusu (2B kafa, elde hakem bayragi), ucan ada kursu + iki fener; kepenkte Kiko neon yuzu\n"
      "//   - giris kanca: BOSS onizleme -> geri sarma -> bulut perdesi aralanir, ada yukselir, kus surusu\n"
      "//   - SUBSCRIBE WALL (d.aboneDuvar): dev dugme kapilarin ustunde, yumruk pozu, SUBSCRIBED + zil, tam ekranda yarim ekran dugme\n"
      "// --- motor 30 aciklamasi ---\n"
      "// MOTOR 30 — HUMAN TETRIS 33 (REF-085 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor30-yama.py):")

# gokte ucusan cicek yapraklari
degis("const KONF_R = ['#ff1e3c', '#ffd21e', '#ff7a14', '#ff3ab4', '#a040ff', '#2fd04a'];   // motor 30: renkli flama kagitlari",
      "const KONF_R = ['#ff3aa8', '#ffd21e', '#2fd04a', '#7ad0ff', '#a040ff', '#ff7a14'];   // motor 34: ucusan cicek yapraklari")

# elde hakem bayragi + kursu feneri
degis("function kristalCiz(x, y, r, t) {",
      "function bayrakCiz(x, y, r, t) {                             // motor 34: Kiko'nun elinde kirmizi-sari hakem bayragi (dalgalanir)\n"
      "  cx.save(); cx.translate(x, y); cx.rotate(-0.25 + 0.12 * Math.sin(t * 2.6));\n"
      "  cx.strokeStyle = '#5a2a08'; cx.lineWidth = r * 0.16; cx.lineCap = 'round';\n"
      "  cx.beginPath(); cx.moveTo(0, r * 1.2); cx.lineTo(0, -r * 1.1); cx.stroke();\n"
      "  const dl = Math.sin(t * 7) * r * 0.12;\n"
      "  cx.fillStyle = '#e8102c'; cx.strokeStyle = '#3a0008'; cx.lineWidth = r * 0.08;\n"
      "  cx.beginPath(); cx.moveTo(0, -r * 1.1); cx.quadraticCurveTo(r * 0.7, -r * 1.1 + dl, r * 1.4, -r * 1.0); cx.lineTo(r * 1.4, -r * 0.1);\n"
      "  cx.quadraticCurveTo(r * 0.7, -r * 0.2 - dl, 0, -r * 0.2); cx.closePath(); cx.fill(); cx.stroke();\n"
      "  cx.fillStyle = '#ffd21e'; cx.beginPath(); cx.moveTo(0, -r * 1.1); cx.lineTo(r * 1.4, -r * 1.0); cx.lineTo(0, -r * 0.2); cx.closePath(); cx.fill();\n"
      "  cx.restore();\n"
      "}\n"
      "function fenerCiz(x, y, r, t) {                              // motor 34: kursu feneri (altin direk + sicak isikli kure; kendi isigi)\n"
      "  const f = 1 + 0.06 * Math.sin(t * 5 + x);\n"
      "  cx.save(); cx.fillStyle = '#c88a1a'; cx.fillRect(x - r * 0.08, y - r * 1.2, r * 0.16, r * 1.6);\n"
      "  cx.shadowColor = '#ffd88a'; cx.shadowBlur = r * 1.4;\n"
      "  const g = cx.createRadialGradient(x - r * 0.15, y - r * 1.6, r * 0.05, x, y - r * 1.5, r * 0.55 * f);\n"
      "  g.addColorStop(0, '#fffbe0'); g.addColorStop(1, '#ffc23a'); cx.fillStyle = g;\n"
      "  cx.beginPath(); cx.arc(x, y - r * 1.5, r * 0.5 * f, 0, 6.283); cx.fill();\n"
      "  cx.restore();\n"
      "}\n"
      "function kristalCiz(x, y, r, t) {")
degis("  if (!yuzSadece) kalkanCiz(x + (78 + bs) * s * k, y - 60 * s * k, 22 * s * k, t);   // motor 30: elde altin kalkan",
      "  if (!yuzSadece) bayrakCiz(x + (78 + bs) * s * k, y - 30 * s * k, 26 * s * k, t);   // motor 34: elde hakem bayragi")

# maskot kafasi: ejderha -> KIKO kartal yavrusu (maskot-ornek-37.py ile ayni cizim; birim u, olcek 2,75 = ejderha bas boyu)
arasi("  // motor 30: KUCUK EJDERHA kafasi", "  cx.restore();\n  cx.restore();\n}\n// alt orta",
"""  // motor 34: KIKO kartal yavrusu kafasi (kullanici 21 Kas onayi; maskot-ornek-37.py ornek 2 ile birebir; kendi tasarimimiz)
  cx.save(); cx.translate(0, -2); cx.scale(2.75, 2.75);
  const KAR = '#a8501a', DISK = '#fff0c8', AMB = '#ffb01a', GAG = '#ffc21a', KAS = '#5a2408', KK = '#3a1606';
  const el = (x, y, rx, ry, dolgu, cizgi = 0) => { cx.beginPath(); cx.ellipse(x, y, rx, ry, 0, 0, 6.283); if (dolgu) { cx.fillStyle = dolgu; cx.fill(); } if (cizgi) { cx.lineWidth = cizgi; cx.strokeStyle = KK; cx.stroke(); } };
  const cok = (P, dolgu, cizgi) => { cx.beginPath(); P.forEach((p, i) => i ? cx.lineTo(p[0], p[1]) : cx.moveTo(p[0], p[1])); cx.closePath(); cx.fillStyle = dolgu; cx.fill(); if (cizgi) { cx.lineWidth = cizgi; cx.strokeStyle = KK; cx.stroke(); } };
  cx.lineJoin = 'round'; cx.lineCap = 'round';
  for (const [dx, h, eg] of [[-9, 27, -10], [0, 33, -3], [9, 27, 6]]) cok([[dx - 5, -16], [dx + eg, -h], [dx + 5, -17]], KAR, 1.6);   // tepe tuyleri
  el(0, 0, 24, 21, KAR, 1.6);                                    // kestane bas
  cok([[-19, -6], [-10, -12], [0, -8], [10, -12], [19, -6], [17, 10], [8, 18], [-8, 18], [-17, 10]], DISK, 0);   // krem yuz maskesi
  for (const sx of [-1, 1]) {
    if (MASKOT_DUYGU === 'sevinc') {                             // PERFECT: kapali ^^ gozler
      cx.strokeStyle = KK; cx.lineWidth = 2.6; cx.beginPath(); cx.arc(sx * 9, 0, 6, Math.PI * 200 / 180, Math.PI * 340 / 180); cx.stroke();
    } else if (MASKOT_DUYGU === 'sasirma') {                     // OUT: iri goz, kaslar yukari
      el(sx * 9, -1, 7.5, 8, '#ffffff', 1.4); el(sx * 9, -1, 4, 4.2, AMB); el(sx * 9, -1, 2.1, 2.1, KK);
      cx.strokeStyle = KAS; cx.lineWidth = 3.0; cx.beginPath(); cx.moveTo(sx * 4, -13); cx.lineTo(sx * 15, -16); cx.stroke();
    } else {
      el(sx * 9, 0, 7, 7.5, '#ffffff', 1.4); el(sx * 9 + 0.8, 0.6, 4.7, 4.9, AMB); el(sx * 9 + 1.1, 0.9, 2.8, 3.0, KK); el(sx * 9 - 1, -2.2, 1.4, 1.4, '#ffffff');
      cx.strokeStyle = KAS; cx.lineWidth = 3.4; cx.beginPath(); cx.moveTo(sx * 3, -9); cx.lineTo(sx * 16, -12); cx.stroke();
    }
    el(sx * 15, 11, 3.6, 2.2, 'rgba(255,122,138,0.9)');          // kizarik yanak
  }
  if (MASKOT_DUYGU === 'sasirma') {                              // gaga acik
    cok([[-6.5, 5], [6.5, 5], [4, 11], [0, 13], [-4, 11]], GAG, 1.1); el(0, 17, 3.4, 2.8, '#7a1020', 1.0);
  } else {                                                       // iri kivrik gaga: genis taban, ucu asagi kanca
    cok([[-7, 4], [7, 4], [5, 11], [1.5, 19], [-1, 16], [-4.5, 11]], GAG, 1.1);
    cx.strokeStyle = '#e8901a'; cx.lineWidth = 0.9; cx.beginPath(); cx.moveTo(-5, 8.5); cx.lineTo(5, 8.5); cx.stroke();
  }
  cx.fillStyle = 'rgba(255,255,255,0.3)'; cx.beginPath(); cx.ellipse(-9, -15, 6, 2.6, -0.4, 0, 6.283); cx.fill();   // cilali isilti
  cx.restore();
""")

# kepenkte Kiko neon yuzu (31 dersi: eski maskotun amblemi kalmasin)
arasi("  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.92, 0, 0, 6.283); cx.stroke();                        // motor 30: ejderha neon yuzu - bas",
      "  cx.shadowBlur = 0;\n  for (const [dx, dy] of",
"""  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.88, 0, 0, 6.283); cx.stroke();                        // motor 34: Kiko neon yuzu - bas
  for (const [dx, h, eg] of [[-0.37, 1.12, -0.42], [0, 1.37, -0.12], [0.37, 1.12, 0.25]]) {         // tepe tuyleri
    cx.beginPath(); cx.moveTo(mx + (dx - 0.2) * r, my - 0.66 * r); cx.lineTo(mx + (dx + eg) * r, my - h * r); cx.lineTo(mx + (dx + 0.2) * r, my - 0.7 * r); cx.stroke();
  }
  for (const sx of [-1, 1]) {
    cx.beginPath(); cx.ellipse(mx + sx * r * 0.37, my, r * 0.29, r * 0.31, 0, 0, 6.283); cx.stroke();   // goz
    cx.beginPath(); cx.moveTo(mx + sx * r * 0.12, my - r * 0.37); cx.lineTo(mx + sx * r * 0.66, my - r * 0.5); cx.stroke();   // kas
  }
  cx.beginPath(); cx.moveTo(mx - r * 0.29, my + r * 0.17); cx.lineTo(mx + r * 0.29, my + r * 0.17); cx.lineTo(mx + r * 0.2, my + r * 0.46);
  cx.lineTo(mx + r * 0.06, my + r * 0.79); cx.lineTo(mx - r * 0.04, my + r * 0.66); cx.lineTo(mx - r * 0.19, my + r * 0.46); cx.closePath(); cx.stroke();   // kivrik gaga
""")

# OUT: kum sicramasi -> bulut pufu
degis("function sicrama(xm, ym, u, olc = 1) {                        // motor 30: kum sicramasi: turuncu-altin taneler + toz halkasi",
      "function sicrama(xm, ym, u, olc = 1) {                        // motor 34: bulut pufu: mavi-pembe bulut toplari + halka (bulut yatagina dusus)")
degis("  cx.strokeStyle = 'rgba(255,214,140,0.95)'; cx.lineWidth = 18 * k * (1 - q);   // motor 30: kum tozu halkasi",
      "  cx.strokeStyle = 'rgba(200,240,255,0.95)'; cx.lineWidth = 18 * k * (1 - q);   // motor 34: bulut halkasi")
degis("    cx.fillStyle = ['#ffd23a', '#ff9a14', '#e8641e'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 30: kum tanesi",
      "    cx.fillStyle = ['#bfeaff', '#ffb0e0', '#7ad0ff'][j % 3]; cx.beginPath(); cx.arc(x, y, (12 + 16 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 34: bulut topu")

# hakem kursusu: terrakota tas -> kucuk ucan ada (cimen ust + turuncu kaya), mesale -> fener
degis("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ffa63a'); g.addColorStop(1, '#c84a14');   // motor 30: terrakota tas kursu",
      "  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#3ad84a'); g.addColorStop(0.28, '#20b030'); g.addColorStop(0.3, '#ff8a3a'); g.addColorStop(1, '#c84a14');   // motor 34: ucan ada kursu")
degis("  cx.fillStyle = '#ffd21e'; cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 9 * k);",
      "  for (let q = 0; q < 7; q++) { cx.fillStyle = KONF_R[q % 6]; cx.beginPath(); cx.arc(xm - w * 0.4 + q * w * 0.133, y0 + 7 * k, 6 * k, 0, 6.283); cx.fill(); }   // cimende cicekler")
degis("  for (const s of [-1, 1]) alevCiz(xm + s * w * 0.62, y0 - 4 * k, 26 * k, t);   // motor 30: iki mesale",
      "  for (const s of [-1, 1]) fenerCiz(xm + s * w * 0.62, y0 + 6 * k, 26 * k, t);   // motor 34: iki fener")
degis("  cx.save(); cx.shadowColor = '#ffb21a'; cx.shadowBlur = 24 * k;   // motor 30: arena hakem isiltisi",
      "  cx.save(); cx.shadowColor = '#7ad0ff'; cx.shadowBlur = 24 * k;   // motor 34: gok hakem isiltisi")
degis("  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc - kf[2] * sc * 0.25, kf[2] * sc * 1.6 / (62 * k), t, 1, true);   // motor 30: yavru ejderha buyuk kafa",
      "  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc - kf[2] * sc * 0.25, kf[2] * sc * 1.6 / (62 * k), t, 1, true);   // motor 34: Kiko buyuk kafa (olcek 2,1 = ornek sayfa)")

# BLIND: kum firtinasi -> bulut sisi; yazi konturu lacivert
degis("function tipi(x, y, w, h, t, alfa) {                          // motor 30 BLIND: kartin ustunde kum firtinasi (sicak sis + capraz akan kum cizgileri)",
      "function tipi(x, y, w, h, t, alfa) {                          // motor 34 BLIND: kartin ustunde bulut sisi (acik mavi sis + suzulen bulut toplari)")
degis("  const g = cx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(255,214,140,0.98)'); g.addColorStop(1, 'rgba(255,160,70,0.98)');",
      "  const g = cx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(210,240,255,0.99)'); g.addColorStop(1, 'rgba(120,200,255,0.99)');")
arasi("  cx.strokeStyle = 'rgba(200,100,30,0.7)'; cx.lineCap = 'round';", "  cx.restore();\n}\nfunction acilma(",
"""  for (let j = 0; j < 26; j++) {                                // suzulen bulut toplari (yavas, saga)
    const r = (30 + R() * 50) * k, px = x + ((R() + t * (0.05 + R() * 0.06)) % 1) * (w + 2 * r) - r, py = y + R() * h;
    cx.fillStyle = j % 3 ? 'rgba(255,255,255,0.55)' : 'rgba(255,190,230,0.45)';
    cx.beginPath(); cx.ellipse(px, py, r * 1.4, r * 0.8, 0, 0, 6.283); cx.fill();
  }
""")
degis("        if (ac < 0.98) {                                       // md. 28: koyu kahve kontur + beyaz dis kontur, kum zeminde okunur",
      "        if (ac < 0.98) {                                       // md. 28: koyu lacivert kontur + beyaz dis kontur, acik bulut zeminde okunur")
degis("          yaziK('BLIND!', x + w / 2, y + h * 0.36, 110 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#4a1400', '#ffffff');",
      "          yaziK('BLIND!', x + w / 2, y + h * 0.36, 110 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#0a2a6a', '#ffffff');")
degis("          yaziK('?', x + w / 2, y + h * 0.7, 150 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#4a1400', '#ffffff');",
      "          yaziK('?', x + w / 2, y + h * 0.7, 150 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#0a2a6a', '#ffffff');")
degis("    yaziK('?', bx, by + 2 * k, 70 * k * (1 + 0.08 * Math.sin(t * 6)), ['#ffffff', '#fff2c0', '#ffd23a'], 1, '#4a1400');",
      "    yaziK('?', bx, by + 2 * k, 70 * k * (1 + 0.08 * Math.sin(t * 6)), ['#ffffff', '#fff2c0', '#ffd23a'], 1, '#0a2a6a');")

# kanca sonrasi mekan acilisi: arena kapisi -> bulut perdesi aralanir, bulut denizinden ada yukselir, kus surusu
arasi("  const ac = ease(kisit(ua / 0.55, 0, 1));                      // motor 30: arena kapisinin dev ahsap kanatlari iki yana acilir",
      "  if (ua < 0.18) { cx.save();",
"""  const ac = ease(kisit(ua / 0.6, 0, 1));                       // motor 34: dev bulut perdesi iki yana aralanir
  if (ac < 1) for (const s of [-1, 1]) {
    const R = rng(s > 0 ? 9191 : 9292), x0 = W / 2 + s * W * 0.55 * ac;
    for (let j = 0; j < 22; j++) {
      const r = (120 + 140 * R()) * k, xx = x0 + s * (R() * W * 0.55), yy = R() * H;
      cx.fillStyle = j % 4 === 0 ? '#ffb8e0' : j % 2 ? '#bfeaff' : '#8ad4ff';
      cx.beginPath(); cx.ellipse(xx, yy, r * 1.3, r, 0, 0, 6.283); cx.fill();
    }
  }
  const yk = ease(kisit((ua - 0.15) / 0.6, 0, 1));              // bulut denizinden ucan ada yukselir (ekranin ortasi, sonra kaybolur)
  const ad = 1 - ease(kisit((ua - 0.95) / 0.3, 0, 1));
  if (yk > 0 && ad > 0) {
    const ax = W / 2, ay = H * (1.25 - 0.62 * yk), r = 230 * k;
    cx.save(); cx.globalAlpha = ad;
    cx.fillStyle = '#e85a1a'; cx.beginPath(); cx.moveTo(ax - r, ay); cx.quadraticCurveTo(ax - r * 0.4, ay + r * 0.6, ax, ay + r * 1.3);
    cx.quadraticCurveTo(ax + r * 0.4, ay + r * 0.6, ax + r, ay); cx.closePath(); cx.fill();                 // kaya govde
    cx.fillStyle = '#ff8a3a'; cx.beginPath(); cx.ellipse(ax, ay + r * 0.18, r * 0.85, r * 0.2, 0, 0, 6.283); cx.fill();
    cx.fillStyle = '#2fd04a'; cx.beginPath(); cx.ellipse(ax, ay, r * 1.04, r * 0.24, 0, 0, 6.283); cx.fill();   // cimen kapak
    for (const [dx, rr, c] of [[-0.55, 0.32, '#20c850'], [-0.1, 0.42, '#ff6ab8'], [0.45, 0.34, '#7ae83a']]) {   // agac taclari
      cx.fillStyle = '#a8501a'; cx.fillRect(ax + dx * r - 8 * k, ay - rr * r * 1.2, 16 * k, rr * r * 1.2);
      cx.fillStyle = c; cx.beginPath(); cx.arc(ax + dx * r, ay - rr * r * 1.4, rr * r * 0.6, 0, 6.283); cx.fill();
    }
    const sw = ease(kisit((ua - 0.5) / 0.3, 0, 1));             // selale akmaya baslar
    cx.fillStyle = '#18b8ff'; cx.fillRect(ax + r * 0.62, ay + r * 0.1, 46 * k, r * 1.6 * sw);
    cx.fillStyle = 'rgba(140,240,255,0.8)'; for (let q = 0; q < 3; q++) cx.fillRect(ax + r * 0.62 + (8 + q * 13) * k, ay + r * 0.1, 5 * k, r * 1.6 * sw);
    cx.restore();
  }
  const R = rng(3333);                                          // motor 34: kus surusu + cicek yapraklari soldan saga
  for (let j = 0; j < 90; j++) {
    const hz = 0.8 + 0.7 * R(), y0 = R() * H * 0.8, ph = R(), r = (16 + 22 * R()) * k;
    const x = (-0.25 + (ua * hz * 1.1 + ph * 0.6 - 0.2)) * W, y = y0 + Math.sin(ua * 5 + ph * 9) * 50 * k;
    if (x < -60 * k || x > W + 60 * k) continue;
    cx.save(); cx.translate(x, y);
    if (j % 3 === 0) {                                          // kus: govde + cirpan kanatlar
      const kn = Math.sin(ua * 26 * hz + ph * 9) * r * 0.7;
      cx.strokeStyle = '#ffffff'; cx.fillStyle = '#ffffff'; cx.lineWidth = 5 * k; cx.lineCap = 'round';
      cx.beginPath(); cx.moveTo(-r * 1.2, -kn); cx.quadraticCurveTo(-r * 0.5, -r * 0.3, 0, 0); cx.quadraticCurveTo(r * 0.5, -r * 0.3, r * 1.2, -kn); cx.stroke();
      cx.beginPath(); cx.ellipse(0, 0, r * 0.35, r * 0.2, 0, 0, 6.283); cx.fill();
    } else {                                                    // cicek yapragi
      cx.rotate(ph * 6 + ua * 6 * hz); cx.scale(1, 0.3 + 0.7 * Math.abs(Math.sin(ua * 7 * hz + ph * 5)));
      cx.fillStyle = KONF_R[Math.floor(ph * 6) % 6]; cx.beginPath(); cx.ellipse(0, 0, r * 0.55, r * 0.3, 0, 0, 6.283); cx.fill();
    }
    cx.restore();
  }
""")

# ---------------- SUBSCRIBE WALL (kullanici 21 Kas A)
degis("function aboneButon(xm, yM, s0, u, t) {", "function aboneButon(xm, yM, s0, u, t, imlec = true) {        // motor 34: imlec=false -> SUBSCRIBE WALL'da dugmeye yumruk basar")
degis("  if (u > 0.5 && u < ABONE_SURE - 0.35) {                        // imlec gelir, tiklar",
      "  if (imlec && u > 0.5 && u < ABONE_SURE - 0.35) {               // imlec gelir, tiklar")
degis("function tamEkran(d, u, t) {\n  const Z = ZD(d);",
"""function aboneDuvarUst(d, u, t) {                               // motor 34 SUBSCRIBE WALL: iki kapinin ustunde ipte asili dev dugme
  const Z = ZD(d), b = Z.kart + Z.say;
  const gir = ease(kisit(u / 0.5, 0, 1)), sal = Math.sin(t * 2.4) * 10 * k * (u < b ? 1 : 0.3);
  const xm = W / 2 + sal, yM = H * 0.225 + (1 - gir) * -H * 0.3;
  cx.save(); cx.strokeStyle = '#ffd21e'; cx.lineWidth = 8 * k;
  for (const dx of [-170, 170]) { cx.beginPath(); cx.moveTo(W / 2 + dx * k, -10); cx.lineTo(xm + dx * k, yM - 60 * k); cx.stroke(); }   // altin ipler
  cx.restore();
  const uu = u < b ? 0.3 + 0.2 * Math.sin(t * 3) : 1.3 + (u - b);   // basilmadan SUBSCRIBE (nabiz), yumrukla basilinca SUBSCRIBED + zil
  aboneButon(xm - 30 * k, yM, 0.85 * gir, uu, t, false);       // on kontak 2: 1,0'da zil PLAYER 2 etiketine degiyordu
  const p = 1 + 0.06 * Math.sin(t * 7);
  // on kontak 1: H*0,31'de Kiko ve 3-2-1 ile ust uste biniyordu -> HUD'un hemen alti (PLAYER etiketleri yanlarda, carpismaz)
  if (u < b) yaziK('PUNCH THE BUTTON!', W / 2, H * 0.115, 56 * k * gir * p, ['#ffffff', '#ffe27a', '#ffc21a'], gir, '#5a0010', '#ffffff');
  else if (u < b + 0.6) for (let j = 0; j < 12; j++) {          // basma ani: yildiz patlamasi
    const a = j / 12 * 6.283, r3 = (u - b) / 0.6, dd = (90 + 260 * r3) * k;
    yildiz5(xm + Math.cos(a) * dd * 1.5, yM + Math.sin(a) * dd * 0.6, 16 * k * (1 - r3), j % 2 ? '#ffd21e' : '#ff2d4a', t);
  }
}
function aboneDuvarTam(d, u, t) {                               // motor 34 SUBSCRIBE WALL tam ekran: yarim ekran dugme + imlec + LIKE/COMMENT/SHARE
  const Z = ZD(d), gir = ease(kisit(u / 0.35, 0, 1)), cik = 1 - ease(kisit((u - (Z.gec - 0.35)) / 0.35, 0, 1)), a = gir * cik;
  cx.save(); cx.globalAlpha = a; kartZeminCiz(t, '#ff3a5a', '#7a0a2a'); cx.restore();
  const uu = u + 0.55;                                          // imlec ~0,75 sn'de tiklar
  const zip = 1 + 0.12 * Math.sin(kisit(u / 0.4, 0, 1) * Math.PI);
  yaziK('JOIN THE SKY TEAM!', W / 2, H * 0.17, 92 * k * a, ['#ffffff', '#fff6a0', '#ffd23a'], a, '#5a0010', '#ffffff');
  aboneButon(W / 2 + 40 * k, H * 0.44, 1.45 * a * zip, uu, t, true);
  begenSatiri(W / 2, H * 0.7, 1.55 * a, uu, t);                 // on kontak 1: kucuk kaliyordu
  yaziK(TEMA.aboneAlt, W / 2, H * 0.88, 54 * k * a, ['#fff6a0', '#ffd23a', '#ff9a1a'], a);
  maskotCiz(W * 0.1, H * 0.46 + Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * -12 * k, 1.7 * a, t);   // Kiko ziplar (on kontak 1: kucuktu)
}
function tamEkran(d, u, t) {
  if (d.aboneDuvar) { aboneDuvarTam(d, u, t); return; }
  const Z = ZD(d);""")
degis("  karakterCiz(d, u, t);\n  if (d.ayna && u < b) {",
      "  karakterCiz(d, u, t);\n  if (d.aboneDuvar) aboneDuvarUst(d, u, t);                       // motor 34 SUBSCRIBE WALL\n  if (d.ayna && u < b) {")
degis("function hakemBalon(d, u, t) {                                  // duvar gecerken hakem tepkisi: PERFECT! / BLUE OUT! (renk adi kendi renginde)\n  const Z = ZD(d), b = Z.kart + Z.say; if (u < b + Z.buyu * 0.5) return;",
      "function hakemBalon(d, u, t) {                                  // duvar gecerken hakem tepkisi: PERFECT! / BLUE OUT! (renk adi kendi renginde)\n  const Z = ZD(d), b = Z.kart + Z.say; if (u < b + Z.buyu * 0.5 || d.aboneDuvar) return;   // motor 34: SUBSCRIBE WALL'da balon yok")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
