"""sahne13.html (HUMAN TETRIS 16, REF-067) uretici: sahne11.html'i kopyalar, REF-067 farklarini uygular.
Eski motorlar degistirilmez (TALIMATLAR §6); yeni motor bu betikle tekrar uretilebilir.

    python sahne13-kur.py
"""
import os, re

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
s = open(os.path.join(M, "sahne11.html"), encoding="utf-8").read()


def degistir(ad, yeni):
    global s
    i = s.index("function " + ad + "(")
    m = re.compile(r"\n(?=function |const |let |// -|window\.)").search(s, i + 10)
    s = s[:i] + yeni.strip("\n") + "\n" + s[m.start() + 1:]


def r1(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


r1("<title>TETRIS MODE PVP - motor 4</title>", "<title>HUMAN TETRIS 16 - motor 13 (sakura)</title>")
r1("// MOTOR 4 — TETRIS MODE PVP (1v1).", """// MOTOR 13 — HUMAN TETRIS 16 (REF-067 TetrisBounce, 1v1). sahne11.html'den, tetris-pvp/sahne13-kur.py uretir.
// REF-067: sol MAVI / sag PEMBE sakura koprusu (Blender toon, varlik-sakura.py), kapida PLAYER kafes karti, duvar = beyaz girdapli
// kart + duz simsiyah poz (oyuk degil), ortada 3-2-1, kart tam ekrana buyur; ustte ROUND + iki avatarli cekisme cubugu;
// tam ekran kartlar piksel yazi + mor izgara zemin; iki kapi arasinda salincakta KENDI maskotumuz (telif: anime kiz yok).
// --- asagisi motor 4 aciklamasi (tarihce) ---
// MOTOR 4 — TETRIS MODE PVP (1v1).""")
r1("const GOK2 = await resim(VARLIK + 'gok2.png');\n", "")
r1("// MOTOR 11 - HUMAN TETRIS 14", "// (motor 11 notu) HUMAN TETRIS 14")

YARDIMCI = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sahne13-parca.js"), encoding="utf-8").read()
r1("// ------------------------------------------------------------ SAHNE (sabit kamera)", YARDIMCI + "\n// ------------------------------------------------------------ SAHNE (sabit kamera)")

PARCA = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sahne13-fonk.js"), encoding="utf-8").read()
for blok in PARCA.split("\n//@@ ")[1:]:
    ad, govde = blok.split("\n", 1)
    degistir(ad.strip(), govde)

r1("const KAM = { z: 1.75, p: -2.1 * Math.PI / 180, tv: 12 / 18 };      // varlik-altinkopru.py KAM",
   "const KAM = { z: 1.7, p: -1.2 * Math.PI / 180, tv: 12 / 17 };       // varlik-sakura.py KAM")
r1("    const y = 8.6 - ((j * ARA + t * HIZ_OK) % (ARA * N));\n    if (y < 3.0 || y > 8.4) continue;\n    const a = Math.min(1, (8.4 - y) / 1.2) * Math.min(1, (y - 3.0) / 0.6);",
   "    const y = 7.8 - ((j * ARA + t * HIZ_OK) % (ARA * N));\n    if (y < 2.6 || y > 7.6) continue;\n    const a = Math.min(1, (7.6 - y) / 1.2) * Math.min(1, (y - 2.6) / 0.6);")
r1("    cx.shadowColor = '#ffb040'; cx.shadowBlur = 12 * k;\n    cx.fillStyle = `rgba(255,236,170,${0.3 * a})`; cx.fill();",
   "    cx.shadowColor = '#ffffff'; cx.shadowBlur = 12 * k;\n    cx.fillStyle = `rgba(255,240,252,${0.32 * a})`; cx.fill();")

KART = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sahne13-kart.js"), encoding="utf-8").read()
for blok in KART.split("\n//== ESKI\n")[1:]:
    eski, yeni = blok.split("\n//== YENI\n")
    r1(eski.rstrip("\n"), yeni.rstrip("\n"))

# maskot saydamligi sahne cizilmeden ONCE (kesit kontrolu 1: sayimda "2" maskotun ustune biniyordu)
r1("  SON_T = t;\n", "  SON_T = t;\n  { const d0 = DUVARLAR.find(x => t >= x.t0 && t < x.t0 + Z.sure); MASKOT_ALFA = d0 ? maskotAlfa(evre(t - d0.t0)) : 1; }\n")
# kesit kontrolu 1 (3 Kas 2026): varlik-08 boksorlerinde p1 pembe ekipmanli -> mavi yarida pembe boksor; tema.boksorTers yer degistirir
r1("  const B = BOKSOR[o];", "  const B = BOKSOR[TEMA.boksorTers ? (o === 'p1' ? 'p2' : 'p1') : o];")
# REF-067'de 3-2-1-GO tam ekran kart: HUD ve SUBSCRIBE bu kartta da cizilmez
r1("kk.tip !== 'basla'", "(kk.tip !== 'basla' || TEMA.baslaTam)")
open(os.path.join(M, "sahne13.html"), "w", encoding="utf-8").write(s)
print("sahne13.html", len(s.splitlines()), "satir")
