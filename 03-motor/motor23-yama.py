"""motor 23 (HUMAN TETRIS 26) = sahne22.html + bu yamalar. python motor23-yama.py -> sahne23.html (bir kez; sonra sahne23.html dogrudan duzenlenir)."""
import os
BURA = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(BURA, "sahne22.html"), encoding="utf-8").read()


def R(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


R('<title>HUMAN TETRIS 25 - motor 22 (iki serit oyun gorunumlu spor salonu, FREEZE turu, yarisan karakterler, hakem maskot)</title>',
  '<title>HUMAN TETRIS 26 - motor 23 (iki serit tropik plaj, MIRROR turu, yarisan karakterler, cankurtaran hakem maskot)</title>')
R("// =====================================================================\n// MOTOR 22",
  "// =====================================================================\n"
  "// MOTOR 23 — HUMAN TETRIS 26 (REFERANSSIZ, 14 Kas 2026; motor 22'den). TALIMATLAR §2b 3. mekan (tropik plaj) + §4 cilali 3D oyun gorunumu:\n"
  "//   - sahne: tetris-pvp/varlik-plaj.py (altin kum, turkuaz deniz, palmiye, cankurtaran kulesi; canli renk 14 Kas)\n"
  "//   - OUT: karakter dis taraftaki kum yiginina yuvarlanir; sicrama = kum tanesi + toz halkasi (ses: efekt.py --kum)\n"
  "//   - hakem maskot cankurtaran: kirmizi kursu + can simidi, boynunda sari duduk; elinde plaj topu; koselerde can simidi ustunde\n"
  "//   - MIRROR ROUND (d.ayna): duvar silueti, tam ekran panel, yarisan karakterler ve maskot aynalanir; ustte MIRROR! yazisi\n"
  "// =====================================================================\n// MOTOR 22")
# 1) kum sicramasi
R("    cx.fillStyle = j % 3 ? 'rgba(255,255,255,0.85)' : '#ffd23a'; cx.beginPath(); cx.arc(x, y, (7 + 9 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();",
  "    cx.fillStyle = ['#ffd27a', '#f3a53a', '#fff1c4'][j % 3]; cx.beginPath(); cx.arc(x, y, (5 + 8 * R2()) * k * olc * (1 - q * 0.5), 0, 6.283); cx.fill();   // motor 23: kum tanesi")
R("  cx.strokeStyle = '#ffffff'; cx.lineWidth = 8 * k * (1 - q); cx.beginPath(); cx.ellipse(xm, ym, 180 * k * olc * q + 30 * k",
  "  cx.strokeStyle = 'rgba(255,214,140,0.9)'; cx.lineWidth = 14 * k * (1 - q); cx.beginPath(); cx.ellipse(xm, ym, 180 * k * olc * q + 30 * k")
# 2) cankurtaran kursusu
R("""  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#5a4ff0'); g.addColorStop(1, '#2a1f9a');
  cx.fillStyle = g; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(xm - w / 2 + 10 * k, y0 + 6 * k, w - 20 * k, 10 * k, 5 * k); cx.fill();
  yildiz5(xm, y0 + h * 0.5, 16 * k, '#ffd23a', t);""",
  """  const g = cx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, '#ff3a4a'); g.addColorStop(1, '#c4102a');   // motor 23: kirmizi cankurtaran kursusu
  cx.fillStyle = g; cx.strokeStyle = '#ffffff'; cx.lineWidth = 6 * k;
  cx.beginPath(); cx.roundRect(xm - w / 2, y0, w, h, 14 * k); cx.fill(); cx.stroke();
  cx.fillStyle = '#ffffff'; cx.fillRect(xm - w / 2 + 3 * k, y0 + h * 0.42, w - 6 * k, 9 * k);
  cx.fillStyle = 'rgba(255,255,255,0.35)'; cx.beginPath(); cx.roundRect(xm - w / 2 + 10 * k, y0 + 6 * k, w - 20 * k, 10 * k, 5 * k); cx.fill();
  simitCiz(xm + w * 0.36, y0 + h * 0.2, 20 * k);""")
# 3) plaj topu + can simidi + duduk
R("// REF-077 lunaparkinda: elinde ipli sabun kabarcigi",
  """function topCiz(x, y, r, t) {                                  // motor 23: plaj topu (gezegen yerine)
  cx.save(); cx.translate(x, y); cx.rotate(t * 1.2);
  const RN = ['#ff3b4e', '#ffffff', '#1e9cff', '#ffcc1e', '#2fd06a', '#ffffff'];
  for (let i = 0; i < 6; i++) { cx.fillStyle = RN[i]; cx.beginPath(); cx.moveTo(0, 0); cx.arc(0, 0, r, i * 1.0472, (i + 1) * 1.0472); cx.closePath(); cx.fill(); }
  cx.lineWidth = Math.max(2, r * 0.1); cx.strokeStyle = '#ffffff'; cx.beginPath(); cx.arc(0, 0, r, 0, 6.283); cx.stroke();
  cx.fillStyle = '#ffffff'; cx.beginPath(); cx.arc(0, 0, r * 0.2, 0, 6.283); cx.fill();
  cx.rotate(-t * 1.2); cx.fillStyle = 'rgba(255,255,255,0.6)'; cx.beginPath(); cx.ellipse(-r * 0.38, -r * 0.42, r * 0.22, r * 0.12, -0.7, 0, 6.283); cx.fill();
  cx.restore();
}
function simitCiz(x, y, r) {                                    // motor 23: can simidi (kirmizi-beyaz dilimli halka)
  cx.save(); cx.translate(x, y); cx.lineWidth = r * 0.55;
  for (let i = 0; i < 8; i++) { cx.strokeStyle = i % 2 ? '#ffffff' : '#ff2a3a'; cx.beginPath(); cx.arc(0, 0, r, i * 0.7854, (i + 1) * 0.7854); cx.stroke(); }
  cx.lineWidth = Math.max(1.5, r * 0.08); cx.strokeStyle = '#8a0a1a';
  cx.beginPath(); cx.arc(0, 0, r * 1.27, 0, 6.283); cx.stroke(); cx.beginPath(); cx.arc(0, 0, r * 0.73, 0, 6.283); cx.stroke();
  cx.restore();
}
// REF-077 lunaparkinda: elinde ipli sabun kabarcigi""")
R("  if (!yuzSadece) gezegenCiz(x + (88 + bs) * s * k, y - 100 * s * k, 22 * s * k, '#7ad8ff', '#2a5aff', t);",
  "  if (!yuzSadece) topCiz(x + (88 + bs) * s * k, y - 100 * s * k, 24 * s * k, t);")
R("""  cx.strokeStyle = KN; cx.lineWidth = 4; cx.beginPath(); cx.arc(0, 12, 9, 0.2, Math.PI - 0.2); cx.stroke();""",
  """  cx.strokeStyle = KN; cx.lineWidth = 4; cx.beginPath(); cx.arc(0, 12, 9, 0.2, Math.PI - 0.2); cx.stroke();
  cx.strokeStyle = '#ff2a3a'; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(-30, 40); cx.quadraticCurveTo(0, 62, 26, 42); cx.stroke();   // motor 23: cankurtaran duduk ipi
  cx.save(); cx.translate(10, 56); cx.rotate(-0.25); cx.fillStyle = '#ffd23a'; cx.strokeStyle = KN; cx.lineWidth = 3;
  cx.beginPath(); cx.roundRect(-14, -8, 28, 16, 7); cx.fill(); cx.stroke(); cx.beginPath(); cx.arc(-10, 0, 9, 0, 6.283); cx.fill(); cx.stroke(); cx.restore();""")
R("""    gezegenCiz(96 * k, 160 * k, 42 * k, '#b48cff', '#5a2ad0', t);""", """    simitCiz(96 * k, 166 * k, 34 * k);""")
R("""  gezegenCiz(W / 2, H * 0.955, 46 * k, '#b48cff', '#5a2ad0', t);""", """  simitCiz(W / 2, H * 0.96, 38 * k);""")
# 4) MIRROR: aynali maske
R("function siluet(ad, x, y, w, h, alfa = 1, renk = '#000000', kontur = 0, isilti = null) {\n  const m = MASKE[ad]; if (!m || alfa <= 0.01) return;",
  """let AYNA = false;                                                 // motor 23 MIRROR ROUND: o anki duvar aynali mi (kareKur'da kurulur)
const AYNA_M = {};
function aynaMaske(ad) {
  if (AYNA_M[ad]) return AYNA_M[ad];
  const m = MASKE[ad]; if (!m) return null;
  const c = Object.assign(document.createElement('canvas'), { width: m.width, height: m.height }), g = c.getContext('2d');
  g.translate(m.width, 0); g.scale(-1, 1); g.drawImage(m, 0, 0);
  return (AYNA_M[ad] = c);
}
function siluet(ad, x, y, w, h, alfa = 1, renk = '#000000', kontur = 0, isilti = null) {
  const m = AYNA ? aynaMaske(ad) : MASKE[ad]; if (!m || alfa <= 0.01) return;""")
# karakterler aynali
R("""    cx.shadowColor = RENK[i]; cx.shadowBlur = 26 * k;
    cx.drawImage(im, xm - px / 2, ay - Y.zemin_px * sc, px, px);""",
  """    cx.shadowColor = RENK[i]; cx.shadowBlur = 26 * k;
    if (d.ayna) { cx.translate(xm, 0); cx.scale(-1, 1); cx.translate(-xm, 0); }   // motor 23 MIRROR: karakter ters pozu yapar
    cx.drawImage(im, xm - px / 2, ay - Y.zemin_px * sc, px, px);""")
# maskot aynali
R("""  cx.save(); cx.shadowColor = '#ff6ad6'; cx.shadowBlur = 24 * k; cx.drawImage(im, x0, y0, px, px); cx.restore();
  const kf = Y.poz[ad].kafa[Math.round(j)];
  maskotCiz(x0 + kf[0] * sc, y0 + kf[1] * sc, kf[2] * sc * 1.25 / (62 * k), t, 1, true);""",
  """  const ayn = d && d.ayna;
  cx.save(); cx.shadowColor = '#ff6ad6'; cx.shadowBlur = 24 * k;
  if (ayn) { cx.translate(xm, 0); cx.scale(-1, 1); cx.translate(-xm, 0); }        // motor 23 MIRROR: maskot da ters pozu gosterir
  cx.drawImage(im, x0, y0, px, px); cx.restore();
  const kf = Y.poz[ad].kafa[Math.round(j)], kx = x0 + kf[0] * sc;
  maskotCiz(ayn ? 2 * xm - kx : kx, y0 + kf[1] * sc, kf[2] * sc * 1.25 / (62 * k), t, 1, true);""")
# MIRROR yazisi (poz gosterilirken)
R("""  karakterCiz(d, u, t);
  if (T && u >= c) freezeCiz(u - c, T, t);""",
  """  karakterCiz(d, u, t);
  if (d.ayna && u < b) {                                         // motor 23 MIRROR ROUND: ustte MIRROR! (gumus-camgobegi), kapi gelirken parlar
    const gir = ease(kisit(u / 0.4, 0, 1)), p = 1 + 0.06 * Math.sin(t * 6);
    yaziK('MIRROR!', W / 2, H * 0.165, 96 * k * gir * p, ['#ffffff', '#c8f4ff', '#3ab8ff'], gir, '#06306a', '#ffffff');
  }
  if (T && u >= c) freezeCiz(u - c, T, t);""")
R("""function kareKur(n) {
  const t = n / FPS;""", """function kareKur(n) {
  const t = n / FPS;
  AYNA = false;""")
R("""    const Z = ZD(d); tam = t - d.t0 >= Z.kart + Z.say + Z.buyu + (Z.tut || 0);""",
  """    const Z = ZD(d); tam = t - d.t0 >= Z.kart + Z.say + Z.buyu + (Z.tut || 0);
    AYNA = !!d.ayna;""")
open(os.path.join(BURA, "sahne23.html"), "w", encoding="utf-8").write(s)
print("sahne23.html", len(s))
