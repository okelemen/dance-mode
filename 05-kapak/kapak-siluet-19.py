"""HUMAN TETRIS 19 kapak silueti - zarif insan silueti (bird-dog), kendi cizimimiz (5 Kas 2026).

Kullanici: "referansin siluetine bak, bir de bizimkine bak". REF-070 kapagindaki siluet: ince uzun govde (kalca kavisi, ince bel),
geri bacak govde cizgisinin devami gibi capraz yukari, duz, sivri ayak; diz cokulen bacakta uyluk dik, baldir ve ayak yerde geride;
destek kolu dumduz yere, el yerde duz; ileri kol yatay ince; kafa ayri yuvarlak. Mixamo giysili manken bu inceligi vermiyor (kapak 1-7).
Oranlar referanstan (1 birim = kalca-omuz), cizgi birebir kopya degil: kendi anatomik kapsul zincirimiz + yumusatma.
Cikti: <klasor>/poz/<ad>.png (+ yerlesim.json kafa_px) -> kapak-tek-19.py --poz-klasor <klasor>.

    python kapak-siluet-19.py --klasor ../03-motor/tetris-pvp/varlik-19-insan
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFilter

p = argparse.ArgumentParser(); p.add_argument("--klasor", required=True); a = p.parse_args()
os.makedirs(os.path.join(a.klasor, "poz"), exist_ok=True)
S = 600   # birim -> piksel (cizim olcegi; sonra 1/3)
Z = -0.89  # zemin


def zincir(d, don, noktalar):
    """[(x, y, yaricap), ...] boyunca yaricapi araya katarak yuvarlak dolgu (anatomik incelen uzuv)"""
    for (x0, y0, r0), (x1, y1, r1) in zip(noktalar, noktalar[1:]):
        n = max(8, int(math.hypot(x1 - x0, y1 - y0) * 120))
        for i in range(n + 1):
            t = i / n; x, y = don((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)); r = (r0 + (r1 - r0) * t) * S
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)


def poz(arka_uc, kol_uc, kol_y):
    """bird-dog: arka_uc = geri bacak ayak ucu, kol_uc = ileri kol el ucu (x), kol_y = el yuksekligi"""
    kx, ky = arka_uc
    # geri bacak: kalca -> diz (%45) -> baldir (%62) -> bilek (%92) -> sivri uc
    def ara(t):
        return (-0.02 + (kx + 0.02) * t, 0.12 + (ky - 0.12) * t)   # taslak 2: bacak kalca ustunden cikar (uylukla kose yapmasin)
    # taslak 1: baldirdaki 0,10 -> 0,105 artis dizde dugum yapti -> tekduze incelen
    geri = [(*ara(0.0), 0.20), (*ara(0.25), 0.155), (*ara(0.45), 0.115), (*ara(0.62), 0.10), (*ara(0.80), 0.075), (*ara(0.92), 0.05), (*ara(1.0), 0.025)]
    return {
        # govde: kalca (arkada dolgun, ustte kavis) -> ince bel -> gogus -> omuz
        # taslak 1: govde referanstan ince -> kalca/popo dolgun (ustte kavis), bel, gogus
        "govde": [(0.0, 0.10, 0.20), (0.08, 0.09, 0.24), (0.30, 0.04, 0.215), (0.55, 0.06, 0.19), (0.78, 0.12, 0.195), (0.95, 0.17, 0.16)],
        "geri": geri,
        "diz": [(0.08, -0.04, 0.22), (0.06, -0.42, 0.16), (0.04, -0.80, 0.11), (-0.05, Z + 0.07, 0.09), (-0.40, Z + 0.075, 0.10),
                (-0.68, Z + 0.06, 0.055), (-0.80, Z + 0.06, 0.045), (-0.96, Z + 0.10, 0.022)],
        "destek": [(0.92, 0.12, 0.085), (0.925, -0.40, 0.065), (0.93, Z + 0.06, 0.05), (1.00, Z + 0.035, 0.04), (1.12, Z + 0.03, 0.025)],
        "kol": [(0.98, 0.18, 0.08), (1.35, (0.18 + kol_y) / 2 + 0.01, 0.06), (kol_uc - 0.18, kol_y, 0.045), (kol_uc, kol_y - 0.01, 0.022)],
        "boyun": [(0.96, 0.17, 0.11), (1.04, 0.33, 0.075)],
        "kafa": ((1.12, 0.52), 0.21),
    }


POZLAR = {
    "insan-bird-dog": poz((-1.42, 0.46), 1.98, 0.16),        # referans durusu
    "insan-bird-dog-high": poz((-1.30, 0.74), 1.92, 0.34),   # B: bacak ve kol biraz daha yukarida
}

Y = {"poz": {}}
for ad, P in POZLAR.items():
    W, H = int(4.0 * S), int(2.2 * S)
    ox, oy = 1.7 * S, 1.2 * S
    don = lambda q: (ox + q[0] * S, oy - q[1] * S)
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    for k in ("govde", "geri", "diz", "destek", "kol", "boyun"):
        zincir(d, don, P[k])
    # eklem birlesimleri yumusasin (kesik kapsul gorunmesin)
    m = m.filter(ImageFilter.GaussianBlur(0.025 * S)).point(lambda v: 255 if v > 128 else 0)
    (kx, ky), kr = P["kafa"]; kx, ky = don((kx, ky)); kr *= S; g = 0.035 * S
    d = ImageDraw.Draw(m)
    d.ellipse((kx - kr - g, ky - kr - g, kx + kr + g, ky + kr + g), fill=0)   # kafa govdeden ince boslukla ayri
    d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.5))
    b = m.getbbox(); m = m.crop(b); m = m.resize((m.width // 3, m.height // 3), Image.LANCZOS)
    im = Image.new("RGBA", m.size, (0, 0, 0, 0)); im.putalpha(m)
    im.save(os.path.join(a.klasor, "poz", ad + ".png"))
    # kafa_px: kirpilmis + 1/3 olcekte (kapak-tek-19 maske kirpma oncesi koordinat bekler: kirpma bbox'i tam goruntu oldugundan ayni)
    Y["poz"][ad] = {"kafa_px": [round((kx - b[0]) / 3, 1), round((ky - b[1]) / 3, 1), round(kr / 3, 1)]}
    print(ad, im.size, Y["poz"][ad])
json.dump(Y, open(os.path.join(a.klasor, "yerlesim.json"), "w", encoding="utf-8"), indent=1)
