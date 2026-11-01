"""HUMAN TETRIS 13 kapagi (REF-064 HumanWarmUp, CO-OP) - 1280x720. kapak-tek-12.py'den.

    python kapak-coop-13.py --poz duo-peak-lean-palms-overhead --arka varlik-13-kapak-0 --cikti A.jpg

REF-064 kapagi (olculdu: 22-HUMANWARMUP-13-KAPAK-OLCUM.md; doygunluk 0,382, parlaklik 0,425, renklilik 0,290, siyah 0,333):
yildizli gok, kopru + chevron + kafes kapi, kapida MAVI duvar ve duvarda ayni pozun oyugu; ustte beyaz yuzlu, harf harf renkli golgeli
HUMAN TETRIS; solda egik "2 Player", altinda kirmizi NEW rozeti; onde duz simsiyah siluet + beyaz kontur.
Referanstaki "-200 kcal" YOK (kullanici 30 Eki 2026). Arka plan Blender kapak modu, 2B ton boyamasi yok.
Cizim sirasi: arka plan -> kapidaki duvar -> yan etiket/rozet -> siluet -> baslik.
"""
import argparse, json, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-13-kapak-0")
p.add_argument("--boy", type=float, default=530); p.add_argument("--x", type=float, default=0.63)
p.add_argument("--duvar", default="#2a9ad4")
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--parilti", type=float, default=0.3)
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
maske = Image.open(os.path.join(TP, "varlik-13-poz2", "grup", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
maske = maske.crop(maske.getchannel("A").getbbox())   # bos kenarlar boyu kucultmesin
ma = maske.getchannel("A")

# neon parlamasi (Blender kapakta glare yok): yalniz parlak neon piksellerden, yapi silinmez
par = im.convert("RGB").point(lambda v: 0 if v < 215 else v).filter(ImageFilter.GaussianBlur(10))
im = ImageChops.add(im.convert("RGB"), par.point(lambda v: int(v * a.parilti))).convert("RGBA")

# kapidaki duvar: aciklik kadar mavi panel, ortasinda ayni pozun oyugu (REF-064)
pw, ph = int(x1 - x0), int(y1 - y0)
mh = int(ph * 0.72); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.8:
    mw = int(pw * 0.8); mh = int(mw * maske.height / maske.width)
delik = Image.new("L", (pw, ph), 0); delik.paste(ma.resize((mw, mh), Image.LANCZOS), (int(pw * 0.3 - mw / 2), int(ph * 0.97) - mh))
panel = Image.new("RGBA", (pw, ph), a.duvar)
panel.putalpha(Image.eval(delik, lambda v: 255 - v))
im.alpha_composite(panel, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)

RENK = ["#ff4fa8", "#ff4fa8", "#35e0d0", "#35e0d0", "#ffc21f", None, "#ff4fa8", "#ffc21f", "#ff4fa8", "#c77dff", "#a65cff", "#a65cff"]


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


# etiket + rozet (siluetten once)
_ana = im; im = Image.new("RGBA", (W, H), (0, 0, 0, 0))       # REF-064: etiket yukari egik
yazi("2 Player", 215, 300, 74, ["#ff4fa8", "#35e0d0", "#ffc21f", "#ff4fa8", "#35e0d0", "#ffc21f", "#c77dff", "#a65cff"], ara=1.0, isilti=0.75, derin_oran=0.07)
_e = im.rotate(17, center=(215, 300), resample=Image.BICUBIC); im = _ana; im.alpha_composite(_e)
rozet(130, 545, 80)

# siluet: duz simsiyah + kalin beyaz dis kontur, tabani alt kenarda
sb = int(a.boy); sw = int(sb * maske.width / maske.height)
if sw > W * 0.5:
    sw = int(W * 0.5); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(W * a.x - sw / 2), H - sb - 6
kont = Image.new("L", (sw + 40, sb + 40), 0); kont.paste(sa, (20, 20)); kont = kont.filter(ImageFilter.MaxFilter(11))
im.paste((255, 255, 255, 255), (sx - 20, sy - 20), kont)
im.paste((0, 0, 0, 255), (sx, sy), sa)

# baslik en onde
yazi("HUMAN TETRIS", W / 2, 76, 112, RENK, ara=1.1, derin_oran=0.06)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
