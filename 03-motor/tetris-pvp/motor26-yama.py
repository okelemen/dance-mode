"""MOTOR 26 (HUMAN TETRIS 29) = sahne23.html (motor 23, 1v1 plaj/MIRROR) + yama -> 03-motor/sahne26.html. sahne23 degismez.

    python motor26-yama.py

29: referanssiz, 1v1, gunduz orman tapinagi (varlik-orman.py), ozel tur SPEED (son 4 duvar hizlanir, d.hiz -> FASTER!),
OUT = camur birikintisine kayar (camur sicramasi), hakem maskot kasif (2B kasif sapkasi + yesil fular, elinde mesale),
hakem kursusu oymali tas + iki mesale; gokte dusen yapraklar/cicek yapraklari (konfeti yerine).
GIRIS (kullanici 15 Kas 2026 "B: Tas kapi", yalniz 29): TEMA.acilis = 'taskapi' -> maskot mesaleyle dev tas kapiyi iter, kapi gurleyerek
iki yana acilir, iki boksor karakter iceri kosar, VS tas tablete oyulmus parlar + WHO WILL WIN?; ilk duvarin 3-2-1'i tas blok olarak duser.
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne23.html")
HEDEF = os.path.join(BURA, "..", "sahne26.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


# ---------------------------------------------------------------- baslik + aciklama
degis("<title>HUMAN TETRIS 26 - motor 23 (iki serit tropik plaj, MIRROR turu, yarisan karakterler, cankurtaran hakem maskot)</title>",
      "<title>HUMAN TETRIS 29 - motor 26 (iki serit orman tapinagi, tas kapi girisi, SPEED turu, kasif hakem maskot)</title>")
degis("// MOTOR 23 — HUMAN TETRIS 26 (REFERANSSIZ, 14 Kas 2026; motor 22'den).",
      "// MOTOR 26 — HUMAN TETRIS 29 (REFERANSSIZ, 16 Kas 2026; motor 23'ten, tetris-pvp/motor26-yama.py). TALIMATLAR §2b 6. mekan (orman tapinagi):\n"
      "//   - sahne: tetris-pvp/varlik-orman.py; gokte dusen yapraklar; OUT camura kayar (camur sicramasi)\n"
      "//   - hakem maskot kasif (2B sapka + fular, elinde mesale), tas kursu + iki mesale; SPEED ROUND: d.hiz duvarlarinda FASTER!\n"
      "//   - GIRIS tas kapi (TEMA.acilis='taskapi'): maskot kapiyi iter -> kapi acilir -> boksorler kosar -> VS tas tablet; ilk 3-2-1 tas blok\n"
      "// --- motor 23 aciklamasi ---\n"
      "// MOTOR 23 — HUMAN TETRIS 26 (REFERANSSIZ, 14 Kas 2026; motor 22'den).")

# ---------------------------------------------------------------- gokte konfeti yerine dusen yapraklar / cicek yapraklari
degis("const KONF_R = ['#ff4a6a', '#ffd23a', '#2ac86a', '#ffffff', '#a65aff', '#1aa8ff'];",
      "const KONF_R = ['#3ccf3e', '#1fae3a', '#ffcc1e', '#ff6ab0', '#7ae05a', '#ff8a1e'];   // motor 26: orman yapraklari + cicek yapraklari")
degis("    cx.fillStyle = KONF_R[p.c]; cx.fillRect(-7 * k * p.w, -4 * k, 14 * k * p.w, 8 * k); cx.restore();",
      "    cx.fillStyle = KONF_R[p.c]; cx.beginPath(); cx.ellipse(0, 0, 9 * k * p.w, 4.5 * k, 0, 0, 6.283); cx.fill(); cx.restore();   // yaprak")

# ---------------------------------------------------------------- mesale (plaj topu yerine) + tas disk (can simidi yerine)
degis("function topCiz(x, y, r, t) {                                  // motor 23: plaj topu (gezegen yerine)",
      """function mesaleCiz(x, y, r, t) {                               // motor 26: mesale - tahta sap, bakir hazne, titreyen alev (kendi isigi)
  cx.save(); cx.translate(x, y);
  cx.strokeStyle = '#6a3a14'; cx.lineWidth = r * 0.42; cx.lineCap = 'round'; cx.beginPath(); cx.moveTo(0, r * 2.4); cx.lineTo(0, r * 0.4); cx.stroke();
  cx.fillStyle = '#b8642a'; cx.strokeStyle = '#4a2408'; cx.lineWidth = r * 0.12;
  cx.beginPath(); cx.moveTo(-r * 0.7, -r * 0.1); cx.lineTo(r * 0.7, -r * 0.1); cx.lineTo(r * 0.36, r * 0.55); cx.lineTo(-r * 0.36, r * 0.55); cx.closePath(); cx.fill(); cx.stroke();
  const fl = 1 + 0.12 * Math.sin(t * 23) + 0.08 * Math.sin(t * 37);
  cx.globalCompositeOperation = 'lighter';
  const ha = cx.createRadialGradient(0, -r * 0.9, 0, 0, -r * 0.9, r * 3.2); ha.addColorStop(0, 'rgba(255,190,80,0.55)'); ha.addColorStop(1, 'rgba(255,140,40,0)');
  cx.fillStyle = ha; cx.beginPath(); cx.arc(0, -r * 0.9, r * 3.2, 0, 6.283); cx.fill();
  cx.globalCompositeOperation = 'source-over';
  for (const [s, c] of [[1.0, '#ff6a1a'], [0.72, '#ffb02e'], [0.42, '#fff2a0']]) {
    cx.fillStyle = c; cx.beginPath(); cx.moveTo(-r * 0.62 * s, -r * 0.1);
    cx.quadraticCurveTo(-r * 0.7 * s, -r * 1.2 * s * fl, Math.sin(t * 9) * r * 0.15, -r * 2.1 * s * fl);
    cx.quadraticCurveTo(r * 0.7 * s, -r * 1.2 * s * fl, r * 0.62 * s, -r * 0.1); cx.closePath(); cx.fill();
  }
  cx.restore();
}
function topCiz(x, y, r, t) {                                  // motor 23: plaj topu (gezegen yerine)""")
degis("""function simitCiz(x, y, r) {                                    // motor 23: can simidi (kirmizi-beyaz dilimli halka)
  cx.save(); cx.translate(x, y); cx.lineWidth = r * 0.55;
  for (let i = 0; i < 8; i++) { cx.strokeStyle = i % 2 ? '#ffffff' : '#ff2a3a'; cx.beginPath(); cx.arc(0, 0, r, i * 0.7854, (i + 1) * 0.7854); cx.stroke(); }
  cx.lineWidth = Math.max(1.5, r * 0.08); cx.strokeStyle = '#8a0a1a';
  cx.beginPath(); cx.arc(0, 0, r * 1.27, 0, 6.283); cx.stroke(); cx.beginPath(); cx.arc(0, 0, r * 0.73, 0, 6.283); cx.stroke();
  cx.restore();
}""", """function simitCiz(x, y, r) {                                    // motor 26: yosunlu tas disk (can simidi yerine; maskotun basamagi)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.6, 0, r * 0.6); g.addColorStop(0, '#ffbe55'); g.addColorStop(1, '#c8702c');
  cx.fillStyle = g; cx.strokeStyle = '#6a3410'; cx.lineWidth = Math.max(2, r * 0.1);
  cx.beginPath(); cx.ellipse(0, 0, r * 1.5, r * 0.6, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.fillStyle = '#2fd04a'; for (const [dx, rr] of [[-0.8, 0.28], [0.5, 0.22], [1.0, 0.16]]) { cx.beginPath(); cx.ellipse(dx * r, -r * 0.32, rr * r, rr * r * 0.55, 0, 0, 6.283); cx.fill(); }
  cx.restore();
}""")

# ---------------------------------------------------------------- maskot: elde mesale, duduk ipi yerine yesil fular, cicek + toka yerine kasif sapkasi
degis("  if (!yuzSadece) { cx.strokeStyle = '#ffffff'; cx.lineWidth = 2.5; cx.beginPath(); cx.moveTo(60, 0); cx.quadraticCurveTo(80, -40, 88 + bs, -78); cx.stroke(); }\n", "")
degis("  if (!yuzSadece) topCiz(x + (88 + bs) * s * k, y - 100 * s * k, 24 * s * k, t);",
      "  if (!yuzSadece) mesaleCiz(x + (78 + bs) * s * k, y - 70 * s * k, 22 * s * k, t);   // motor 26: elde mesale")
degis("""  cx.strokeStyle = '#ff2a3a'; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(-30, 40); cx.quadraticCurveTo(0, 62, 26, 42); cx.stroke();   // motor 23: cankurtaran duduk ipi
  cx.save(); cx.translate(10, 56); cx.rotate(-0.25); cx.fillStyle = '#ffd23a'; cx.strokeStyle = KN; cx.lineWidth = 3;
  cx.beginPath(); cx.roundRect(-14, -8, 28, 16, 7); cx.fill(); cx.stroke(); cx.beginPath(); cx.arc(-10, 0, 9, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
  cx.save(); cx.translate(-26, -50);                            // yildiz tokasi (altin)
  cx.rotate(-0.3); cx.beginPath();
  for (let q = 0; q <= 10; q++) { const a = -Math.PI / 2 + q * Math.PI / 5, rr = q % 2 ? 6 : 14; q ? cx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : cx.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  cx.closePath(); cx.fillStyle = '#ffd23a'; cx.fill(); cx.lineWidth = 3; cx.stroke(); cx.restore();
  cx.save(); cx.translate(0, -58);                              // basta cicek (seri tanirligi)
  for (let i = 0; i < 5; i++) { cx.save(); cx.rotate(i * 1.2566 + t * 0.6); cx.fillStyle = '#ffffff'; cx.beginPath(); cx.ellipse(0, -11, 7, 11, 0, 0, 6.283); cx.fill(); cx.lineWidth = 2.5; cx.stroke(); cx.restore(); }
  cx.fillStyle = '#ffd94a'; cx.beginPath(); cx.arc(0, 0, 6, 0, 6.283); cx.fill(); cx.restore();""",
      """  cx.fillStyle = '#1fae3a'; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(-32, 44); cx.lineTo(32, 44); cx.lineTo(0, 74); cx.closePath(); cx.fill(); cx.stroke();   // motor 26: yesil fular
  cx.save(); cx.translate(0, -50); cx.rotate(-0.06 + 0.04 * Math.sin(t * 3));       // motor 26: kasif sapkasi (genis kenar, haki, yesil bant)
  const sg = cx.createLinearGradient(0, -52, 0, 8); sg.addColorStop(0, '#ffd27a'); sg.addColorStop(1, '#e0962e');
  cx.fillStyle = sg; cx.lineWidth = 4;
  cx.beginPath(); cx.ellipse(0, 0, 84, 17, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.beginPath(); cx.moveTo(-46, -2); cx.bezierCurveTo(-48, -58, 48, -58, 46, -2); cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = '#1fae3a'; cx.beginPath(); cx.moveTo(-46, -6); cx.lineTo(46, -6); cx.lineTo(45, -18); cx.lineTo(-45, -18); cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.ellipse(-16, -36, 14, 6, -0.4, 0, 6.283); cx.fill();
  cx.restore();""")

# ---------------------------------------------------------------- hakem kursusu: oymali tas + iki mesale
degis("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ff3a4a'); g.addColorStop(1, '#c4102a');   // motor 23: kirmizi cankurtaran kursusu",
      "  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ffb04a'); g.addColorStop(1, '#c06a24');   // motor 26: oymali tas kursu")
degis("  simitCiz(xm + w * 0.36, y0 + h * 0.2, 20 * k);\n",
      "  cx.fillStyle = '#2fd04a'; for (const dx of [-0.38, 0.12, 0.4]) { cx.beginPath(); cx.ellipse(xm + dx * w, y0 + 4 * k, 18 * k, 8 * k, 0, 0, 6.283); cx.fill(); }   // yosun\n"
      "  mesaleCiz(xm - w * 0.56, y0 - 34 * k, 13 * k, t); mesaleCiz(xm + w * 0.56, y0 - 34 * k, 13 * k, t);\n")

# ---------------------------------------------------------------- OUT: kum yerine camur sicramasi
degis("  cx.strokeStyle = 'rgba(255,214,140,0.9)'; cx.lineWidth = 14 * k * (1 - q);",
      "  cx.strokeStyle = 'rgba(122,66,32,0.9)'; cx.lineWidth = 14 * k * (1 - q);   // motor 26: camur halkasi")
degis("    cx.fillStyle = ['#ffd27a', '#f3a53a', '#fff1c4'][j % 3]; cx.beginPath(); cx.arc(x, y, (5 + 8 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 23: kum tanesi",
      "    cx.fillStyle = ['#7a4220', '#5a3016', '#a8642e'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 26: camur damlasi")

# ---------------------------------------------------------------- SPEED: hizlanan duvarlarda FASTER! (MIRROR! bloguyla ayni yer, abone gorunurken soner)
degis("  if (T && u >= c) freezeCiz(u - c, T, t);",
      """  if (d.hiz && u < b) {                                          // motor 26 SPEED ROUND: hizlanan duvarda ustte FASTER! (abone dugmesiyle ust uste binmez)
    const ab = ABONE.reduce((m, x) => Math.max(m, kisit(1 - Math.max(x - t, t - x - ABONE_SURE, 0) / 0.3, 0, 1)), 0);
    const gir = ease(kisit(u / 0.3, 0, 1)) * (1 - ab), p = 1 + 0.08 * Math.sin(t * 14);
    if (gir > 0.01) yaziK('FASTER!', W / 2, H * 0.165, 104 * k * ease(kisit(u / 0.3, 0, 1)) * p, ['#fff6a0', '#ffd23a', '#ff6a1a'], gir, '#4a1400', '#ffffff');
  }
  if (T && u >= c) freezeCiz(u - c, T, t);""")

# ---------------------------------------------------------------- ilk duvarin 3-2-1'i tas blok olarak duser
degis("""function sayimCiz(e) {
  if (e === null) return;
  const n = 3 - Math.min(2, Math.floor(e * 3)), q = (e * 3) % 1;""",
      """let SAYIM_TAS = false;                                          // motor 26: ilk duvarda 3-2-1 tas blok (giris devami)
function tasBlok(x, y, r, q) {
  const dus = q < 0.22 ? -H * 0.5 * (1 - ease(q / 0.22)) : 0, sars = q >= 0.22 && q < 0.32 ? Math.sin((q - 0.22) * 90) * 8 * k : 0;
  cx.save(); cx.translate(x + sars, y + dus);
  const g = cx.createLinearGradient(0, -r, 0, r); g.addColorStop(0, '#ffc25a'); g.addColorStop(1, '#b8642a');
  cx.fillStyle = g; cx.strokeStyle = '#4a2008'; cx.lineWidth = 8 * k; cx.beginPath(); cx.roundRect(-r, -r, 2 * r, 2 * r, r * 0.22); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(90,40,10,0.5)'; cx.lineWidth = 4 * k; cx.beginPath(); cx.roundRect(-r * 0.8, -r * 0.8, 1.6 * r, 1.6 * r, r * 0.16); cx.stroke();
  cx.fillStyle = '#2fd04a'; cx.beginPath(); cx.ellipse(-r * 0.55, -r * 0.92, r * 0.36, r * 0.14, 0, 0, 6.283); cx.fill();
  cx.restore();
  if (q >= 0.22 && q < 0.5) {                                   // carpma tozu
    const p = (q - 0.22) / 0.28, R3 = rng(991);
    for (let j = 0; j < 14; j++) { const a = Math.PI * (0.05 + 0.9 * R3()); cx.fillStyle = `rgba(230,180,110,${0.7 * (1 - p)})`;
      cx.beginPath(); cx.arc(x + Math.cos(a) * r * (1 + p * 1.4) * (R3() < 0.5 ? -1 : 1), y + r * 0.9 - Math.sin(a) * r * 0.5 * p, (10 + 12 * R3()) * k * (1 - p * 0.5), 0, 6.283); cx.fill(); }
  }
  return dus;
}
function sayimCiz(e) {
  if (e === null) return;
  const n = 3 - Math.min(2, Math.floor(e * 3)), q = (e * 3) % 1;
  if (SAYIM_TAS) {
    const dus = tasBlok(W / 2, H * 0.37, 118 * k, q);
    yaziK(String(n), W / 2, H * 0.37 + dus, 170 * k, ['#ffffff', '#ffd6f2', '#ff4ad0'], 1, '#24083e', '#ff6ad6');
    return;
  }""")
degis("    AYNA = !!d.ayna;\n", "    AYNA = !!d.ayna; SAYIM_TAS = d.no === 1 && TEMA.acilis === 'taskapi';\n")

# ---------------------------------------------------------------- TAS KAPI GIRISI
degis("""let acilisSoru = 0;
function acilisCiz(kart, u, t) {
  acilisSoru = 0;""",
      """let acilisSoru = 0;
function tasKapak(x0, w, i, sars) {                              // tas kapi kanadi: oymali cerceve, oyuncu renginde parlayan halka, yosun
  cx.save(); cx.translate(sars, 0);
  const g = cx.createLinearGradient(x0, 0, x0 + w, H); g.addColorStop(0, '#f6ae52'); g.addColorStop(0.5, '#e09440'); g.addColorStop(1, '#b8682a');
  cx.fillStyle = g; cx.fillRect(x0, 0, w, H);
  cx.strokeStyle = 'rgba(80,36,8,0.55)'; cx.lineWidth = 10 * k;
  for (const m of [40, 90]) { cx.beginPath(); cx.roundRect(x0 + m * k, m * k, w - 2 * m * k, H - 2 * m * k, 26 * k); cx.stroke(); }
  for (let j = 1; j < 6; j++) { cx.lineWidth = 5 * k; cx.beginPath(); cx.moveTo(x0 + 90 * k, j * H / 6); cx.lineTo(x0 + w - 90 * k, j * H / 6 + (j % 2 ? 14 : -10) * k); cx.stroke(); }
  const cxm = x0 + w / 2, cy = H * 0.46, R = Math.min(w, H) * 0.24;
  cx.save(); cx.shadowColor = RENK[i]; cx.shadowBlur = 40 * k; cx.strokeStyle = RENK[i]; cx.lineWidth = 22 * k;
  cx.beginPath(); cx.arc(cxm, cy, R, 0, 6.283); cx.stroke(); cx.lineWidth = 9 * k; cx.beginPath(); cx.arc(cxm, cy, R * 0.62, 0, 6.283); cx.stroke(); cx.restore();
  cx.fillStyle = ACIK[i]; cx.beginPath();
  for (let q = 0; q <= 10; q++) { const a = -Math.PI / 2 + q * Math.PI / 5, rr = q % 2 ? R * 0.18 : R * 0.42; q ? cx.lineTo(cxm + Math.cos(a) * rr, cy + Math.sin(a) * rr) : cx.moveTo(cxm + Math.cos(a) * rr, cy + Math.sin(a) * rr); }
  cx.closePath(); cx.fill();
  const R4 = rng(300 + i);
  for (let j = 0; j < 9; j++) { cx.fillStyle = j % 2 ? '#2fd04a' : '#1fae3a'; cx.beginPath(); cx.ellipse(x0 + R4() * w, R4() < 0.5 ? R4() * H * 0.2 : H - R4() * H * 0.18, (30 + 40 * R4()) * k, (12 + 14 * R4()) * k, 0, 0, 6.283); cx.fill(); }
  cx.restore();
}
function tasKapiCiz(kart, u, t) {
  const S1 = 1.0, S2 = 1.9;                                     // 0-S1 itme (sarsinti) / S1-S2 acilis / S2- VS tablet
  const acik = ease(kisit((u - S1) / (S2 - S1), 0, 1));
  const sars = u < S1 ? Math.sin(u * 70) * 6 * k * (u / S1) : (acik < 1 ? Math.sin(u * 50) * 4 * k * (1 - acik) : 0);
  // sahne zaten cizili (sahneCiz); acilan kanatlarin arasindan orman gorunur
  if (acik < 1) { tasKapak(-acik * SW, SW, 0, sars); tasKapak(SW + acik * SW, SW, 1, sars);
    cx.save(); cx.fillStyle = 'rgba(40,16,4,0.85)'; cx.fillRect(SW - 5 * k + sars, 0, 10 * k, H * (1 - acik)); cx.restore(); }
  if (u >= S1 * 0.4 && u < S2 + 0.6) {                          // kapi dibinde toz bulutu
    const R5 = rng(77), p = kisit((u - S1 * 0.4) / (S2 + 0.6 - S1 * 0.4), 0, 1);
    for (let j = 0; j < 30; j++) { const x = SW + (R5() - 0.5) * W * (0.2 + acik * 1.1), y = H * (0.9 + 0.1 * R5()) - p * 120 * k * R5();
      cx.fillStyle = `rgba(235,190,120,${0.55 * Math.sin(p * Math.PI)})`; cx.beginPath(); cx.arc(x, y, (30 + 50 * R5()) * k * (0.6 + p), 0, 6.283); cx.fill(); }
  }
  // boksor karakterler iceri kosar (S1+0.3 -> S2+0.4)
  const kos = ease(kisit((u - S1 - 0.3) / 1.0, 0, 1));
  if (kos > 0) [['p1', 0, -0.15, 0.27], ['p2', 1, 1.15, 0.73]].forEach(([o, i, a, b]) => {
    const x = W * lerp(a, b, kos), zip = kos < 1 ? Math.abs(Math.sin(u * 14)) * 30 * k : 0;
    cx.save(); cx.shadowColor = RENK[i]; cx.shadowBlur = 40 * k; boksorCiz(o, u, x, H * 0.99 - zip, H * 0.66, kos < 1 ? null : 'jab'); cx.restore();
    const pa = ease(kisit((u - S2 - 0.4) / 0.25, 0, 1));          // onizleme 1: alfa 0'da bos beyaz patlama ciziliyordu
    if (kos >= 1 && pa > 0.01) pYazi(['P1', 'P2'][i], x, H * 0.88, 120 * k, RENK[i], pa);
  });
  // maskot: once kapinin onunde buyuk (iter), sonra alt ortaya kucuk iner
  const m = ease(kisit((u - S1) / 0.8, 0, 1)), zip = Math.abs(Math.sin(t * BPM / 60 * Math.PI)) * 10 * k;
  if (u < S1) maskotCiz(W / 2 + Math.sin(u * 30) * 5 * k, H * 0.74, 1.15, t);
  else maskotCiz(W / 2, lerp(H * 0.74, H * 0.9, m) - zip * m, lerp(1.15, 0.55, m), t);
  if (u < S1) yaziK('PUSH!', W / 2, H * 0.36, 96 * k * (1 + 0.1 * Math.sin(u * 18)), ['#fff6a0', '#ffd23a', '#ff8a1a'], ease(kisit(u / 0.25, 0, 1)), '#4a1400', '#ffffff');
  // VS tas tablet: yukaridan duser, oyulmus V (mavi) S (pembe) parlar
  const q = u - S2;
  if (q >= 0) {
    acilisSoru = kart.soru ? ease(kisit((q - 0.3) / 0.35, 0, 1)) : 0;
    const dus = q < 0.25 ? -H * 0.6 * (1 - ease(q / 0.25)) : 0, zp = q >= 0.25 && q < 0.45 ? 1 + 0.08 * Math.sin((q - 0.25) * 40) : 1;
    const vx = W / 2, vy = H * 0.47 + dus, R = 170 * k * zp;
    cx.save(); cx.shadowColor = '#000000'; cx.shadowBlur = 30 * k;
    const g = cx.createRadialGradient(vx - R * 0.3, vy - R * 0.3, R * 0.1, vx, vy, R); g.addColorStop(0, '#ffcf6a'); g.addColorStop(1, '#b8642a');
    cx.fillStyle = g; cx.strokeStyle = '#4a2008'; cx.lineWidth = 10 * k; cx.beginPath(); cx.arc(vx, vy, R, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();
    cx.save(); cx.strokeStyle = 'rgba(90,40,10,0.55)'; cx.lineWidth = 5 * k; cx.beginPath(); cx.arc(vx, vy, R * 0.82, 0, 6.283); cx.stroke();
    cx.fillStyle = '#2fd04a'; cx.beginPath(); cx.ellipse(vx - R * 0.5, vy - R * 0.82, R * 0.34, R * 0.12, -0.3, 0, 6.283); cx.fill(); cx.restore();
    const isik = kisit((q - 0.25) / 0.3, 0, 1);
    cx.save(); cx.translate(vx, vy); cx.rotate(-0.08); cx.transform(1, 0, -0.16, 1, 0, 0);
    const px = 150 * k * zp; cx.font = F(px); const wV = cx.measureText('V').width, wS = cx.measureText('S').width;
    yazi('V', -wS / 2 + 4 * k, 0, px, ['#ffffff', ACIK[0], RENK[0], KOYU[0]], '#1a0630', 1, isik > 0 ? RENK[0] : null);
    yazi('S', wV / 2 - 4 * k, 0, px, ['#ffffff', ACIK[1], RENK[1], KOYU[1]], '#1a0630', 1, isik > 0 ? RENK[1] : null);
    cx.restore();
    if (q >= 0.25 && q < 0.6) {                                  // tablet yere oturunca tas kirintisi
      const p = (q - 0.25) / 0.35, R6 = rng(515);
      for (let j = 0; j < 24; j++) { const a = R6() * 6.283, dd = (R + 40 * k) + 260 * k * p * R6();
        cx.fillStyle = `rgba(${R6() < 0.5 ? '240,180,100' : '120,70,30'},${1 - p})`; cx.beginPath(); cx.arc(vx + Math.cos(a) * dd, vy + Math.sin(a) * dd, (5 + 8 * R6()) * k, 0, 6.283); cx.fill(); }
    }
    parilti4(vx - R * 0.72, vy - R * 0.72, 30 * k, isik * (0.6 + 0.4 * Math.sin(u * 9)));
  }
}
function acilisCiz(kart, u, t) {
  acilisSoru = 0;
  if (TEMA.acilis === 'taskapi') { tasKapiCiz(kart, u, t); return; }""")
# giriste alt ortadaki maskot tas kapi girisinde tasKapiCiz icinde (cift cizilmesin)
degis("    if (kart.tip === 'acilis') {                                 // TALIMATLAR §4: maskot video boyunca; VS kartinda alt ortada (P1/P2 ve can barlarina degmez)\n"
      "      const v = (t * BPM / 60) % 1; maskotCiz(W / 2, H * 0.9 - Math.abs(Math.sin(v * Math.PI)) * 10 * k, 0.55, t);",
      "    if (kart.tip === 'acilis') {                                 // TALIMATLAR §4: maskot video boyunca; VS kartinda alt ortada (P1/P2 ve can barlarina degmez)\n"
      "      const v = (t * BPM / 60) % 1; if (TEMA.acilis !== 'taskapi') maskotCiz(W / 2, H * 0.9 - Math.abs(Math.sin(v * Math.PI)) * 10 * k, 0.55, t);")
# tas kapi girisinde soru bandi ustte (VS tableti ve boksorlerle cakismaz) - ayni yer (H*0.13) kalir

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", os.path.abspath(HEDEF), len(t))
