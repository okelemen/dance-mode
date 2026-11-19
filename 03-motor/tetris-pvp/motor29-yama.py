"""MOTOR 29 (HUMAN TETRIS 32) = sahne28.html (motor 28, 1v1 buzul) + yama -> 03-motor/sahne29.html. sahne28 degismez.

    python motor29-yama.py

32: REF-084 yapi, 3 PLAYER BATTLE (P1 BLUE sol / P2 PINK orta / P3 GREEN sag), gunduz Noel oyuncak atolyesi (varlik-atolye.py,
3 x 640 serit), ozel tur SPEED (motor 26'dan beri d.hiz + d.z), OUT = hediye kutusu yiginina duser (renkli kutular sacilir),
hakem maskot PANDA YAVRUSU (TALIMATLAR §4 maskot sirasi; 2B kafa: beyaz yuvarlak bas, siyah kulak, egik siyah goz lekeleri,
siyah burun, kizarik yanak, kirmizi Noel atkisi; elde seker cubugu), hakem kursusu kirmizi hediye kutusu + altin kurdele.
3 seritte orta serit = P2: hakem orta seridin solunda, P2 karakteri sagda (ikisi de orta seritte, birbirine binmez).
3-2-1 ortada kapilarin ustunde (y 0,205 H), FASTER! ve abone satiri ustte (y 0,12 H; abone varken FASTER! soner).
Giris KANCA (30-31 gibi) ama mekan acilisi farkli: dev hediye kutusu ustten duser, kapagi firlar, icinden konfeti + kurdele firtinasi.
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne28.html")
HEDEF = os.path.join(BURA, "..", "sahne29.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


degis("<title>HUMAN TETRIS 31 - motor 28 (iki serit kutup buzul kiyisi, FREEZE turu, penguen hakem maskot)</title>",
      "<title>HUMAN TETRIS 32 - motor 29 (uc serit Noel oyuncak atolyesi, SPEED turu, panda hakem maskot)</title>")
degis("// MOTOR 28 — HUMAN TETRIS 31 (REF-083 yapi, 18 Kas 2026; motor 27'den, tetris-pvp/motor28-yama.py):",
      "// MOTOR 29 — HUMAN TETRIS 32 (REF-084 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor29-yama.py):\n"
      "//   - UC SERIT (P1 BLUE sol / P2 PINK orta / P3 GREEN sag); sahne tetris-pvp/varlik-atolye.py (3 x 640)\n"
      "//   - OUT hediye kutusu yiginina duser (renkli kutular sacilir); SPEED ROUND (d.hiz)\n"
      "//   - hakem maskot panda yavrusu (2B kafa, kirmizi atki, elde seker cubugu), hediye kutusu kursu\n"
      "//   - giris kanca: BOSS onizleme -> geri sarma -> dev hediye kutusu duser, kapak firlar, konfeti + kurdele\n"
      "// --- motor 28 aciklamasi ---\n"
      "// MOTOR 28 — HUMAN TETRIS 31 (REF-083 yapi, 18 Kas 2026; motor 27'den, tetris-pvp/motor28-yama.py):")

# ---- uc serit
degis("const OY = ['p1', 'p2'];", "const OY = ['p1', 'p2', 'p3'];")
degis("const SW = W / 2;", "const SW = W / 3;")
degis("SERIT.forEach((im, i) => bg.drawImage(im, i * W / 2 - 20, -40, W / 2 + 40, H + 80));",
      "SERIT.forEach((im, i) => bg.drawImage(im, i * SW - 20, -40, SW + 40, H + 80));")
degis("const KR = { p1: {}, p2: {}, maskot: {} };", "const KR = { p1: {}, p2: {}, p3: {}, maskot: {} };")
degis("await Promise.all(['p1', 'p2', 'maskot'].flatMap(o => {", "await Promise.all(['p1', 'p2', 'p3', 'maskot'].flatMap(o => {")
degis("window.KARAKTER_VAR = ['p1', 'p2', 'maskot'].every(", "window.KARAKTER_VAR = ['p1', 'p2', 'p3', 'maskot'].every(")
degis("  for (let i = 0; i < 2; i++) {\n    const K = aciklik(i);", "  for (let i = 0; i < OY.length; i++) {\n    const K = aciklik(i);")
degis("    if (gir > 0.01) yaziK('FASTER!', W / 2, H * 0.165,", "    if (gir > 0.01) yaziK('FASTER!', W / 2, H * 0.12,")
# PLAYER n etiketi biraz asagi (3-2-1 ustte ortada)
degis("yaziK('PLAYER ' + (i + 1), K.x + K.w / 2, K.y - 92 * k, 46 * k,", "yaziK('PLAYER ' + (i + 1), K.x + K.w / 2, K.y - 64 * k, 40 * k,")

degis("    oyuncuEtiket(i, K, 1 - kar);", "    oyuncuEtiket(i, K, (1 - kar) * (i === 1 && u >= a - 0.15 && u < b ? 0 : 1));   // motor 29: 3-2-1 sayilirken ortadaki etiket gizli (ust uste binme)")
# ---- tam ekran panel: uc panel
degis("  for (let i = 0; i < 2; i++) {\n    const x = i * SW;", "  for (let i = 0; i < OY.length; i++) {\n    const x = i * SW;")
degis("    } else yaziK('+1', x + SW * (i ? 0.84 : 0.16), H * 0.2, 120 * k * ps,", "    } else yaziK('+1', x + SW * 0.5, H * 0.2, 110 * k * ps,")
degis("  cx.save(); cx.globalAlpha = a; cx.fillStyle = '#ffffff'; cx.fillRect(SW - 4 * k, 0, 8 * k, H); cx.restore();   // orta ayrim",
      "  cx.save(); cx.globalAlpha = a; cx.fillStyle = '#ffffff'; cx.fillRect(SW - 4 * k, 0, 8 * k, H); cx.fillRect(2 * SW - 4 * k, 0, 8 * k, H); cx.restore();   // serit ayrimlari")
degis("  if (d.out && (d.out.p1 || d.out.p2)) return;                 // biri OUT ise ortadaki ovgu yerine taraf yazilari",
      "  if (d.out && OY.some(o => d.out[o])) return;                 // biri OUT ise ortadaki ovgu yerine taraf yazilari")

# ---- 3-2-1 kapilarin ustunde ortada
degis("    const dus = tasBlok(W / 2, H * 0.37, 118 * k, q);\n    yaziK(String(n), W / 2, H * 0.37 + dus,", "    const dus = tasBlok(W / 2, H * 0.205, 90 * k, q);\n    yaziK(String(n), W / 2, H * 0.205 + dus,")
degis("  yaziK(String(n), W / 2, H * 0.37, 170 * k * s, ['#ffffff', '#ffd6f2', '#ff4ad0'], 1, '#24083e', '#ff6ad6');   // md. 28: alt uc 2,6 -> 6,1",
      "  yaziK(String(n), W / 2, H * 0.205, 120 * k * s, ['#ffffff', '#ffd6f2', '#ff4ad0'], 1, '#24083e', '#ff6ad6');   // motor 29: uc seritte orta kapinin ustu")

# ---- skor: uc kapsul
degis("  let s = { p1: 0, p2: 0 }, son = -1;", "  let s = { p1: 0, p2: 0, p3: 0 }, son = -1;")
st = t.index("  const y = H * 0.055, w = 560 * k, h = 84 * k;")
en = t.index("  const ad = TEMA.turAd[tur] || ('ROUND ' + tur);")
t = t[:st] + """  const y = H * 0.055, w = 780 * k, h = 84 * k;           // motor 29: uc oyuncu - BLUE n | PINK n | GREEN n
  cx.save(); cx.shadowColor = 'rgba(10,30,90,0.5)'; cx.shadowBlur = 18 * k;
  cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(W / 2 - w / 2, y - h / 2, w, h, h / 2); cx.fill(); cx.shadowBlur = 0;
  cx.lineWidth = 6 * k; cx.strokeStyle = KON; cx.stroke();
  const cw = (w - 28 * k) / 3;
  for (let i = 0; i < 3; i++) {
    cx.fillStyle = RENK[i]; cx.beginPath(); cx.roundRect(W / 2 - w / 2 + 7 * k + i * (cw + 7 * k), y - h / 2 + 7 * k, cw, h - 14 * k, (h - 14 * k) / 2); cx.fill();
  }
  cx.restore();
  const KONT = ['#06306e', '#5a0640', '#064a1a'];
  for (let i = 0; i < 3; i++) {
    const xm = W / 2 - w / 2 + 7 * k + i * (cw + 7 * k) + cw / 2;
    yaziK(TEMA.ad[i], xm - 40 * k, y, 42 * k, ['#ffffff', '#ffffff'], 1, KONT[i]);
    yaziK(String(s[OY[i]]), xm + 70 * k, y, 54 * k * pop, ['#ffffff', '#ffffff'], 1, KONT[i]);
  }
""" + t[en:]

# ---- HOW TO PLAY seridi
degis("satir([['COPY THE SHAPE ON YOUR SIDE  ·  ', '#ffffff'], ['BLUE', RENK[0]], [' LEFT  ', '#ffffff'], ['PINK', '#ff6ade'], [' RIGHT', '#ffffff']], W / 2, H * 0.118, 42 * k, a);",
      "satir([['COPY THE SHAPE IN YOUR LANE  ·  ', '#ffffff'], ['BLUE', '#5ab8ff'], [' LEFT  ', '#ffffff'], ['PINK', '#ff6ade'], [' MIDDLE  ', '#ffffff'], ['GREEN', '#5ae87a'], [' RIGHT', '#ffffff']], W / 2, H * 0.118, 40 * k, a);")
degis("satir([['1. PICK A SIDE: ', '#ffffff'], ['BLUE', RENK[0]], [' LEFT · ', '#ffffff'], ['PINK', RENK[1]], [' RIGHT', '#ffffff']], W / 2, H * 0.38, 60 * k, g(0));",
      "satir([['1. PICK A LANE: ', '#ffffff'], ['BLUE', RENK[0]], [' · ', '#ffffff'], ['PINK', RENK[1]], [' · ', '#ffffff'], ['GREEN', RENK[2]]], W / 2, H * 0.38, 60 * k, g(0));")
degis("  for (let i = 0; i < 2; i++) {                                // iki mini kart (serit renkleri)", "  for (let i = 0; i < 3; i++) {                                // uc mini kart (serit renkleri)")
degis("const w = 160 * k, h = 200 * k, x = W / 2 + (i - 0.5) * 230 * k - w / 2, y = H * 0.74;", "const w = 160 * k, h = 200 * k, x = W / 2 + (i - 1) * 230 * k - w / 2, y = H * 0.74;")

# ---- karakterler: uc serit; P2 orta seridin saginda (hakem solunda)
degis("const KAR_BOY = 0.34;", "const KAR_BOY = 0.30;")
degis("const MAS_BOY = 0.32;", "const MAS_BOY = 0.25;")
# video 1 duzeltmesi: hakem duvarlardan SONRA cizilir (kapilarin arasinda, hep onde gorunur)
degis("    if (!tam) hakemCiz(t, d, t - d.t0);                       // maskot kapilarin arasinda; karakterler duvarCiz icinde ustte\n    e = duvarCiz(d, t - d.t0, t);",
      "    e = duvarCiz(d, t - d.t0, t);\n    if (!tam) hakemCiz(t, d, t - d.t0);                       // motor 29: maskot 1.-2. kapi arasinda, duvar ve karakterlerin onunde")
degis("  for (let i = 0; i < 2; i++) {\n    const o = OY[i], ad = d[o], out = d.out && d.out[o], Y = KY[o];",
      "  for (let i = 0; i < OY.length; i++) {\n    const o = OY[i], ad = d[o], out = d.out && d.out[o], Y = KY[o];\n    const yon = i === 0 ? -1 : 1, xs = i * SW + SW / 2;")
degis("      dx = (i ? 1 : -1) * 420 * k * q; dy = 260 * k * q * q - 120 * k * Math.sin(q * Math.PI); don = (i ? 1 : -1) * 1.6 * q;\n"
      "      if (q >= 0.85) sicrama(i * SW + SW / 2 + (i ? 1 : -1) * 400 * k, H * 0.86, (q - 0.85) * Z.buyu * 0.55, 1);",
      "      dx = yon * 300 * k * q; dy = 260 * k * q * q - 120 * k * Math.sin(q * Math.PI); don = yon * 1.6 * q;\n"
      "      if (q >= 0.85) sicrama(xs + yon * 280 * k, H * 0.86, (q - 0.85) * Z.buyu * 0.55, 1);")
degis("    const xm = i * SW + SW / 2 + dx, ay = H * 0.985 + dy - bob;", "    const xm = xs + dx, ay = H * 0.985 + dy - bob;")

# ---- OUT: hediye kutulari sacilir (su sicramasi yerine)
st = t.index("function sicrama(xm, ym, u, olc = 1) {")
en = t.index("function karakterCiz(d, u, t) {")
t = t[:st] + """function sicrama(xm, ym, u, olc = 1) {                        // motor 29: hediye kutusu yigini sacilir (renkli kutu + altin kurdele + yildiz)
  if (u < 0 || u > 1.6) return;
  const q = u / 1.6, R2 = rng(4711 + Math.round(xm));
  const KR6 = ['#e8102c', '#14a83a', '#ffc21a', '#8a2ae8', '#1e7cff', '#ff2aa0'];
  cx.save(); cx.globalAlpha = 1 - q * q;
  for (let j = 0; j < 16; j++) {
    const a = -Math.PI * (0.1 + 0.8 * R2()), v = (260 + 420 * R2()) * k * olc, tt = u, r = (18 + 22 * R2()) * k * olc;
    const x = xm + Math.cos(a) * v * tt * 0.6, y = ym + Math.sin(a) * v * tt + 900 * k * tt * tt;
    cx.save(); cx.translate(x, y); cx.rotate((R2() - 0.5) * 8 * tt);
    cx.fillStyle = KR6[j % 6]; cx.strokeStyle = '#3a1478'; cx.lineWidth = 3 * k;
    cx.beginPath(); cx.roundRect(-r, -r, 2 * r, 2 * r, r * 0.2); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffd21e'; cx.fillRect(-r * 0.16, -r, r * 0.32, 2 * r); cx.fillRect(-r, -r * 0.16, 2 * r, r * 0.32);
    cx.restore();
  }
  for (let j = 0; j < 10; j++) { const a = j / 10 * 6.283, dd = (60 + 260 * q) * k * olc; yildiz5(xm + Math.cos(a) * dd, ym - 40 * k + Math.sin(a) * dd * 0.6, 14 * k * olc * (1 - q), '#ffd21e', u); }
  cx.restore();
}
""" + t[en:]

# ---- hakem: orta seridin solunda; isaret oku hangi oyuncu
degis("  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;", "  const xm = SW, y0 = H * 0.61, w = 130 * k, h = 70 * k;   // motor 29 (video 1 duzeltmesi): kursu 1. ve 2. kapinin arasinda")
st = t.index("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#7ae8ff'); g.addColorStop(1, '#0a6ad8');   // motor 28: buz blogu kursu")
en = t.index("  cx.restore();\n}\nfunction hakemCiz(t, d, u) {")
t = t[:st] + """  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ff3a4a'); g.addColorStop(1, '#b8081c');   // motor 29: kirmizi hediye kutusu kursu
  cx.fillStyle = g; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd21e'; cx.fillRect(xm - 12 * k, y0 + 3 * k, 24 * k, h); cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 14 * k);   // altin kurdele
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(xm - w / 2 + 10 * k, y0 + 6 * k, w - 20 * k, 10 * k, 5 * k); cx.fill();
  for (const s of [-1, 1]) yildiz5(xm + s * w * 0.6, y0 - 26 * k, 20 * k, '#ffd21e', t * s);   // motor 29: iki altin yildiz
""" + t[en:]
degis("  const xm = W / 2, ay = H * 0.935, Y = KY.maskot;", "  const xm = SW, ay = H * 0.615, Y = KY.maskot;   // motor 29 (kullanici: maskot kapilarin arasinda, onde kalmasin, hep gorunsun)")
degis("      const yari = sq < 0.5 ? 0 : 1, q = (sq - yari * 0.5) / 0.5;\n      ad = d[OY[yari]]; isaret = yari ? 1 : -1;",
      "      const yari = Math.min(2, Math.floor(sq * 3)), q = sq * 3 - yari;   // motor 29: uc oyuncunun pozunu sirayla gosterir\n      ad = d[OY[yari]]; isaret = yari + 1;")
degis("    } else ad = d.p2;\n  }", "    } else ad = d.p3;\n  }")
degis("  if (d && u >= ZD(d).kart + ZD(d).say + ZD(d).buyu * 0.5) MASKOT_DUYGU = (d.out && (d.out.p1 || d.out.p2)) ? 'sasirma' : 'sevinc';",
      "  if (d && u >= ZD(d).kart + ZD(d).say + ZD(d).buyu * 0.5) MASKOT_DUYGU = (d.out && OY.some(o => d.out[o])) ? 'sasirma' : 'sevinc';")
degis("  cx.save(); cx.shadowColor = '#7ae0ff'; cx.shadowBlur = 24 * k;   // motor 28: buz dunyasi hakem isiltisi",
      "  cx.save(); cx.shadowColor = '#ffd21e'; cx.shadowBlur = 24 * k;   // motor 29: altin hakem isiltisi")
degis("    const i = isaret > 0 ? 1 : 0, ox = xm + isaret * 230 * k, oy = H * 0.62;\n"
      "    cx.save(); cx.fillStyle = RENK[i]; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k; cx.translate(ox + Math.sin(t * 8) * 8 * k * isaret, oy);\n"
      "    cx.scale(isaret, 1);",
      "    const i = isaret - 1, hx = i * SW + SW / 2, ox = xm + (hx - xm) * 0.45, oy = H * 0.5, aci = Math.atan2(0, hx - xm + 1);\n"
      "    cx.save(); cx.fillStyle = RENK[i]; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k; cx.translate(ox + Math.sin(t * 8) * 8 * k * Math.cos(aci), oy);\n"
      "    cx.rotate(aci);")
degis("  else satir([[outlar[0] === 'p1' ? 'BLUE' : 'PINK', ['#ffffff', RENK[outlar[0] === 'p1' ? 0 : 1]]], [' OUT!', ['#ffffff', '#ff8a8a', '#ff1a2a']]], W / 2, y, 64 * k * s, q);",
      "  else satir([[TEMA.ad[OY.indexOf(outlar[0])], ['#ffffff', RENK[OY.indexOf(outlar[0])]]], [' OUT!', ['#ffffff', '#ff8a8a', '#ff1a2a']]], W / 2, y, 64 * k * s, q);")

degis("  if (!outlar.length) yaziK(d.ovgu || 'PERFECT!', W / 2, y, 64 * k * s, ['#fff6a0', '#ffd23a', '#ff8a1a'], q);",
      "  if (!outlar.length) yaziK(d.ovgu || 'PERFECT!', W / 2, y, 64 * k * s, ['#fff6a0', '#ffd23a', '#ff8a1a'], q);\n"
      "  else if (outlar.length > 1) satir([...outlar.flatMap((o, j) => [[(j ? ' & ' : '') , ['#ffffff', '#ffffff']], [TEMA.ad[OY.indexOf(o)], ['#ffffff', RENK[OY.indexOf(o)]]]]).slice(1), [' OUT!', ['#ffffff', '#ff8a8a', '#ff1a2a']]], W / 2, y, 56 * k * s, q);   // motor 29: BOSS'ta iki OUT")

# ---- sonuc karti: uc oyuncu
degis("  const i = kart.kazanan === 'p1' ? 0 : 1, gir = ease(kisit(u / 0.4, 0, 1)), s = gir * (1 + 0.12 * Math.sin(gir * Math.PI));",
      "  const i = OY.indexOf(kart.kazanan), gir = ease(kisit(u / 0.4, 0, 1)), s = gir * (1 + 0.12 * Math.sin(gir * Math.PI));")
degis("  satir([[i ? 'PINK' : 'BLUE', ['#ffffff', ACIK[i], RENK[i]]], [' WINS!', KART_DOLGU]], W / 2, H * 0.17, 150 * k * s, 1);\n"
      "  satir([['BLUE ', ['#ffffff', ACIK[0], RENK[0]]], [String(kart.skor.p1) + ' - ' + String(kart.skor.p2), KART_DOLGU], [' PINK', ['#ffffff', ACIK[1], RENK[1]]]], W / 2, H * 0.36, 90 * k * s, 1);",
      "  satir([[TEMA.ad[i], ['#ffffff', ACIK[i], RENK[i]]], [' WINS!', KART_DOLGU]], W / 2, H * 0.17, 150 * k * s, 1);\n"
      "  satir([['BLUE ', ['#ffffff', ACIK[0], RENK[0]]], [String(kart.skor.p1) + '  ', KART_DOLGU], ['PINK ', ['#ffffff', ACIK[1], RENK[1]]], [String(kart.skor.p2) + '  ', KART_DOLGU],\n"
      "         ['GREEN ', ['#ffffff', ACIK[2], RENK[2]]], [String(kart.skor.p3), KART_DOLGU]], W / 2, H * 0.36, 80 * k * s, 1);")

# ---- acilis sorusu
degis("satir([['WHO WILL WIN? ', KART_DOLGU], ['BLUE', ['#ffffff', ACIK[0], RENK[0]]], [' OR ', KART_DOLGU], ['PINK', ['#ffffff', ACIK[1], RENK[1]]], ['?', KART_DOLGU]], W / 2, H * 0.13, 84 * k * acilisSoru, acilisSoru);",
      "satir([['WHO WILL WIN? ', KART_DOLGU], ['BLUE', ['#ffffff', ACIK[0], RENK[0]]], [', ', KART_DOLGU], ['PINK', ['#ffffff', ACIK[1], RENK[1]]], [' OR ', KART_DOLGU], ['GREEN', ['#ffffff', ACIK[2], RENK[2]]], ['?', KART_DOLGU]], W / 2, H * 0.13, 76 * k * acilisSoru, acilisSoru);")
degis("cx.roundRect(W / 2 - 620 * k, H * 0.13 - 62 * k, 1240 * k, 124 * k, 62 * k); cx.fill(); cx.restore();\n      satir([['WHO WILL WIN? '",
      "cx.roundRect(W / 2 - 780 * k, H * 0.13 - 62 * k, 1560 * k, 124 * k, 62 * k); cx.fill(); cx.restore();\n      satir([['WHO WILL WIN? '")

# ---- abone satiri ustte (3-2-1 ortada kapilarin ustunde)
degis("  aboneButon(W / 2, H * 0.18, ease(gir) * zip * cik * 0.62, u, t);\n  begenSatiri(W / 2, H * 0.265, cik * 0.5, u, t);",
      "  aboneButon(W / 2 - 330 * k, H * 0.125, ease(gir) * zip * cik * 0.56, u, t);   // motor 29: uc seritte 3-2-1 ortada -> abone satiri ustte, yan yana\n"
      "  begenSatiri(W / 2 + 300 * k, H * 0.125, cik * 0.56, u, t);")

# ---- konfeti: Noel renkleri
degis("const KONF_R = ['#ffffff', '#c8f2ff', '#7ae0ff', '#3ac0ff', '#ffffff', '#e6faff'];   // motor 28: kar taneleri",
      "const KONF_R = ['#e8102c', '#14a83a', '#ffd21e', '#ff2aa0', '#1e7cff', '#ffffff'];   // motor 29: Noel konfetisi")

# ---- kanca acilisi: dev hediye kutusu
st = t.index("  const dus = kisit(ua / 0.35, 0, 1);                           // motor 28: buz kutlesi ustten kopar, ekranin ortasina duser")
en = t.index("  if (ua < 0.18) { cx.save(); cx.fillStyle = `rgba(255,255,255,${0.85 * (1 - ua / 0.18)})`; cx.fillRect(0, 0, W, H); cx.restore(); }")
t = t[:st] + """  const dus = kisit(ua / 0.35, 0, 1);                           // motor 29: dev hediye kutusu ustten duser, kapagi firlar
  if (ua < 1.0) {
    const yb = lerp(-H * 0.4, H * 0.66, dus * dus), al = 1 - kisit((ua - 0.6) / 0.4, 0, 1), r = H * 0.2;
    const kp = kisit((ua - 0.36) / 0.3, 0, 1);                   // kapak: carpinca yukari firlar, doner
    cx.save(); cx.globalAlpha = al; cx.translate(W / 2, yb);
    const gk = cx.createLinearGradient(0, -r, 0, r); gk.addColorStop(0, '#ff3a4a'); gk.addColorStop(1, '#b8081c');
    cx.fillStyle = gk; cx.strokeStyle = '#3a1478'; cx.lineWidth = 10 * k; cx.beginPath(); cx.roundRect(-r * 1.1, -r * 0.8, r * 2.2, r * 1.8, r * 0.12); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffd21e'; cx.fillRect(-r * 0.14, -r * 0.8, r * 0.28, r * 1.8);
    cx.save(); cx.translate(0, -r * 0.8 - kp * H * 0.5); cx.rotate(kp * 2.4);
    cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(-r * 1.25, -r * 0.32, r * 2.5, r * 0.36, r * 0.08); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffd21e'; cx.fillRect(-r * 0.16, -r * 0.32, r * 0.32, r * 0.36);
    for (const s of [-1, 1]) { cx.beginPath(); cx.ellipse(s * r * 0.3, -r * 0.5, r * 0.3, r * 0.17, s * 0.5, 0, 6.283); cx.fill(); cx.stroke(); }
    cx.restore(); cx.restore();
  }
  if (ua > 0.33) sicrama(W / 2, H * 0.6, (ua - 0.33) * 1.2, 2.4);   // kutudan hediyeler sacilir
  const R = rng(3131);                                          // motor 29: konfeti + kurdele firtinasi ortadan disa
  for (let j = 0; j < 120; j++) {
    const a = R() * 6.283, hz = 0.6 + 0.9 * R(), c = KONF_R[Math.floor(R() * 6)], r = (10 + 18 * R()) * k;
    const d0 = kisit((ua - 0.36) * hz * 1.4, 0, 2) * W * 0.6;
    if (d0 <= 0) break;
    const x = W / 2 + Math.cos(a) * d0, y = H * 0.55 + Math.sin(a) * d0 * 0.6 + 200 * k * (ua - 0.36) ** 2;
    if (x < -60 * k || x > W + 60 * k || y > H + 60 * k) continue;
    cx.save(); cx.translate(x, y); cx.rotate(a + ua * 6 * hz); cx.scale(1, 0.4 + 0.6 * Math.abs(Math.sin(ua * 7 * hz + a * 5)));
    cx.fillStyle = c; cx.fillRect(-r, -r * 0.4, 2 * r, r * 0.8);
    cx.restore();
  }
""" + t[en:]
degis("  if (pa > 0.01) for (let i = 0; i < 2; i++) pYazi(['P1', 'P2'][i], i * SW + SW / 2, H * 0.6, 150 * k, RENK[i], pa);",
      "  if (pa > 0.01) for (let i = 0; i < 3; i++) pYazi(['P1', 'P2', 'P3'][i], i * SW + SW / 2, H * 0.6, 130 * k, RENK[i], pa);")

# ---- maskot: panda kafasi + seker cubugu
degis("  if (!yuzSadece) balikCiz(x + (78 + bs) * s * k, y - 60 * s * k, 20 * s * k, t);   // motor 28: elde sari balik",
      "  if (!yuzSadece) sekerCiz(x + (78 + bs) * s * k, y - 60 * s * k, 26 * s * k, t);   // motor 29: elde seker cubugu")
st = t.index("  // motor 28: PENGUEN YAVRUSU kafasi (TALIMATLAR §4 maskot sirasi; kendi tasarimimiz)")
en = t.index("  cx.restore();\n  cx.restore();\n}\n// alt orta: iki seridin")
t = t[:st] + """  // motor 29: PANDA YAVRUSU kafasi (TALIMATLAR §4 maskot sirasi; kendi tasarimimiz)
  for (const sx of [-1, 1]) {                                   // siyah yuvarlak kulaklar
    cx.fillStyle = '#16161e'; cx.strokeStyle = '#000000'; cx.lineWidth = 4; cx.beginPath(); cx.arc(sx * 50, -50, 24, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = '#ff9ac0'; cx.beginPath(); cx.arc(sx * 50, -50, 10, 0, 6.283); cx.fill();
  }
  const gv = cx.createRadialGradient(-18, -26, 8, 0, 0, 74); gv.addColorStop(0, '#ffffff'); gv.addColorStop(1, '#dfe4ee');
  cx.fillStyle = gv; cx.strokeStyle = '#16161e'; cx.lineWidth = 5; cx.beginPath(); cx.ellipse(0, -2, 66, 58, 0, 0, 6.283); cx.fill(); cx.stroke();
  for (const sx of [-1, 1]) {                                   // egik siyah goz lekeleri + gozler: 3 duygu (mutlu / sevinc / sasirma)
    cx.fillStyle = '#16161e'; cx.beginPath(); cx.ellipse(sx * 22, -2, 17, 22, sx * -0.5, 0, 6.283); cx.fill();
    if (MASKOT_DUYGU === 'sevinc') {                            // PERFECT: kapali ^^ gozler
      cx.strokeStyle = '#ffffff'; cx.lineWidth = 5; cx.lineCap = 'round';
      cx.beginPath(); cx.arc(sx * 22, 2, 9, Math.PI * 1.15, Math.PI * 1.85); cx.stroke();
    } else if (MASKOT_DUYGU === 'sasirma') {                    // OUT: iri beyaz gozler, kucuk bebek
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 22, -4, 12, 0, 6.283); cx.fill();
      cx.fillStyle = '#16161e'; cx.beginPath(); cx.arc(sx * 22, -2, 5, 0, 6.283); cx.fill();
    } else {
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 22, -4, 9, 0, 6.283); cx.fill();
      cx.fillStyle = '#16161e'; cx.beginPath(); cx.arc(sx * 22 + 1, -2, 5.5, 0, 6.283); cx.fill();
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 22 - 1, -5, 2, 0, 6.283); cx.fill();
    }
    cx.fillStyle = 'rgba(255,110,150,0.6)'; cx.beginPath(); cx.ellipse(sx * 42, 22, 10, 6, 0, 0, 6.283); cx.fill();   // kizarik yanak
  }
  cx.fillStyle = '#16161e'; cx.beginPath(); cx.ellipse(0, 18, 10, 7, 0, 0, 6.283); cx.fill();   // burun
  cx.strokeStyle = '#16161e'; cx.lineWidth = 3; cx.lineCap = 'round';
  if (MASKOT_DUYGU === 'sasirma') { cx.beginPath(); cx.ellipse(0, 34, 7, 9, 0, 0, 6.283); cx.stroke(); }
  else { cx.beginPath(); cx.moveTo(0, 24); cx.quadraticCurveTo(-8, 34, -15, 28); cx.moveTo(0, 24); cx.quadraticCurveTo(8, 34, 15, 28); cx.stroke(); }
  cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.ellipse(-22, -38, 18, 8, -0.4, 0, 6.283); cx.fill();   // cilali isilti
  cx.strokeStyle = '#3a0a10'; cx.lineWidth = 3;                // kirmizi Noel atkisi, yesil serit
  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(-46, 46, 92, 18, 9); cx.fill(); cx.stroke();
  cx.fillStyle = '#14a83a'; for (const xx of [-30, -6, 18]) { cx.fillRect(xx, 47, 9, 16); }
  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(22, 56, 18, 34, 6); cx.fill(); cx.stroke();
  cx.fillStyle = '#14a83a'; cx.fillRect(23, 68, 16, 7);
""" + t[en:]
# seker cubugu cizimi (balikCiz'in yanina)
degis("function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {",
      """function sekerCiz(x, y, r, t) {                               // motor 29: kirmizi-beyaz seker cubugu (hafif sallanir)
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2.2) * 0.12);
  cx.lineCap = 'round'; cx.lineWidth = r * 0.42;
  cx.strokeStyle = '#3a1478'; cx.lineWidth = r * 0.55; cx.beginPath(); cx.moveTo(0, r * 1.6); cx.lineTo(0, -r * 0.3); cx.arc(-r * 0.5, -r * 0.3, r * 0.5, 0, Math.PI, true); cx.stroke();
  cx.strokeStyle = '#ffffff'; cx.lineWidth = r * 0.4; cx.beginPath(); cx.moveTo(0, r * 1.6); cx.lineTo(0, -r * 0.3); cx.arc(-r * 0.5, -r * 0.3, r * 0.5, 0, Math.PI, true); cx.stroke();
  cx.strokeStyle = '#e8102c'; cx.lineWidth = r * 0.4; cx.setLineDash([r * 0.3, r * 0.3]); cx.beginPath(); cx.moveTo(0, r * 1.6); cx.lineTo(0, -r * 0.3); cx.arc(-r * 0.5, -r * 0.3, r * 0.5, 0, Math.PI, true); cx.stroke();
  cx.setLineDash([]); cx.restore();
}
function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {""")
# kepenk neon: panda yuzu
st = t.index("  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.92, 0, 0, 6.283); cx.stroke();                        // motor 28: Nilo neon yuzu - bas")
en = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:st] + """  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.88, 0, 0, 6.283); cx.stroke();                        // motor 29: panda neon yuzu - bas
  for (const sx of [-1, 1]) {
    cx.beginPath(); cx.arc(mx + sx * r * 0.78, my - r * 0.78, r * 0.32, 0, 6.283); cx.stroke();          // kulaklar
    cx.beginPath(); cx.ellipse(mx + sx * r * 0.34, my - r * 0.02, r * 0.24, r * 0.32, sx * -0.5, 0, 6.283); cx.stroke();   // goz lekeleri
  }
  cx.beginPath(); cx.ellipse(mx, my + r * 0.3, r * 0.14, r * 0.1, 0, 0, 6.283); cx.stroke();   // burun
""" + t[en:]

# kalan iki-oyuncu izi kalmasin
assert "i < 2;" not in t.split("function nasilKart")[0].split("function duvarCiz")[1], "duvarCiz/karakterCiz'de 2 kaldi"
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF)
