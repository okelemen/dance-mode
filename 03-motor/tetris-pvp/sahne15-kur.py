"""sahne15.html (HUMAN TETRIS 18, REF-069 TetrisBounce 2 oyuncu cift / CO-OP) uretici: sahne14.html'i (galaksi; level yapisi, grup maskesi)
kopyalar, REF-069 farklarini tema bayragi `yildiz` ile ekler (sahne15-ek.js). Eski motorlar degistirilmez (TALIMATLAR §6).

    python sahne15-kur.py
"""
import os

B = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(B, "..")
s = open(os.path.join(M, "sahne14.html"), encoding="utf-8").read()


def r1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


r1("<title>HUMAN TETRIS 17 - motor 14 (galaksi solo)</title>", "<title>HUMAN TETRIS 18 - motor 15 (yildiz sahnesi cift)</title>")
r1("// MOTOR 14 — HUMAN TETRIS 17", """// MOTOR 15 — HUMAN TETRIS 18 (REF-069 TetrisBounce 2 PLAYER cift, CO-OP, 3 level x 8). sahne14.html'den, tetris-pvp/sahne15-kur.py uretir.
// REF-069: neon yildiz sahnesi (varlik-yildizsahne.py); dongu: kapi ekraninda sonuk neon cift tabelasi -> kapida renkli DAMALI kart + siyah cift
// silueti, sagda sari 3-2-1 -> kart buyur (yakinda P1/P2 renginde neon kontur); ustte Start -> kupa ilerleme cubugu, kapi ustunde level etiketi;
// pastel kartlar; SUBSCRIBE altinda LIKE / COMMENT / SHARE (Masaustu md. 27); kendi maskotumuz yildiz kiyafetiyle sol altta.
// --- asagisi motor 14 aciklamasi (tarihce) ---
// MOTOR 14 — HUMAN TETRIS 17""")

EK = open(os.path.join(B, "sahne15-ek.js"), encoding="utf-8").read()
r1("// ------------------------------------------------------------ SAHNE (sabit kamera)", EK + "\n// ------------------------------------------------------------ SAHNE (sabit kamera)")
r1("  if (TEMA.galaksi) { galaksiGok(t); cx.drawImage(SERIT, 0, 0, W, H); yolOklari(t); return; }",
   "  if (TEMA.yildiz) { yildizGok(t); cx.drawImage(SERIT, 0, 0, W, H); kapiEkran(t); levelEtiket(t); return; }\n"
   "  if (TEMA.galaksi) { galaksiGok(t); cx.drawImage(SERIT, 0, 0, W, H); yolOklari(t); return; }")
r1("function duvarIc(i, x, y, w, h, panel, maske, alfa) {\n",
   "function duvarIc(i, x, y, w, h, panel, maske, alfa) {\n  if (TEMA.yildiz) { yildizDuvar(i, x, y, w, h, maske, alfa); return; }\n")
r1("  if (e.ad === 'kart' && TEMA.galaksi) {",
   "  if (e.ad === 'kart' && TEMA.yildiz) {\n    // REF-069: duvar gelmeden kapi ekraninda sonuk neon cift tabelasi (sahneCiz -> kapiEkran)\n  } else if (e.ad === 'kart' && TEMA.galaksi) {")
r1("  if (TEMA.galaksi) {\n    const a = Math.min(1, q / 0.08) * Math.min(1, (1 - q) / 0.2);",
   "  if (TEMA.yildiz) {                                   // REF-069: sagda sari parlak rakam, turuncu kontur\n"
   "    const a = Math.min(1, q / 0.08) * Math.min(1, (1 - q) / 0.2);\n"
   "    yazi(String(n), W * 0.83, H * 0.42, 240 * k * s, ['#fffbd0', '#ffe23a', '#ffb000'], '#a04a00', a, '#ffe23a');\n"
   "    return;\n  }\n"
   "  if (TEMA.galaksi) {\n    const a = Math.min(1, q / 0.08) * Math.min(1, (1 - q) / 0.2);")
r1("  if (TEMA.galaksi) { galaksiHud(t); return; }", "  if (TEMA.yildiz) { yildizHud(t, tur, ilerleme); return; }\n  if (TEMA.galaksi) { galaksiHud(t); return; }")
r1("  if (TEMA.galaksi && kart.tip === 'tur') levelKart(kart, u, t);",
   "  if (TEMA.yildiz && ['yazi', 'nasil', 'tur', 'basla', 'abone'].includes(kart.tip)) yildizKart(kart, u, t);\n"
   "  else if (TEMA.galaksi && kart.tip === 'tur') levelKart(kart, u, t);")
r1("  maskotCiz(W * 0.075, H * 0.86 - zip, 1.05, t);", "  (TEMA.yildiz ? maskotYildiz : maskotCiz)(W * 0.075, H * 0.86 - zip, 1.05, t);")
r1("    cx.restore();\n  }\n}\n\nwindow.kareKur = kareKur;",
   "    cx.restore();\n  }\n  if (TEMA.yildiz) begenSatiri(W / 2, yM + 96 * k, cik, u, t);   // Masaustu md. 27\n}\n\nwindow.kareKur = kareKur;")
# CO-OP acilis: P2 boksoru duvara donmesin (sahne12'deki 15. video dersi)
r1("      if (TEMA.tekOyuncu && i === 1) duvarMini(", "      if (TEMA.tekOyuncu && !TEMA.acilisIkili && i === 1) duvarMini(")
r1("    if (TEMA.tekOyuncu && o === 'p2') duvarMini(", "    if (TEMA.tekOyuncu && !TEMA.acilisIkili && o === 'p2') duvarMini(")
# kesit 1 mantik kontrolu: PLAYER 1 / PLAYER 2 kendi renginde ama kendi renkli bandinda beyaz konturla okunmuyordu -> koyu kontur
r1("  yazi(m, 0, 0, px, ['#ffffff', renk, renk], '#ffffff', a, renk);",
   "  yazi(m, 0, 0, px, TEMA.yildiz ? [renk, renk, renk] : ['#ffffff', renk, renk], TEMA.yildiz ? '#1a0630' : '#ffffff', a, renk);")
open(os.path.join(M, "sahne15.html"), "w", encoding="utf-8").write(s)
print("sahne15.html", len(s.splitlines()), "satir")
