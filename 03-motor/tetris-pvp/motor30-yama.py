"""MOTOR 30 (HUMAN TETRIS 33) = sahne28.html (motor 28, 1v1 buzul kiyisi) + yama -> 03-motor/sahne30.html. sahne28 degismez.

    python motor30-yama.py

33: REF-085 yapi, 1v1, gunduz antik kum arenasi (varlik-arena.py), ozel tur BLIND (motor 24'ten tasindi: d.blind; duvar kum
firtinasiyla ortulu, BLIND! + ?, siluet sayimin son 1,5 sn'sinde belirir; karakterler ve maskot ondan sonra poza girer, maskot
o ana kadar soru balonu gosterir). OUT = kum yiginina yuvarlanir (kum sicramasi: turuncu-altin taneler + toz halkasi).
Hakem maskot KUCUK EJDERHA (TALIMATLAR §4 maskot sirasi): 2B kafa = yesil yuvarlak bas, sari-yesil burun, iki sari boynuz,
turuncu kulak yuzgecleri, buyuk gozler, kizarik yanak, kirmizi-altin hakem fulari; elde kucuk altin kalkan. Kepenkte ejderha neon
yuzu (31 dersi: kepenk amblemi her maskotla degisir). Hakem kursusu terrakota tas + iki kucuk mesale. Giris KANCA (30'dan beri),
mekan acilisi farkli: arena kapisinin dev ahsap kanatlari iki yana acilir, kum firtinasi + renkli flama kagitlari yaziyi acar.
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne28.html")
HEDEF = os.path.join(BURA, "..", "sahne30.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


def arasi(bas, son, yeni):
    """bas'tan son'a kadar (son haric) olan blogu degistirir; ikisi de tek olmali"""
    global t
    assert t.count(bas) == 1, ("bas", t.count(bas), bas[:80])
    i = t.index(bas); j = t.index(son, i)
    t = t[:i] + yeni + t[j:]


degis("<title>HUMAN TETRIS 31 - motor 28 (iki serit kutup buzul kiyisi, FREEZE turu, penguen hakem maskot)</title>",
      "<title>HUMAN TETRIS 33 - motor 30 (iki serit antik kum arenasi, BLIND turu, ejderha hakem maskot)</title>")
degis("// MOTOR 28 — HUMAN TETRIS 31 (REF-083 yapi, 18 Kas 2026; motor 27'den, tetris-pvp/motor28-yama.py):",
      "// MOTOR 30 — HUMAN TETRIS 33 (REF-085 yapi, 19 Kas 2026; motor 28'den, tetris-pvp/motor30-yama.py):\n"
      "//   - sahne: tetris-pvp/varlik-arena.py; gokte renkli flama kagitlari; OUT kum yiginina yuvarlanir (kum sicramasi)\n"
      "//   - BLIND ROUND (d.blind, motor 24'ten): duvar kum firtinasiyla ortulu, siluet son 1,5 sn'de; maskot o ana kadar soru balonu\n"
      "//   - hakem maskot kucuk ejderha (2B kafa, kirmizi-altin ful, elde altin kalkan), tas kursu + iki mesale; kepenkte ejderha neon yuzu\n"
      "//   - giris kanca: BOSS onizleme -> geri sarma -> arena kapisi kanatlari acilir, kum firtinasi\n"
      "// --- motor 28 aciklamasi ---\n"
      "// MOTOR 28 — HUMAN TETRIS 31 (REF-083 yapi, 18 Kas 2026; motor 27'den, tetris-pvp/motor28-yama.py):")

# gokte renkli flama kagitlari (konfeti)
degis("const KONF_R = ['#ffffff', '#c8f2ff', '#7ae0ff', '#3ac0ff', '#ffffff', '#e6faff'];   // motor 28: kar taneleri",
      "const KONF_R = ['#ff1e3c', '#ffd21e', '#ff7a14', '#ff3ab4', '#a040ff', '#2fd04a'];   // motor 30: renkli flama kagitlari")

# elde altin kalkan + kursu mesalesi (yeni cizim fonksiyonlari kristalCiz'den once)
degis("function kristalCiz(x, y, r, t) {",
      "function kalkanCiz(x, y, r, t) {                             // motor 30: ejderhanin elinde kucuk altin kalkan (hafif sallanir)\n"
      "  cx.save(); cx.translate(x, y); cx.rotate(0.15 * Math.sin(t * 2.2));\n"
      "  const g = cx.createRadialGradient(-r * 0.3, -r * 0.3, r * 0.1, 0, 0, r); g.addColorStop(0, '#fff2a0'); g.addColorStop(1, '#e8a010');\n"
      "  cx.fillStyle = g; cx.strokeStyle = '#7a4a00'; cx.lineWidth = r * 0.14; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.fill(); cx.stroke();\n"
      "  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.arc(0, 0, r * 0.55, 0, 6.283); cx.fill();\n"
      "  cx.fillStyle = '#ffd21e'; cx.beginPath(); cx.arc(0, 0, r * 0.22, 0, 6.283); cx.fill();\n"
      "  cx.restore();\n"
      "}\n"
      "function alevCiz(x, y, r, t) {                               // motor 30: mesale alevi (titrer; kendi isigi)\n"
      "  const f = 1 + 0.12 * Math.sin(t * 17 + x) + 0.08 * Math.sin(t * 29);\n"
      "  cx.save(); cx.shadowColor = '#ff9a1a'; cx.shadowBlur = r * 1.6;\n"
      "  cx.fillStyle = '#8a4a10'; cx.fillRect(x - r * 0.12, y, r * 0.24, r * 1.6);\n"
      "  cx.fillStyle = '#c88a1a'; cx.beginPath(); cx.ellipse(x, y, r * 0.5, r * 0.22, 0, 0, 6.283); cx.fill();\n"
      "  const g = cx.createRadialGradient(x, y - r * 0.6 * f, 0, x, y - r * 0.5 * f, r * f); g.addColorStop(0, '#fff6c0'); g.addColorStop(0.45, '#ffb21a'); g.addColorStop(1, 'rgba(255,60,20,0)');\n"
      "  cx.fillStyle = g; cx.beginPath(); cx.moveTo(x - r * 0.45, y); cx.quadraticCurveTo(x - r * 0.5, y - r * f, x, y - r * 1.7 * f);\n"
      "  cx.quadraticCurveTo(x + r * 0.5, y - r * f, x + r * 0.45, y); cx.closePath(); cx.fill();\n"
      "  cx.restore();\n"
      "}\n"
      "function kristalCiz(x, y, r, t) {")
degis("  if (!yuzSadece) balikCiz(x + (78 + bs) * s * k, y - 60 * s * k, 20 * s * k, t);   // motor 28: elde sari balik",
      "  if (!yuzSadece) kalkanCiz(x + (78 + bs) * s * k, y - 60 * s * k, 22 * s * k, t);   // motor 30: elde altin kalkan")

# maskot kafasi: penguen -> kucuk ejderha
arasi("  // motor 28: PENGUEN YAVRUSU kafasi", "  cx.restore();\n  cx.restore();\n}\n// alt orta",
"""  // motor 30: KUCUK EJDERHA kafasi (TALIMATLAR §4 maskot sirasi; kendi tasarimimiz)
  cx.lineWidth = 3;
  for (const sx of [-1, 1]) {                                   // boynuzlar (sari) + kulak yuzgecleri (turuncu)
    cx.fillStyle = '#ffc21e'; cx.strokeStyle = '#7a4a00';
    cx.beginPath(); cx.moveTo(sx * 22, -50); cx.lineTo(sx * 40, -50); cx.quadraticCurveTo(sx * 42, -70, sx * 38, -84); cx.closePath(); cx.fill(); cx.stroke();
    cx.fillStyle = '#ff7a14'; cx.strokeStyle = '#7a3000';
    cx.beginPath(); cx.moveTo(sx * 58, -18); cx.lineTo(sx * 64, 6); cx.lineTo(sx * 92, -28); cx.closePath(); cx.fill(); cx.stroke();
  }
  const gv = cx.createRadialGradient(-18, -26, 8, 0, 0, 74); gv.addColorStop(0, '#5ae86a'); gv.addColorStop(1, '#14a02a');
  cx.fillStyle = gv; cx.strokeStyle = '#0a5a1a'; cx.lineWidth = 5; cx.beginPath(); cx.ellipse(0, -2, 66, 60, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.fillStyle = '#c8f05a'; cx.strokeStyle = '#0a5a1a'; cx.lineWidth = 2; cx.beginPath(); cx.ellipse(0, 26, 40, 26, 0, 0, 6.283); cx.fill(); cx.stroke();   // burun
  for (const sx of [-1, 1]) {
    cx.fillStyle = '#0a5a1a'; cx.beginPath(); cx.ellipse(sx * 12, 18, 4, 3, 0, 0, 6.283); cx.fill();   // burun delikleri
    if (MASKOT_DUYGU === 'sevinc') {                            // PERFECT: kapali ^^ gozler
      cx.strokeStyle = '#0a2a10'; cx.lineWidth = 6; cx.lineCap = 'round';
      cx.beginPath(); cx.arc(sx * 24, -6, 12, Math.PI * 1.15, Math.PI * 1.85); cx.stroke();
    } else if (MASKOT_DUYGU === 'sasirma') {                    // OUT: iri beyaz gozler, kucuk bebek
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#0a2a10'; cx.lineWidth = 3; cx.beginPath(); cx.arc(sx * 24, -8, 16, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = '#0a2a10'; cx.beginPath(); cx.arc(sx * 24, -6, 6, 0, 6.283); cx.fill();
    } else {
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#0a2a10'; cx.lineWidth = 2; cx.beginPath(); cx.ellipse(sx * 24, -8, 15, 17, 0, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = '#1a2a10'; cx.beginPath(); cx.ellipse(sx * 24, -5, 9, 11, 0, 0, 6.283); cx.fill();
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 24 - 4, -11, 4, 0, 6.283); cx.fill();
    }
    cx.fillStyle = 'rgba(255,110,150,0.6)'; cx.beginPath(); cx.ellipse(sx * 44, 12, 10, 6, 0, 0, 6.283); cx.fill();   // kizarik yanak
  }
  cx.strokeStyle = '#0a2a10'; cx.lineWidth = 2;
  if (MASKOT_DUYGU === 'sasirma') { cx.fillStyle = '#8a1020'; cx.beginPath(); cx.ellipse(0, 36, 9, 11, 0, 0, 6.283); cx.fill(); cx.stroke(); }
  else if (MASKOT_DUYGU === 'sevinc') {
    cx.fillStyle = '#8a1020'; cx.beginPath(); cx.moveTo(-18, 30); cx.quadraticCurveTo(0, 56, 18, 30); cx.closePath(); cx.fill(); cx.stroke();
    cx.fillStyle = '#ffffff'; cx.fillRect(-6, 30, 5, 5); cx.fillRect(1, 30, 5, 5);
  } else {
    cx.lineWidth = 4; cx.lineCap = 'round'; cx.beginPath(); cx.arc(0, 26, 15, Math.PI * 0.15, Math.PI * 0.85); cx.stroke();
    cx.fillStyle = '#ffffff'; cx.beginPath(); cx.moveTo(-7, 39); cx.lineTo(-1, 39); cx.lineTo(-4, 45); cx.closePath(); cx.fill();   // kucuk dis
  }
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.ellipse(-22, -38, 18, 8, -0.4, 0, 6.283); cx.fill();   // cilali isilti
  cx.strokeStyle = '#3a0008'; cx.lineWidth = 3;                 // kirmizi-altin seritli hakem fulari
  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(-46, 52, 92, 18, 9); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd21e'; for (const xx of [-30, -6, 18]) { cx.fillRect(xx, 53, 9, 16); }
  cx.fillStyle = '#e8102c'; cx.beginPath(); cx.roundRect(22, 62, 18, 34, 6); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffd21e'; cx.fillRect(23, 74, 16, 7);
""")

# kepenkte ejderha neon yuzu (31 dersi: eski maskotun amblemi kalmasin)
arasi("  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.92, 0, 0, 6.283); cx.stroke();                        // motor 28: Nilo neon yuzu - bas",
      "  cx.shadowBlur = 0;\n  for (const [dx, dy] of",
"""  cx.beginPath(); cx.ellipse(mx, my, r, r * 0.92, 0, 0, 6.283); cx.stroke();                        // motor 30: ejderha neon yuzu - bas
  for (const sx of [-1, 1]) {
    cx.beginPath(); cx.moveTo(mx + sx * r * 0.32, my - r * 0.78); cx.lineTo(mx + sx * r * 0.6, my - r * 0.72); cx.lineTo(mx + sx * r * 0.56, my - r * 1.25); cx.closePath(); cx.stroke();   // boynuz
    cx.beginPath(); cx.moveTo(mx + sx * r * 0.88, my - r * 0.25); cx.lineTo(mx + sx * r * 0.96, my + r * 0.1); cx.lineTo(mx + sx * r * 1.38, my - r * 0.42); cx.closePath(); cx.stroke();   // kulak yuzgeci
    cx.beginPath(); cx.ellipse(mx + sx * r * 0.36, my - r * 0.12, r * 0.15, r * 0.18, 0, 0, 6.283); cx.stroke();   // goz
  }
  cx.beginPath(); cx.ellipse(mx, my + r * 0.42, r * 0.58, r * 0.36, 0, 0, 6.283); cx.stroke();   // burun
  for (const sx of [-1, 1]) { cx.beginPath(); cx.arc(mx + sx * r * 0.18, my + r * 0.3, r * 0.04, 0, 6.283); cx.stroke(); }
""")

# OUT: su sicramasi -> kum sicramasi
degis("function sicrama(xm, ym, u, olc = 1) {                        // su sicramasi: beyaz-camgobegi damlalar + halka",
      "function sicrama(xm, ym, u, olc = 1) {                        // motor 30: kum sicramasi: turuncu-altin taneler + toz halkasi")
degis("  cx.strokeStyle = 'rgba(230,250,255,0.95)'; cx.lineWidth = 14 * k * (1 - q);   // motor 28: kopuk halkasi",
      "  cx.strokeStyle = 'rgba(255,214,140,0.95)'; cx.lineWidth = 18 * k * (1 - q);   // motor 30: kum tozu halkasi")
degis("    cx.fillStyle = ['#ffffff', '#7ae0ff', '#1aa8ff'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 28: su damlasi",
      "    cx.fillStyle = ['#ffd23a', '#ff9a14', '#e8641e'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 30: kum tanesi")

# hakem kursusu: buz blogu -> terrakota tas + altin serit; kar kristalleri -> mesale
degis("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#7ae8ff'); g.addColorStop(1, '#0a6ad8');   // motor 28: buz blogu kursu",
      "  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ffa63a'); g.addColorStop(1, '#c84a14');   // motor 30: terrakota tas kursu")
degis("  cx.fillStyle = '#ffffff'; cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 9 * k);",
      "  cx.fillStyle = '#ffd21e'; cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 9 * k);")
degis("  cx.strokeStyle = 'rgba(255,255,255,0.55)'; cx.lineWidth = 2 * k; for (const dx of [-0.3, 0.05, 0.28]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 14 * k); cx.lineTo(xm + (dx + 0.06) * w, H); cx.stroke(); }   // buz catlaklari",
      "  cx.strokeStyle = 'rgba(120,40,8,0.55)'; cx.lineWidth = 3 * k; for (const dx of [-0.22, 0.22]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 14 * k); cx.lineTo(xm + dx * w, H); cx.stroke(); }   // tas derzleri")
degis("  for (const s of [-1, 1]) kristalCiz(xm + s * w * 0.56, y0 - 30 * k, 22 * k, t * s);   // motor 28: iki kar kristali",
      "  for (const s of [-1, 1]) alevCiz(xm + s * w * 0.62, y0 - 4 * k, 26 * k, t);   // motor 30: iki mesale")
degis("  cx.save(); cx.shadowColor = '#7ae0ff'; cx.shadowBlur = 24 * k;   // motor 28: buz dunyasi hakem isiltisi",
      "  cx.save(); cx.shadowColor = '#ffb21a'; cx.shadowBlur = 24 * k;   // motor 30: arena hakem isiltisi")

# ---------------- BLIND ROUND (motor 24'ten tasindi; iki serit)
degis("function duvarCiz(d, u, t) {",
"""function tipi(x, y, w, h, t, alfa) {                          // motor 30 BLIND: kartin ustunde kum firtinasi (sicak sis + capraz akan kum cizgileri)
  if (alfa <= 0.01) return;
  cx.save(); cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.clip();
  cx.globalAlpha = alfa;
  const g = cx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(255,214,140,0.98)'); g.addColorStop(1, 'rgba(255,160,70,0.98)');
  cx.fillStyle = g; cx.fillRect(x, y, w, h);
  const R = rng(3333);
  cx.strokeStyle = 'rgba(200,100,30,0.7)'; cx.lineCap = 'round';
  for (let j = 0; j < 70; j++) {
    const px = x + ((R() + t * (0.35 + R() * 0.3)) % 1) * (w + 200 * k) - 100 * k, py = y + ((R() + t * (0.6 + R() * 0.4)) % 1) * h, L = (20 + R() * 40) * k;
    cx.lineWidth = (2 + R() * 3) * k; cx.beginPath(); cx.moveTo(px, py); cx.lineTo(px + L, py + L * 0.3); cx.stroke();
  }
  cx.restore();
}
function acilma(d, u) {                                       // BLIND: 0 = gizli, 1 = acik (sayimin son 1,5 sn'si); BLIND olmayan duvarda 1
  if (!d.blind) return 1;
  const Z = ZD(d), b = Z.kart + Z.say;
  return ease(kisit((u - (b - 1.5)) / 0.3, 0, 1));
}
function duvarCiz(d, u, t) {""")
degis("""      kartZemin(i, x, y, w, h, t, alfa * (1 - kar));
      siluet(d[OY[i]], x, y, w, h, alfa * (1 - kar));
    }""",
"""      kartZemin(i, x, y, w, h, t, alfa * (1 - kar));
      const ac = acilma(d, u);                                 // motor 30 BLIND: siluet son 1,5 sn'de belirir
      siluet(d[OY[i]], x, y, w, h, alfa * (1 - kar) * ac);
      if (d.blind) {
        tipi(x, y, w, h, t, alfa * (1 - ac));
        const p = 1 + 0.05 * Math.sin(t * 5);
        if (ac < 0.98) {                                       // md. 28: koyu kahve kontur + beyaz dis kontur, kum zeminde okunur
          yaziK('BLIND!', x + w / 2, y + h * 0.36, 110 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#4a1400', '#ffffff');
          yaziK('?', x + w / 2, y + h * 0.7, 150 * k * p, ['#ffffff', '#fff2c0', '#ffd23a'], alfa * (1 - ac), '#4a1400', '#ffffff');
        }
      }
    }""")
# karakterler BLIND'da siluet acilinca poza girer
degis("""    if (u < a || sq < 0.35) bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 8 * k;          // ayakta ritimle hafif ziplar (donmus durus yok)
    else j = (out ? 0.5 : 1) * (KK - 1) * ease(kisit((sq - 0.35) / 0.4, 0, 1));""",
"""    const bas = d.blind ? (Z.say - 1.5) / Z.say : 0.35, sure = d.blind ? 1.2 / Z.say : 0.4;   // motor 30 BLIND: siluet acilinca poza girer
    if (u < a || sq < bas) bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 8 * k;          // ayakta ritimle hafif ziplar (donmus durus yok)
    else j = (out ? 0.5 : 1) * (KK - 1) * ease(kisit((sq - bas) / sure, 0, 1));""")
# maskot BLIND'da soru balonu, siluet acilinca iki pozu hizla gosterir
degis("""  let ad = d ? d.p1 : POZ_ADLAR[0], j = 0, bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 10 * k, isaret = 0;
  if (d) {
    const Z = ZD(d), sq = (u - Z.kart) / Z.say;
    if (u < Z.kart) { ad = d.p1; isaret = -1; }
    else if (sq < 1) {
      const yari = sq < 0.5 ? 0 : 1, q = (sq - yari * 0.5) / 0.5;""",
"""  let ad = d ? d.p1 : POZ_ADLAR[0], j = 0, bob = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 10 * k, isaret = 0, soru = false;
  if (d) {
    const Z = ZD(d), sq = (u - Z.kart) / Z.say;
    if (d.blind && acilma(d, u) < 0.5 && u < Z.kart + Z.say) soru = true;     // motor 30 BLIND: maskot da goremiyor
    else if (u < Z.kart) { ad = d.p1; isaret = -1; }
    else if (sq < 1) {
      const sb = d.blind ? kisit((u - (Z.kart + Z.say - 1.5)) / 1.5, 0, 1) : sq;   // BLIND: son 1,5 sn'de once P1 sonra P2
      const yari = sb < 0.5 ? 0 : 1, q = (sb - yari * 0.5) / 0.5;""")
degis("""  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc - kf[2] * sc * 0.25, kf[2] * sc * 1.6 / (62 * k), t, 1, true);   // motor 28: yavru penguen buyuk kafa""",
"""  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc - kf[2] * sc * 0.25, kf[2] * sc * 1.6 / (62 * k), t, 1, true);   // motor 30: yavru ejderha buyuk kafa
  if (soru) {                                                    // motor 30 BLIND: maskotun yaninda soru balonu
    const bx = xm + 150 * k, by = y0 + px * 0.22;
    cx.save(); cx.fillStyle = '#ffffff'; cx.strokeStyle = KON; cx.lineWidth = 6 * k;
    cx.beginPath(); cx.ellipse(bx, by, 56 * k, 50 * k, 0, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
    yaziK('?', bx, by + 2 * k, 70 * k * (1 + 0.08 * Math.sin(t * 6)), ['#ffffff', '#fff2c0', '#ffd23a'], 1, '#4a1400');
  }""")

# ---------------- kanca sonrasi mekan acilisi: buz kutlesi -> arena kapisi kanatlari + kum firtinasi
arasi("  const dus = kisit(ua / 0.35, 0, 1);                           // motor 28: buz kutlesi ustten kopar, ekranin ortasina duser",
      "  if (ua < 0.18) { cx.save();",
"""  const ac = ease(kisit(ua / 0.55, 0, 1));                      // motor 30: arena kapisinin dev ahsap kanatlari iki yana acilir
  if (ac < 1) for (const s of [-1, 1]) {
    const w = W / 2, x0 = s < 0 ? -w * ac : W / 2 + w * ac;
    cx.save(); cx.translate(x0, 0);
    const g = cx.createLinearGradient(0, 0, w, 0); g.addColorStop(0, '#a8541a'); g.addColorStop(0.5, '#d07a2a'); g.addColorStop(1, '#8a3a10');
    cx.fillStyle = g; cx.fillRect(0, 0, w, H);
    cx.strokeStyle = '#5a2008'; cx.lineWidth = 8 * k;
    for (let q = 1; q < 6; q++) { cx.beginPath(); cx.moveTo(w * q / 6, 0); cx.lineTo(w * q / 6, H); cx.stroke(); }   // tahta lataları
    cx.fillStyle = '#e8a010'; cx.strokeStyle = '#6a3a00'; cx.lineWidth = 6 * k;
    for (const yy of [0.18, 0.5, 0.82]) {                       // altin demir bantlar + civiler
      cx.fillRect(0, H * yy - 22 * k, w, 44 * k); cx.strokeRect(0, H * yy - 22 * k, w, 44 * k);
      for (let q = 0; q < 8; q++) { cx.beginPath(); cx.arc(w * (q + 0.5) / 8, H * yy, 9 * k, 0, 6.283); cx.fillStyle = '#fff2a0'; cx.fill(); cx.fillStyle = '#e8a010'; }
    }
    const hx = s < 0 ? w - 90 * k : 90 * k;                     // kapi halkasi
    cx.strokeStyle = '#ffd21e'; cx.lineWidth = 14 * k; cx.beginPath(); cx.arc(hx, H * 0.5 + 70 * k, 46 * k, 0, 6.283); cx.stroke();
    cx.restore();
  }
  if (ua > 0.3) sicrama(W / 2, H * 0.78, (ua - 0.3) * 1.2, 2.6);    // kapi acilinca kum patlamasi
  const R = rng(3333);                                          // motor 30: kum firtinasi + renkli flama kagitlari soldan saga
  for (let j = 0; j < 110; j++) {
    const hz = 0.8 + 0.7 * R(), y0 = R() * H, ph = R(), r = (14 + 22 * R()) * k;
    const x = (-0.25 + (ua * hz * 1.1 + ph * 0.6 - 0.2)) * W, y = y0 + Math.sin(ua * 5 + ph * 9) * 50 * k;
    if (x < -60 * k || x > W + 60 * k) continue;
    cx.save(); cx.translate(x, y); cx.rotate(ph * 6 + ua * 6 * hz);
    if (j % 3 === 0) {                                          // renkli flama kagidi
      cx.scale(1, 0.3 + 0.7 * Math.abs(Math.sin(ua * 7 * hz + ph * 5)));
      cx.fillStyle = KONF_R[Math.floor(ph * 6) % 6]; cx.fillRect(-r * 0.6, -r * 0.3, r * 1.2, r * 0.6);
    } else {                                                    // kum topagi
      cx.fillStyle = ['#ffd23a', '#ff9a14', '#e8641e'][j % 3]; cx.globalAlpha = 0.85;
      cx.beginPath(); cx.ellipse(0, 0, r * 0.55, r * 0.35, 0, 0, 6.283); cx.fill();
    }
    cx.restore();
  }
""")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
