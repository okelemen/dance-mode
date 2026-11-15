"""motor 25 (HUMAN TETRIS 28, CO-OP dev mutfak) = sahne24.html + bu yamalar -> sahne25.html. Eski motorlar degismez (TALIMATLAR §6).

    python motor25-yama.py

CO-OP (tek serit, tek sari duvar, ikili siluet) motor 24'ten aynen. Farklar:
  - sahne varlik-mutfak.py; gokte kar yerine yukselen sabun kopukleri (hareketli ust bosluk, ekran dolu)
  - FREEZE ROUND (d.freeze): duvar gecince 'tut' evresi (d.z.tut sn) - motor 22 freezeCiz (FREEZE! + dolan cubuk + HOLD IT! n);
    karakterler pozda kalir. FREEZE duvarinda gec paneli yok (gec 0): tut biter bitmez sonraki duvar.
  - OUT: duvar ikisini dev jole kaselerine iter (P1 sol mavi jole, P2 sag pembe jole) - jole sicramasi kendi renginde
  - hakem maskot asci (karakter.py --asci: sapka + fular); elinde donut, ayak altinda pembe kremali pasta
  - tam ekran panel ve kartlar sicak mutfak tonu (turuncu-pembe); OUT paneli ayni (koyu)
"""
import os

BURA = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(BURA, "..", "sahne24.html"), encoding="utf-8").read()


def r(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:80])
    t = t.replace(a, b)


r('<title>HUMAN TETRIS 27 - motor 24 (CO-OP tek serit karli zirve, BLIND turu, ikili karakterler, kayakci hakem maskot)</title>',
  '<title>HUMAN TETRIS 28 - motor 25 (CO-OP tek serit dev mutfak, FREEZE turu, ikili karakterler, asci hakem maskot)</title>')
r('html,body { margin:0; background:#1a8cff; overflow:hidden; }', 'html,body { margin:0; background:#ff9a1a; overflow:hidden; }')
r('''// =====================================================================
// MOTOR 24 — HUMAN TETRIS 27''', '''// =====================================================================
// MOTOR 25 — HUMAN TETRIS 28 (REFERANSSIZ, CO-OP 2 oyuncu, 15 Kas 2026; motor 24'ten, tetris-pvp/motor25-yama.py). TALIMATLAR §2b 5. mekan:
//   - sahne: tetris-pvp/varlik-mutfak.py (TEK serit: kesme tahtasi pist, makaron siniri, makaron kuleli kapi); ust boslukta sabun kopukleri
//   - FREEZE ROUND (d.freeze): duvar gecince 'tut' evresi: FREEZE! + dolan cubuk + HOLD IT! n, karakterler pozda kalir; gec paneli yok
//   - OUT: duvar ikisini dev jole kaselerine iter (P1 sol mavi, P2 sag pembe); jole sicramasi kendi renginde
//   - hakem maskot asci sapkasi + fular (karakter.py --asci); elinde donut, ayak altinda pasta
// =====================================================================
// MOTOR 24 — HUMAN TETRIS 27''')

# ---- elde donut (kartopu yerine), ayak alti / kose: pembe kremali pasta (kar tepecigi yerine)
r('''function topCiz(x, y, r, t) {                                  // motor 24: kartopu (plaj topu yerine) - beyaz, buz mavisi golge, parilti
  cx.save(); cx.translate(x, y);
  const g = cx.createRadialGradient(-r * 0.35, -r * 0.35, r * 0.1, 0, 0, r); g.addColorStop(0, '#ffffff'); g.addColorStop(0.7, '#e6f4ff'); g.addColorStop(1, '#9fd0ff');
  cx.fillStyle = g; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.fill();
  cx.lineWidth = Math.max(2, r * 0.08); cx.strokeStyle = '#5a8ad8'; cx.stroke();
  cx.restore();''', '''function topCiz(x, y, r, t) {                                  // motor 25: donut (kartopu yerine) - hamur halka + pembe krema + serpinti
  cx.save(); cx.translate(x, y); cx.rotate(Math.sin(t * 2) * 0.2);
  cx.lineWidth = Math.max(2, r * 0.1); cx.strokeStyle = '#7a3a12';
  cx.fillStyle = '#e8a04a'; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.arc(0, 0, r * 0.38, 0, 6.283, true); cx.fill('evenodd'); cx.stroke();
  cx.fillStyle = '#ff5fc0'; cx.beginPath(); cx.arc(0, -r * 0.04, r * 0.86, 0, 6.283); cx.arc(0, -r * 0.04, r * 0.44, 0, 6.283, true); cx.fill('evenodd');
  const SR = ['#ffd23a', '#2fd06a', '#1e9cff', '#ffffff', '#8a5aff'];
  for (let i = 0; i < 10; i++) { const a = i * 0.628 + 0.3, rr = r * 0.65; cx.save(); cx.translate(Math.cos(a) * rr, Math.sin(a) * rr - r * 0.04); cx.rotate(a * 2.3);
    cx.fillStyle = SR[i % 5]; cx.fillRect(-r * 0.12, -r * 0.035, r * 0.24, r * 0.07); cx.restore(); }
  cx.restore();''')
r('''function simitCiz(x, y, r) {                                    // motor 24: kar tepecigi (can simidi yerine)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.7, 0, r * 0.5); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#bfe0ff');
  cx.fillStyle = g; cx.strokeStyle = '#5a8ad8'; cx.lineWidth = Math.max(1.5, r * 0.08);''', '''function simitCiz(x, y, r) {                                    // motor 25: pembe kremali pasta tepesi (kar tepecigi yerine)
  cx.save(); cx.translate(x, y);
  const g = cx.createLinearGradient(0, -r * 0.7, 0, r * 0.5); g.addColorStop(0, '#ffd0ec'); g.addColorStop(1, '#ff6ac8');
  cx.fillStyle = g; cx.strokeStyle = '#a0186a'; cx.lineWidth = Math.max(1.5, r * 0.08);''')

# ---- kar yagisi -> yukselen sabun kopukleri
r('''function karYagisi(t, alfa = 1) {                              // motor 24: gokte ve sahnede yavas dusen kar taneleri (hareketli gok)
  cx.save();
  for (const p of KAR_T) {
    const y = ((p.y + t * p.v) % 1.05) * H - 0.02 * H, x = ((p.x + Math.sin(t * 0.8 + p.f) * 0.01) % 1) * W;
    cx.globalAlpha = p.a * alfa; cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(x, y, p.r * k, 0, 6.283); cx.fill();
  }
  cx.restore();
}''', '''function karYagisi(t, alfa = 1) {                              // motor 25: yukselen sabun kopukleri (kar yerine; hareketli ust bosluk)
  cx.save();
  for (const p of KAR_T) {
    if (p.y > 0.62) continue;                                   // yalniz ust bosluk + yanlar (pist ve duvar temiz kalir)
    const y = (1 - ((1 - p.y + t * p.v * 0.6) % 1.05)) * H * 0.62, x = ((p.x + Math.sin(t * 0.9 + p.f) * 0.015) % 1) * W;
    if (Math.abs(x - W / 2) < W * 0.2 && y > H * 0.25) continue;
    const rr = (p.r * 2.6 + 4) * k;
    cx.globalAlpha = 0.55 * p.a * alfa;
    const g = cx.createRadialGradient(x - rr * 0.35, y - rr * 0.35, rr * 0.05, x, y, rr);
    g.addColorStop(0, 'rgba(255,255,255,0.9)'); g.addColorStop(0.55, 'rgba(255,220,250,0.12)'); g.addColorStop(1, 'rgba(140,220,255,0.55)');
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, rr, 0, 6.283); cx.fill();
    cx.lineWidth = 1.5 * k; cx.strokeStyle = 'rgba(255,255,255,0.8)'; cx.stroke();
  }
  cx.restore();
}''')

# ---- FREEZE: duvar gecince 'tut' evresi (motor 22 freezeCiz zaten var; motor 24 cagirmiyordu)
r('''  karakterCiz(d, u, t);
  return u >= a && u < b ? (u - a) / Z.say : null;
}''', '''  karakterCiz(d, u, t);
  if (T && u >= c) freezeCiz(u - c, T, t);                    // motor 25: FREEZE ROUND tut evresi
  return u >= a && u < b ? (u - a) / Z.say : null;
}''')

# ---- jole sicramasi: tarafin renginde (sol mavi, sag pembe)
r('''    cx.fillStyle = ['#ffffff', '#dff2ff', '#b8e2ff'][j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 24: kar topagi''',
  '''    cx.fillStyle = (xm < W / 2 ? ['#1e8cff', '#7ac4ff', '#ffffff'] : ['#ff3aa8', '#ff9ad8', '#ffffff'])[j % 3]; cx.beginPath(); cx.arc(x, y, (6 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 25: jole damlasi''')
r('''  cx.strokeStyle = 'rgba(235,248,255,0.95)'; cx.lineWidth = 16 * k * (1 - q);''',
  '''  cx.strokeStyle = xm < W / 2 ? 'rgba(120,190,255,0.95)' : 'rgba(255,140,210,0.95)'; cx.lineWidth = 16 * k * (1 - q);''')
r("    if (out && u >= b) {                                        // OUT: duvar ikisini iter -> kendi tarafindaki kar yiginina gomulur",
  "    if (out && u >= b) {                                        // OUT: duvar ikisini iter -> kendi tarafindaki jole kasesine duser (motor 25)")

# ---- hakem: ayak alti pasta (kar tepecigi yerine), parilti sicak
r('''  cx.save(); cx.fillStyle = '#ffffff'; cx.shadowColor = 'rgba(120,180,255,0.8)'; cx.shadowBlur = 14 * k;   // kar tepecigi (ayak alti)
  cx.beginPath(); cx.ellipse(xm, ay + 4 * k, 120 * k, 26 * k, 0, 0, 6.283); cx.fill(); cx.restore();''',
  '''  cx.save(); cx.shadowColor = 'rgba(255,120,200,0.8)'; cx.shadowBlur = 14 * k;   // motor 25: pembe kremali pasta tabakasi (ayak alti)
  const pg = cx.createLinearGradient(0, ay - 20 * k, 0, ay + 30 * k); pg.addColorStop(0, '#ffd0ec'); pg.addColorStop(1, '#ff5fc0');
  cx.fillStyle = pg; cx.strokeStyle = '#a0186a'; cx.lineWidth = 4 * k;
  cx.beginPath(); cx.ellipse(xm, ay + 4 * k, 120 * k, 26 * k, 0, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();''')
r("  cx.save(); cx.shadowColor = '#7ad8ff'; cx.shadowBlur = 24 * k;\n  cx.drawImage(im, x0, y0, px, px); cx.restore();",
  "  cx.save(); cx.shadowColor = '#ffd23a'; cx.shadowBlur = 24 * k;\n  cx.drawImage(im, x0, y0, px, px); cx.restore();")

# ---- tam ekran panel: sicak mutfak tonu (normal); OUT koyu kalir
r('''g.addColorStop(0, out ? 'rgba(90,150,230,0.55)' : 'rgba(40,160,255,0.55)'); g.addColorStop(1, out ? 'rgba(20,40,110,0.8)' : 'rgba(10,70,180,0.75)');''',
  '''g.addColorStop(0, out ? 'rgba(120,60,140,0.55)' : 'rgba(255,140,40,0.55)'); g.addColorStop(1, out ? 'rgba(40,10,60,0.8)' : 'rgba(200,40,110,0.75)');''')
r("  siluet(d.grup, W / 2 - sw / 2, H * 0.14 + (H * 0.84 - sh), sw, sh, a * (out ? 0.45 : 1), '#000000', 7 * k, '#7ad8ff');",
  "  siluet(d.grup, W / 2 - sw / 2, H * 0.14 + (H * 0.84 - sh), sw, sh, a * (out ? 0.45 : 1), '#000000', 7 * k, '#ffd23a');")

# ---- FREEZE blogu sagda (motor 22'de ortada ustteydi; motor 25'te ortada kapi kirisinde maskot var -> sag tarafa, hakem balonu solda)
r("""  yaziK('FREEZE!', W / 2, H * 0.165, 118 * k * p, ['#ffffff', '#bff0ff', '#3ac8ff'], gir, '#06306a', '#ffffff');
  const bw = 640 * k, bh = 34 * k, bx = W / 2 - bw / 2, by = H * 0.235;""",
  """  const fx = W * 0.83;                                          // motor 25: sag blok (ortada maskot)
  yaziK('FREEZE!', fx, H * 0.36, 104 * k * p, ['#ffffff', '#bff0ff', '#3ac8ff'], gir, '#06306a', '#ffffff');
  const bw = 420 * k, bh = 34 * k, bx = fx - bw / 2, by = H * 0.43;""")
r("  yaziK('HOLD IT! ' + Math.max(1, Math.ceil(T * (1 - q))), W / 2, by + bh + 36 * k,",
  "  yaziK('HOLD IT! ' + Math.max(1, Math.ceil(T * (1 - q))), fx, by + bh + 40 * k,")

# ---- kontak 1: FREEZE tut evresinde kapi kapkara bos delik gibi duruyordu -> tut sirasinda kararma hafif
r("    cx.save(); cx.globalAlpha = kar * 0.88; cx.fillStyle = '#0a0618'; cx.fillRect(K.x, K.y, K.w, K.h); cx.restore();",
  "    cx.save(); cx.globalAlpha = kar * (T && u >= c ? 0.3 : 0.88); cx.fillStyle = '#0a0618'; cx.fillRect(K.x, K.y, K.w, K.h); cx.restore();")
# ---- kontak 1: 3B asci sapkasi 2B yuzun altinda kaliyordu -> 2B asci sapkasi (bant + uc kabarik top), cicek bantta
r("""  cx.save(); cx.translate(0, -58);                              // basta cicek (seri tanirligi)""",
  """  cx.save(); cx.fillStyle = '#ffffff'; cx.strokeStyle = KN; cx.lineWidth = 4;   // motor 25: asci sapkasi (hakem asci)
  for (const [px_, py_, pr_] of [[-30, -100, 22], [30, -100, 22], [0, -112, 27]]) { cx.beginPath(); cx.arc(px_, py_, pr_, 0, 6.283); cx.fill(); cx.stroke(); }
  cx.beginPath(); cx.roundRect(-40, -92, 80, 30, 8); cx.fill(); cx.stroke();
  cx.strokeStyle = 'rgba(90,31,134,0.35)'; cx.lineWidth = 3; for (const lx of [-14, 14]) { cx.beginPath(); cx.moveTo(lx, -90); cx.lineTo(lx, -64); cx.stroke(); }
  cx.restore();
  cx.save(); cx.translate(0, -58);                              // basta cicek (seri tanirligi)""")

open(os.path.join(BURA, "..", "sahne25.html"), "w", encoding="utf-8").write(t)
print("-> sahne25.html", len(t))
