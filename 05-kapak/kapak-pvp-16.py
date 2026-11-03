"""HUMAN TETRIS 16 kapagi (REF-067 TetrisBounce, 1v1) - 1280x720.

    python kapak-pvp-16.py --sol petal-sky-point --sag petal-hip-side-kick --arka varlik-16-kapak-0 --poz varlik-16-poz --cikti A.jpg

REF-067 kapagi (olculdu: 25-TETRISBOUNCE-01-KAPAK-OLCUM.md; doygunluk 0,621, parlaklik 0,780, renklilik 0,594, siyah 0,116):
sol MAVI / sag PEMBE kopru seridi ve kapisi, ustte tum genislikte baloncuk HUMAN TETRIS (HUMAN mavi->pembe, TETRIS pembe->turuncu->sari->mavi
yatay degrade, mor dis kontur, cam yansimasi), ortada baloncuk VS (V mavi, S pembe) + altinda kanatli "PVP" rozeti, onde iki dev duz simsiyah siluet
(kontursuz). Arka plan Blender kapak modu (varlik-sakura.py), 2B ton boyamasi yok.
Alinmaz (telif): anime kiz, ucan sari yaratik, kanatli yildiz amblemi. Kapidaki kafes+kiz yerine videodaki girdapli poz karti.
Cizim sirasi: arka plan -> kapidaki kart -> siluet -> VS + rozet -> baslik.
"""
import argparse, json, math, os
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--sol", required=True); p.add_argument("--sag", required=True)
p.add_argument("--ayna-sol", action="store_true"); p.add_argument("--ayna-sag", action="store_true")
p.add_argument("--arka", default="varlik-16-kapak-0"); p.add_argument("--poz", default="varlik-16-poz")
p.add_argument("--boy-sol", type=float, default=560); p.add_argument("--boy-sag", type=float, default=560)
p.add_argument("--x-sol", type=float, default=0.22); p.add_argument("--x-sag", type=float, default=0.78)
p.add_argument("--kontur", type=int, default=0)        # REF-067 siluetinde kontur yok; gerekirse px
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")


def font(boy):
    f = ImageFont.truetype(FONT, boy)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


V = os.path.join(TP, a.arka, "tetris-varlik")
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
yer = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8")); s = (W / 2) / 960
for i, o in enumerate(("p1", "p2")):
    ser = Image.open(os.path.join(V, "kapak-serit-%s.png" % o)).convert("RGBA").resize((W // 2, H), Image.LANCZOS)
    im.alpha_composite(ser, (i * W // 2, 0))


def girdap_kart(w, h, renk):
    """videodaki poz karti: beyaz zemin, oyuncu renginde iki kollu girdap, yuvarlak kose"""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h * 0.55
    r = np.hypot(x - cx, y - cy) / max(w, h); t = np.arctan2(y - cy, x - cx)
    sv = np.sin(r * 18 + 2 * t)
    q = np.clip((sv + 0.15) * 2.2, 0, 1)[..., None]
    c = np.array([int(renk[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    rgb = (255 * (1 - q) + c * q).astype(np.uint8)
    k = Image.fromarray(rgb, "RGB").convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(w * 0.06), fill=255)
    k.putalpha(m)
    return k


for i, (o, renk) in enumerate((("p1", "#a8e8ff"), ("p2", "#ffbfe8"))):
    x0, y0, x1, y1 = [v * s for v in yer["aciklik_" + o]]
    kw, kh = int((x1 - x0) * 0.86), int((y1 - y0) * 0.9)
    im.alpha_composite(girdap_kart(kw, kh, renk), (int(i * W // 2 + (x0 + x1) / 2 - kw / 2), int(y1 - kh - (y1 - y0) * 0.03)))


def maske_al(ad, ayna):
    m = Image.open(os.path.join(TP, a.poz, "tetris-varlik", "poz", ad + ".png")).convert("RGBA")
    if ayna:
        m = m.transpose(Image.FLIP_LEFT_RIGHT)
    al = m.getchannel("A")
    return al.crop(al.getbbox())


def siluet(ma, boy, xo):
    sb = int(boy); sw = int(sb * ma.width / ma.height)
    if sw > W * 0.44:
        sw = int(W * 0.44); sb = int(sw * ma.height / ma.width)
    sa = ma.resize((sw, sb), Image.LANCZOS)
    sx, sy = int(max(6, min(W - sw - 6, W * xo - sw / 2))), H - sb + 6
    if a.kontur:
        k = Image.new("L", (sw + 40, sb + 40), 0); k.paste(sa, (20, 20)); k = k.filter(ImageFilter.MaxFilter(a.kontur * 2 + 1))
        im.paste((255, 255, 255, 255), (sx - 20, sy - 20), k)
    im.paste((0, 0, 0, 255), (sx, sy), sa)
    print(a.cikti, "siluet kutu", sx, sy, sx + sw, sy + sb)


siluet(maske_al(a.sol, a.ayna_sol), a.boy_sol, a.x_sol)
siluet(maske_al(a.sag, a.ayna_sag), a.boy_sag, a.x_sag)


def baloncuk(metin, cx, cy, boy, renkler, kontur="#4a1f86", ara=0.0):
    """REF-067 basligi: yatay cok renkli degrade, kalin mor dis kontur, ustte cam yansimasi, beyaz ince ic hat"""
    f = font(boy); S = 2
    fS = font(boy * S)
    bx = fS.getbbox(metin); tw, th = bx[2] - bx[0], bx[3] - bx[1]
    pad = int(boy * S * 0.25)
    w, h = tw + 2 * pad, th + 2 * pad
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255)
    dis = Image.new("L", (w, h), 0); ImageDraw.Draw(dis).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.075), stroke_fill=255)
    ic = Image.new("L", (w, h), 0); ImageDraw.Draw(ic).text((pad - bx[0], pad - bx[1]), metin, font=fS, fill=255, stroke_width=int(boy * S * 0.02), stroke_fill=255)
    # degrade: renkler metin boyunca yatay
    xs = np.linspace(0, 1, w)[None, :].repeat(h, 0); cs = [np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.float32) for c in renkler]
    pos = np.linspace(0, 1, len(cs)); rgb = np.zeros((h, w, 3), np.float32)
    for ch in range(3):
        rgb[..., ch] = np.interp(xs, pos, [c[ch] for c in cs])
    yy = np.linspace(0, 1, h)[:, None]
    rgb = rgb * (0.9 + 0.25 * (1 - yy))[..., None].clip(0, 1.15)            # ust acik, alt hafif koyu (dolgun)
    dol = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    K = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    golge = Image.new("RGBA", (w, h), (40, 10, 80, 160)); K.paste(golge, (int(boy * S * 0.03), int(boy * S * 0.05)), dis)
    K.paste(Image.new("RGBA", (w, h), kontur), (0, 0), dis)
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), ic)
    K.paste(dol, (0, 0), m)
    # cam yansimasi: harfin ust ~%38'inde yari saydam beyaz bant
    yans = Image.new("L", (w, h), 0); ImageDraw.Draw(yans).rectangle((0, pad + int(th * 0.06), w, pad + int(th * 0.38)), fill=120)
    yans = ImageChops.multiply(yans, m.filter(ImageFilter.MinFilter(int(boy * S * 0.05) | 1))).filter(ImageFilter.GaussianBlur(boy * S * 0.012))
    K.paste(Image.new("RGBA", (w, h), "#ffffff"), (0, 0), yans)
    K = K.resize((w // S, h // S), Image.LANCZOS)
    im.alpha_composite(K, (int(cx - K.width / 2), int(cy - K.height / 2)))


def rozet_pvp(cx, cy):
    """kanatli PVP rozeti: koyu mor yuvarlak plaka, altin degrade PVP, iki yanda mavi/pembe kanat"""
    S = 3; K = Image.new("RGBA", (420 * S, 160 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(K); c = (210 * S, 80 * S)
    for sx, renk in ((-1, (150, 220, 255, 255)), (1, (255, 170, 220, 255))):
        for j in range(5):                                                 # tuy: kademeli elips
            L = (150 - j * 22) * S; ang = math.radians(-18 + j * 15)
            x0 = c[0] + sx * 60 * S; y0 = c[1] - 8 * S + j * 9 * S
            q = Image.new("RGBA", K.size, (0, 0, 0, 0)); qd = ImageDraw.Draw(q)
            qd.ellipse((x0 - (L if sx < 0 else 0), y0 - 17 * S, x0 + (L if sx > 0 else 0), y0 + 17 * S), fill=renk, outline=(255, 255, 255, 255), width=3 * S)
            K.alpha_composite(q.rotate(sx * math.degrees(ang) * -1, center=(x0, y0), resample=Image.BICUBIC))
    d.rounded_rectangle((c[0] - 92 * S, c[1] - 44 * S, c[0] + 92 * S, c[1] + 44 * S), 26 * S, fill="#3a1060", outline="#ffd24a", width=5 * S)
    f = font(62 * S)
    t = Image.new("L", K.size, 0); ImageDraw.Draw(t).text(c, "PVP", font=f, anchor="mm", fill=255)
    g = Image.new("RGBA", K.size); gd = ImageDraw.Draw(g)
    for y in range(K.height):
        q_ = max(0, min(1, (y - (c[1] - 30 * S)) / (60 * S)))
        gd.line((0, y, K.width, y), fill=(255, int(236 - 70 * q_), int(120 - 90 * q_), 255))
    ImageDraw.Draw(K).text(c, "PVP", font=f, anchor="mm", fill="#7a3a00", stroke_width=4 * S, stroke_fill="#7a3a00")
    K.paste(g, (0, 0), t)
    K = K.resize((420, 160), Image.LANCZOS)
    im.alpha_composite(K, (int(cx - 210), int(cy - 80)))


baloncuk("V", W / 2 - 62, 360, 190, ["#7ae8ff", "#2aa8ff", "#5a7cff"])
baloncuk("S", W / 2 + 62, 380, 190, ["#ff7ad8", "#ff3a9a", "#ff5ab8"])
rozet_pvp(W / 2, 505)
baloncuk("HUMAN", 330, 92, 150, ["#9ee8ff", "#7ab8ff", "#c88cff", "#ff8ad8"])
baloncuk("TETRIS", 920, 92, 150, ["#ff6ac8", "#ff9a5a", "#ffe24a", "#9ae86a", "#7ad0ff"])

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
