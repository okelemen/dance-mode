"""MOTOR 27 (HUMAN TETRIS 30) = sahne26.html (motor 26, 1v1 orman) + yama -> 03-motor/sahne27.html. sahne26 degismez.

    python motor27-yama.py

30: REF-082 yapi, 1v1, gunduz yel degirmenli lale tarlasi (varlik-lale.py), ozel tur MIRROR (motor 23'ten beri d.ayna; 29'un SPEED'i yok),
OUT = saman yiginina gomulur (saman sicramasi), hakem maskot ciftci (2B hasir sapka + kirmizi fular, elinde lale), hakem kursusu
ahsap + iki saksi lale; gokte ucusan lale yapraklari. Giris: normal VS boksor karti (TALIMATLAR §4; tas kapi yalniz 29'du).
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(BURA, "..", "sahne26.html")
HEDEF = os.path.join(BURA, "..", "sahne27.html")
t = open(KAYNAK, encoding="utf-8").read()


def degis(eski, yeni, n=1):
    global t
    assert t.count(eski) == n, (t.count(eski), eski[:90])
    t = t.replace(eski, yeni)


degis("<title>HUMAN TETRIS 29 - motor 26 (iki serit orman tapinagi, tas kapi girisi, SPEED turu, kasif hakem maskot)</title>",
      "<title>HUMAN TETRIS 30 - motor 27 (iki serit lale tarlasi, MIRROR turu, ciftci hakem maskot)</title>")
degis("// MOTOR 26 — HUMAN TETRIS 29 (REFERANSSIZ, 16 Kas 2026; motor 23'ten, tetris-pvp/motor26-yama.py).",
      "// MOTOR 27 — HUMAN TETRIS 30 (REF-082 yapi, 17 Kas 2026; motor 26'dan, tetris-pvp/motor27-yama.py):\n"
      "//   - sahne: tetris-pvp/varlik-lale.py; gokte ucusan lale yapraklari; OUT saman yiginina gomulur (saman sicramasi)\n"
      "//   - hakem maskot ciftci (2B hasir sapka + kirmizi fular, elinde lale), ahsap kursu + iki saksi lale; MIRROR ROUND (d.ayna)\n"
      "// --- motor 26 aciklamasi ---\n"
      "// MOTOR 26 — HUMAN TETRIS 29 (REFERANSSIZ, 16 Kas 2026; motor 23'ten, tetris-pvp/motor26-yama.py).")

# gokte lale yapraklari
degis("const KONF_R = ['#3ccf3e', '#1fae3a', '#ffcc1e', '#ff6ab0', '#7ae05a', '#ff8a1e'];   // motor 26: orman yapraklari + cicek yapraklari",
      "const KONF_R = ['#ff1e3c', '#ffd21e', '#ff7a14', '#ff3ab4', '#a040ff', '#ffffff'];   // motor 27: lale yapraklari")

# elde lale (mesale yerine) - laleCiz fonksiyonu mesaleCiz'in onune
degis("function mesaleCiz(x, y, r, t) {",
      """function laleCiz(x, y, r, t, renk) {                          // motor 27: lale - yesil sap + iki yaprak + uc tac yaprakli kirmizi cicek
  cx.save(); cx.translate(x, y); cx.rotate(0.08 * Math.sin(t * 3));
  cx.strokeStyle = '#1f9a2e'; cx.lineWidth = r * 0.22; cx.lineCap = 'round'; cx.beginPath(); cx.moveTo(0, r * 2.4); cx.lineTo(0, r * 0.2); cx.stroke();
  cx.fillStyle = '#2fc44a'; cx.strokeStyle = '#14601e'; cx.lineWidth = r * 0.08;
  for (const s of [-1, 1]) { cx.beginPath(); cx.ellipse(s * r * 0.42, r * 1.6, r * 0.28, r * 0.85, s * 0.45, 0, 6.283); cx.fill(); cx.stroke(); }
  const c = renk || '#ff1e3c';
  cx.fillStyle = c; cx.strokeStyle = '#5a0010'; cx.lineWidth = r * 0.1;
  cx.beginPath(); cx.moveTo(-r * 0.7, -r * 0.2); cx.quadraticCurveTo(-r * 0.8, r * 0.75, 0, r * 0.75); cx.quadraticCurveTo(r * 0.8, r * 0.75, r * 0.7, -r * 0.2);
  cx.lineTo(r * 0.4, r * 0.15); cx.lineTo(0, -r * 0.55); cx.lineTo(-r * 0.4, r * 0.15); cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.ellipse(-r * 0.3, r * 0.2, r * 0.12, r * 0.3, -0.3, 0, 6.283); cx.fill();
  cx.restore();
}
function mesaleCiz(x, y, r, t) {""")
degis("  if (!yuzSadece) mesaleCiz(x + (78 + bs) * s * k, y - 70 * s * k, 22 * s * k, t);   // motor 26: elde mesale",
      "  if (!yuzSadece) laleCiz(x + (78 + bs) * s * k, y - 70 * s * k, 22 * s * k, t);   // motor 27: elde lale")

# maskot: kirmizi fular + hasir sapka
degis("  cx.fillStyle = '#1fae3a'; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(-32, 44); cx.lineTo(32, 44); cx.lineTo(0, 74); cx.closePath(); cx.fill(); cx.stroke();   // motor 26: yesil fular",
      "  cx.fillStyle = '#ff2a3a'; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(-32, 44); cx.lineTo(32, 44); cx.lineTo(0, 74); cx.closePath(); cx.fill(); cx.stroke();   // motor 27: kirmizi fular\n"
      "  cx.fillStyle = '#ffffff'; for (const [px, py] of [[-14, 52], [10, 50], [0, 62]]) { cx.beginPath(); cx.arc(px, py, 3, 0, 6.283); cx.fill(); }   // puantiye")
degis("""  cx.save(); cx.translate(0, -50); cx.rotate(-0.06 + 0.04 * Math.sin(t * 3));       // motor 26: kasif sapkasi (genis kenar, haki, yesil bant)
  const sg = cx.createLinearGradient(0, -52, 0, 8); sg.addColorStop(0, '#ffd27a'); sg.addColorStop(1, '#e0962e');
  cx.fillStyle = sg; cx.lineWidth = 4;
  cx.beginPath(); cx.ellipse(0, 0, 84, 17, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.beginPath(); cx.moveTo(-46, -2); cx.bezierCurveTo(-48, -58, 48, -58, 46, -2); cx.closePath(); cx.fill(); cx.stroke();
  cx.fillStyle = '#1fae3a'; cx.beginPath(); cx.moveTo(-46, -6); cx.lineTo(46, -6); cx.lineTo(45, -18); cx.lineTo(-45, -18); cx.closePath(); cx.fill(); cx.stroke();""",
      """  cx.save(); cx.translate(0, -50); cx.rotate(-0.06 + 0.04 * Math.sin(t * 3));       // motor 27: hasir sapka (genis duz kenar, sari, kirmizi bant)
  const sg = cx.createLinearGradient(0, -52, 0, 8); sg.addColorStop(0, '#fff07a'); sg.addColorStop(1, '#f0b020');
  cx.fillStyle = sg; cx.lineWidth = 4;
  cx.beginPath(); cx.ellipse(0, 0, 92, 16, 0, 0, 6.283); cx.fill(); cx.stroke();
  cx.beginPath(); cx.moveTo(-42, -2); cx.lineTo(-38, -44); cx.quadraticCurveTo(0, -54, 38, -44); cx.lineTo(42, -2); cx.closePath(); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(160,100,10,0.55)'; cx.lineWidth = 2;
  for (const yy of [-26, -36]) { cx.beginPath(); cx.moveTo(-39, yy); cx.lineTo(39, yy); cx.stroke(); }   // hasir orgu
  cx.strokeStyle = KN; cx.lineWidth = 4;
  cx.fillStyle = '#ff2a3a'; cx.beginPath(); cx.moveTo(-42, -4); cx.lineTo(42, -4); cx.lineTo(41, -16); cx.lineTo(-41, -16); cx.closePath(); cx.fill(); cx.stroke();
  laleCiz(30, -26, 9, t, '#ffd21e');                                 // bantta kucuk sari lale""")

# hakem kursusu: ahsap + iki saksi lale
degis("  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ffb04a'); g.addColorStop(1, '#c06a24');   // motor 26: oymali tas kursu",
      "  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ff8a2a'); g.addColorStop(1, '#b8501a');   // motor 27: ahsap kursu")
degis("""  cx.fillStyle = '#2fd04a'; for (const dx of [-0.38, 0.12, 0.4]) { cx.beginPath(); cx.ellipse(xm + dx * w, y0 + 4 * k, 18 * k, 8 * k, 0, 0, 6.283); cx.fill(); }   // yosun
  mesaleCiz(xm - w * 0.56, y0 - 34 * k, 13 * k, t); mesaleCiz(xm + w * 0.56, y0 - 34 * k, 13 * k, t);""",
      """  cx.strokeStyle = 'rgba(90,30,8,0.5)'; cx.lineWidth = 2 * k; for (const dx of [-0.25, 0.0, 0.25]) { cx.beginPath(); cx.moveTo(xm + dx * w, y0 + 18 * k); cx.lineTo(xm + dx * w, H); cx.stroke(); }   // tahta cizgileri
  for (const [s, c] of [[-1, '#ff1e3c'], [1, '#ffd21e']]) {          // iki saksi lale
    const xs = xm + s * w * 0.56;
    laleCiz(xs, y0 - 46 * k, 13 * k, t, c);
    cx.fillStyle = '#d8562a'; cx.strokeStyle = '#6a2008'; cx.lineWidth = 3 * k;
    cx.beginPath(); cx.moveTo(xs - 16 * k, y0 - 16 * k); cx.lineTo(xs + 16 * k, y0 - 16 * k); cx.lineTo(xs + 11 * k, y0 + 6 * k); cx.lineTo(xs - 11 * k, y0 + 6 * k); cx.closePath(); cx.fill(); cx.stroke();
  }""")

# OUT: camur yerine saman sicramasi
degis("  cx.strokeStyle = 'rgba(122,66,32,0.9)'; cx.lineWidth = 14 * k * (1 - q);   // motor 26: camur halkasi",
      "  cx.strokeStyle = 'rgba(240,176,32,0.9)'; cx.lineWidth = 14 * k * (1 - q);   // motor 27: saman halkasi (26'da yorum satiri halkayi yutuyordu)\n ")
degis("    cx.fillStyle = ['#7a4220', '#5a3016', '#a8642e'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 26: camur damlasi",
      "    cx.strokeStyle = ['#ffd23a', '#f0a018', '#ffe58a'][j % 3]; cx.lineWidth = (3 + 3 * R2()) * k * olc * (1 - q * 0.5); cx.lineCap = 'round';\n"
      "    { const a_ = R2() * 6.283, l_ = (10 + 14 * R2()) * k * olc; cx.beginPath(); cx.moveTo(x - Math.cos(a_) * l_, y - Math.sin(a_) * l_); cx.lineTo(x + Math.cos(a_) * l_, y + Math.sin(a_) * l_); cx.stroke(); }   // motor 27: saman copu")

# YENI GIRIS (17 Kas 2026, kullanici: "box eldivenleri falan olmasin ... 1 ve 3 olsun"; TALIMATLAR §4):
# TEMA.acilis='kanca': 0-1,6 BOSS WALL onizleme + CAN YOU PASS THIS? -> 1,6-2,0 geri sarma -> 2,0- yel degirmeni kanadi + lale yapragi
# firtinasi sahneyi acar, hakem maskot kursude, WHO WILL WIN? BLUE OR PINK? Boksor yok. Ilk duvar yine 3,53 sn.
degis("function acilisCiz(kart, u, t) {\n  acilisSoru = 0;\n  if (TEMA.acilis === 'taskapi') { tasKapiCiz(kart, u, t); return; }",
      r"""const KH = 1.6, KR_ = 0.4;                                      // motor 27 kanca: onizleme / geri sarma sureleri
function kancaBoss(ub) {                                        // BOSS WALL'un gercek karesini (karakterler + hakem dahil) ciz
  const d = DUVARLAR[DUVARLAR.length - 1], tb = d.t0 + ub;
  AYNA = false; sahneCiz(tb); hakemCiz(tb, d, ub); duvarCiz(d, ub, tb);
}
function kanatCiz(x, y, L, a) {                                 // yel degirmeni kanadi: ahsap kafes + kirmizi-beyaz bez, cilali
  cx.save(); cx.translate(x, y); cx.rotate(a);
  const b = L * 0.16;
  for (let j = 0; j < 4; j++) {
    cx.save(); cx.rotate(j * Math.PI / 2);
    const g = cx.createLinearGradient(0, -b, 0, b); g.addColorStop(0, '#ff5a5a'); g.addColorStop(0.5, '#e01a2a'); g.addColorStop(1, '#a00818');
    cx.fillStyle = g; cx.strokeStyle = '#5a2a0a'; cx.lineWidth = 10 * k;
    cx.beginPath(); cx.roundRect(L * 0.12, -b, L * 0.88, b * 2, 18 * k); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.92)';
    for (let q = 0; q < 4; q++) { cx.beginPath(); cx.roundRect(L * (0.16 + q * 0.21), -b * 0.82, L * 0.17, b * 0.7, 8 * k); cx.fill(); }
    cx.strokeStyle = '#8a4a1a'; cx.lineWidth = 7 * k;
    for (let q = 0; q <= 8; q++) { const xx = L * (0.12 + q * 0.11); cx.beginPath(); cx.moveTo(xx, -b); cx.lineTo(xx, b); cx.stroke(); }
    cx.beginPath(); cx.moveTo(L * 0.12, 0); cx.lineTo(L, 0); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(L * 0.14, -b * 0.95, L * 0.84, b * 0.22, 6 * k); cx.fill();
    const gk = cx.createLinearGradient(0, -b * 0.3, 0, b * 0.3); gk.addColorStop(0, '#c8843a'); gk.addColorStop(1, '#6a3410');
    cx.fillStyle = gk; cx.fillRect(0, -b * 0.28, L * 0.2, b * 0.56);
    cx.restore();
  }
  const gh = cx.createRadialGradient(-b * 0.3, -b * 0.3, b * 0.1, 0, 0, b * 1.2); gh.addColorStop(0, '#ffe08a'); gh.addColorStop(1, '#a8601a');
  cx.fillStyle = gh; cx.strokeStyle = '#4a2008'; cx.lineWidth = 10 * k; cx.beginPath(); cx.arc(0, 0, b * 1.1, 0, 6.283); cx.fill(); cx.stroke();
  cx.restore();
}
function kancaCiz(kart, u, t) {
  if (u < KH + KR_) {
    const d = DUVARLAR[DUVARLAR.length - 1], Z = ZD(d), u0 = Z.kart + Z.say * 0.55, u1 = Z.kart + Z.say + Z.buyu * 0.4;
    const ub = u < KH ? lerp(u0, u1, ease(u / KH)) : lerp(u1, Z.kart * 0.5, ease((u - KH) / KR_));   // geri sarmada zaman geri akar
    kancaBoss(ub);
    if (u < KH) {
      cx.save(); cx.globalAlpha = 0.25 + 0.2 * Math.sin(u * 14); cx.strokeStyle = '#ff1a2a'; cx.lineWidth = 60 * k; cx.strokeRect(0, 0, W, H); cx.restore();
      const g = ease(kisit((u - 0.1) / 0.25, 0, 1)), p = 1 + 0.12 * Math.max(0, 1 - (u - 0.1) * 5) + 0.03 * Math.sin(u * 9);
      if (g > 0.01) {
        cx.save(); cx.globalAlpha = g * 0.82; cx.fillStyle = '#1a0408'; cx.beginPath(); cx.roundRect(W / 2 - 680 * k, H * 0.13 - 74 * k, 1360 * k, 148 * k, 74 * k); cx.fill(); cx.restore();
        yaziK('CAN YOU PASS THIS?', W / 2, H * 0.13, 110 * k * g * p, ['#ffffff', '#fff27a', '#ffc21a'], g, '#3a0a00', '#ffffff');
      }
    } else {                                                    // geri sarma: VHS seritleri + << isareti
      const q = (u - KH) / KR_;
      cx.save(); cx.globalCompositeOperation = 'lighter';
      for (let j = 0; j < 7; j++) { const yy = ((j * 0.31 + q * 3.7) % 1) * H; cx.fillStyle = 'rgba(255,255,255,0.18)'; cx.fillRect(0, yy, W, (10 + 22 * ((j * 7) % 3)) * k); }
      cx.restore();
      cx.save(); cx.fillStyle = 'rgba(20,10,40,0.18)'; cx.fillRect(0, 0, W, H); cx.restore();
      cx.save(); cx.fillStyle = '#ffffff'; cx.strokeStyle = '#1a0630'; cx.lineWidth = 8 * k; cx.translate(150 * k, 140 * k);
      for (const dx of [0, 70 * k]) { cx.beginPath(); cx.moveTo(dx, 0); cx.lineTo(dx + 70 * k, -48 * k); cx.lineTo(dx + 70 * k, 48 * k); cx.closePath(); cx.stroke(); cx.fill(); }
      cx.restore();
    }
    return;
  }
  // mekan acilisi (30: lale tarlasi) - sahne kareKur'da zaten cizili
  const ua = u - KH - KR_;
  hakemCiz(t, null, 0);                                         // hakem kursusunde, ilk duvarla ayni yer
  const ac = ease(kisit((ua - 0.3) / 0.6, 0, 1));                // kanat donerken buyur, kameranin icinden gecer
  if (ac < 1) {
    cx.save(); cx.globalAlpha = 1 - ac; kanatCiz(W / 2, H * 0.5, W * 0.62 * (1 + 1.6 * ac), ua * 4.2 + 0.4); cx.restore();
  }
  const R = rng(3030);                                          // lale yapragi firtinasi soldan saga
  for (let j = 0; j < 110; j++) {
    const hz = 0.8 + 0.7 * R(), y0 = R() * H, ph = R(), c = KONF_R[Math.floor(R() * 5)], r = (16 + 26 * R()) * k;
    const x = (-0.25 + (ua * hz * 1.1 + ph * 0.6 - 0.2)) * W, y = y0 + Math.sin(ua * 5 + ph * 9) * 50 * k;
    if (x < -60 * k || x > W + 60 * k) continue;
    cx.save(); cx.translate(x, y); cx.rotate(ph * 6 + ua * 6 * hz); cx.scale(1, 0.4 + 0.6 * Math.abs(Math.sin(ua * 7 * hz + ph * 5)));
    cx.fillStyle = c; cx.strokeStyle = 'rgba(80,0,20,0.5)'; cx.lineWidth = 2 * k;
    cx.beginPath(); cx.ellipse(0, 0, r, r * 0.55, 0, 0, 6.283); cx.fill(); cx.stroke();
    cx.fillStyle = 'rgba(255,255,255,0.45)'; cx.beginPath(); cx.ellipse(-r * 0.3, -r * 0.15, r * 0.35, r * 0.15, 0, 0, 6.283); cx.fill();
    cx.restore();
  }
  if (ua < 0.18) { cx.save(); cx.fillStyle = `rgba(255,255,255,${0.85 * (1 - ua / 0.18)})`; cx.fillRect(0, 0, W, H); cx.restore(); }
  acilisSoru = kart.soru ? ease(kisit((ua - 0.55) / 0.3, 0, 1)) : 0;
  const pa = ease(kisit((ua - 0.7) / 0.25, 0, 1));
  if (pa > 0.01) for (let i = 0; i < 2; i++) pYazi(['P1', 'P2'][i], i * SW + SW / 2, H * 0.6, 150 * k, RENK[i], pa);
}
function acilisCiz(kart, u, t) {
  acilisSoru = 0;
  if (TEMA.acilis === 'kanca') { kancaCiz(kart, u, t); return; }
  if (TEMA.acilis === 'taskapi') { tasKapiCiz(kart, u, t); return; }""")
degis("if (TEMA.acilis !== 'taskapi') maskotCiz(W / 2, H * 0.9",
      "if (TEMA.acilis !== 'taskapi' && TEMA.acilis !== 'kanca') maskotCiz(W / 2, H * 0.9")

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
