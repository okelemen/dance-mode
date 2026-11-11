"""sahne20.html (HUMAN TETRIS 23, REF-078 HumanWarmUp CO-OP 2 oyuncu) uretici: sahne15.html'i kopyalar, tema bayragi `altigen` ile
REF-078 farklarini ekler. galaksi / yildiz bayraklari KAPALI -> HumanWarmUp dongusu (motor 7-9): "Coming Soon" tabelasi -> "!" -> 3-2-1 ->
duz SARI duvar (oyuk cift) buyur -> gecer; Mission n/N + Next Challenge. Eski motorlar degistirilmez (TALIMATLAR §6).

    python sahne20-kur.py
"""
import os

B = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(B, "..")
s = open(os.path.join(M, "sahne15.html"), encoding="utf-8").read()


def r1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


r1("<title>HUMAN TETRIS 18 - motor 15 (yildiz sahnesi cift)</title>", "<title>HUMAN TETRIS 23 - motor 20 (altigen tunel CO-OP)</title>")
r1("// MOTOR 15 — HUMAN TETRIS 18", """// MOTOR 20 — HUMAN TETRIS 23 (REF-078 HumanWarmUp CO-OP 2 Players #89, 24 Mission). sahne15.html'den, tetris-pvp/sahne20-kur.py uretir.
// REF-078: altigen neon tunel (varlik-altigentunel.py; gok.png'de sabit halkalar + burada akan pembe / mavi halkalar), tek serit neon kopru;
// dongu motor 7-9 (HumanWarmUp): kafes kapida "Coming Soon" tabelasi -> kirmizi "!" -> 3-2-1 -> duz SARI duvar, oyuk cift silueti, buyur, gecer.
// Alt ortada "Mission n/N", sag altta "Next Challenge" ikonu. Seri sabitleri: kendi maskotumuz video boyunca (sol alt), SUBSCRIBE altinda
// LIKE / COMMENT / SHARE (Masaustu md. 27), yazilar konturlu (md. 28). 3-2-1 sagda: ust ortada SUBSCRIBE ile ust uste binmesin.
// --- asagisi motor 15 aciklamasi (tarihce) ---
// MOTOR 15 — HUMAN TETRIS 18""")
r1("  if (TEMA.yildiz) { yildizGok(t); cx.drawImage(SERIT, 0, 0, W, H); kapiEkran(t); levelEtiket(t); return; }",
   "  if (TEMA.altigen) { tunelHareket(t); cx.drawImage(SERIT, 0, 0, W, H); yolOklari(t); ampulCiz(t); return; }\n"
   "  if (TEMA.yildiz) { yildizGok(t); cx.drawImage(SERIT, 0, 0, W, H); kapiEkran(t); levelEtiket(t); return; }")
r1("    const rk = j % 2 ? '#ff4fd8' : '#9b5bff';", "    const rk = j % 2 ? '#ff4fd8' : (TEMA.altigen ? '#4f8bff' : '#9b5bff');")
# 3-2-1: REF-078'de ust ortada beyaz egik rakam; bizde ust orta SUBSCRIBE'in yeri -> ayni rakam sagda (dolu beyaz + koyu kontur, md. 28)
r1("  if (TEMA.yildiz) {                                   // REF-069: sagda sari parlak rakam, turuncu kontur",
   "  if (TEMA.altigen) {\n"
   "    const a = Math.min(1, q / 0.08) * Math.min(1, (1 - q) / 0.2);\n"
   "    cx.save(); cx.translate(W * 0.85, H * 0.34); cx.transform(1, 0, -0.16, 1, 0, 0);\n"
   "    yazi(String(n), 0, 0, 250 * k * s, ['#ffffff', '#ffffff', '#e6dcff'], '#1a0630', a, '#ffffff');\n"
   "    cx.restore();\n    return;\n  }\n"
   "  if (TEMA.yildiz) {                                   // REF-069: sagda sari parlak rakam, turuncu kontur")
# Mission sayaci: REF-078'de alt ortada; sol alt kose maskotun
r1("    cx.save(); cx.translate(28 * k, H - 42 * k); cx.transform(1, 0, -0.2, 1, 0, 0);\n    cx.font = F(44 * k); cx.textAlign = 'left';",
   "    cx.save(); cx.translate(TEMA.altigen ? W / 2 : 28 * k, H - 42 * k); cx.transform(1, 0, -0.2, 1, 0, 0);\n    cx.font = F(44 * k); cx.textAlign = TEMA.altigen ? 'center' : 'left';")
# Next Challenge yazisi sari duvarin ustunde beyaz kaliyordu -> koyu kontur (md. 28)
r1("    cx.fillText('Next', 0, -15 * k); cx.fillText('Challenge:', 0, 15 * k);".replace("    ", "  ", 1),
   "  cx.lineJoin = 'round'; cx.lineWidth = 7 * k; cx.strokeStyle = 'rgba(10,4,30,0.92)'; cx.strokeText('Next', 0, -15 * k); cx.strokeText('Challenge:', 0, 15 * k);\n"
   "  cx.fillText('Next', 0, -15 * k); cx.fillText('Challenge:', 0, 15 * k);")
r1("  if (TEMA.galaksi) maskotKose(t);", "  if (TEMA.galaksi || TEMA.altigen) maskotKose(t);")
r1("  const ust = TEMA.yildiz && KARTLAR.some(kk => kk.tip === 'acilis' && t >= kk.t && t < kk.t + kk.sure);",
   "  const ust = (TEMA.yildiz || TEMA.altigen) && KARTLAR.some(kk => kk.tip === 'acilis' && t >= kk.t && t < kk.t + kk.sure);")
r1("  if (TEMA.yildiz) begenSatiri(W / 2, yM + 96 * k, cik, u, t);   // Masaustu md. 27",
   "  if (TEMA.yildiz || TEMA.altigen) begenSatiri(W / 2, yM + 96 * k, cik, u, t);   // Masaustu md. 27")
# tam video kontrolu 1 (md. 28): acilista PLAYER 1 / PLAYER 2 kendi renkli bandinda beyaz konturla okunmuyordu -> duz renk + koyu kontur (motor 15'teki gibi)
r1("  yazi(m, 0, 0, px, TEMA.yildiz ? [renk, renk, renk] : ['#ffffff', renk, renk], TEMA.yildiz ? '#1a0630' : '#ffffff', a, renk);",
   "  yazi(m, 0, 0, px, (TEMA.yildiz || TEMA.altigen) ? [renk, renk, renk] : ['#ffffff', renk, renk], (TEMA.yildiz || TEMA.altigen) ? '#1a0630' : '#ffffff', a, renk);")
# tam video kontrolu 1 (md. 27): kapanis SUBSCRIBE kartinda LIKE / COMMENT / SHARE yoktu
r1("    yazi(TEMA.aboneAlt, W / 2, H * 0.68, 70 * k * g + 1, ['#ffffff', TEMA.p1acik], '#06122e', g);",
   "    yazi(TEMA.aboneAlt, W / 2, H * 0.68, 70 * k * g + 1, ['#ffffff', TEMA.p1acik], '#06122e', g);\n"
   "    if (TEMA.altigen) begenSatiri(W / 2, H * 0.85, 1.2, u, t);")
open(os.path.join(M, "sahne20.html"), "w", encoding="utf-8", newline="\n").write(s)
print("sahne20.html", len(s.splitlines()), "satir")
