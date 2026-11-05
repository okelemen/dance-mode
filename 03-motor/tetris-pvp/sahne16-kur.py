"""sahne16.html (HUMAN TETRIS 19, REF-070 TetrisBounce SOLO Easy Beginner) uretici: sahne15.html'i kopyalar, REF-070 farklarini
tema bayragi `kopru` ile ekler (sahne16-ek.js). Motor 15 fonksiyonlari ...18 adiyla korunur; bayrak yoksa aynen calisir.

    python sahne16-kur.py
"""
import os

B = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(B, "..")
s = open(os.path.join(M, "sahne15.html"), encoding="utf-8").read()


def r1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


r1("<title>HUMAN TETRIS 18 - motor 15 (yildiz sahnesi cift)</title>", "<title>HUMAN TETRIS 19 - motor 16 (yildiz koprusu solo)</title>")
r1("// MOTOR 15 — HUMAN TETRIS 18", """// MOTOR 16 — HUMAN TETRIS 19 (REF-070 TetrisBounce SOLO Easy Beginner, 3 level x 6). sahne15.html'den, tetris-pvp/sahne16-kur.py uretir.
// REF-070: neon yildiz koprusu (varlik-yildizkopru.py), yanardoner hologram duvar karti + Openclipart kamu mali yoga siluetleri (REF-071),
// pembe 3-2-1, MISSIONS n/6, EASY / MEDIUM / ALL OUT.
// --- asagisi motor 15 aciklamasi (tarihce) ---
// MOTOR 15 — HUMAN TETRIS 18""")
for ad in ("yildizDuvar", "kapiEkran", "yildizHud"):
    r1("function %s(" % ad, "function %s18(" % ad)
EK = open(os.path.join(B, "sahne16-ek.js"), encoding="utf-8").read()
r1("// ------------------------------------------------------------ SAHNE (sabit kamera)", EK + "\n// ------------------------------------------------------------ SAHNE (sabit kamera)")
r1("  const t = n / FPS;\n  sahneCiz(t);", "  const t = n / FPS; ZAMAN_T = t;\n  sahneCiz(t);")
# REF-070 3-2-1: beyaz rakam, pembe kontur (motor 15'te sari)
r1("    yazi(String(n), W * 0.83, H * 0.42, 240 * k * s, ['#fffbd0', '#ffe23a', '#ffb000'], '#a04a00', a, '#ffe23a');",
   "    if (TEMA.kopru) yazi(String(n), W * 0.83, H * 0.42, 240 * k * s, ['#ffffff', '#ffeaf8', '#ffc6ee'], '#e0209e', a, '#ff6ad6');\n"
   "    else yazi(String(n), W * 0.83, H * 0.42, 240 * k * s, ['#fffbd0', '#ffe23a', '#ffb000'], '#a04a00', a, '#ffe23a');")
open(os.path.join(M, "sahne16.html"), "w", encoding="utf-8").write(s)
print("sahne16.html", len(s.splitlines()), "satir")
