"""HUMAN TETRIS 15 kapagi (REF-066 HumanWarmUp, CO-OP) - 1280x720. kapak-coop-13.py'den.

    python kapak-coop-15.py --poz duo-heart-arch-hands-on-hips --arka varlik-15-kapak-03 --cikti A.jpg

REF-066 kapagi (olculdu: 24-HUMANWARMUP-15-KAPAK-OLCUM.md; doygunluk 0,493, parlaklik 0,555, renklilik 0,303, siyah 0,120):
mavi izgara tunel + buz kopru + chevron + kafes kapi, kapida PEMBE duvar ve duvarda ayni pozun oyugu, kar taneleri; ustte beyaz yuzlu,
pembe-turuncu-mavi golgeli HUMAN TETRIS; solda "Full Body", sagda "2 Players / Co-op"; ortada kalp yapan iki duz simsiyah siluet + beyaz kontur.
Referanstaki "1M+ VIEWS" rozeti YOK (bizim icin dogru degil). Arka plan Blender kapak modu, 2B ton boyamasi yok.
Cizim sirasi: arka plan -> kapidaki duvar -> kar -> yan etiketler -> siluet -> baslik.
"""
import argparse, json, math, os, random
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-15-kapak-03")
p.add_argument("--boy", type=float, default=520); p.add_argument("--x", type=float, default=0.5)
p.add_argument("--duvar", default="#e83cc8")
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--parilti", type=float, default=0.3)
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
TFONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")

V = os.path.join(TP, a.arka, "tetris-varlik")
if not os.path.isdir(V):
    V = os.path.join(TP, a.arka)
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
ac = Y["kapak-aciklik_p1"]; s = W / 1920
x0, y0, x1, y1 = ac[0] * s, ac[1] * s, ac[2] * s, ac[3] * s
maske = Image.open(os.path.join(TP, "varlik-15-poz2", "grup", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
maske = maske.crop(maske.getchannel("A").getbbox())   # bos kenarlar boyu kucultmesin
ma = maske.getchannel("A")

# neon parlamasi (Blender kapakta glare yok): yalniz parlak neon piksellerden, yapi silinmez
par = im.convert("RGB").point(lambda v: 0 if v < 215 else v).filter(ImageFilter.GaussianBlur(10))
im = ImageChops.add(im.convert("RGB"), par.point(lambda v: int(v * a.parilti))).convert("RGBA")

# kapidaki duvar: aciklik kadar pembe panel, ortasinda ayni pozun oyugu (REF-066)
pw, ph = int(x1 - x0), int(y1 - y0)
mh = int(ph * 0.78); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.8:
    mw = int(pw * 0.8); mh = int(mw * maske.height / maske.width)
delik = Image.new("L", (pw, ph), 0); delik.paste(ma.resize((mw, mh), Image.LANCZOS), ((pw - mw) // 2, int(ph * 0.97) - mh))
panel = Image.new("RGBA", (pw, ph), a.duvar)
panel.putalpha(Image.eval(delik, lambda v: 255 - v))
im.alpha_composite(panel, (int(x0), int(y0)))
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)

# REF-066: beyaz yari saydam kar taneleri (sahnenin parcasi, ton boyamasi degil)
kar = Image.new("RGBA", (W, H), (0, 0, 0, 0)); kd = ImageDraw.Draw(kar); rnd = random.Random(66)
for _ in range(46):
    x, y, r = rnd.uniform(0, W), rnd.uniform(140, H), rnd.uniform(5, 13); dn = rnd.uniform(0, math.pi)
    for j in range(3):
        q = dn + j * math.pi / 3
        kd.line((x - r * math.cos(q), y - r * math.sin(q), x + r * math.cos(q), y + r * math.sin(q)), fill=(235, 245, 255, 150), width=2)
im.alpha_composite(kar)

RENK = ["#ff3fb0", "#ff3fb0", "#ff8a2a", "#ff8a2a", "#ff8a2a", None, "#ff8a2a", "#3fb0ff", "#3fb0ff", "#3fb0ff", "#3fb0ff", "#3fb0ff"]


def harf(c, boy, renk, yon, derin_oran=0.085):
    """REF-066 harfi: beyaz yuz + beyaz kontur, renkli golge kabartma"""
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
        g = Image.new("RGBA", r.size, rk or "#ffffff"); g.putalpha(r.getchannel("A")); par.alpha_composite(g, (px + M, py + M))
        x += adv * ara
    par = par.filter(ImageFilter.GaussianBlur(boy * 0.13)); par.putalpha(par.getchannel("A").point(lambda v: int(v * isilti)))
    im.alpha_composite(par.crop((M, M, M + W, M + H))); im.alpha_composite(kat.crop((M, M, M + W, M + H)))


def egik(metin, cx, cy, boy, renkler, aci):
    """REF-066 yan etiketi: hafif yukari egik, beyaz yuz, pembe-turuncu golge"""
    global im
    ana = im; im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    yazi(metin, cx, cy, boy, renkler, ara=1.07, isilti=0.7, derin_oran=0.05)   # kapak 2: "Players" harfleri yapisik okundu
    e = im.rotate(aci, center=(cx, cy), resample=Image.BICUBIC); im = ana; im.alpha_composite(e)


PEMBE_TURUNCU = ["#ff3fb0", "#ff8a2a"]
egik("Full Body", 235, 228, 70, PEMBE_TURUNCU, 6)
egik("2 Players", 1080, 200, 64, PEMBE_TURUNCU, 6)
egik("Co-op", 1085, 262, 64, PEMBE_TURUNCU, 6)

# siluet: duz simsiyah + kalin beyaz dis kontur, tabani alt kenarda, basliga degmez
ust_sinir = 150
sb = int(min(a.boy, H - 6 - ust_sinir)); sw = int(sb * maske.width / maske.height)
if sw > W * 0.7:                                          # kapak 1: genis kalp pozu 0,56'da kisa kaldi, REF'te siluet kapi ustune cikar
    sw = int(W * 0.7); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(W * a.x - sw / 2), H - sb - 6
kont = Image.new("L", (sw + 40, sb + 40), 0); kont.paste(sa, (20, 20)); kont = kont.filter(ImageFilter.MaxFilter(11))
im.paste((255, 255, 255, 255), (sx - 20, sy - 20), kont)
im.paste((0, 0, 0, 255), (sx, sy), sa)
print(a.cikti, "siluet kutu", sx, sy, sx + sw, sy + sb)

# baslik en onde
yazi("HUMAN TETRIS", W / 2, 80, 118, RENK, ara=1.1, derin_oran=0.06)

im.convert("RGB").save(a.cikti, quality=95)
print("->", a.cikti)
