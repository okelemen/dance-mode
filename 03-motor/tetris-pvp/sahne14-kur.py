"""sahne14.html (HUMAN TETRIS 17, REF-068 TetrisBounce SOLO) uretici: sahne9.html'i (tek oyuncu, oyuklu duvar) kopyalar, REF-068 farklarini
tema bayragi `galaksi` ile ekler. Eski motorlar degistirilmez (TALIMATLAR §6); yeni motor bu betikle tekrar uretilebilir.

    python sahne14-kur.py
"""
import os

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
s = open(os.path.join(M, "sahne9.html"), encoding="utf-8").read()


def r1(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


r1("<title>HUMAN TETRIS 1 OYUNCU - motor 9</title>", "<title>HUMAN TETRIS 17 - motor 14 (galaksi solo)</title>")
r1("// MOTOR 9 — HUMAN TETRIS 1 OYUNCU", """// MOTOR 14 — HUMAN TETRIS 17 (REF-068 TetrisBounce SOLO, 3 level x 8). sahne9.html'den, tetris-pvp/sahne14-kur.py uretir.
// REF-068: galaksi gogu + neon izgara + truss kapi (varlik-galaksi.py); dongu: kapida sari START! karti -> asagi kayar -> pembe-sari degrade
// duvar (poz OYUK, icinden gok gorunur) + sag ustte pembe konturlu 3-2-1 -> duvar buyur; ust ortada MISSIONS n/8; level basinda LEVEL secim
// ekrani; acilista THREE/TWO/ONE/GO; ara ara hiz cizgili tam ekran ovgu; KENDI maskotumuz video boyunca sol altta.
// --- asagisi motor 9 aciklamasi (tarihce) ---
// MOTOR 9 — HUMAN TETRIS 1 OYUNCU""")

EK = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sahne14-ek.js"), encoding="utf-8").read()
r1("// ------------------------------------------------------------ SAHNE (sabit kamera)", EK + "\n// ------------------------------------------------------------ SAHNE (sabit kamera)")

# sahne: galaksi gogu hareketi + kapi + izgarada akan ince camgobegi oklar
r1("  if (TEMA.neonYildiz) {", "  if (TEMA.galaksi) { galaksiGok(t); cx.drawImage(SERIT, 0, 0, W, H); yolOklari(t); return; }\n  if (TEMA.neonYildiz) {")
# duvar: tek renk yerine pembe-sari degrade
r1("  kc.fillStyle = panel; kc.fillRect(x, y, w, h);", "  kc.fillStyle = TEMA.galaksi ? duvarDegrade(kc, x, y, w, h) : panel; kc.fillRect(x, y, w, h);")
r1("  if (!maske) { cx.save(); cx.globalAlpha = alfa; cx.fillStyle = panel;", "  if (!maske) { cx.save(); cx.globalAlpha = alfa; cx.fillStyle = TEMA.galaksi ? duvarDegrade(cx, x, y, w, h) : panel;")
# kart evresi: START! karti, son %30'da asagi kayar; her 4. duvarda arada kirmizi "!" (REF-068'de ara ara)
r1("""  if (e.ad === 'kart') {
    // REF-061: tabela, ikinci yarıda kırmızı "!" uyarısı""", """  if (e.ad === 'kart' && TEMA.galaksi) {
    const kay = ease(kisit((e.p - 0.7) / 0.3, 0, 1));
    startKart(t, kay, 1 - kay);
    if (d.no % 4 === 3 && e.p > 0.3 && e.p < 0.7) uyariCiz(t, (e.p - 0.3) / 0.4);
  } else if (e.ad === 'kart') {
    // REF-061: tabela, ikinci yarıda kırmızı "!" uyarısı""")
r1("  } else bosPanel(t, ease(Math.min(1, e.p * 2)));\n  return e;", "  } else if (!TEMA.galaksi) bosPanel(t, ease(Math.min(1, e.p * 2)));\n  return e;")
r1("  if (e) sayimCiz(e);", "  if (!d && !TEMA.galaksi) {} \n  if (e) sayimCiz(e);")
r1("  if (d) e = duvarlarCiz(d, t - d.t0, t); else bosPanel(t);", "  if (d) e = duvarlarCiz(d, t - d.t0, t); else if (!TEMA.galaksi) bosPanel(t);")
# izdusum: varlik-galaksi.py ufku lens kaydirmayla (shift_y) indirir -> ekran y'si kaydir * 1920 px asagi
r1("const sx = 960 + (X / zc) / KAM.th * 960, sy = 540 - (yc / zc) / KAM.tv * 540;",
   "const sx = 960 + (X / zc) / KAM.th * 960, sy = 540 - (yc / zc) / KAM.tv * 540 + (KY.kaydir || 0) * 1920;")
# 3-2-1: sag ustte beyaz rakam, pembe kalin kontur (REF-068)
r1("  if (TEMA.sayimKose) {", """  if (TEMA.galaksi) {
    const a = Math.min(1, q / 0.08) * Math.min(1, (1 - q) / 0.2);
    yazi(String(n), W * 0.84, H * 0.2, 230 * k * s, ['#ffffff', '#fff4fb'], '#ff3fae', a, '#ffffff');
    return;
  }
  if (TEMA.sayimKose) {""")
# HUD
r1("  if (TEMA.tekOyuncu) {                                 // REF-061", "  if (TEMA.galaksi) { galaksiHud(t); return; }\n  if (TEMA.tekOyuncu) {                                 // REF-061")
# kartlar
r1("  if (kart.tip === 'vs') {", """  if (TEMA.galaksi && kart.tip === 'tur') levelKart(kart, u, t);
  else if (TEMA.galaksi && kart.tip === 'basla') galaksiBasla(kart, u, t);
  else if (TEMA.galaksi && kart.tip === 'ovgu_kart') galaksiOvgu(kart, u, t);
  else if (kart.tip === 'vs') {""")
# maskot her karede en onde (abone kartinin da ustunde, kosede)
r1("  if (!kartVar) aboneCiz(t);\n}", "  if (!kartVar) aboneCiz(t);\n  if (TEMA.galaksi) maskotKose(t);\n}")
# 3-2-1-GO tam ekran: HUD ve SUBSCRIBE bu kartta cizilmez (sahne13 ile ayni)
r1("kk.tip !== 'basla'", "(kk.tip !== 'basla' || TEMA.baslaTam)")
open(os.path.join(M, "sahne14.html"), "w", encoding="utf-8").write(s)
print("sahne14.html", len(s.splitlines()), "satir")
