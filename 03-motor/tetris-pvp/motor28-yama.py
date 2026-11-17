"""MOTOR 28 (HUMAN TETRIS 31) = sahne27.html (motor 27, 1v1 lale tarlasi) + yama -> 03-motor/sahne28.html. sahne27 degismez.

    python motor28-yama.py

31: REF-083 yapi, 1v1, gunduz kutup buzul kiyisi (varlik-buzul.py), ozel tur FREEZE (motor 22'den beri Z.tut; 'HOLD IT!' sayaci 3'ten baslar),
OUT = buzlu suya kayar (su sicramasi: camgobegi damlalar + kopuk halkasi), hakem maskot PENGUEN YAVRUSU (TALIMATLAR §4 maskot sirasi:
2B kafa = lacivert yuvarlak bas, beyaz kalp yuz lekesi, buyuk gozler, turuncu gaga, kizarik yanak; kirmizi-beyaz seritli atki; elde
kucuk sari balik), hakem kursusu buz blogu + iki kar kristali; gokte kar taneleri. Giris KANCA (30'daki gibi) ama mekan acilisi
farkli: buzuldan dev buz kutlesi kopar, ekranin ortasina duser, su sicrar, kar firtinasi yaziyi acar (TALIMATLAR §4: her videoda farkli).
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne27.html")
HEDEF = os.path.join(BURA, "..", "sahne28.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


degis("<title>HUMAN TETRIS 30 - motor 27 (iki serit lale tarlasi, MIRROR turu, ciftci hakem maskot)</title>",
      "<title>HUMAN TETRIS 31 - motor 28 (iki serit kutup buzul kiyisi, FREEZE turu, penguen hakem maskot)</title>")
degis("// MOTOR 27 — HUMAN TETRIS 30 (REF-082 yapi, 17 Kas 2026; motor 26'dan, tetris-pvp/motor27-yama.py):",
      "// MOTOR 28 — HUMAN TETRIS 31 (REF-083 yapi, 18 Kas 2026; motor 27'den, tetris-pvp/motor28-yama.py):\n"
      "//   - sahne: tetris-pvp/varlik-buzul.py; gokte kar taneleri; OUT buzlu suya kayar (su sicramasi); FREEZE ROUND (Z.tut)\n"
      "//   - hakem maskot penguen yavrusu (2B kafa, kirmizi atki, elde sari balik), buz blogu kursu + kar kristalleri\n"
      "//   - giris kanca: BOSS onizleme -> geri sarma -> buz kutlesi kopar, suya duser, kar firtinasi\n"
      "// --- motor 27 aciklamasi ---\n"
      "// MOTOR 27 — HUMAN TETRIS 30 (REF-082 yapi, 17 Kas 2026; motor 26'dan, tetris-pvp/motor27-yama.py):")

# gokte kar taneleri (beyaz + camgobegi tonlari)
degis("const KONF_R = ['#ff1e3c', '#ffd21e', '#ff7a14', '#ff3ab4', '#a040ff', '#ffffff'];   // motor 27: lale yapraklari",
      "const KONF_R = ['#ffffff', '#c8f2ff', '#7ae0ff', '#3ac0ff', '#ffffff', '#e6faff'];   // motor 28: kar taneleri")

# FREEZE sayaci 3'ten baslasin (tut 3,17 sn -> ilk 0,17 sn '4' gostermesin)
degis("yaziK('HOLD IT! ' + Math.max(1, Math.ceil(T * (1 - q))),",
      "yaziK('HOLD IT! ' + Math.min(3, Math.max(1, Math.ceil(T * (1 - q)))),")

# elde balik + kar kristali cizimleri (laleCiz'in onune)
degis("function laleCiz(x, y, r, t, renk) {",
      """function balikCiz(x, y, r, t) {                              // motor 28: penguenin elinde kucuk sari balik (kuyruk sallanir)
  cx.save(); cx.translate(x, y); cx.rotate(-0.5 + 0.15 * Math.sin(t * 4));
  const g = cx.createLinearGradient(0, -r, 0, r); g.addColorStop(0, '#fff07a'); g.addColorStop(1, '#ffb21a');
  cx.fillStyle = g; cx.strokeStyle = '#7a3a00'; cx.lineWidth = r * 0.12;
  cx.beginPath(); cx.ellipse(0, 0, r * 1.2, r * 0.62, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.save(); cx.translate(r * 1.1, 0); cx.rotate(0.35 * Math.sin(t * 9));
  cx.beginPath(); cx.moveTo(0, 0); cx.lineTo(r * 0.8, -r * 0.6); cx.lineTo(r * 0.8, r * 0.6); cx.closePath(); cx.fill(); cx.stroke(); cx.restore();
  cx.fillStyle = '#1a0a00'; cx.beginPath(); cx.arc(-r * 0.62, -r * 0.12, r * 0.14, 0, 6.283); cx.fill();
  cx.fillStyle = 'rgba(255,255,255,0.55)'; cx.beginPath(); cx.ellipse(-r * 0.2, -r * 0.3, r * 0.5, r * 0.14, -0.2, 0, 6.283); cx.fill();
  cx.restore();
}
function kristalCiz(x, y, r, t) {                             // motor 28: alti kollu kar kristali (camgobegi, beyaz kenarli, doner)
  cx.save(); cx.translate(x, y); cx.rotate(t * 0.6);
  for (const [c, w] of [['#ffffff', r * 0.34], ['#3ac0ff', r * 0.18]]) {
    cx.strokeStyle = c; cx.lineWidth = w; cx.lineCap = 'round';
    for (let j = 0; j < 6; j++) {
      cx.save(); cx.rotate(j * Math.PI / 3);
      cx.beginPath(); cx.moveTo(0, 0); cx.lineTo(0, -r); cx.stroke();
      cx.beginPath(); cx.moveTo(0, -r * 0.55); cx.lineTo(-r * 0.28, -r * 0.8); cx.moveTo(0, -r * 0.55); cx.lineTo(r * 0.28, -r * 0.8); cx.stroke();
      cx.restore();
    }
  }
  cx.restore();
}
function laleCiz(x, y, r, t, renk) {""")
degis("  if (!yuzSadece) laleCiz(x + (78 + bs) * s * k, y - 70 * s * k, 22 * s * k, t);   // motor 27: elde lale",
      "  if (!yuzSadece) balikCiz(x + (78 + bs) * s * k, y - 60 * s * k, 20 * s * k, t);   // motor 28: elde sari balik")

# maskot kafasi: pembe jole kafa + yaprak kulaklar + hasir sapka -> PENGUEN YAVRUSU kafasi + kirmizi-beyaz atki
bas = t.index("  for (const sx of [-1, 1]) {                                   // yaprak kulaklar")
son = t.index("  cx.restore();\n  cx.restore();\n}\n// alt orta: iki seridin birlesim cizgisinde")
t = t[:bas] + """  // motor 28: PENGUEN YAVRUSU kafasi (TALIMATLAR §4 maskot sirasi; kendi tasarimimiz)
  const gv = cx.createRadialGradient(-18, -26, 8, 0, 0, 74); gv.addColorStop(0, '#3a5ab8'); gv.addColorStop(1, '#141e48');
  cx.fillStyle = gv; cx.strokeStyle = '#0a0f2a'; cx.beginPath(); cx.ellipse(0, -2, 66, 60, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.fillStyle = '#f6faff';                                     // beyaz kalp yuz lekesi
  cx.beginPath(); cx.moveTo(0, -14); cx.bezierCurveTo(-14, -44, -60, -36, -50, 4); cx.bezierCurveTo(-44, 34, -14, 50, 0, 52);
  cx.bezierCurveTo(14, 50, 44, 34, 50, 4); cx.bezierCurveTo(60, -36, 14, -44, 0, -14); cx.closePath(); cx.fill();
  for (const sx of [-1, 1]) {                                   // gozler: 3 duygu (MASKOT_DUYGU: mutlu / sevinc / sasirma)
    if (MASKOT_DUYGU === 'sevinc') {                            // PERFECT: kapali ^^ gozler
      cx.strokeStyle = '#141e48'; cx.lineWidth = 6; cx.lineCap = 'round';
      cx.beginPath(); cx.arc(sx * 20, 2, 11, Math.PI * 1.15, Math.PI * 1.85); cx.stroke();
    } else if (MASKOT_DUYGU === 'sasirma') {                    // OUT: iri beyaz gozler, kucuk bebek
      cx.fillStyle = '#ffffff'; cx.strokeStyle = '#141e48'; cx.lineWidth = 3; cx.beginPath(); cx.arc(sx * 21, -4, 15, 0, 6.283); cx.fill(); cx.stroke();
      cx.fillStyle = '#141e48'; cx.beginPath(); cx.arc(sx * 21, -2, 6, 0, 6.283); cx.fill();
    } else {
      cx.fillStyle = '#141e48'; cx.beginPath(); cx.ellipse(sx * 20, -2, 11, 14, 0, 0, 6.283); cx.fill();
      cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(sx * 20 - 4, -8, 5, 0, 6.283); cx.fill();
      cx.beginPath(); cx.arc(sx * 20 + 3, 3, 2.2, 0, 6.283); cx.fill();
    }
    cx.fillStyle = 'rgba(255,110,150,0.6)'; cx.beginPath(); cx.ellipse(sx * 36, 20, 10, 6, 0, 0, 6.283); cx.fill();   // kizarik yanak
  }
  const gb = cx.createLinearGradient(0, 10, 0, 34); gb.addColorStop(0, '#ffb22a'); gb.addColorStop(1, '#ff7a10');
  cx.fillStyle = gb; cx.strokeStyle = '#7a3000'; cx.lineWidth = 3;   // turuncu gaga (sasirmada acik)
  if (MASKOT_DUYGU === 'sasirma') {
    cx.beginPath(); cx.moveTo(-13, 12); cx.quadraticCurveTo(0, 4, 13, 12); cx.lineTo(0, 20); cx.closePath(); cx.fill(); cx.stroke();
    cx.beginPath(); cx.moveTo(-10, 24); cx.lineTo(10, 24); cx.quadraticCurveTo(0, 38, -10, 24); cx.closePath(); cx.fill(); cx.stroke();
  } else {
    cx.beginPath(); cx.moveTo(-12, 14); cx.quadraticCurveTo(0, 8, 12, 14); cx.quadraticCurveTo(0, 34, -12, 14); cx.closePath(); cx.fill(); cx.stroke();
  }
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.ellipse(-22, -40, 18, 8, -0.4, 0, 6.283); cx.fill();   // cilali isilti
  cx.strokeStyle = '#0a0f2a'; cx.lineWidth = 3;               // kirmizi-beyaz seritli atki
  cx.fillStyle = '#ff2a3a'; cx.beginPath(); cx.roundRect(-46, 46, 92, 18, 9); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffffff'; for (const xx of [-30, -6, 18]) { cx.fillRect(xx, 47, 9, 16); }
  cx.fillStyle = '#ff2a3a'; cx.beginPath(); cx.roundRect(22, 56, 18, 34, 6); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffffff'; cx.fillRect(23, 68, 16, 7);
""" + t[son:]

# hakem kursusu: ahsap + saksi lale -> buz blogu + iki kar kristali
degis("g.addColorStop(0, '#ff8a2a'); g.addColorStop(1, '#b8501a');   // motor 27: ahsap kursu",
      "g.addColorStop(0, '#7ae8ff'); g.addColorStop(1, '#0a6ad8');   // motor 28: buz blogu kursu")
degis("  cx.strokeStyle = 'rgba(90,30,8,0.5)'; cx.lineWidth = 2 * k; for (const dx of [-0.25, 0.0, 0.25]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 18 * k); cx.lineTo(xm + dx * w, H); cx.stroke(); }   // tahta cizgileri",
      "  cx.strokeStyle = 'rgba(255,255,255,0.55)'; cx.lineWidth = 2 * k; for (const dx of [-0.3, 0.05, 0.28]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 14 * k); cx.lineTo(xm + (dx + 0.06) * w, H); cx.stroke(); }   // buz catlaklari")
bas = t.index("  for (const [s, c] of [[-1, '#ff1e3c'], [1, '#ffd21e']]) {          // iki saksi lale")
son = t.index("  cx.restore();\n}\nfunction hakemCiz(t, d, u) {")
t = t[:bas] + "  for (const s of [-1, 1]) kristalCiz(xm + s * w * 0.56, y0 - 30 * k, 22 * k, t * s);   // motor 28: iki kar kristali\n" + t[son:]

# OUT: saman -> buzlu su sicramasi
degis("  cx.strokeStyle = 'rgba(240,176,32,0.9)'; cx.lineWidth = 14 * k * (1 - q);   // motor 27: saman halkasi (26'da yorum satiri halkayi yutuyordu)",
      "  cx.strokeStyle = 'rgba(230,250,255,0.95)'; cx.lineWidth = 14 * k * (1 - q);   // motor 28: kopuk halkasi")
degis("    cx.strokeStyle = ['#ffd23a', '#f0a018', '#ffe58a'][j % 3]; cx.lineWidth = (3 + 3 * R2()) * k * olc * (1 - q * 0.5); cx.lineCap = 'round';\n"
      "    { const a_ = R2() * 6.283, l_ = (10 + 14 * R2()) * k * olc; cx.beginPath(); cx.moveTo(x - Math.cos(a_) * l_, y - Math.sin(a_) * l_); cx.lineTo(x + Math.cos(a_) * l_, y + Math.sin(a_) * l_); cx.stroke(); }   // motor 27: saman copu",
      "    cx.fillStyle = ['#ffffff', '#7ae0ff', '#1aa8ff'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 28: su damlasi")

# KANCA mekan acilisi: yel degirmeni kanadi + lale firtinasi -> buz kutlesi kopar, duser, su sicrar, kar firtinasi
degis("function kanatCiz(x, y, L, a) {",
      """function buzKutleCiz(x, y, r, a) {                            // motor 28: kose koseli dev buz kutlesi (camgobegi yuzeyler, beyaz kenar, kar sapka)
  cx.save(); cx.translate(x, y); cx.rotate(a);
  const P = [[-1, -0.55], [-0.45, -1], [0.5, -0.9], [1, -0.3], [0.85, 0.7], [0.1, 1], [-0.8, 0.75]];
  const yz = [['#bff4ff', '#5ad8ff'], ['#7ae8ff', '#1aa8ff'], ['#3ac0ff', '#0a78e0'], ['#1a9cf0', '#0a50b8']];
  for (let j = 0; j < P.length; j++) {
    const [x1, y1] = P[j], [x2, y2] = P[(j + 1) % P.length], c = yz[j % 4];
    const g = cx.createLinearGradient(x1 * r, y1 * r, 0, 0); g.addColorStop(0, c[0]); g.addColorStop(1, c[1]);
    cx.fillStyle = g; cx.beginPath(); cx.moveTo(0, 0); cx.lineTo(x1 * r, y1 * r); cx.lineTo(x2 * r, y2 * r); cx.closePath(); cx.fill();
  }
  cx.strokeStyle = '#ffffff'; cx.lineWidth = 10 * k; cx.lineJoin = 'round';
  cx.beginPath(); P.forEach(([px, py], j) => j ? cx.lineTo(px * r, py * r) : cx.moveTo(px * r, py * r)); cx.closePath(); cx.stroke();
  cx.fillStyle = '#e6f8ff'; cx.beginPath(); cx.moveTo(-1 * r, -0.55 * r); cx.quadraticCurveTo(-0.6 * r, -1.25 * r, -0.45 * r, -1 * r);
  cx.lineTo(0.5 * r, -0.9 * r); cx.quadraticCurveTo(0.9 * r, -0.7 * r, 1 * r, -0.3 * r); cx.quadraticCurveTo(0, -0.62 * r, -1 * r, -0.55 * r); cx.fill();
  cx.restore();
}
function kanatCiz(x, y, L, a) {""")
degis("""  const ac = ease(kisit((ua - 0.3) / 0.6, 0, 1));                // kanat donerken buyur, kameranin icinden gecer
  if (ac < 1) {
    cx.save(); cx.globalAlpha = 1 - ac; kanatCiz(W / 2, H * 0.5, W * 0.62 * (1 + 1.6 * ac), ua * 4.2 + 0.4); cx.restore();
  }""",
      """  const dus = kisit(ua / 0.35, 0, 1);                           // motor 28: buz kutlesi ustten kopar, ekranin ortasina duser
  if (ua < 0.9) {
    const yb = lerp(-H * 0.35, H * 0.62, dus * dus), al = 1 - kisit((ua - 0.45) / 0.45, 0, 1);
    cx.save(); cx.globalAlpha = al; buzKutleCiz(W / 2, yb, H * 0.34, 0.25 * dus); cx.restore();
  }
  if (ua > 0.33) sicrama(W / 2, H * 0.7, (ua - 0.33) * 1.2, 2.6);   // suya dustugu an dev su sicramasi""")
degis("  const R = rng(3030);                                          // lale yapragi firtinasi soldan saga",
      "  const R = rng(3131);                                          // motor 28: kar firtinasi soldan saga")
degis("""    cx.fillStyle = c; cx.strokeStyle = 'rgba(80,0,20,0.5)'; cx.lineWidth = 2 * k;
    cx.beginPath(); cx.ellipse(0, 0, r, r * 0.55, 0, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.ellipse(-r * 0.3, -r * 0.15, r * 0.35, r * 0.15, 0, 0, 6.283); cx.fill();""",
      """    if (j % 4 === 0) { cx.restore(); kristalCiz(x, y, r * 0.8, ua * 3 + ph * 6); continue; }   // motor 28: her 4 taneden biri kar kristali
    cx.fillStyle = c; cx.strokeStyle = 'rgba(10,60,140,0.5)'; cx.lineWidth = 2 * k;
    cx.beginPath(); cx.arc(0, 0, r * 0.55, 0, 6.283); cx.fill(); cx.stroke();""")

degis("function maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {",
      "let MASKOT_DUYGU = 'mutlu';                                   // motor 28: penguen hakem duygusu\nfunction maskotCiz(x, y, s, t, alfa = 1, yuzSadece = false) {")
degis("  const kf = Y.poz[ad].kafa[Math.round(j)], kx = x0 + kf[0] * sc;",
      "  const kf = Y.poz[ad].kafa[Math.round(j)], kx = x0 + kf[0] * sc;\n"
      "  MASKOT_DUYGU = 'mutlu';                                      // motor 28: duvar gecince PERFECT -> sevinc, OUT -> sasirma\n"
      "  if (d && u >= ZD(d).kart + ZD(d).say + ZD(d).buyu * 0.5) MASKOT_DUYGU = (d.out && (d.out.p1 || d.out.p2)) ? 'sasirma' : 'sevinc';")
degis("  cx.save(); cx.shadowColor = '#ff6ad6'; cx.shadowBlur = 24 * k;",
      "  cx.save(); cx.shadowColor = '#7ae0ff'; cx.shadowBlur = 24 * k;   // motor 28: buz dunyasi hakem isiltisi")
degis("  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc, kf[2] * sc * 1.25 / (62 * k), t, 1, true);",
      "  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc - kf[2] * sc * 0.25, kf[2] * sc * 1.6 / (62 * k), t, 1, true);   // motor 28: yavru penguen buyuk kafa")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
