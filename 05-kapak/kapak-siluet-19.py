"""HUMAN TETRIS 19 kapak silueti - anatomik insan silueti (bird-dog), kendi cizimimiz (5 Kas 2026).

Kullanici: "referansin siluetine bak, bir de bizimkine bak" -> Mixamo giysili manken kaba/kirisik; "vucut hatlari insan vucut hattina
benzemiyor" -> esit kalin boru uzuvlar yerine her uzvun IKI KENARI ayri profille: kas tarafi siskin, kemik tarafi duz
(uyluk onu/arkasi, dizde daralma, baldir siskinligi, ince bilek, kalca kavisi, bel cukuru, kurek kemigi, omuz yuvarligi, dirsek).
Oranlar REF-070'ten (1 birim = kalca-omuz), cizgi birebir kopya degil. Kafa ayri yuvarlak (ince bosluk).
Cikti: <klasor>/poz/<ad>.png + yerlesim.json (kafa_px) -> kapak-tek-19.py --poz-klasor <klasor>.

    python kapak-siluet-19.py --klasor ../03-motor/tetris-pvp/varlik-19-insan5
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFilter

p = argparse.ArgumentParser(); p.add_argument("--klasor", required=True); a = p.parse_args()
os.makedirs(os.path.join(a.klasor, "poz"), exist_ok=True)
S = 600   # birim -> piksel (cizim olcegi; sonra 1/3)
Z = -0.89  # zemin


def ip(prof, t):
    """[(t, deger), ...] -> puruzsuz egri: dogrusal ara deger + gauss yumusatma (taslak 3: kosinus ara deger her noktada basamak/dalga yapti)"""
    key = tuple(prof)   # id() yeniden kullanilinca profiller karisti
    if key not in _EGRI:
        import numpy as np
        ts = np.linspace(0, 1, 401); v = np.interp(ts, [q[0] for q in prof], [q[1] for q in prof])
        k = np.exp(-0.5 * (np.arange(-40, 41) / 14.0) ** 2); k /= k.sum()
        vp = np.pad(v, 40, mode="edge"); _EGRI[key] = (ts, np.convolve(vp, k, mode="same")[40:-40])
    ts, v = _EGRI[key]
    return float(v[min(400, max(0, int(round(t * 400))))])


_EGRI = {}


def uzuv(d, don, p0, p1, sol, sag, n=60):
    """p0 -> p1 eksenli uzuv; sol = eksenin solundaki (yon vektorunun +90 derecesi) kenar profili, sag = diger kenar"""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    s_, g_ = [], []
    for i in range(n + 1):
        t = i / n; cx, cy = p0[0] + dx * t, p0[1] + dy * t
        s_.append(don((cx + nx * ip(sol, t), cy + ny * ip(sol, t))))
        g_.append(don((cx - nx * ip(sag, t), cy - ny * ip(sag, t))))
    d.polygon(s_ + g_[::-1], fill=255)
    for (x, y), r in ((don(p0), min(sol[0][1], sag[0][1])), (don(p1), min(sol[-1][1], sag[-1][1]))):   # yuvarlak uclar
        r *= S; d.ellipse((x - r, y - r, x + r, y + r), fill=255)


def ciz(d, don, arka_uc, kol_uc):
    # GOVDE: kalca arkasi -> omuz (yon saga; sol kenar = SIRT: kalca yuvarligi, bel cukuru, kurek kemigi; sag kenar = KARIN/GOGUS)
    uzuv(d, don, (-0.20, 0.08), (1.02, 0.20),
         # taslak 2: referanstan zayif -> kalca/popo, bel ve gogus dolgun
         # taslak 4: govde kalas gibi duzdu -> ortadan sarkar: sirtta bel cukuru, karin asagi kavis
         [(0, 0.07), (0.06, 0.22), (0.16, 0.28), (0.30, 0.20), (0.48, 0.10), (0.64, 0.12), (0.80, 0.20), (0.92, 0.19), (1, 0.08)],
         [(0, 0.09), (0.08, 0.23), (0.20, 0.28), (0.36, 0.29), (0.52, 0.29), (0.68, 0.27), (0.82, 0.24), (0.95, 0.17), (1, 0.07)])
    # DIZ COKEN BACAK - uyluk (asagi; sol kenar = on/quadriceps, sag = arka), baldir (geriye; sol = zemin tarafi duz, sag = baldir siskin), ayak
    uzuv(d, don, (0.06, 0.0), (0.05, -0.82), [(0, 0.22), (0.30, 0.21), (0.60, 0.17), (0.85, 0.12), (1, 0.105)],
         [(0, 0.22), (0.25, 0.19), (0.60, 0.15), (0.90, 0.11), (1, 0.105)])
    uzuv(d, don, (0.05, -0.80), (-0.70, Z + 0.035), [(0, 0.10), (0.5, 0.08), (1, 0.04)],
         [(0, 0.10), (0.22, 0.15), (0.45, 0.13), (0.80, 0.07), (1, 0.045)])
    uzuv(d, don, (-0.70, Z + 0.035), (-0.97, Z + 0.07), [(0, 0.035), (1, 0.012)], [(0, 0.045), (0.3, 0.04), (1, 0.012)])
    # GERI BACAK: kalca -> sivri ayak ucu (sol kenar = alt/arka: hamstring + baldir, sag = ust/on: quadriceps + kaval)
    uzuv(d, don, (-0.02, 0.12), arka_uc,
         [(0, 0.23), (0.20, 0.19), (0.42, 0.12), (0.48, 0.105), (0.58, 0.12), (0.70, 0.095), (0.88, 0.05), (1, 0.014)],
         [(0, 0.22), (0.20, 0.18), (0.42, 0.12), (0.50, 0.10), (0.70, 0.08), (0.86, 0.048), (0.92, 0.055), (1, 0.014)])
    # DESTEK KOLU: omuz -> bilek (asagi; sol = on: deltoid/biseps, sag = arka: triseps), el zeminde ileri
    uzuv(d, don, (0.90, 0.14), (0.93, Z + 0.05), [(0, 0.12), (0.15, 0.12), (0.40, 0.085), (0.50, 0.072), (0.62, 0.08), (0.95, 0.05), (1, 0.048)],
         [(0, 0.12), (0.25, 0.10), (0.50, 0.074), (0.65, 0.078), (1, 0.048)])
    uzuv(d, don, (0.93, Z + 0.04), (1.13, Z + 0.015), [(0, 0.045), (0.5, 0.042), (1, 0.014)], [(0, 0.03), (0.5, 0.025), (1, 0.01)])
    # ILERI KOL: omuz -> parmak ucu (sol = ust, sag = alt)
    kx, ky = kol_uc
    uzuv(d, don, (1.00, 0.20), (kx, ky), [(0, 0.11), (0.15, 0.10), (0.40, 0.072), (0.48, 0.065), (0.60, 0.068), (0.80, 0.046), (0.86, 0.048), (1, 0.014)],
         [(0, 0.12), (0.20, 0.09), (0.45, 0.066), (0.60, 0.066), (0.82, 0.044), (0.90, 0.04), (1, 0.012)])
    # BOYUN
    uzuv(d, don, (0.98, 0.20), (1.07, 0.36), [(0, 0.075), (1, 0.06)], [(0, 0.075), (1, 0.06)])


POZLAR = {
    "insan-bird-dog": ((-1.42, 0.46), (1.98, 0.17), ((1.14, 0.58), 0.22)),        # referans durusu
    "insan-bird-dog-high": ((-1.30, 0.74), (1.92, 0.36), ((1.14, 0.60), 0.22)),   # B: bacak ve kol biraz daha yukarida
}

Y = {"poz": {}}
for ad, (arka, kol, kafa) in POZLAR.items():
    W, H = int(4.0 * S), int(2.2 * S)
    ox, oy = 1.7 * S, 1.2 * S
    don = lambda q: (ox + q[0] * S, oy - q[1] * S)
    m = Image.new("L", (W, H), 0)
    ciz(ImageDraw.Draw(m), don, arka, kol)
    m = m.filter(ImageFilter.GaussianBlur(0.02 * S)).point(lambda v: 255 if v > 128 else 0)   # eklem gecisleri yumusak
    (kx, ky), kr = kafa; kx, ky = don((kx, ky)); kr *= S; g = 0.035 * S
    d = ImageDraw.Draw(m)
    d.ellipse((kx - kr - g, ky - kr - g, kx + kr + g, ky + kr + g), fill=0)   # kafa govdeden ince boslukla ayri
    d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.5))
    b = m.getbbox(); m = m.crop(b); m = m.resize((m.width // 3, m.height // 3), Image.LANCZOS)
    im = Image.new("RGBA", m.size, (0, 0, 0, 0)); im.putalpha(m)
    im.save(os.path.join(a.klasor, "poz", ad + ".png"))
    Y["poz"][ad] = {"kafa_px": [round((kx - b[0]) / 3, 1), round((ky - b[1]) / 3, 1), round(kr / 3, 1)]}
    print(ad, im.size)
json.dump(Y, open(os.path.join(a.klasor, "yerlesim.json"), "w", encoding="utf-8"), indent=1)
