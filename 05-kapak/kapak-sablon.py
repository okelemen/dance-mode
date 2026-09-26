from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import math, os
S = ""  # kare yolu tam verilir
SIL = "C:/Users/eleme/DANCE-MODE/05-kapak/siluetler/"
F = "C:/Windows/Fonts/"
W, H = 1280, 720

def arka(kare, kutu, doygun=1.35, kontrast=1.15):
    im = Image.open(os.path.join(S, kare)).convert("RGB").crop(kutu).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(doygun)
    im = ImageEnhance.Contrast(im).enhance(kontrast)
    # kenar karartma
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse((-260, -200, W + 260, H + 200), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(120))
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), m).convert("RGBA")

def hiz_cizgileri(im, renk=(255, 255, 255, 150), n=26):
    k = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(k)
    cx, cy = W / 2, H * 0.55
    for i in range(n):
        a = i / n * 2 * math.pi + 0.13
        r1, r2 = 560 + (i * 37) % 120, 900
        p = lambda r, w=0: (cx + math.cos(a + w) * r, cy + math.sin(a + w) * r)
        d.polygon([p(r1), p(r2, 0.012), p(r2, -0.012)], fill=renk)
    im.alpha_composite(k)

def siluet(im, dosya, yuk, merkez_x, alt_y, parlama=(90, 230, 255), cizgi=7):
    s = Image.open(SIL + dosya); s = s.crop(s.getchannel("A").getbbox())
    s = s.resize((int(s.width * yuk / s.height), yuk), Image.LANCZOS)
    a = s.getchannel("A")
    pad = 40
    A = Image.new("L", (s.width + 2 * pad, s.height + 2 * pad)); A.paste(a, (pad, pad))
    dis = A.filter(ImageFilter.MaxFilter(cizgi * 2 + 1))
    kat = Image.new("RGBA", A.size)
    glow = dis.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    kat.alpha_composite(Image.merge("RGBA", [Image.new("L", A.size, c) for c in parlama] + [glow]))
    kat.alpha_composite(Image.merge("RGBA", [Image.new("L", A.size, 255)] * 3 + [dis]))
    kat.alpha_composite(Image.merge("RGBA", [Image.new("L", A.size, c) for c in (6, 3, 18)] + [A]))
    im.alpha_composite(kat, (int(merkez_x - kat.width / 2), int(alt_y - kat.height + pad)))

def yazi(im, metin, font, boy, merkez, dolgu=(255, 255, 255), kontur=(0, 0, 0), kk=8,
         egim=0.22, parlama=None, genislik=None):
    f = ImageFont.truetype(F + font, boy)
    x0, y0, x1, y1 = ImageDraw.Draw(im).textbbox((0, 0), metin, font=f, stroke_width=kk)
    tw, th = x1 - x0, y1 - y0
    pad = 60
    k = Image.new("RGBA", (tw + 2 * pad + int(th * egim), th + 2 * pad))
    ImageDraw.Draw(k).text((pad - x0 + int(th * egim), pad - y0), metin, font=f, fill=dolgu,
                           stroke_width=kk, stroke_fill=kontur)
    k = k.transform(k.size, Image.AFFINE, (1, egim, -egim * k.height * 0.5, 0, 1, 0), Image.BICUBIC)
    if genislik and tw > genislik:
        k = k.resize((int(k.width * genislik / tw), k.height), Image.LANCZOS)
    if parlama:
        g = k.getchannel("A").filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(14))
        gl = Image.merge("RGBA", [Image.new("L", k.size, c) for c in parlama] + [g])
        gl.alpha_composite(k); k = gl
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))

def yildiz(im, merkez, r, satirlar, zemin=(255, 205, 20), aci=-10, parlama=None, kk=4):
    k = Image.new("RGBA", (int(r * 2.6), int(r * 2.6))); d = ImageDraw.Draw(k)
    c = k.width / 2; n = 14; pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * 0.62
        a = i * math.pi / n
        pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
    d.polygon(pts, fill=(0, 0, 0));
    ic = [(c + (x - c) * 0.9, c + (y - c) * 0.9) for x, y in pts]
    d.polygon(ic, fill=zemin)
    im2 = Image.new("RGBA", k.size); y = c - sum(b for _, b, *_ in satirlar) / 2
    for metin, boy, renk in satirlar:
        f = ImageFont.truetype(F + "impact.ttf", boy)
        tw = d.textlength(metin, font=f)
        d.text((c - tw / 2, y - boy * 0.08), metin, font=f, fill=renk, stroke_width=kk, stroke_fill=(0, 0, 0))
        y += boy
    k = k.rotate(aci, Image.BICUBIC)
    if parlama:
        g = k.getchannel("A").filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(18))
        gl = Image.merge("RGBA", [Image.new("L", k.size, c) for c in parlama] + [g])
        gl.alpha_composite(k); k = gl
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))

def serit(im, metin, merkez, zemin=(255, 45, 140), boy=46, egim=0.22):
    f = ImageFont.truetype(F + "impact.ttf", boy)
    tw = ImageDraw.Draw(im).textlength(metin, font=f)
    k = Image.new("RGBA", (int(tw + 120), boy + 60)); d = ImageDraw.Draw(k)
    d.rectangle((30, 20, k.width - 30, k.height - 20), fill=(0, 0, 0))
    d.rectangle((36, 26, k.width - 36, k.height - 26), fill=zemin)
    d.text((60, 22), metin, font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    k = k.transform(k.size, Image.AFFINE, (1, egim, -egim * k.height * 0.5, 0, 1, 0), Image.BICUBIC)
    im.alpha_composite(k, (int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)))

def kaydet(im, ad):
    im.convert("RGB").save(os.path.join(S, ad), quality=92)
    print(ad, os.path.getsize(os.path.join(S, ad)) // 1024, "KB")


# ============================================================================
# KILITLI KAPAK SABLONU (17 Eyl 2026, kullanici onayi) — kurallar:
#   docs/KURALLAR.md bolum 6 "KAPAK SABLONU". Asagidaki KONUM/YAZI TIPI sabitleri
#   kullanici sormadan degistirilmez. Arka plan, tema adi, renkler, poz, sayilar serbest.
# ============================================================================
BASLIK      = dict(font="impact.ttf", boy=190, merkez=(640, 105), egim=0.22, kk=8, genislik=1180)
TEMA_SERIT  = dict(merkez=(640, 225), boy=46)
SILUET      = dict(yuk=490, merkez_x=640, alt_y=745)
LEVEL_ROZET = dict(merkez=(185, 545), r=150, aci=-10)
COMBO_ROZET = dict(merkez=(1080, 540), r=170, aci=8)

import argparse
p = argparse.ArgumentParser()
p.add_argument("--kare", required=True, help="masterdan alinmis 1920x1080 kare")
p.add_argument("--kutu", default="455,300,1425,846", help="HUD'suz kirpma x0,y0,x1,y1")
p.add_argument("--baslik", default="DANCE MODE")
p.add_argument("--tema", required=True)
p.add_argument("--level", default="5")
p.add_argument("--combo", default="336")
p.add_argument("--poz", default="siluet-raise-roof.png")
p.add_argument("--tema-renk", default="230,30,40")
p.add_argument("--parlama", default="255,60,170")
p.add_argument("--combo-renk", default="255,40,150")
p.add_argument("--combo-etiket", default="COMBO", help="sag yildizin alt yazisi (SEKER: KCAL, COMBO yok)")
p.add_argument("--cikti", required=True)
a = p.parse_args()
rgb = lambda t: tuple(int(x) for x in t.split(","))

im = arka(a.kare, rgb(a.kutu)); hiz_cizgileri(im)
siluet(im, a.poz, SILUET["yuk"], SILUET["merkez_x"], SILUET["alt_y"])
yazi(im, a.baslik, BASLIK["font"], BASLIK["boy"], BASLIK["merkez"], kk=BASLIK["kk"], egim=BASLIK["egim"],
     parlama=rgb(a.parlama), genislik=BASLIK["genislik"])
serit(im, a.tema, TEMA_SERIT["merkez"], zemin=rgb(a.tema_renk), boy=TEMA_SERIT["boy"])
tr = rgb(a.tema_renk)
yildiz(im, LEVEL_ROZET["merkez"], LEVEL_ROZET["r"], [("NEW", 58, tr), ("LEVEL", 58, tr), (a.level, 96, tr)],
       aci=LEVEL_ROZET["aci"], parlama=(255, 255, 255))
yildiz(im, COMBO_ROZET["merkez"], COMBO_ROZET["r"], [(a.combo, 118, (255, 255, 255)), (a.combo_etiket, 56, (255, 255, 255))],
       zemin=rgb(a.combo_renk), aci=COMBO_ROZET["aci"], parlama=(255, 255, 255), kk=6)
im.convert("RGB").save(a.cikti, quality=92)
print(a.cikti)
