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

open(HEDEF, "w", encoding="utf-8").write(t)
print("->", HEDEF, len(t))
