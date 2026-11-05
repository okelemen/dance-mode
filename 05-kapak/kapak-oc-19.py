"""HUMAN TETRIS 19 kapak siluetleri: Openclipart kamu mali siluetler (REF-071, GDJ) -> poz maskesi (dogal kafa + yuvarlak kafa).
Kullanici secimi 5 Kas 2026: A 1 = 302291 (ucgen pozu), B 11 = 275978 (dans pozu). Kafa konumlari 664x770 kaynakta olculdu.

    python kapak-oc-19.py --kaynak <REFERANSLAR/OC-yoga-siluet> --klasor ../03-motor/tetris-pvp/varlik-19-oc
"""
import argparse, json, os
from PIL import Image, ImageDraw

p = argparse.ArgumentParser(); p.add_argument("--kaynak", required=True); p.add_argument("--klasor", required=True); a = p.parse_args()
os.makedirs(os.path.join(a.klasor, "poz"), exist_ok=True)
# id: (ad, kafa merkezi, kafa yaricapi, silme elipsi (cx, cy, rx, ry, x_ust_sinir, y_alt_sinir))
SIL = {
    "302291": ("oc-ucgen", (150, 313), 47, (150, 313, 54, 52, 199, 362)),
    "275978": ("oc-dans", (389, 223), 49, (390, 222, 56, 54, 450, 262)),
}
Y = {"poz": {}}
for kid, (ad, (kx, ky), kr, (ex, ey, rx, ry, xs, ys)) in SIL.items():
    al = Image.open(os.path.join(a.kaynak, kid + "-2000.png")).convert("RGBA").getchannel("A")
    al = al.resize((al.width * 2, al.height * 2), Image.LANCZOS); f = 2
    al.save(os.path.join(a.klasor, "poz", ad + "-dogal.png").replace(".png", "_a.png"))
    im = Image.new("RGBA", al.size, (0, 0, 0, 0)); im.putalpha(al); im.save(os.path.join(a.klasor, "poz", ad + "-dogal.png"))
    # yuvarlak kafa: dogal kafa (sac dahil) silinir, ayni yere tam daire + ince bosluk (kapakta beyaz kontura doner)
    y_ = al.copy(); d = ImageDraw.Draw(y_)
    sil = Image.new("L", al.size, 0); ds = ImageDraw.Draw(sil)
    ds.ellipse(((ex - rx) * f, (ey - ry) * f, (ex + rx) * f, (ey + ry) * f), fill=255)
    ds.rectangle((xs * f, 0, al.width, al.height), fill=0); ds.rectangle((0, ys * f, al.width, al.height), fill=0)
    y_.paste(0, (0, 0), sil)
    g = 6 * f; R = kr * f
    d.ellipse((kx * f - R - g, ky * f - R - g, kx * f + R + g, ky * f + R + g), fill=0)
    d.ellipse((kx * f - R, ky * f - R, kx * f + R, ky * f + R), fill=255)
    im = Image.new("RGBA", y_.size, (0, 0, 0, 0)); im.putalpha(y_); im.save(os.path.join(a.klasor, "poz", ad + "-yuvarlak.png"))
    print(ad, al.size)
json.dump(Y, open(os.path.join(a.klasor, "yerlesim.json"), "w", encoding="utf-8"), indent=1)
