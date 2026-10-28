"""HUMAN TETRIS 10 kapagi (REF-061 HumanWarmUp, 1 oyuncu) - 1280x720.

    python kapak-tek-10.py --poz daily-front-kick-high-guard --arka varlik-10-kapak-04 --cikti A.jpg [--ayna]

REF-061 kapagi (olculdu: 20-HUMANWARMUP-01-KAPAK-OLCUM.md; doygunluk 0,43, renklilik 0,24, parlaklik 0,50):
ustte HUMAN TETRIS (beyaz harf, her harfin arkasinda baska renk kabartma golgesi), solda "X1 Player", sagda "Full Body" + "#N";
arkada videonun tuneli + gumus kafes kapi, kapida kirmizi duvar ve duvarda AYNI pozun oyugu; onde tam boy DUZ SIMSIYAH siluet +
beyaz dis kontur, yazinin altinda. Referanstaki "1M+ VIEWS" rozeti YOK (kullanici 28 Eki 2026: dogru olmayan sayi yazilmaz).
Arka plan Blender kapak modu (varlik.py --mod tunel --yalniz kapak --kapak-pozlama), 2B ton boyamasi yok.
Cizim sirasi: arka plan -> kapidaki duvar -> yan etiketler -> siluet -> baslik (kontrol listesi: siluet yazinin arkasinda kalmaz).
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TP = os.path.join(KOK, "03-motor", "tetris-pvp")
p = argparse.ArgumentParser()
p.add_argument("--poz", required=True); p.add_argument("--ayna", action="store_true")
p.add_argument("--arka", default="varlik-10-kapak-04")
p.add_argument("--no", default="#10")
p.add_argument("--boy", type=float, default=560); p.add_argument("--x", type=float, default=0.5)
p.add_argument("--duvar", default="#e23a55")
p.add_argument("--renk", type=float, default=1.0); p.add_argument("--parlak", type=float, default=1.0)   # yalniz hafif genel ayar
p.add_argument("--cikti", required=True)
a = p.parse_args()
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf")


def yfont(boy):
    f = ImageFont.truetype(FONT, boy)
    f.set_variation_by_axes([700, 112])      # Bold + genis (deneme 2: ad ile secim sessizce Light birakiyordu)
    return f


# ---------------------------------------------------------------- arka plan: tunel + kopru + kafes kapi (Blender kapak modu)
V = os.path.join(TP, a.arka, "tetris-varlik")
im = Image.open(os.path.join(V, "kapak-gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
im.alpha_composite(Image.open(os.path.join(V, "kapak-serit.png")).convert("RGBA").resize((W, H), Image.LANCZOS))
Y = json.load(open(os.path.join(V, "yerlesim.json"), encoding="utf-8"))
ac = Y["kapak-aciklik_p1"]; s = W / 1920
x0, y0, x1, y1 = ac[0] * s, ac[1] * s, ac[2] * s, ac[3] * s
maske = Image.open(os.path.join(TP, "varlik-10", "poz", a.poz + ".png")).convert("RGBA")
if a.ayna:
    maske = maske.transpose(Image.FLIP_LEFT_RIGHT)
ma = maske.getchannel("A")

# kapidaki duvar: aciklik kadar kirmizi panel, ortasinda ayni pozun oyugu (oyukta tunel, hafif koyu) - REF-061 kapagi
pw, ph = int(x1 - x0), int(y1 - y0)
mh = int(ph * 0.9); mw = int(mh * maske.width / maske.height)
if mw > pw * 0.94:
    mw = int(pw * 0.94); mh = int(mw * maske.height / maske.width)
oy = ma.resize((mw, mh), Image.LANCZOS)
panel = Image.new("RGBA", (pw, ph), a.duvar)
delik = Image.new("L", (pw, ph), 0); delik.paste(oy, ((pw - mw) // 2, int(ph * 0.97) - mh))
panel.putalpha(Image.eval(delik, lambda v: 255 - v))
golge = Image.new("RGBA", (pw, ph), (20, 6, 50, 0)); golge.putalpha(delik.point(lambda v: int(v * 0.3)))
im.alpha_composite(golge, (int(x0), int(y0))); im.alpha_composite(panel, (int(x0), int(y0)))
# genel ton ayari YALNIZ arka plana (kullanici 28 Eki: "parlakligi biraz kisalim"; tum kapaga uygulaninca beyaz yazi griye donuyordu)
if a.renk != 1.0:
    im = ImageEnhance.Color(im).enhance(a.renk)
if a.parlak != 1.0:
    im = ImageEnhance.Brightness(im).enhance(a.parlak)

d = ImageDraw.Draw(im)
# baslik yazisi (kullanici 28 Eki 2026: "referans aldigin yaziyla ayni fontta mi, ayni tarzda mi?" -> yakin plan karsilastirma):
# REF-061 basligi cok kalin, genis, yuvarlak koseli, M/A sivri tepeli (elimizdeki en yakini Titan One, %8 genisletilmis);
# beyaz-mavimsi yuz, KOYU KONTUR YOK; renkli kisim harf GRUPLARINA gore (HU pembe, MA camgobegi, N-TET altin, RIS mor) parlayan
# neon kabartma; kabartma perspektifli (ortanin solundaki harflerde sola-asagi, sagindakilerde saga-asagi); harfler hafif oynak.
TFONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
# kullanici 28 Eki: "yazilar cok parlak, parlakligini kis" -> yuz saf beyaz degil kirli acik gri-lavanta, isilti zayif, kabartma bir ton koyu
YUZ = "#f2f7ff"   # kullanici 28 Eki: iki kismadan sonra "parlakligi ilk haline getir"
GRUP = {"HUMAN TETRIS": ["#ff5fd2", "#ff5fd2", "#3fe8dc", "#3fe8dc", "#e9c06a", None, "#e9c06a", "#e9c06a", "#e9c06a", "#a57cff", "#a57cff", "#a57cff"]}
ETIKET = ["#ff5fd2", "#3fe8dc", "#e9c06a", "#a57cff"]


def harf_resmi(c, boy, renk, yon, aci, font=None, derin_oran=0.09, gen=1.08):
    f = yfont(boy) if font == "fredoka" else ImageFont.truetype(TFONT, boy)
    bx = f.getbbox(c); w, h = bx[2] - bx[0] + boy, bx[3] - bx[1] + boy
    k = Image.new("RGBA", (int(w * 1.08), h), (0, 0, 0, 0)); kd = ImageDraw.Draw(k)
    ox, oy = boy // 2 - bx[0], boy // 2 - bx[1]
    derin = max(3, int(boy * derin_oran))
    kal = int(boy * 0.045) if font == "fredoka" else 0   # Fredoka Bold referans etiketinden ince: ayni renkte kontur ile kalinlastir
    for t in range(derin, 0, -1):                        # renkli kabartma (perspektif yonunde)
        kd.text((ox + yon * t, oy + t), c, font=f, fill=renk, stroke_width=kal, stroke_fill=renk)
    kd.text((ox, oy), c, font=f, fill=YUZ, stroke_width=kal, stroke_fill=YUZ)
    k = k.resize((int(k.width * gen), k.height), Image.LANCZOS)          # Titan One'i referansin genisligine yaklastir
    return k.rotate(aci, resample=Image.BICUBIC, expand=True), f.getlength(c) * gen


def kabartma(metin, cx, cy, boy, renkler=None, oynak=False, font=None, derin_oran=0.09, gen=1.08, isilti_guc=0.75):
    """REF-061 kapak yazi tarzi: beyaz harf + grup renginde parlayan neon kabartma, koyu kontur yok"""
    ARA = 1.06 if font else 0.96                        # etikette kalinlastirma konturu harfleri birlestiriyordu
    renkler = renkler or GRUP.get(metin) or [ETIKET[i % 4] for i in range(len(metin))]
    harfler, top = [], 0
    for i, c in enumerate(metin):
        if c == " ":
            harfler.append(None); top += boy * 0.32; continue
        yon = -1 if (i + 0.5) < len(metin) / 2 else 1
        aci = ((-3, 2, -2, 3, -1)[i % 5]) if oynak else 0
        r, adv = harf_resmi(c, boy, renkler[i % len(renkler)] or "#e9c06a", 1 if font else yon, aci, font, derin_oran, gen)
        harfler.append((r, adv, renkler[i % len(renkler)])); top += adv * ARA
    x = cx - top / 2
    M = 300                                              # kenar payi: ust kenara tasan harf kutusu kirpilmasin (deneme 2: max(0, py) basligi asagi itiyordu)
    katman = Image.new("RGBA", (W + 2 * M, H + 2 * M), (0, 0, 0, 0)); isilti = Image.new("RGBA", katman.size, (0, 0, 0, 0))
    for i, h in enumerate(harfler):
        if h is None:
            x += boy * 0.32; continue
        r, adv, renk = h
        dy = ((4, -6, 2, -4, 5)[i % 5]) * boy / 120 if oynak else 0
        px, py = int(x + adv * 0.48 - r.width / 2), int(cy + dy - r.height / 2)
        katman.alpha_composite(r, (px + M, py + M))
        g = Image.new("RGBA", r.size, renk or "#e9c06a"); g.putalpha(r.getchannel("A"))
        isilti.alpha_composite(g, (px + M, py + M))
        x += adv * ARA
    isilti = isilti.filter(ImageFilter.GaussianBlur(boy * 0.12)); isilti.putalpha(isilti.getchannel("A").point(lambda v: int(v * isilti_guc)))
    im.alpha_composite(isilti.crop((M, M, M + W, M + H))); im.alpha_composite(katman.crop((M, M, M + W, M + H)))


# yan etiketler (siluetten once)
# yan etiketler basligla AYNI font (kullanici 28 Eki: "ayni fontlar olsun"), duz hizada, her harfe ayri renkli ince kabartma
GOKKUSAGI = ["#ff5fd2", "#ffd84f", "#3fe8dc", "#a57cff", "#5dffb0", "#ff8a3d"]
kabartma("X1 Player", 245, 222, 66, GOKKUSAGI, derin_oran=0.06, gen=1.04, isilti_guc=0.35)
kabartma("Full Body", 1075, 214, 66, GOKKUSAGI, derin_oran=0.06, gen=1.04, isilti_guc=0.12)
kabartma(a.no, 1150, 322, 72, GOKKUSAGI, derin_oran=0.06, gen=1.04, isilti_guc=0.12)

# siluet: duz simsiyah + kalin beyaz dis kontur, tam boy, tabani alt kenarda
sb = int(a.boy); sw = int(sb * maske.width / maske.height)
if sw > W * 0.62:
    sw = int(W * 0.62); sb = int(sw * maske.height / maske.width)
sa = ma.resize((sw, sb), Image.LANCZOS)
sx, sy = int(W * a.x - sw / 2), H - sb - 6
kont = Image.new("L", (sw + 40, sb + 40), 0); kont.paste(sa, (20, 20)); kont = kont.filter(ImageFilter.MaxFilter(11))
im.paste((255, 255, 255, 255), (sx - 20, sy - 20), kont)
im.paste((0, 0, 0, 255), (sx, sy), sa)

# baslik en onde
kabartma("HUMAN TETRIS", W / 2, 74, 132, derin_oran=0.065, isilti_guc=0.95)   # kullanici 28 Eki: harfler simetrik, duz hizada (oynaklik yok)

out = im.convert("RGB")
out.save(a.cikti, quality=95)
print("->", a.cikti)
