"""HUMAN TETRIS 14 kapagi (REF-065 HumanWarmUp, 1v1) - 1280x720. kapak-coop-13.py'den.

    python kapak-pvp-14.py --sol duel-deep-bow-stride --sag duel-sword-arm-open-stance --ayna-sag --arka varlik-14-kapak-06 --cikti A.jpg

REF-065 kapagi (olculdu: 23-HUMANWARMUP-14-KAPAK-OLCUM.md; doygunluk 0,660, parlaklik 0,559, renklilik 0,426, siyah 0,107):
iki yari ayri kamerali altin kopru, kafes kapilarda yesil + turkuaz duvar ve duvarda ayni pozun oyugu; harf harf renkli neon HUMAN TETRIS;
kirmizi-mavi VS cubugu, "2P PvP Version", kirmizi NEW rozeti; onde duz simsiyah iki siluet + beyaz kontur.
Arka plan Blender kapak modu, 2B ton boyamasi yok. Cizim sirasi: arka plan -> kapidaki duvar -> etiket/rozet -> siluet -> VS -> baslik.
"""
import argparse, json, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--sol", required=True); p.add_argument("--sag", required=True)
p.add_argument("--ayna-sol", action="store_true"); p.add_argument("--ayna-sag", action="store_true")
p.add_argument("--arka", default="varlik-14-kapak-0")
p.add_argument("--boy-sol", type=float, default=400); p.add_argument("--boy-sag", type=float, default=500)
p.add_argument("--x-sol", type=float, default=0.22); p.add_argument("--x-sag", type=float, default=0.80)
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--parilti", type=float, default=0.3)
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
TFONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
DUVAR = ("#10b45e", "#22b4ac")   # REF-065: yesil, turkuaz

V = os.path.join(TP, a.arka, "tetris-varlik")
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
ser = Image.open(os.path.join(V, "kapak-serit-p1.png")).convert("RGBA").resize((W // 2, H), Image.LANCZOS)
im.alpha_composite(ser, (0, 0)); im.alpha_composite(ser, (W // 2, 0))
ac = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))["aciklik_p1"]; s = (W / 2) / 960


def maske_al(ad, ayna):
    m = Image.open(os.path.join(TP, "varlik-14", "poz", ad + ".png")).convert("RGBA")
    if ayna:
        m = m.transpose(Image.FLIP_LEFT_RIGHT)
    return m.getchannel("A").crop(m.getchannel("A").getbbox())


M_SOL, M_SAG = maske_al(a.sol, a.ayna_sol), maske_al(a.sag, a.ayna_sag)
par = im.convert("RGB").point(lambda v: 0 if v < 215 else v).filter(ImageFilter.GaussianBlur(10))
im = ImageChops.add(im.convert("RGB"), par.point(lambda v: int(v * a.parilti))).convert("RGBA")

# kapidaki duvar: aciklik kadar panel, ortasinda ayni pozun oyugu
x0, y0, x1, y1 = [v * s for v in ac]; pw, ph = int(x1 - x0), int(y1 - y0)
for i, (ma, renk) in enumerate(zip((M_SOL, M_SAG), DUVAR)):
    mh = int(ph * 0.82); mw = int(mh * ma.width / ma.height)
    if mw > pw * 0.85:
        mw = int(pw * 0.85); mh = int(mw * ma.height / ma.width)
    delik = Image.new("L", (pw, ph), 0); delik.paste(ma.resize((mw, mh), Image.LANCZOS), ((pw - mw) // 2, int(ph * 0.96) - mh))
    panel = Image.new("RGBA", (pw, ph), renk); panel.putalpha(Image.eval(delik, lambda v: 255 - v))
    im.alpha_composite(panel, (int(x0) + i * W // 2, int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)

RENK = ["#ff4fa8", "#ff4fa8", "#20d8ff", "#20d8ff", "#ffb01f", None, "#b060ff", "#ff4fa8", "#ffb01f", "#ff4fa8", "#ff4040", "#a65cff"]


def ton(h, k):
    r = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return tuple(min(255, int(v * k + 255 * max(0, k - 1))) for v in r)


def harf(c, boy, renk, yon, derin_oran=0.085):
    """REF-064 harfi: beyaz yuz + beyaz kontur, renkli golge kabartma"""
    f = ImageFont.truetype(TFONT, boy)
    bx = f.getbbox(c); w, h = bx[2] - bx[0] + boy, bx[3] - bx[1] + boy
    ox, oy = boy // 2 - bx[0], boy // 2 - bx[1]
    k = Image.new("RGBA", (w, h), (0, 0, 0, 0)); kd = ImageDraw.Draw(k)
    derin = max(3, int(boy * derin_oran)); kon = max(2, int(boy * 0.035))
    for t in range(derin, 0, -1):
        kd.text((ox + yon * t, oy + t), c, font=f, fill=renk, stroke_width=kon, stroke_fill=renk)
    kd.text((ox, oy), c, font=f, fill="#ffffff", stroke_width=kon, stroke_fill="#ffffff")
    yuz = Image.new("L", (w, h), 0); ImageDraw.Draw(yuz).text((ox, oy), c, font=f, fill=255)
    gr = Image.new("RGBA", (w, h))
    px = gr.load()
    ust, alt = (255, 255, 255), (232, 236, 244)
    b0, b1 = oy + bx[1], oy + bx[3]
    for y in range(h):
        q = max(0.0, min(1.0, (y - b0) / max(1, b1 - b0)))
        rk = tuple(int(ust[i] + (alt[i] - ust[i]) * q) for i in range(3)) + (255,)
        for x in range(w):
            px[x, y] = rk
    k.paste(gr, (0, 0), yuz)
    return k, f.getlength(c)


def yazi(metin, cx, cy, boy, renkler, ara=1.03, isilti=0.8, derin_oran=0.085):
    M = 300
    kat = Image.new("RGBA", (W + 2 * M, H + 2 * M), (0, 0, 0, 0)); par = Image.new("RGBA", kat.size, (0, 0, 0, 0))
    H_ = [(harf(c, boy, renkler[i % len(renkler)] or "#ffffff", -1 if (i + 0.5) < len(metin) / 2 else 1, derin_oran), renkler[i % len(renkler)]) if c != " " else None for i, c in enumerate(metin)]
    top = sum(h[0][1] * ara if h else boy * 0.3 for h in H_)
    x = cx - top / 2
    for h in H_:
        if not h:
            x += boy * 0.3; continue
        (r, adv), rk = h
        px, py = int(x + adv / 2 - r.width / 2), int(cy - r.height / 2)
        kat.alpha_composite(r, (px + M, py + M))
        g = Image.new("RGBA", r.size, rk); g.putalpha(r.getchannel("A")); par.alpha_composite(g, (px + M, py + M))
        x += adv * ara
    par = par.filter(ImageFilter.GaussianBlur(boy * 0.13)); par.putalpha(par.getchannel("A").point(lambda v: int(v * isilti)))
    im.alpha_composite(par.crop((M, M, M + W, M + H))); im.alpha_composite(kat.crop((M, M, M + W, M + H)))


def rozet(cx, cy, r):
    """REF-064 kirmizi NEW rozeti: dalgali disk + iki kurdele"""
    S = 3; n = 4 * r
    k = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)); d = ImageDraw.Draw(k); c = n * S // 2
    for sx in (-1, 1):
        q = [(c + sx * 0.18 * r * S, c + 0.5 * r * S), (c + sx * 0.72 * r * S, c + 0.5 * r * S), (c + sx * 0.82 * r * S, c + 1.68 * r * S), (c + sx * 0.5 * r * S, c + 1.42 * r * S), (c + sx * 0.22 * r * S, c + 1.68 * r * S)]
        d.polygon(q, fill="#f02a22")
    def dalga(R, g):
        return [(c + (R + g * math.cos(16 * t)) * S * math.cos(t), c + (R + g * math.cos(16 * t)) * S * math.sin(t)) for t in (i * math.pi / 180 for i in range(360))]
    d.polygon(dalga(r + 2, r * 0.07), fill="#f02a22")
    q = int(r * 0.72 * S); d.ellipse((c - q, c - q, c + q, c + q), fill="#f02a22", outline="#ffffff", width=3 * S)
    f = ImageFont.truetype(TFONT, int(r * 0.54 * S))
    d.text((c, c), "NEW", font=f, fill="#ffffff", anchor="mm", stroke_width=1 * S, stroke_fill="#c9d4ff")
    k = k.resize((n, n), Image.LANCZOS)
    im.alpha_composite(k, (int(cx - n / 2), int(cy - n / 2)))


def siluet(ma, boy, xo):
    sb = int(boy); sw = int(sb * ma.width / ma.height)
    if sw > W * 0.42:
        sw = int(W * 0.42); sb = int(sw * ma.height / ma.width)
    sa = ma.resize((sw, sb), Image.LANCZOS)
    sx, sy = int(max(14, min(W - sw - 14, W * xo - sw / 2))), H - sb - 8
    kont = Image.new("L", (sw + 40, sb + 40), 0); kont.paste(sa, (20, 20)); kont = kont.filter(ImageFilter.MaxFilter(11))
    im.paste((255, 255, 255, 255), (sx - 20, sy - 20), kont)
    im.paste((0, 0, 0, 255), (sx, sy), sa)
    print(a.cikti, "siluet kutu", sx, sy, sx + sw, sy + sb)


def vs_cubuk(cx, cy):
    """REF-065 VS: kirmizi-mavi neon cubuk, ortada egik beyaz VS + simsek; arkasinda patlama ve kivilcim"""
    S = 3; K = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(K)
    x0_, x1_, h_ = (cx - 162) * S, (cx + 162) * S, 21 * S; y_ = cy * S
    for r_, ops in ((22, 70), (12, 130)):
        q = Image.new("RGBA", K.size, (0, 0, 0, 0)); qd = ImageDraw.Draw(q)
        qd.rounded_rectangle((x0_ - r_, y_ - h_ - r_, cx * S, y_ + h_ + r_), h_ + r_, fill=(255, 30, 40, ops))
        qd.rounded_rectangle((cx * S, y_ - h_ - r_, x1_ + r_, y_ + h_ + r_), h_ + r_, fill=(30, 60, 255, ops))
        K.alpha_composite(q.filter(ImageFilter.GaussianBlur(r_ * S / 2)))
    d.rounded_rectangle((x0_, y_ - h_, cx * S, y_ + h_), h_, fill="#ff0a14", outline="#ff9a9a", width=2 * S)
    d.rounded_rectangle((cx * S, y_ - h_, x1_, y_ + h_), h_, fill="#0a24ff", outline="#9ab4ff", width=2 * S)
    for t in range(16):                                    # patlama isinlari
        ang = t / 16 * 2 * math.pi; r0, r1 = 34 * S, (56 if t % 2 else 72) * S
        d.line((cx * S + r0 * math.cos(ang), y_ + r0 * math.sin(ang), cx * S + r1 * math.cos(ang), y_ + r1 * math.sin(ang)), fill=(255, 240, 170, 230), width=2 * S)
    sim = [(cx + 16, cy - 52), (cx - 12, cy - 3), (cx + 7, cy - 3), (cx - 18, cy + 52), (cx + 20, cy + 4), (cx + 1, cy + 4)]
    d.polygon([(x * S, y * S) for x, y in sim], fill="#ffe24a", outline="#ff5a2a")
    k_ = K.resize((W, H), Image.LANCZOS); im.alpha_composite(k_)
    f = ImageFont.truetype(TFONT, 76)
    y = Image.new("RGBA", (W, H), (0, 0, 0, 0)); yd = ImageDraw.Draw(y)
    yd.text((cx - 22, cy), "V", font=f, fill="#ffffff", anchor="mm", stroke_width=5, stroke_fill="#b00018")
    yd.text((cx + 25, cy + 3), "S", font=f, fill="#ffffff", anchor="mm", stroke_width=5, stroke_fill="#0a1cb0")
    im.alpha_composite(y.rotate(8, center=(cx, cy), resample=Image.BICUBIC))


# etiket + rozet (siluetten once)
def etiket(metin, cy, boy):
    f = ImageFont.truetype(TFONT, boy)
    par_ = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(par_).text((W / 2, cy), metin, font=f, fill="#ff3fc0", anchor="mm", stroke_width=6, stroke_fill="#ff3fc0")
    im.alpha_composite(par_.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(im).text((W / 2, cy), metin, font=f, fill="#ffffff", anchor="mm", stroke_width=2, stroke_fill="#ffd0f0")


etiket("2P PvP", 290, 58); etiket("Version", 352, 62)
rozet(W // 2, 505, 80)
siluet(M_SOL, a.boy_sol, a.x_sol); siluet(M_SAG, a.boy_sag, a.x_sag)
vs_cubuk(W // 2, 199)

# baslik en onde
yazi("HUMAN TETRIS", W / 2, 84, 122, RENK, ara=1.12, derin_oran=0.06)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
