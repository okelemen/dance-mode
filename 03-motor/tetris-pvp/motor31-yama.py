"""MOTOR 31 (HUMAN TETRIS 34) = sahne29.html (motor 29, 3 serit Noel atolyesi) + yama -> 03-motor/sahne31.html. sahne29 degismez.

    python motor31-yama.py

34: REF-086 yapi, 3P CO-OP (P1 BLUE sol / P2 PINK orta / P3 GREEN sag; uc kapi yan yana = takimin ortak formasyonu), gunduz oyuncak
blok sehri (varlik-blok.py, 3 x 640), ozel tur MIRROR (motor 23'ten beri d.ayna; motorda hazir), OUT = blok yiginina duser (bloklar
sacilir), hakem maskot JOLE KUP (TALIMATLAR §4 maskot sirasi; govde Blender'da kup, yuz 2B: kupun ust yarisina iri gozler, kizarik
yanak, gulumseme; elde kucuk oyuncak blok), hakem kursusu ust uste uc blok.
CO-OP skor (mobil paket md. 3): ustte ortada WALLS CLEARED n/24 (d.skor = takimin gectigi duvar sayisi); sonda TEAM SCORE + rutbe.
Acilis sorusu "CAN YOUR TEAM CLEAR ALL 24?" (mobil paket md. 5), cevabi sonuc kartinda.
Giris KANCA (30-33 gibi) ama mekan acilisi farkli: gokten dev bloklar dusup kule olur, kule devrilir, bloklar + konfeti sacilir.
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne29.html")
HEDEF = os.path.join(BURA, "..", "sahne31.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


degis("<title>HUMAN TETRIS 32 - motor 29 (uc serit Noel oyuncak atolyesi, SPEED turu, panda hakem maskot)</title>",
      "<title>HUMAN TETRIS 34 - motor 31 (uc serit CO-OP oyuncak blok sehri, MIRROR turu, jole kup hakem maskot)</title>")
degis("// MOTOR 29 — HUMAN TETRIS 32 (REF-084 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor29-yama.py):",
      "// MOTOR 31 — HUMAN TETRIS 34 (REF-086 yapi, 20 Kas 2026; motor 29'dan, tetris-pvp/motor31-yama.py):\n"
      "//   - 3P CO-OP: uc serit ayni (P1 BLUE sol / P2 PINK orta / P3 GREEN sag); sahne tetris-pvp/varlik-blok.py (3 x 640)\n"
      "//   - ustte WALLS CLEARED n/24 (takim); sonda TEAM SCORE + rutbe; acilis sorusu CAN YOUR TEAM CLEAR ALL 24?\n"
      "//   - OUT blok yiginina duser (bloklar sacilir); MIRROR ROUND (d.ayna)\n"
      "//   - hakem maskot jole kup (3B kup govde + 2B yuz, elde oyuncak blok), blok kursu\n"
      "//   - giris kanca: BOSS onizleme -> geri sarma -> gokten bloklar duser, kule olur, devrilir, konfeti\n"
      "// --- motor 29 aciklamasi ---\n"
      "// MOTOR 29 — HUMAN TETRIS 32 (REF-084 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor29-yama.py):")

# ---- elde oyuncak blok (seker cubugu yerine)
degis("function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {",
      "function blokCiz(x, y, r, t, renk = '#1e7cff') {                // motor 31: maskotun elinde kucuk oyuncak blok (hafif doner)\n"
      "  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2.2) * 0.25);\n"
      "  cx.fillStyle = renk; cx.strokeStyle = '#1a0630'; cx.lineWidth = r * 0.16; cx.beginPath(); cx.roundRect(-r, -r, 2 * r, 2 * r, r * 0.3); cx.fill(); cx.stroke();\n"
      "  cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.roundRect(-r * 0.7, -r * 0.75, r * 0.9, r * 0.32, r * 0.16); cx.fill();\n"
      "  cx.restore();\n"
      "}\n"
      "function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {")
degis("  if (!yuzSadece) sekerCiz(x + (78 + bs) * s * k, y - 60 * s * k, 26 * s * k, t);   // motor 29: elde seker cubugu",
      "  if (!yuzSadece) blokCiz(x + (84 + bs) * s * k, y - 40 * s * k, 24 * s * k, t);   // motor 31: elde oyuncak blok")

# ---- panda kafasi -> jole kup yuzu (yuzSadece: Blender kupunun ustune yalniz yuz; degilse 2B kup + yuz)
i0 = t.index("  // motor 29: PANDA YAVRUSU kafasi")
i1 = t.index("  cx.restore();\n  cx.restore();\n}\n// alt orta:")
t = t[:i0] + """  // motor 31: JOLE KUP (TALIMATLAR §4 maskot sirasi; kendi tasarimimiz). yuzSadece = 3B kup govdenin uzerine yalniz yuz
  if (yuzSadece) { cx.translate(0, TEMA.yuzDy || 0); cx.scale(TEMA.yuzOlcek || 1, TEMA.yuzOlcek || 1); }
  if (!yuzSadece) {                                             // kartlarda / acilista: 2B tombul jole kup
    const gv = cx.createLinearGradient(0, -70, 0, 70); gv.addColorStop(0, '#ffb040'); gv.addColorStop(1, '#e85a00');
    cx.fillStyle = gv; cx.strokeStyle = '#7a2600'; cx.lineWidth = 6; cx.beginPath(); cx.roundRect(-70, -70, 140, 140, 30); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.roundRect(-52, -58, 54, 16, 8); cx.fill();   // cilali isilti
  }
  for (const sx of [-1, 1]) {                                   // iri gozler: 3 duygu (mutlu / sevinc / sasirma)
    if (MASKOT_DUYGU === 'sevinc') {                            // PERFECT: kapali ^^ gozler
      cx.strokeStyle = '#2a0a00'; cx.lineWidth = 7; cx.lineCap = 'round';
      cx.beginPath(); cx.arc(sx * 24, -6, 12, Math.PI * 1.15, Math.PI * 1.85); cx.stroke();
    } else if (MASKOT_DUYGU === 'sasirma') {                    // OUT: iri beyaz gozler, kucuk bebek
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#2a0a00'; cx.lineWidth = 4; cx.beginPath(); cx.arc(sx * 24, -8, 17, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = '#2a0a00'; cx.beginPath(); cx.arc(sx * 24, -6, 6, 0, 6.283); cx.fill();
    } else {
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#2a0a00'; cx.lineWidth = 4; cx.beginPath(); cx.ellipse(sx * 24, -8, 15, 18, 0, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = '#2a0a00'; cx.beginPath(); cx.arc(sx * 24 + 2, -5, 9, 0, 6.283); cx.fill();
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 24 - 1, -10, 3.5, 0, 6.283); cx.fill();
    }
    cx.fillStyle = 'rgba(255,60,90,0.55)'; cx.beginPath(); cx.ellipse(sx * 46, 18, 12, 7, 0, 0, 6.283); cx.fill();   // kizarik yanak
  }
  cx.strokeStyle = '#2a0a00'; cx.lineWidth = 5; cx.lineCap = 'round';
  if (MASKOT_DUYGU === 'sasirma') { cx.fillStyle = '#7a1020'; cx.beginPath(); cx.ellipse(0, 30, 9, 12, 0, 0, 6.283); cx.fill(); cx.stroke(); }
  else { cx.fillStyle = '#7a1020'; cx.beginPath(); cx.moveTo(-20, 22); cx.quadraticCurveTo(0, 46, 20, 22); cx.closePath(); cx.fill(); cx.stroke(); }
  cx.fillStyle = '#e8102c'; cx.strokeStyle = '#3a0a10'; cx.lineWidth = 3;                    // kirmizi hakem duduğu (ip boyunda)
  cx.beginPath(); cx.roundRect(34, 58, 26, 13, 6); cx.fill(); cx.stroke();
  cx.strokeStyle = '#ffd21e'; cx.lineWidth = 2.5; cx.beginPath(); cx.moveTo(36, 64); cx.quadraticCurveTo(0, 74, -36, 56); cx.stroke();
""" + t[i1:]

# ---- kepenk: panda neon yuzu -> jole kup neon yuzu
i0 = t.index("  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.88, 0, 0, 6.283); cx.stroke();                        // motor 29: panda neon yuzu - bas")
i1 = t.index("  cx.shadowBlur = 0;\n  for (const [dx, dy] of [[-1.5, -0.6]")
t = t[:i0] + """  cx.beginPath(); cx.roundRect(mx - r, my - r, 2 * r, 2 * r, r * 0.35); cx.stroke();                 // motor 31: jole kup neon yuzu
  for (const sx of [-1, 1]) { cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.12, r * 0.18, r * 0.22, 0, 0, 6.283); cx.stroke(); }   // gozler
  cx.beginPath(); cx.moveTo(mx - r * 0.3, my + r * 0.3); cx.quadraticCurveTo(mx, my + r * 0.62, mx + r * 0.3, my + r * 0.3); cx.stroke();   // gulumseme
""" + t[i1:]

# ---- OUT: hediye kutusu -> duz oyuncak bloklar (kurdele yok)
degis("function sicrama(xm, ym, u, olc = 1) {                        // motor 29: hediye kutusu yigini sacilir (renkli kutu + altin kurdele + yildiz)",
      "function sicrama(xm, ym, u, olc = 1) {                        // motor 31: blok yigini sacilir (renkli oyuncak bloklar + yildiz)")
degis("    cx.fillStyle = '#ffd21e'; cx.fillRect(-r * 0.16, -r, r * 0.32, 2 * r); cx.fillRect(-r, -r * 0.16, 2 * r, r * 0.32);\n",
      "    cx.fillStyle = 'rgba(255,255,255,0.4)'; cx.beginPath(); cx.roundRect(-r * 0.7, -r * 0.75, r * 0.9, r * 0.3, r * 0.15); cx.fill();\n")

# ---- kursu: hediye kutusu -> ust uste uc blok
i0 = t.index("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ff3a4a'); g.addColorStop(1, '#b8081c');   // motor 29: kirmizi hediye kutusu kursu")
i1 = t.index("  for (const s of [-1, 1]) yildiz5(xm + s * w * 0.6, y0 - 26 * k, 20 * k, '#ffd21e', t * s);   // motor 29: iki altin yildiz")
t = t[:i0] + """  [['#e8102c', 0, 1.0], ['#ffc21a', 1, 0.82], ['#1e7cff', 2, 0.64]].forEach(([c, j, gw]) => {   // motor 31: ust uste uc oyuncak blok (alttan buyuge)
    const bh = h / 3 + 4 * k, by = y0 + h - (j + 1) * (h / 3), bw = w * gw;
    cx.fillStyle = c; cx.strokeStyle = '#ffffff'; cx.lineWidth = 5 * k; cx.beginPath(); cx.roundRect(xm - bw / 2, by, bw, bh, 9 * k); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(xm - bw / 2 + 8 * k, by + 4 * k, bw * 0.45, 6 * k, 3 * k); cx.fill();
  });
""" + t[i1:]

# ---- CO-OP skor: ustte ortada WALLS CLEARED n/24 (d.skor = sayi)
i0 = t.index("function skorBul(t) {")
i1 = t.index("// ilk iki duvarda ustte HOW TO PLAY seridi")
t = t[:i0] + """function skorBul(t) {                                          // motor 31: CO-OP - d.skor takimin gectigi duvar sayisi
  let s = 0, son = -1, onceki = 0;
  for (const d of DUVARLAR) { const Z = ZD(d); const tt = d.t0 + Z.kart + Z.say + Z.buyu; if (t >= tt) { if (d.skor !== onceki) son = tt; s = d.skor; onceki = d.skor; } }
  return [s, son];
}
// motor 31: ustte ortada WALLS CLEARED n/24 (mobil paket md. 3, CO-OP; motor 24 kapsulu), solda tur adi
function hudCiz(t, tur) {
  const [s, son] = skorBul(t), pop = son >= 0 && t - son < 0.5 ? 1 + 0.35 * Math.sin((t - son) / 0.5 * Math.PI) : 1;
  const w = 520 * k, h = 84 * k, xm = W / 2, y = H * 0.055;
  cx.save(); cx.shadowColor = 'rgba(10,30,90,0.5)'; cx.shadowBlur = 18 * k;
  cx.fillStyle = '#ffffff'; cx.beginPath(); cx.roundRect(xm - w / 2, y - h / 2, w, h, h / 2); cx.fill(); cx.shadowBlur = 0;
  cx.lineWidth = 6 * k; cx.strokeStyle = KON; cx.stroke();
  cx.fillStyle = '#ff7a10'; cx.beginPath(); cx.roundRect(xm - w / 2 + 7 * k, y - h / 2 + 7 * k, 310 * k, h - 14 * k, (h - 14 * k) / 2); cx.fill();
  cx.restore();
  yaziK('WALLS CLEARED', xm - w / 2 + 162 * k, y, 36 * k, ['#ffffff', '#ffffff'], 1, '#5a1a00');
  yaziK(s + '/' + TOPLAM_DUVAR, xm + w / 2 - 98 * k, y, 54 * k * pop, ['#ffffff', '#ffe0b0', '#ff7a10'], 1, '#24083e');
  const ad = TEMA.turAd[tur] || ('ROUND ' + tur);
  cx.font = F(52 * k); const yw = cx.measureText(ad).width;
  yaziK(ad, Math.max(190 * k, yw / 2 + 34 * k), H * 0.055, 52 * k, ['#f0fff8', '#7affd0', '#1ac8a0'], 1);
}
""" + t[i1:]
degis("  satir([['COPY THE SHAPE IN YOUR LANE  ·  ', '#ffffff'],", "  satir([['TEAM UP! COPY YOUR SHAPE  ·  ', '#ffffff'],")

# ---- acilis: dev hediye kutusu -> gokten bloklar dusup kule olur, kule devrilir
i0 = t.index("  const dus = kisit(ua / 0.35, 0, 1);                           // motor 29: dev hediye kutusu ustten duser, kapagi firlar")
i1 = t.index("  const R = rng(3131);                                          // motor 29: konfeti + kurdele firtinasi ortadan disa")
t = t[:i0] + """  const KUL = ['#e8102c', '#ffc21a', '#1e7cff', '#18c840', '#ff6a10', '#8a2ae8'], bs = H * 0.085;   // motor 31: blok kulesi
  if (ua < 0.95) {
    const dev = kisit((ua - 0.62) / 0.3, 0, 1);                 // devrilme
    cx.save(); cx.globalAlpha = 1 - kisit((ua - 0.8) / 0.15, 0, 1);
    cx.translate(W / 2 + bs, H * 0.70); cx.rotate(dev * dev * 1.4); cx.translate(-W / 2 - bs, -H * 0.70);
    for (let j = 0; j < 6; j++) {
      const d0 = j * 0.09, q = kisit((ua - d0) / 0.14, 0, 1);    // her blok sirayla duser
      if (q <= 0) continue;
      const yh = H * 0.70 - (j + 1) * bs * 2, y = lerp(-H * 0.3, yh, q * q), sq = q >= 1 ? 1 + 0.12 * Math.exp(-(ua - d0 - 0.14) * 20) : 1;
      cx.save(); cx.translate(W / 2, y + bs); cx.scale(sq, 2 - sq); cx.translate(-W / 2, -y - bs);
      cx.fillStyle = KUL[j]; cx.strokeStyle = '#1a0630'; cx.lineWidth = 8 * k; cx.beginPath(); cx.roundRect(W / 2 - bs * 1.3, y, bs * 2.6, bs * 2, bs * 0.3); cx.fill(); cx.stroke();
      cx.fillStyle = 'rgba(255,255,255,0.4)'; cx.beginPath(); cx.roundRect(W / 2 - bs * 1.05, y + bs * 0.2, bs * 1.2, bs * 0.3, bs * 0.15); cx.fill();
      cx.restore();
    }
    cx.restore();
  }
  if (ua > 0.78) sicrama(W / 2, H * 0.45, (ua - 0.78) * 1.2, 2.4);   // kule yere carpar, bloklar sacilir
""" + t[i1:]
degis("    const d0 = kisit((ua - 0.36) * hz * 1.4, 0, 2) * W * 0.6;", "    const d0 = kisit((ua - 0.8) * hz * 1.4, 0, 2) * W * 0.6;")
degis("    const x = W / 2 + Math.cos(a) * d0, y = H * 0.55 + Math.sin(a) * d0 * 0.6 + 200 * k * (ua - 0.36) ** 2;",
      "    const x = W / 2 + Math.cos(a) * d0, y = H * 0.55 + Math.sin(a) * d0 * 0.6 + 200 * k * (ua - 0.8) ** 2;")
degis("    cx.save(); cx.translate(x, y); cx.rotate(a + ua * 6 * hz); cx.scale(1, 0.4 + 0.6 * Math.abs(Math.sin(ua * 7 * hz + a * 5)));",
      "    cx.save(); cx.translate(x, y); cx.rotate(a + ua * 6 * hz); cx.scale(1, 0.4 + 0.6 * Math.abs(Math.sin(ua * 7 * hz + a * 5)));   // motor 31: kule devrilince")
degis("  if (ua < 0.18) { cx.save(); cx.fillStyle = `rgba(255,255,255,${0.85 * (1 - ua / 0.18)})`; cx.fillRect(0, 0, W, H); cx.restore(); }",
      "  if (ua > 0.78 && ua < 0.92) { cx.save(); cx.fillStyle = `rgba(255,255,255,${0.6 * (1 - (ua - 0.78) / 0.14)})`; cx.fillRect(0, 0, W, H); cx.restore(); }")
degis("  acilisSoru = kart.soru ? ease(kisit((ua - 0.55) / 0.3, 0, 1)) : 0;", "  acilisSoru = kart.soru ? ease(kisit((ua - 0.85) / 0.25, 0, 1)) : 0;")
degis("  const pa = ease(kisit((ua - 0.7) / 0.25, 0, 1));", "  const pa = ease(kisit((ua - 0.95) / 0.25, 0, 1));")

# ---- sonuc: kazanan yerine TAKIM SKORU + rutbe (motor 24 duzeni, uc karakter)
i0 = t.index("function sonucKart(kart, u, t) {")
i1 = t.index("// md. 28 (tam render 1): BRONZE alt tonu")
t = t[:i0] + """function sonucKart(kart, u, t) {                              // motor 31: bastaki "CAN YOUR TEAM CLEAR ALL 24?" sorusunun cevabi (takim)
  kartZeminCiz(t);
  const gir = ease(kisit(u / 0.4, 0, 1)), s = gir * (1 + 0.12 * Math.sin(gir * Math.PI));
  konfeti(t, 1.0, 70);
  const son = DUVARLAR[DUVARLAR.length - 1];
  for (let i = 0; i < 3; i++) {
    const o = OY[i], Y = KY[o], im = karKare(o, son[o], KK - 1); if (!im) continue;
    const sc = H * 0.4 / Y.boy_px, px = im.width * sc;
    cx.save(); cx.shadowColor = RENK[i]; cx.shadowBlur = 40 * k; cx.drawImage(im, W * (0.25 + 0.25 * i) - px / 2, H * 0.99 - Y.zemin_px * sc - Math.abs(Math.sin(t * 5 + i)) * 16 * k, px, px); cx.restore();
  }
  const dol = { GOLD: ['#fff6c0', '#ffd23a', '#e09a00'], SILVER: ['#ffffff', '#dfe6f2', '#9aa6ba'], BRONZE: ['#ffe0c0', '#ec9a5a', '#d8843a'] }[kart.rutbe];
  yaziK('TEAM SCORE', W / 2, H * 0.12, 100 * k * s, KART_DOLGU, 1, KON, '#7ad8ff');
  yaziK(kart.skor + ' / ' + kart.toplam, W / 2, H * 0.27, 130 * k * s, ['#fff6a0', '#ffd23a', '#ff9a1a'], 1);
  yaziK(kart.rutbe + '!', W / 2, H * 0.42, 110 * k * s, dol, 1);
}
""" + t[i1:]

# ---- acilis sorusu
degis("      satir([['WHO WILL WIN? ', KART_DOLGU], ['BLUE', ['#ffffff', ACIK[0], RENK[0]]], [', ', KART_DOLGU], ['PINK', ['#ffffff', ACIK[1], RENK[1]]], [' OR ', KART_DOLGU], ['GREEN', ['#ffffff', ACIK[2], RENK[2]]], ['?', KART_DOLGU]], W / 2, H * 0.13, 76 * k * acilisSoru, acilisSoru);",
      "      satir([['CAN YOUR TEAM CLEAR ALL ' + TOPLAM_DUVAR + '?', KART_DOLGU]], W / 2, H * 0.13, 80 * k * acilisSoru, acilisSoru);   // motor 31: CO-OP sorusu")

# ---- on kontak 1: MIRROR! yazisi 3-2-1 rakamina biniyordu -> FASTER! gibi ustte (0,12 H; abone varken zaten soner)
degis("    if (gir > 0.01) yaziK('MIRROR!', W / 2, H * 0.165, 96 * k", "    if (gir > 0.01) yaziK('MIRROR!', W / 2, H * 0.131, 64 * k")   # tam render 1: 0,12 H / 96 px kapsule ve 3-2-1'e degiyordu
# ---- yakin plan: Bobo turuncu-sari blok duvarinin onunde kayboluyordu -> altin yerine beyaz hakem isiltisi
degis("  cx.save(); cx.shadowColor = '#ffd21e'; cx.shadowBlur = 24 * k;   // motor 29: altin hakem isiltisi",
      "  cx.save(); cx.shadowColor = '#ffffff'; cx.shadowBlur = 30 * k;   // motor 31: beyaz hakem isiltisi (turuncu Bobo blok duvarindan ayrilsin)")
open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
