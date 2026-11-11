"""motor 22 (HUMAN TETRIS 25) = sahne21.html + bu yamalar. python motor22-yama.py -> sahne22.html (bir kez; sonra sahne22.html dogrudan duzenlenir)."""
import os
BURA = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(BURA, "sahne21.html"), encoding="utf-8").read()


def R(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


R('<title>HUMAN TETRIS 24 - motor 21 (iki serit havuzlu stadyum, yarisan karakterler, hakem maskot)</title>',
  '<title>HUMAN TETRIS 25 - motor 22 (iki serit oyun gorunumlu spor salonu, FREEZE turu, yarisan karakterler, hakem maskot)</title>')
R("// =====================================================================\n// MOTOR 21",
  "// =====================================================================\n"
  "// MOTOR 22 — HUMAN TETRIS 25 (REFERANSSIZ, 11 Kas 2026; motor 21'den). TALIMATLAR §2b 2. mekan (okul spor salonu) + §4 CILALI 3D OYUN GORUNUMU:\n"
  "//   - sahne: tetris-pvp/varlik-salon.py (cilali parke, gokkusagi tribun, flama + balon); havuz isiltisi kaldirildi\n"
  "//   - pastel kart yok: kapi ici kart = buzlu beyaz pano + oyuncu renginde cerceve; tam ekran kart / panel zemini = bulanik salon + koyu renk tonu\n"
  "//   - OUT: karakter dis taraftaki kendi minderine duser; su sicramasi yerine minder tozu + yildiz (duduk sesi efekt.py'de)\n"
  "//   - hakem maskot cankurtaran kulesi yerine hakem kursusunde\n"
  "//   - FREEZE ROUND: duvar gecince 'tut' evresi (d.z.tut sn): FREEZE! + dolan tutma cubugu, karakterler pozda kalir; sonra tam ekran panel\n"
  "// =====================================================================\n// MOTOR 21")
# 1) havuz isiltisi yok
R("  for (const p of SU_P) {                                      // havuz suyunda gunes isiltisi",
  "  for (const p of []) {                                        // motor 22: havuz isiltisi yok (spor salonu)")
# 2) bulanik salon (yukte bir kez)
R("const [GOK, ...SERIT] = await Promise.all(['gok.png', ...OY.map(o => 'serit-' + o + '.png')].map(a => resim(VARLIK + a)));",
  "const [GOK, ...SERIT] = await Promise.all(['gok.png', ...OY.map(o => 'serit-' + o + '.png')].map(a => resim(VARLIK + a)));\n"
  "// motor 22: kart / panel zemini icin bulaniklastirilmis salon (pastel duz degrade yerine; TALIMATLAR §4)\n"
  "const BULANIK = Object.assign(document.createElement('canvas'), { width: W, height: H });\n"
  "{ const bg = BULANIK.getContext('2d'); bg.filter = 'blur(' + Math.round(22 * H / 1080) + 'px)';\n"
  "  bg.drawImage(GOK, -40, -40, W + 80, H + 80); SERIT.forEach((im, i) => bg.drawImage(im, i * W / 2 - 20, -40, W / 2 + 40, H + 80)); bg.filter = 'none'; }")
# 3) kapi ici kart: buzlu pano
R("""  const g = cx.createRadialGradient(x + w / 2, y + h * 0.45, 0, x + w / 2, y + h * 0.45, Math.max(w, h) * 0.75);
  g.addColorStop(0, '#ffffff'); g.addColorStop(0.45, ACIK[i]); g.addColorStop(1, ACIK[i]);
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.fill();""",
  """  // motor 22: buzlu beyaz pano + oyuncu renginde kalin cerceve - pastel degrade yok
  const g = cx.createLinearGradient(0, y, 0, y + h);
  g.addColorStop(0, '#ffffff'); g.addColorStop(0.5, '#f3f5f9'); g.addColorStop(1, '#e4e8ef');
  cx.fillStyle = g; cx.beginPath(); cx.roundRect(x, y, w, h, Math.min(w, h) * 0.03); cx.fill();
  cx.strokeStyle = RENK[i]; cx.lineWidth = Math.max(6 * k, w * 0.025); cx.stroke();""")
# 4) tam ekran panel
R("""    const g = cx.createRadialGradient(x + SW / 2, H * 0.5, 0, x + SW / 2, H * 0.5, SW * 0.8);
    g.addColorStop(0, '#ffffff'); g.addColorStop(0.4, ACIK[i]); g.addColorStop(1, hex(RENK[i], 0.55));
    cx.fillStyle = ACIK[i]; cx.fillRect(x, 0, SW, H); cx.fillStyle = g; cx.fillRect(x, 0, SW, H);""",
  """    // motor 22: bulanik salon + doygun oyuncu rengi tonu (pastel degil), ortada siluet icin acik isik halesi
    cx.drawImage(BULANIK, x, 0, SW, H, x, 0, SW, H);
    const g = cx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, hex(RENK[i], 0.62)); g.addColorStop(1, hex(KOYU[i], 0.8));
    cx.fillStyle = g; cx.fillRect(x, 0, SW, H);
    const hl = cx.createRadialGradient(x + SW / 2, H * 0.55, 0, x + SW / 2, H * 0.55, SW * 0.55);
    hl.addColorStop(0, 'rgba(255,255,255,0.85)'); hl.addColorStop(0.6, 'rgba(255,255,255,0.35)'); hl.addColorStop(1, 'rgba(255,255,255,0)');
    cx.fillStyle = hl; cx.fillRect(x, 0, SW, H);""")
# 5) tam ekran kart zemini
R("""  const g = cx.createRadialGradient(W / 2, H / 2, 50 * k, W / 2, H / 2, W * 0.7);
  g.addColorStop(0, renkA); g.addColorStop(1, renkB); cx.fillStyle = g; cx.fillRect(0, 0, W, H);""",
  """  // motor 22: bulanik salon + koyu renk tonu (pastel / uzay zemini yok)
  cx.drawImage(BULANIK, 0, 0, W, H);
  const g = cx.createRadialGradient(W / 2, H / 2, 50 * k, W / 2, H / 2, W * 0.7);
  g.addColorStop(0, hex(renkA, 0.55)); g.addColorStop(1, hex(renkB, 0.85)); cx.fillStyle = g; cx.fillRect(0, 0, W, H);""")
R("  ZEMIN_GEZEGEN.forEach((p, j) => gezegenCiz(", "  if (false) ZEMIN_GEZEGEN.forEach((p, j) => gezegenCiz(")
# 6) su sicramasi -> minder tozu
R("    cx.fillStyle = j % 3 ? '#ffffff' : '#7ae8ff'; cx.beginPath();",
  "    cx.fillStyle = j % 3 ? 'rgba(255,255,255,0.85)' : '#ffd23a'; cx.beginPath();")
# 7) kule -> hakem kursusu
i0 = s.index("function kule(t) {"); i1 = s.index("function hakemCiz(t, d, u) {")
s = s[:i0] + """function kule(t) {                                             // motor 22: iki kapinin arasinda hakem kursusu (mor-lacivert, sari yildiz, cilali)
  const xm = W / 2, y0 = H * 0.925, w = 170 * k, h = H - y0 + 10 * k;
  cx.save();
  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#5a4ff0'); g.addColorStop(1, '#2a1f9a');
  cx.fillStyle = g; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(xm - w / 2 + 10 * k, y0 + 6 * k, w - 20 * k, 10 * k, 5 * k); cx.fill();
  yildiz5(xm, y0 + h * 0.5, 16 * k, '#ffd23a', t);
  cx.restore();
}
""" + s[i1:]
# 8) FREEZE tut evresi
R("""  const Z = ZD(d), a = Z.kart, b = a + Z.say, c = b + Z.buyu;
  if (u >= c) { tamEkran(d, u - c, t); return null; }""",
  """  const Z = ZD(d), a = Z.kart, b = a + Z.say, c = b + Z.buyu, T = Z.tut || 0;
  if (u >= c + T) { tamEkran(d, u - c - T, t); return null; }""")
R("""  karakterCiz(d, u, t);
  return u >= a && u < b ? (u - a) / Z.say : null;
}""",
  """  karakterCiz(d, u, t);
  if (T && u >= c) freezeCiz(u - c, T, t);
  return u >= a && u < b ? (u - a) / Z.say : null;
}
function freezeCiz(u, T, t) {                                  // motor 22 FREEZE ROUND: duvar gecti, pozu tut - buzlu kenar, FREEZE!, dolan cubuk
  const gir = ease(kisit(u / 0.3, 0, 1)), q = kisit(u / T, 0, 1);
  cx.save(); cx.globalAlpha = 0.55 * gir;
  const v = cx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.62);
  v.addColorStop(0, 'rgba(160,230,255,0)'); v.addColorStop(1, 'rgba(120,210,255,0.9)'); cx.fillStyle = v; cx.fillRect(0, 0, W, H);
  cx.restore();
  const p = ease(kisit(u / 0.35, 0, 1)) * (1 + 0.1 * Math.sin(kisit(u / 0.35, 0, 1) * Math.PI));
  yaziK('FREEZE!', W / 2, H * 0.2, 140 * k * p, ['#ffffff', '#bff0ff', '#3ac8ff'], gir, '#06306a', '#ffffff');
  const bw = 760 * k, bh = 42 * k, bx = W / 2 - bw / 2, by = H * 0.31;
  cx.save(); cx.globalAlpha = gir;
  cx.fillStyle = '#06306a'; cx.beginPath(); cx.roundRect(bx - 6 * k, by - 6 * k, bw + 12 * k, bh + 12 * k, (bh + 12 * k) / 2); cx.fill();
  const bg = cx.createLinearGradient(bx, 0, bx + bw, 0); bg.addColorStop(0, '#7ae8ff'); bg.addColorStop(1, '#ffffff');
  cx.fillStyle = bg; cx.beginPath(); cx.roundRect(bx, by, Math.max(bh, bw * q), bh, bh / 2); cx.fill();
  cx.restore();
  yaziK('HOLD IT! ' + Math.max(1, Math.ceil(T * (1 - q))), W / 2, by + bh + 50 * k, 56 * k, ['#ffffff', '#e6f8ff', '#9ae4ff'], gir, '#06306a', '#ffffff');
}""")
R("    const Z = ZD(d); tam = t - d.t0 >= Z.kart + Z.say + Z.buyu;",
  "    const Z = ZD(d); tam = t - d.t0 >= Z.kart + Z.say + Z.buyu + (Z.tut || 0);")
open(os.path.join(BURA, "sahne22.html"), "w", encoding="utf-8").write(s)
print("sahne22.html yazildi")
