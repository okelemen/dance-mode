"""HUMAN TETRIS 12 kapagi (REF-063 HumanWarmUp, 1 oyuncu) - 1280x720. kapak-tek-10.py'den (ayni kanal, ayni kapak dili).

    python kapak-tek-12.py --poz solo-side-bend-lunge-arm-over --arka varlik-12-kapak-0 --cikti A.jpg

REF-063 kapagi (olculdu: 21-HUMANWARMUP-10-KAPAK-OLCUM.md; doygunluk 0,750, parlaklik 0,552, renklilik 0,509, siyah 0,112):
ustte HUMAN TETRIS (her harf baska renk, parlak kabartma, acik kontur); sag ustte "1 Player", sol altta altin NEW rozeti; gokte pembe lazerler,
neon korkuluklu kopru + kafes kapi, kapida SARI duvar ve duvarda ayni pozun oyugu; onde tam boy DUZ SIMSIYAH siluet + beyaz kontur.
Referanstaki "-200 kcal" YOK (kullanici 30 Eki 2026: dogrulanamayan sayi yazilmaz). Arka plan Blender kapak modu, 2B ton boyamasi yok.
Cizim sirasi: arka plan -> kapidaki duvar -> yan etiket/rozet -> siluet -> baslik.
"""
import argparse, json, math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-12-kapak-0")
p.add_argument("--boy", type=float, default=520); p.add_argument("--x", type=float, default=0.45)
p.add_argument("--duvar", default="#fff200")
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
TFONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")

V = os.path.join(TP, a.arka, "tetris-varlik")
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
ac = Y["kapak-aciklik_p1"]; s = W / 1920
x0, y0, x1, y1 = ac[0] * s, ac[1] * s, ac[2] * s, ac[3] * s
maske = Image.open(os.path.join(TP, "varlik-12", "poz", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
ma = maske.getchannel("A")

# kapidaki duvar: aciklik kadar sari panel, ortasinda ayni pozun oyugu (REF-063)
pw, ph = int(x1 - x0), int(y1 - y0)
mh = int(ph * 0.82); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.8:
    mw = int(pw * 0.8); mh = int(mw * maske.height / maske.width)
delik = Image.new("L", (pw, ph), 0); delik.paste(ma.resize((mw, mh), Image.LANCZOS), ((pw - mw) // 2, int(ph * 0.95) - mh))
panel = Image.new("RGBA", (pw, ph), a.duvar)
panel.putalpha(Image.eval(delik, lambda v: 255 - v))
im.alpha_composite(panel, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)

RENK = ["#35d6ff", "#ff5fd2", "#ffc21f", "#2fe05c", "#a65cff", None, "#ff4a2e", "#2f9bff", "#ffb31a", "#25d85a", "#ff5fd2", "#c77dff"]


def ton(h, k):
    r = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return tuple(min(255, int(v * k + 255 * max(0, k - 1))) for v in r)


def harf(c, boy, renk, yon, derin_oran=0.085):
    """REF-063 harfi: acik kontur, renkli parlak yuz (ustte acik, altta doygun), koyu ton kabartma"""
    f = ImageFont.truetype(TFONT, boy)
    bx = f.getbbox(c); w, h = bx[2] - bx[0] + boy, bx[3] - bx[1] + boy
    ox, oy = boy // 2 - bx[0], boy // 2 - bx[1]
    k = Image.new("RGBA", (w, h), (0, 0, 0, 0)); kd = ImageDraw.Draw(k)
    derin = max(3, int(boy * derin_oran)); kon = max(2, int(boy * 0.035))
    for t in range(derin, 0, -1):
        kd.text((ox + yon * t, oy + t), c, font=f, fill=ton(renk, 0.55), stroke_width=kon, stroke_fill=ton(renk, 0.55))
    kd.text((ox, oy), c, font=f, fill=ton(renk, 1.15), stroke_width=kon, stroke_fill=ton(renk, 1.15))   # acik kontur
    yuz = Image.new("L", (w, h), 0); ImageDraw.Draw(yuz).text((ox, oy), c, font=f, fill=255)
    gr = Image.new("RGBA", (w, h))
    px = gr.load()
    ust, alt = ton(renk, 1.1), ton(renk, 0.88)   # 1. taslak: yuz soluk (ton 1,32) -> doygun
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
    """REF-063 altin NEW rozeti: dalgali disk + iki kurdele"""
    S = 3; n = 4 * r
    k = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)); d = ImageDraw.Draw(k); c = n * S // 2
    for sx in (-1, 1):
        q = [(c + sx * 0.18 * r * S, c + 0.5 * r * S), (c + sx * 0.72 * r * S, c + 0.5 * r * S), (c + sx * 0.82 * r * S, c + 1.68 * r * S), (c + sx * 0.5 * r * S, c + 1.42 * r * S), (c + sx * 0.22 * r * S, c + 1.68 * r * S)]
        d.polygon(q, fill="#e8331f"); d.polygon([(x + (c - x) * 0.14, y - 6 * S) for x, y in q], fill="#ffc21f")
    def dalga(R, g):
        return [(c + (R + g * math.cos(16 * t)) * S * math.cos(t), c + (R + g * math.cos(16 * t)) * S * math.sin(t)) for t in (i * math.pi / 180 for i in range(360))]
    d.polygon(dalga(r + 2, r * 0.07), fill="#e8331f"); d.polygon(dalga(r - 4, r * 0.07), fill="#ffc21f")
    q = int(r * 0.72 * S); d.ellipse((c - q, c - q, c + q, c + q), fill="#ffe14f", outline="#e8331f", width=4 * S)
    f = ImageFont.truetype(TFONT, int(r * 0.54 * S))
    d.text((c, c), "NEW", font=f, fill="#e8231f", anchor="mm", stroke_width=2 * S, stroke_fill="#ffffff")
    k = k.resize((n, n), Image.LANCZOS)
    im.alpha_composite(k, (int(cx - n / 2), int(cy - n / 2)))


# etiket + rozet (siluetten once)
yazi("1 Player", 1122, 180, 62, ["#35a8ff"], ara=1.0, isilti=0.75, derin_oran=0.07)
rozet(186, 530, 92)

# siluet: duz simsiyah + kalin beyaz dis kontur, tabani alt kenarda
sb = int(a.boy); sw = int(sb * maske.width / maske.height)
if sw > W * 0.62:
    sw = int(W * 0.62); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(W * a.x - sw / 2), H - sb - 14
kont = Image.new("L", (sw + 40, sb + 40), 0); kont.paste(sa, (20, 20)); kont = kont.filter(ImageFilter.MaxFilter(11))
im.paste((255, 255, 255, 255), (sx - 20, sy - 20), kont)
im.paste((0, 0, 0, 255), (sx, sy), sa)

# baslik en onde
yazi("HUMAN TETRIS", W / 2, 80, 132, RENK, ara=1.0)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
