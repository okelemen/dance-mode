"""HUMAN TETRIS 9 kapagi (REF-060, --tema 09: varlik-09, P1 pembe / P2 mavi, uzay + kafes kapilar ici yildizli isin paneli, pembe-mor-mavi
baloncuk VS + sari simsek, sure rozeti YOK (REF-060 kapaginda yok); arka plan Blender kapak modu, 2B ton boyamasi yok; olcum
19-GLOWMOTION-3P-BATTLE-3-KAPAK-OLCUM.md). Kaynak kapak-pvp-08.py. Onceki: HUMAN TETRIS 8 kapagi (REF-059, --tema 08: varlik-08, P1 pembe / P2 mavi, disko kapilar ici spot isikli sahne, yesil baloncuk VS +
"5 MINS" rozeti; olcum 18-GLOWMOTION-PVP10-KAPAK-OLCUM.md). Onceki: TETRIS MODE 6 kapagi: kapak-pvp-04.py + --tema 06 (REF-057). TETRIS MODE PVP kapagi - 4. video (REF-055) kopyasi. Kaynak kapak-pvp.py (REF-053/054 onayli yontem); 3. video oturumu o dosyada
calistigi icin ayri dosya (19 Eki 2026). Tema 04: varlik-04, kirmizi/safir, REF-055 atesli VS + sari simsek, duz baslik.

TETRIS MODE PVP kapagi (REF-053 duzeni, bizim renkler) - 1280x720.

    python kapak-pvp.py --p1 gate-pose --p2 extended-side-angle [--ayna2] --cikti KAPAK-A.jpg

REF-053 kapagi (olculdu: 11-GLOWMOTION-PVP3-KAPAK-OLCUM.md): ustte tam genislik iki renkli tombul parlak baslik; arkada videonun
kendi sahnesi (iki kafes kapi + jole yol); onde yazinin ALTINDA iki dev DUZ SIMSIYAH siluet + kalin beyaz dis kontur; ortada VS.
Sayi / soru / yuz / P1-P2 yazisi YOK. Bizde: baslik seri adi TETRIS MODE (kullanici 18 Eki 2026), TETRIS yesil, MODE turuncu;
arka plan videonun Blender varliklari (03-motor/tetris-pvp/varlik), siluet = videodaki pozun Mixamo maskesi; VS altin + camgobegi.
Baslik harf yontemi kapak-tetris.py parlak_yazi ile ayni (17 Eki onayli: hacim + beyaz kontur + parlak bant + isilti).
"""
import argparse, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageEnhance

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
p = argparse.ArgumentParser()
p.add_argument("--tema", default="02", choices=["02", "03", "04", "06", "08", "09"])   # 03: REF-054, mor/sari, galaksi, jole VS
p.add_argument("--p1", required=True); p.add_argument("--p2", required=True)
p.add_argument("--ayna1", action="store_true"); p.add_argument("--ayna2", action="store_true")
p.add_argument("--baslik", default="TETRIS MODE")
p.add_argument("--boy1", type=float, default=540); p.add_argument("--boy2", type=float, default=540)
p.add_argument("--gen1", type=float, default=600); p.add_argument("--gen2", type=float, default=600)
p.add_argument("--cikti", required=True)
p.add_argument("--ton", type=float, default=0.0); p.add_argument("--renk", type=float, default=1.6); p.add_argument("--parlak", type=float, default=1.05)   # onayli (24 Eki): doygunluk 0,62-0,63 / ref 0,66
a = p.parse_args()
TON_GUC, RENK_GUC, PARLAK = a.ton, a.renk, a.parlak
T3 = a.tema == "03"
T9 = a.tema == "09"   # 9. video (REF-060): uzay, kapakta kapak-gok/serit/panel (Blender), VS pembe-mor-mavi, rozet yok
T8 = a.tema == "08"   # 8. video (REF-059): disko, yesil VS + 5 MINS
T6 = a.tema in ("06", "08", "09")   # 6. video (REF-057): HUMAN TETRIS, mavi/pembe, kuzey isigi + buz daglar, sari simsekli iki renkli VS
T4 = a.tema in ("04", "06")
V = os.path.join(KOK, "03-motor", "tetris-pvp", "varlik-09" if T9 else "varlik-08" if T8 else "varlik-06" if T6 else "varlik-04" if T4 else "varlik-03" if T3 else "varlik")
W, H = 1280, 720
FONT = os.path.join(KOK, "05-kapak", "fontlar", "TitanOne.ttf")
yfont = lambda boy: ImageFont.truetype(FONT, boy)

# ---------------------------------------------------------------- arka plan: videonun sahnesi
im = Image.open(os.path.join(V, "kapak-gok.png" if (T8 or T9) and os.path.exists(os.path.join(V, "kapak-gok.png")) else "gok.png")).convert("RGBA").resize((W, H), Image.LANCZOS)
KS = (T8 or T9) and os.path.exists(os.path.join(V, "kapak-serit-p1.png"))   # 8. video: Blender'da kapaga ozel doygun seritler
for i, ad in enumerate(("kapak-serit-p1.png", "kapak-serit-p2.png") if KS else ("serit-p1.png", "serit-p2.png")):
    s = Image.open(os.path.join(V, ad)).convert("RGBA").resize((W // 2, H), Image.LANCZOS)
    im.alpha_composite(s, (i * W // 2, 0))
import json
Y = json.load(open(os.path.join(V, "kapak-yerlesim.json" if KS else "yerlesim.json"), encoding="utf-8"))
if KS:
    Y = {k.replace("kapak-", ""): v for k, v in Y.items()}
for i, (ad, ac) in enumerate(((("kapak-panel-p1.png" if KS and T9 else "kapak-panel2-p1.png" if KS else "panel2-p1.png" if T8 else "panel-p1.png"), Y["aciklik_p1"]), (("kapak-panel-p2.png" if KS and T9 else "kapak-panel2-p2.png" if KS else "panel2-p2.png" if T8 else "panel-p2.png"), Y["aciklik_p2"]))):
    sx = (W / 2) / 960; sy = H / 1080
    x0, y0, x1, y1 = ac[0] * sx + i * W / 2, ac[1] * sy, ac[2] * sx + i * W / 2, ac[3] * sy
    pw = x1 - x0; ph = pw / (1100 / 904)
    pn = Image.open(os.path.join(V, ad)).convert("RGBA").resize((int(pw), int(ph)), Image.LANCZOS)
    if T9:   # REF-060 kapaginda kapi icindeki isin paneli net ve tam opak
        pass
    elif T4:   # REF-055 kapaginda girdap panel kapida net ve renkli; bizim panelin beyaz merkezi kapakta sis gibi duruyordu (deneme 2)
        al = pn.getchannel("A").point(lambda v: int(v * (0.7 if KS else 0.85)))   # 8. video: tunel isiklari kapidan sizsin
        pn = ImageEnhance.Brightness(ImageEnhance.Color(pn.convert("RGB")).enhance(1.9)).enhance(1.0 if T6 else 0.82).convert("RGBA")
        pn.putalpha(al)
    elif T3:   # REF-054 kapaginda kapi icinden isin patlamasi + arkadaki gok goruluyor: panel yari saydam
        pn.putalpha(pn.getchannel("A").point(lambda v: int(v * 0.38)))
    im.alpha_composite(pn, (int(x0), int(y1 - ph)))
# ampul isiltisi (videodaki kayan isik)
gl = Image.new("RGBA", (W, H)); dg = ImageDraw.Draw(gl)
for i in range(2):
    for q in Y.get("ampul_p%d" % (i + 1), []):
        x = i * W / 2 + q[0] * (W / 2) / 960; y = q[1] * H / 1080
        dg.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 255, 255, 230) if (T8 or T9) else (255, 236, 170, 230))
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(3)))
im.alpha_composite(gl)
# deneme 1 olcumu: referanstan koyu (0,64 / 0,78), az renkli (0,38 / 0,57), az ayrintili (0,10 / 0,26) -> kisma katmani
# kaldirildi, arka plan canlandirildi, goge videodaki gibi havai fisek + huzme + parilti (REF-053'te gok denizanasiyla dolu)
if T8:
    # deneme 1 olcumu (REF-059 / biz): doygunluk 0,66 / 0,41, beyaz 0,07 / 0,26, ayrinti 0,29 / 0,16 -> kapilar kadraji
    # doldursun diye 1,3x yakinlas (REF-059'da pelus kapilar ustten alta kadar), pastel karo zemin koyulastir + doygunlastir
    # deneme 2: 1,3x yakinlasma panel sahnesini tum kadraja yaydi, pelus cerceve + disko topu kadrajdan cikti -> 1,08
    z_ = 1.0 if KS else 1.08; zw, zh = int(W / z_), int(H / z_); x_ = (W - zw) // 2; y_ = (H - zh) // 3
    im = im.crop((x_, max(0, y_), x_ + zw, max(0, y_) + zh)).resize((W, H), Image.LANCZOS)
    # deneme 3 (kullanici 24 Eki: "renkler o kadar soluk ... canlandir ... dag kadar fark var"): pastel/beyaz karo ve panel
    # doygunluk artisini almiyor (beyazin rengi yok) -> sol yarisi sicak pembe, sag yarisi elektrik mavi ile CARPILIR
    # (beyaz -> oyuncu rengi), sonra doygunluk + kontrast. Hedef REF-059 olcumu: doygunluk 0,66, parlaklik 0,79.
    ton = Image.new("RGB", (W, H))
    for x in range(W):
        u = min(1.0, max(0.0, (x - W * 0.42) / (W * 0.16)))          # ortada yumusak gecis
        c0, c1 = (255, 70, 175), (60, 150, 255)
        ImageDraw.Draw(ton).line([(x, 0), (x, H)], fill=tuple(int(c0[j] + (c1[j] - c0[j]) * u) for j in range(3)))
    rgb = im.convert("RGB")
    im = Image.blend(rgb, ImageChops.multiply(rgb, ton), TON_GUC).convert("RGBA")
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(RENK_GUC)).enhance(1.08 if KS else 1.2)
    im = ImageEnhance.Brightness(im).enhance(PARLAK)
im = ImageEnhance.Color(im).enhance(RENK_GUC if T9 else 1.0 if T8 else 1.45 if T6 else 1.4 if T4 else 1.0 if T3 else 1.35)   # 3. video: limon sarisi zaten doygun, yazi/siluet yutulmasin
im = ImageEnhance.Brightness(im).enhance(PARLAK if T9 else 1.0 if T8 else 1.12 if T6 else 0.92 if T4 else 0.9 if T3 else 1.12)
import random
rnd = random.Random(53)
fx = Image.new("RGBA", (W, H)); df = ImageDraw.Draw(fx)
for bx, ang, renk in (() if T9 else ((0.06, -0.25, (90, 170, 255)), (0.5, 0.0, (255, 240, 255)), (0.94, 0.25, (255, 90, 190))) if T6 else
                     ((0.06, -0.25, (255, 90, 120)), (0.5, 0.0, (255, 220, 140)), (0.94, 0.25, (110, 140, 255))) if T4 else
                     ((0.06, -0.25, (190, 120, 255)), (0.5, 0.0, (255, 250, 140)), (0.94, 0.25, (230, 255, 110))) if T3 else
                      ((0.06, -0.25, (90, 255, 240)), (0.5, 0.0, (255, 220, 120)), (0.94, 0.25, (140, 255, 160)))):
    x0, y0, L = W * bx, H * 0.95, H * 1.2
    ux, uy = math.sin(ang), -math.cos(ang)
    df.polygon([(x0, y0), (x0 + ux * L - uy * 60, y0 + uy * L + ux * 60), (x0 + ux * L + uy * 60, y0 + uy * L - ux * 60)], fill=renk + (60,))
# deneme 1 (4. video): efekt katmani sahneyi sisledi (beyaz 0,136 / ref 0,054) -> T4 de az efekt, kapi + girdap gorunsun
NF, NK, NKF, NP = (0, 0, 0, 90) if T9 else (0, 6, 2, 160) if T6 else (2, 8, 4, 140) if T4 else (7, 26, 10, 420)
for _ in range(NF):                                            # havai fisek patlamalari (gokte, kapilarin ustunde ve ortada)
    cx_, cy_ = rnd.choice([rnd.uniform(560, 720), rnd.uniform(20, 1260)]), rnd.uniform(150, 330)
    renk = rnd.choice([(46, 155, 255), (255, 62, 165), (255, 255, 255), (120, 240, 255)] if T6 else
                      [(255, 60, 100), (90, 120, 255), (255, 210, 120), (255, 255, 255)] if T4 else
                      [(245, 255, 61), (180, 92, 255), (255, 122, 230), (255, 255, 255), (143, 180, 255)] if T3 else
                      [(255, 215, 90), (90, 255, 230), (150, 255, 140), (255, 255, 255), (255, 160, 60)])
    R = rnd.uniform(40, 80)
    for i in range(28):
        an = i / 28 * 2 * math.pi; rr = R * rnd.uniform(0.75, 1.05)
        df.line([(cx_ + math.cos(an) * rr * 0.35, cy_ + math.sin(an) * rr * 0.35), (cx_ + math.cos(an) * rr, cy_ + math.sin(an) * rr)], fill=renk + (230,), width=3)
for _ in range(NK):                                           # jole isik kureleri (parlak ust, renkli govde)
    x, y, r = rnd.uniform(0, W), rnd.uniform(140, H * 0.7), rnd.uniform(8, 26)
    renk = rnd.choice([(46, 155, 255), (255, 62, 165), (200, 160, 255), (120, 240, 255)] if T6 else
                      [(255, 45, 85), (47, 84, 255), (255, 200, 110), (95, 230, 208)] if T4 else
                      [(180, 92, 255), (245, 255, 61), (255, 122, 230), (143, 180, 255)] if T3 else
                      [(90, 255, 220), (170, 255, 120), (255, 210, 110), (120, 220, 255)])
    df.ellipse((x - r, y - r, x + r, y + r), fill=renk + (150,), outline=(255, 255, 255, 200), width=2)
    df.ellipse((x - r * 0.55, y - r * 0.7, x - r * 0.05, y - r * 0.25), fill=(255, 255, 255, 210))
for _ in range(NKF):                                           # kucuk havai fisekler
    cx_, cy_ = rnd.uniform(0, W), rnd.uniform(160, 420); R = rnd.uniform(16, 32)
    renk = rnd.choice([(255, 140, 210), (140, 200, 255), (255, 255, 255)] if T6 else
                      [(255, 120, 140), (140, 160, 255), (255, 255, 255)] if T4 else
                      [(245, 255, 61), (200, 140, 255), (255, 255, 255)] if T3 else [(255, 230, 120), (120, 255, 230), (255, 255, 255)])
    for i in range(16):
        an = i / 16 * 2 * math.pi
        df.line([(cx_ + math.cos(an) * R * 0.3, cy_ + math.sin(an) * R * 0.3), (cx_ + math.cos(an) * R, cy_ + math.sin(an) * R)], fill=renk + (220,), width=2)
for _ in range(NP):                                          # parilti
    x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(1.5, 4.5)
    df.ellipse((x - r, y - r, x + r, y + r), fill=(255, 245, 210, rnd.randint(140, 255)))
im.alpha_composite(fx.filter(ImageFilter.GaussianBlur(5))); im.alpha_composite(fx)

# ---------------------------------------------------------------- siluetler (yazinin altinda, iki yanda dev)
def siluet(ad, ayna, merkez_x, alt_y, hedef_h, max_w):
    m = Image.open(os.path.join(V, "poz", ad + ".png")).getchannel("A")
    m = m.crop(m.getbbox())
    if ayna:
        m = m.transpose(Image.FLIP_LEFT_RIGHT)
    s = min(hedef_h / m.height, max_w / m.width)
    m = m.resize((int(m.width * s), int(m.height * s)), Image.LANCZOS)
    tam = Image.new("L", (W, H)); tam.paste(m, (int(merkez_x - m.width / 2), int(alt_y - m.height)))
    return tam.point(lambda v: 255 if v > 110 else 0)

KONTUR = 21                                                   # referansta kontur kalin


def yerlestir(ad, ayna, x0, boy, gen, engel, yon, ust_sinir):
    """deneme 4 (kullanici 18 Eki: "VS yazisi siluetlere degmesin ... VS on planda olsun ama siluetleri de kapatmasin"):
    siluet (kontur + 6 px pay dahil) VS rozetinin dolu alanina ve basliga degene kadar disa kayar; kenara dayaninca %4 kuculur."""
    olc = 1.0
    for _ in range(80):
        x = x0
        while True:
            m = siluet(ad, ayna, x, 718, boy * olc, gen * olc)
            bb = m.getbbox()
            genis = m.filter(ImageFilter.MaxFilter(KONTUR + 12))
            carpisma = ImageChops.multiply(genis, engel).getbbox() is not None
            icerde = bb[0] >= 12 and bb[2] <= W - 12                 # deneme 4 B: kenardan tasip kesiliyordu
            if not carpisma and bb[1] >= ust_sinir and icerde:
                return m
            if carpisma and icerde and (bb[0] - 10 >= 12 if yon < 0 else bb[2] + 10 <= W - 12):
                x += (30 if T8 else 10) * yon                    # once disa kay (8. video: buyuk VS, hizli adim)
                continue
            break
        olc *= 0.92 if T8 else 0.96                                              # kenara dayandi ya da basliga degiyor -> kucul
    return m


def siluetleri_ciz(maskeler):
    mk = Image.new("L", (W, H))
    for m in maskeler:
        mk = Image.composite(Image.new("L", (W, H), 255), mk, m)
    mk = mk.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    kontur = mk.filter(ImageFilter.MaxFilter(KONTUR))
    isilti = kontur.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    # 3. video: limon sarisi zeminde beyaz kontur kayboluyordu -> konturun disinda koyu mor hale (beyaz kontur ayrisir)
    hale_renk, hale_guc = ((40, 8, 80), 0.85) if T3 else ((255, 236, 160), 0.55)
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in hale_renk] + [isilti.point(lambda v: int(v * hale_guc))]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 255)] * 3 + [kontur]))
    im.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), c) for c in (6, 4, 14)] + [mk.filter(ImageFilter.GaussianBlur(0.7))]))


# ---------------------------------------------------------------- VS rozeti (bizim: camgobegi simsek + altin harf)
def vs_jole(merkez, r=150):
    """REF-054 kapagindaki VS: parlak yesil jole harf + arkasinda sari simsek + egik halka ve jole kabarciklar (bizim cizim)"""
    k = Image.new("RGBA", (int(r * 3.4), int(r * 3.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    sm = [(c[0] + 40, c[1] - r * 1.35), (c[0] - 55, c[1] + 5), (c[0] + 5, c[1] + 2), (c[0] - 45, c[1] + r * 1.35),
          (c[0] + 70, c[1] - 20), (c[0] + 8, c[1] - 16)]
    d.polygon(sm, fill=(245, 255, 61), outline=(255, 255, 255), width=5)
    halka = Image.new("RGBA", k.size); dh = ImageDraw.Draw(halka)
    dh.ellipse((c[0] - r * 1.45, c[1] - r * 0.42, c[0] + r * 1.45, c[1] + r * 0.42), outline=(150, 255, 60), width=9)
    k.alpha_composite(halka.rotate(-12, Image.BICUBIC, center=c))
    import random as _r
    rr_ = _r.Random(11)
    for _ in range(9):
        an = rr_.uniform(0, 2 * math.pi); uz = r * rr_.uniform(1.1, 1.5); br = rr_.uniform(9, 20)
        x, y = c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.6
        d.ellipse((x - br, y - br, x + br, y + br), fill=(150, 240, 50), outline=(230, 255, 180), width=2)
        d.ellipse((x - br * 0.5, y - br * 0.65, x - br * 0.05, y - br * 0.25), fill=(255, 255, 255))
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (200, 255, 120)] + [g.point(lambda v: int(v * 0.6))])
    dolu = k.getchannel("A")
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    yz2 = parlak_yazi("VS", yfont(210), [(190, 255, 70), (90, 220, 40)], kontur=12, derinlik=16, dis=(20, 70, 10),
                      parlama=(220, 255, 140), zipla=0, don=7)
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2 - 6)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    return kat, ImageChops.lighter(engel, ym)


def vs_06(merkez, r=100):   # deneme 1: r 150 kapilari ortuyordu; REF-057 VS kucuk rozet
    """REF-057 kapak VS (olculdu 16-GLOWMOTION-3P-BATTLE-2-KAPAK-OLCUM.md): tombul parlak VS + arkasinda sari simsek + beyaz
    4 koseli parilti. 2 oyuncu: V P1 mavisi, S P2 pembesi; simsek sari-beyaz, isilti iki renk."""
    k = Image.new("RGBA", (int(r * 3.4), int(r * 3.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    sm = [(c[0] + 52, c[1] - r * 1.30), (c[0] - 60, c[1] + 10), (c[0] + 4, c[1] + 6), (c[0] - 52, c[1] + r * 1.30),
          (c[0] + 76, c[1] - 22), (c[0] + 10, c[1] - 18)]
    d.polygon(sm, fill=(255, 226, 40), outline=(255, 255, 255), width=6)
    for (px, py, rr) in ((c[0] - r * 0.95, c[1] - r * 0.75, 30), (c[0] + r * 1.0, c[1] + r * 0.7, 22), (c[0] + r * 0.9, c[1] - r * 0.9, 16)):
        d.polygon([(px, py - rr), (px + rr * 0.25, py - rr * 0.25), (px + rr, py), (px + rr * 0.25, py + rr * 0.25), (px, py + rr),
                   (px - rr * 0.25, py + rr * 0.25), (px - rr, py), (px - rr * 0.25, py - rr * 0.25)], fill=(255, 255, 255))
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (255, 240, 150)] + [g.point(lambda v: int(v * 0.55))])
    dolu = k.getchannel("A")
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    yz2 = parlak_yazi("VS", yfont(145), [(46, 155, 255), (255, 62, 165)], kontur=12, derinlik=16, dis=(30, 6, 70),
                      parlama=(255, 255, 255), zipla=0, don=7)
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2 - 6)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    return kat, ImageChops.lighter(engel, ym)


def vs_08(merkez, r=100):
    """REF-059 kapak VS (olculdu 18-GLOWMOTION-PVP10-KAPAK-OLCUM.md): yesil-limon tombul baloncuk VS, arkasinda sari simsek + yesil
    kabarciklar + beyaz parilti, altinda turuncu-sari "N MINS" rozeti (bizde 5 MINS: video 5 dk).
    Kullanici (24 Eki, deneme 2): "VS birazcik daha alimli olsun ... arka plana da bir seyler koyabilirsin" + "8 MINS gorseli gayet
    iyi, buna uydurursan" -> VS arkasinda isinli cizgi-roman patlamasi + yesil yorunge halkalari + bol parilti; rozet REF-059'daki
    gibi dev degrade rakam + yaninda kucuk MINS, egik, kalin koyu kontur."""
    k = Image.new("RGBA", (int(r * 4.2), int(r * 4.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2 - r * 0.35)
    import random as _r
    rr_ = _r.Random(8)
    # 1) arka isinlar: merkezden disa acilan pembe-sari dilimler (yari saydam)
    isin = Image.new("RGBA", k.size); di = ImageDraw.Draw(isin)
    for i in range(16):
        an = i / 16 * 2 * math.pi; da = 0.11
        L = r * 2.0
        di.polygon([c, (c[0] + math.cos(an - da) * L, c[1] + math.sin(an - da) * L * 0.8),
                    (c[0] + math.cos(an + da) * L, c[1] + math.sin(an + da) * L * 0.8)],
                   fill=((255, 240, 120, 150) if i % 2 else (255, 90, 200, 130)))
    k.alpha_composite(isin.filter(ImageFilter.GaussianBlur(3)))
    # 2) cizgi-roman patlamasi: beyaz dis + sari ic dikenli yildiz
    for olc, renk in ((1.28, (255, 255, 255)), (1.12, (255, 214, 40)), (0.92, (255, 150, 30))):
        pts = []
        for i in range(36):
            uz = r * olc * (1.0 if i % 2 == 0 else 0.74) * (1 + 0.08 * rr_.random())
            an = i * math.pi / 18
            pts.append((c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.82))
        d.polygon(pts, fill=renk)
    # 3) sari simsek (iki yana tasar)
    sm = [(c[0] + 56, c[1] - r * 1.45), (c[0] - 64, c[1] + 10), (c[0] + 4, c[1] + 6), (c[0] - 56, c[1] + r * 1.35),
          (c[0] + 82, c[1] - 24), (c[0] + 12, c[1] - 20)]
    d.polygon(sm, fill=(255, 245, 90), outline=(255, 255, 255), width=5)
    # 4) yesil yorunge halkalari (REF-059 VS'nin cevresindeki yesil kivrimlar)
    for (en, boy, ac0, ac1, kal) in ((2.5, 0.9, 200, 350, 9), (2.2, 0.7, 20, 170, 7)):
        bb = (c[0] - r * en / 2 * 1.0, c[1] - r * boy / 2, c[0] + r * en / 2, c[1] + r * boy / 2)
        d.arc(bb, ac0, ac1, fill=(40, 150, 30), width=kal + 6)
        d.arc(bb, ac0, ac1, fill=(150, 255, 70), width=kal)
    # 5) yesil kabarciklar + 4 koseli beyaz parilti
    for _ in range(14):
        an = rr_.uniform(0, 2 * math.pi); uz = r * rr_.uniform(1.15, 1.75); q = rr_.uniform(6, 16)
        x, y = c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.72
        d.ellipse((x - q, y - q, x + q, y + q), fill=(110, 225, 50), outline=(235, 255, 200), width=2)
        d.ellipse((x - q * 0.5, y - q * 0.6, x - q * 0.05, y - q * 0.2), fill=(240, 255, 230))
    for (px, py, rr) in ((c[0] - r * 1.35, c[1] - r * 0.55, 30), (c[0] + r * 1.35, c[1] + r * 0.3, 24), (c[0] + r * 0.95, c[1] - r * 1.05, 18),
                         (c[0] - r * 0.9, c[1] + r * 0.85, 16), (c[0] + r * 0.2, c[1] - r * 1.35, 12)):
        d.polygon([(px, py - rr), (px + rr * 0.22, py - rr * 0.22), (px + rr, py), (px + rr * 0.22, py + rr * 0.22), (px, py + rr),
                   (px - rr * 0.22, py + rr * 0.22), (px - rr, py), (px - rr * 0.22, py - rr * 0.22)], fill=(255, 255, 255))
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(18))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (255, 230, 120)] + [g.point(lambda v: int(v * 0.6))])
    dolu = k.getchannel("A")
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    yz2 = baloncuk_kelime("VS", 165, [(240, 255, 80), (120, 235, 40), (30, 160, 40)], kontur_renk=(15, 70, 20), isilti=(230, 255, 200))
    tx, ty = int(merkez[0] - yz2.width / 2), int(oy + c[1] - yz2.height / 2)
    kat.alpha_composite(yz2, (tx, ty))
    # rozet: dev degrade rakam + kucuk MINS (REF-059 "8 MINS" stili), hafif egik
    sayi = baloncuk_kelime("5", 132, [(255, 245, 90), (255, 160, 30), (255, 60, 40)], kontur_renk=(120, 10, 70), isilti=(255, 235, 200))
    yazi = baloncuk_kelime("MINS", 74, [(255, 245, 90), (255, 160, 30), (255, 60, 40)], kontur_renk=(120, 10, 70), isilti=(255, 235, 200))
    kirp = lambda im_: im_.crop(im_.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox())
    sayi = kirp(sayi); yazi = kirp(yazi)   # deneme 2: bos kenarlar 5 ile MINS'i ayirdi
    rz = Image.new("RGBA", (sayi.width + yazi.width - 6, sayi.height))
    rz.alpha_composite(sayi, (0, 0)); rz.alpha_composite(yazi, (sayi.width - 6, rz.height - yazi.height - 6))
    rz = rz.rotate(6, resample=Image.BICUBIC, expand=True)
    rx, ry = int(merkez[0] - rz.width / 2), ty + yz2.height - 30
    kat.alpha_composite(rz, (rx, ry))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    ym.paste(255, (rx, ry), rz.getchannel("A").point(lambda v: 255 if v > 120 else 0))
    return kat, ImageChops.lighter(engel, ym)


def vs(merkez, r=150):
    """deneme 3: VS buyuk ve en onde (kullanici: "VS yazisini biraz daha buyutelim ... ön planda olsun"),
    atesli: altin-turuncu alev patlamasi + kivilcimlar + camgobegi simsekler (referanstaki kirmizi atesin bizim tonu)"""
    k = Image.new("RGBA", (int(r * 3.4), int(r * 3.4))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    import random as _r
    rr_ = _r.Random(7)
    # alev patlamasi: iki kat dikenli yildiz (dis turuncu, ic altin)
    for kat, (renk, olc) in enumerate((((255, 110, 20), 1.0), ((255, 200, 40), 0.78), ((255, 245, 170), 0.5))):
        n = 22; pts = []
        for i in range(n * 2):
            uz = r * olc * (1.35 + 0.25 * rr_.random() if i % 2 == 0 else 0.8)
            an = i * math.pi / n + kat * 0.07
            pts.append((c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.82))
        d.polygon(pts, fill=renk)
    # camgobegi simsekler (iki yana)
    for s_ in (-1, 1):
        x0 = c[0] + s_ * r * 0.55
        sm = [(x0, c[1] - r * 1.25), (x0 - s_ * 26, c[1] - 10), (x0 + s_ * 6, c[1] - 6), (x0 - s_ * 22, c[1] + r * 1.2),
              (x0 + s_ * 34, c[1] + 18), (x0 + s_ * 4, c[1] + 14)]
        d.polygon(sm, fill=SIMSEK, outline=(255, 255, 255), width=4)
    # kivilcimlar
    for _ in range(46):
        an = rr_.uniform(0, 2 * math.pi); uz = r * rr_.uniform(1.15, 1.6); ln = rr_.uniform(8, 22)
        x, y = c[0] + math.cos(an) * uz, c[1] + math.sin(an) * uz * 0.85
        d.line([(x, y), (x + math.cos(an) * ln, y + math.sin(an) * ln * 0.85)], fill=rr_.choice([(255, 230, 120), (255, 160, 40), (255, 255, 255)]), width=3)
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(18))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (255, 170, 60)] + [g.point(lambda v: int(v * 0.8))])
    dolu = k.getchannel("A")                                      # isiltisiz dolu alan (carpisma maskesi)
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    # VS harfi: kirmizi -> turuncu sicak gecis, beyaz kontur, koyu derinlik
    yz2 = parlak_yazi("VS", yfont(200), [(255, 60, 40), (255, 150, 20)], kontur=12, derinlik=16, dis=(90, 10, 30),
                      parlama=(255, 200, 80), zipla=0, don=7)
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2 - 6)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    engel = ImageChops.lighter(engel, ym)
    return kat, engel


def vs_09(merkez, r=100):
    """REF-060 kapak VS (olculdu 19-GLOWMOTION-3P-BATTLE-3-KAPAK-OLCUM.md): tombul baloncuk VS, arkasinda sari simsek, cevrede sari
    kisa patlama cizgileri ve beyaz 4 koseli parilti. 2 oyuncu, mor ortak: harf yukaridan asagi pembe -> mor -> mavi. Rozet yok."""
    k = Image.new("RGBA", (int(r * 3.6), int(r * 3.6))); d = ImageDraw.Draw(k); c = (k.width / 2, k.height / 2)
    sm = [(c[0] + 50, c[1] - r * 1.40), (c[0] - 62, c[1] + 10), (c[0] + 4, c[1] + 6), (c[0] - 50, c[1] + r * 1.40),
          (c[0] + 78, c[1] - 22), (c[0] + 10, c[1] - 18)]
    d.polygon(sm, fill=(255, 222, 50), outline=(255, 250, 200), width=5)
    for i in range(10):                                            # sari patlama cizgileri (REF-060 VS cevresi)
        an = -0.3 + i * 0.63; r0, r1 = r * 1.15, r * 1.45
        d.line([(c[0] + math.cos(an) * r0, c[1] + math.sin(an) * r0 * 0.8), (c[0] + math.cos(an) * r1, c[1] + math.sin(an) * r1 * 0.8)],
               fill=(255, 220, 60), width=7)
    for (px, py, rr) in ((c[0] - r * 1.1, c[1] - r * 0.8, 24), (c[0] + r * 1.05, c[1] + r * 0.75, 20), (c[0] + r * 0.95, c[1] - r * 1.0, 14)):
        d.polygon([(px, py - rr), (px + rr * 0.22, py - rr * 0.22), (px + rr, py), (px + rr * 0.22, py + rr * 0.22), (px, py + rr),
                   (px - rr * 0.22, py + rr * 0.22), (px - rr, py), (px - rr * 0.22, py - rr * 0.22)], fill=(255, 255, 255))
    g = k.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16))
    gl = Image.merge("RGBA", [Image.new("L", k.size, c_) for c_ in (255, 230, 140)] + [g.point(lambda v: int(v * 0.5))])
    dolu = k.getchannel("A")
    gl.alpha_composite(k); k = gl
    kat = Image.new("RGBA", (W, H)); ox, oy = int(merkez[0] - k.width / 2), int(merkez[1] - k.height / 2)
    kat.alpha_composite(k, (ox, oy))
    engel = Image.new("L", (W, H)); engel.paste(dolu.point(lambda v: 255 if v > 60 else 0), (ox, oy))
    yz2 = baloncuk_kelime("VS", 150, [(255, 90, 200), (175, 90, 255), (60, 150, 255)], kontur_renk=(60, 20, 120), isilti=(255, 225, 250))
    tx, ty = int(merkez[0] - yz2.width / 2), int(merkez[1] - yz2.height / 2)
    kat.alpha_composite(yz2, (tx, ty))
    ym = Image.new("L", (W, H)); ym.paste(yz2.getchannel("A").point(lambda v: 255 if v > 120 else 0), (tx, ty))
    return kat, ImageChops.lighter(engel, ym)


PARLAK_BANT = 150
SIMSEK = (255, 225, 60) if T4 else (110, 250, 255)   # REF-055 VS: sari simsek
# ---------------------------------------------------------------- baslik harfleri (kapak-tetris.py ile ayni yontem)
def parlak_yazi(metin, f, renkler, kontur=9, derinlik=12, dis=(30, 0, 70), parlama=(255, 80, 220),
                zipla=6, don=4, aralik=4):
    d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
    asc, desc = f.getmetrics(); hh = asc + desc
    pad = derinlik + kontur + 40
    gen = int(sum(d0.textlength(c, font=f) for c in metin) + aralik * len(metin)) + 2 * pad
    tuval = Image.new("RGBA", (gen, hh + 2 * pad + zipla * 2))
    x = pad
    for i, c in enumerate(metin):
        cw = d0.textlength(c, font=f)
        if c == " ":
            x += cw + aralik; continue
        hm = Image.new("L", (int(cw) + 2 * pad, hh + 2 * pad)); ImageDraw.Draw(hm).text((pad, pad), c, font=f, fill=255)
        km = Image.new("L", hm.size); ImageDraw.Draw(km).text((pad, pad), c, font=f, fill=255, stroke_width=kontur, stroke_fill=255)
        L = Image.new("RGBA", hm.size)
        dm = km.filter(ImageFilter.MaxFilter(9))
        for k_ in range(derinlik, -1, -2):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(dm); L.alpha_composite(sh, (k_ // 2, k_))
        for k_ in range(derinlik, 0, -1):
            sh = Image.new("RGBA", hm.size, dis + (0,)); sh.putalpha(km); L.alpha_composite(sh, (k_ // 2, k_))
        bk = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bk.putalpha(km); L.alpha_composite(bk)
        r, g, b = renkler[i % len(renkler)]
        grad = Image.new("RGBA", hm.size); gd = ImageDraw.Draw(grad)
        for yy in range(hm.size[1]):
            q = min(1, max(0, (yy - pad) / max(1, asc)))
            if q < 0.45:
                m_ = 0.20 * (1 - q / 0.45); cc = (r + (255 - r) * m_, g + (255 - g) * m_, b + (255 - b) * m_)
            else:
                m_ = 0.35 * (q - 0.45) / 0.55; cc = (r * (1 - m_), g * (1 - m_), b * (1 - m_))
            gd.line([(0, yy), (hm.size[0], yy)], fill=tuple(int(v) for v in cc) + (255,))
        grad.putalpha(hm); L.alpha_composite(grad)
        band = Image.new("L", hm.size, 0); ImageDraw.Draw(band).ellipse((pad - cw * 0.2, pad - hh * 0.3, pad + cw * 1.2, pad + asc * 0.34), fill=PARLAK_BANT)
        band = Image.composite(band, Image.new("L", hm.size, 0), hm).filter(ImageFilter.GaussianBlur(2))
        bw_ = Image.new("RGBA", hm.size, (255, 255, 255, 0)); bw_.putalpha(band); L.alpha_composite(bw_)
        aci = don * (1 if i % 2 == 0 else -1) * (0.6 + 0.4 * ((i * 37) % 5) / 4)
        L = L.rotate(aci, Image.BICUBIC, expand=False)
        dy = int(zipla * math.sin(i * 1.9))
        tuval.alpha_composite(L, (int(x - pad), zipla + dy))
        x += cw + aralik
    tuval = tuval.crop(tuval.getchannel("A").getbbox())
    if parlama:
        e = 40
        big = Image.new("RGBA", (tuval.width + 2 * e, tuval.height + 2 * e)); big.alpha_composite(tuval, (e, e))
        g = big.getchannel("A").filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(18))
        gl = Image.merge("RGBA", [Image.new("L", big.size, c) for c in parlama] + [g.point(lambda v: min(255, int(v * 1.3)))])
        gl.alpha_composite(big); tuval = gl
    return tuval


# ---------------------------------------------------------------- 6. video: REF-057 BALONCUK BASLIK
# Kullanici 21 Eki 2026: "Referanstaki human Tetris yazisi baloncuklu ... baloncuk yapida yazilmis gibi". REF-057 kapak basligi
# yakindan (kapak-taslak/06/ref-baslik.png): cok yuvarlak tombul harfler, harfler birbirine degip tek govde olur; DIKEY renk gecisi
# (HUMAN ust mavi -> alt turkuaz-mint, TETRIS pembe -> turuncu -> sari); her harfin ustunde beyaz oval cam yansimasi; ice ince beyaz
# cizgi, disa kalin lacivert-mor kontur, en disa acik isilti. Font Fredoka Bold (OFL, fontlar/OFL-fredoka.txt).
def baloncuk_kelime(metin, boy, renkler, kontur_renk=(52, 22, 140), isilti=(235, 215, 255), aralik=-0.03):
    # deneme 1: govdeyi bulaniklastirip esiklemek harfleri eritti (R/S okunmadi), MaxFilter kontur koseli kutu oldu ->
    # kontur yazi tipinin kendi yuvarlak stroke'uyla; once butun harflerin dis konturu, sonra beyaz cizgi, sonra dolgu
    # (harfler birbirine degdiginde konturlar birlesir, ic bosluklar korunur)
    f = ImageFont.truetype(os.path.join(KOK, "05-kapak", "fontlar", "Fredoka.ttf"), boy)
    f.set_variation_by_name("Bold")
    d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
    DK, BK = int(boy * 0.13), int(boy * 0.045)                    # dis kontur, beyaz ic cizgi
    pad = DK + 30
    xs = []; x = pad
    for c in metin:
        xs.append(x); x += d0.textlength(c, font=f) + boy * aralik
    S = (int(x + pad), int(boy * 1.25) + 2 * pad)
    def maske(stroke):
        m = Image.new("L", S); dm = ImageDraw.Draw(m)
        for c, x_ in zip(metin, xs):
            dm.text((x_, pad), c, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        return m
    KAL = int(boy * 0.018)                                       # harfi tombullastir (REF daha kalin)
    dis, beyaz, govde = maske(DK + KAL), maske(BK + KAL), maske(KAL)
    out = Image.new("RGBA", (S[0] + 80, S[1] + 80)); o = (40, 40)
    def kat(m, renk, alfa=1.0):
        out.alpha_composite(Image.merge("RGBA", [Image.new("L", S, c) for c in renk] + [m.point(lambda v: int(v * alfa))]), o)
    big = Image.new("L", out.size); big.paste(dis, o)
    gl = big.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14))
    out.alpha_composite(Image.merge("RGBA", [Image.new("L", out.size, c) for c in isilti] + [gl.point(lambda v: min(255, int(v * 1.2)))]))
    kat(dis, kontur_renk)
    kat(beyaz, (255, 255, 255))
    bb = govde.getbbox(); y0, y1 = bb[1], bb[3]
    grad = Image.new("RGB", S); gd = ImageDraw.Draw(grad)
    for yy in range(S[1]):
        q = min(1, max(0, (yy - y0) / max(1, y1 - y0)))
        n = len(renkler) - 1; i = min(n - 1, int(q * n)); t = q * n - i
        gd.line([(0, yy), (S[0], yy)], fill=tuple(int(renkler[i][j] + (renkler[i + 1][j] - renkler[i][j]) * t) for j in range(3)))
    out.alpha_composite(Image.merge("RGBA", (*grad.split(), govde)), o)
    # alt kenarda hafif koyulasma (tombul hacim)
    alt = ImageChops.subtract(govde, ImageChops.offset(govde, 0, -int(boy * 0.05))).filter(ImageFilter.GaussianBlur(3))
    kat(alt, tuple(int(c * 0.6) for c in renkler[-1]), 0.5)
    # cam yansimasi: her harfin ust kisminda tek beyaz oval (harf govdesi icinde kirpilir)
    ym = Image.new("L", S); dy = ImageDraw.Draw(ym)
    for c, x_ in zip(metin, xs):
        b_ = f.getbbox(c); a0, b0, a1, b1 = x_ + b_[0], pad + b_[1], x_ + b_[2], pad + b_[3]
        w_, h_ = a1 - a0, b1 - b0
        dy.ellipse((a0 + w_ * 0.12, b0 + h_ * 0.07, a0 + w_ * 0.50, b0 + h_ * 0.24), fill=230)
    ym = ImageChops.multiply(ym.filter(ImageFilter.GaussianBlur(2)), govde.filter(ImageFilter.MinFilter(7)))
    kat(ym, (255, 255, 255), 0.85)
    return out.crop(out.getchannel("A").getbbox())


def baloncuk_baslik(w1, w2, yuk=170):
    k1 = baloncuk_kelime(w1, yuk, [(25, 85, 255), (15, 190, 255), (55, 255, 185)])
    k2 = baloncuk_kelime(w2, yuk, [(255, 35, 205), (255, 105, 95), (255, 238, 35)], kontur_renk=(110, 20, 120), isilti=(255, 210, 245))
    ara = 6
    t = Image.new("RGBA", (k1.width + k2.width + ara, max(k1.height, k2.height)))
    t.alpha_composite(k1, (0, (t.height - k1.height) // 2)); t.alpha_composite(k2, (k1.width + ara, (t.height - k2.height) // 2))
    return t


def gecis(n, c0, c1):          # kelime ici soldan saga renk gecisi (referanstaki gibi kelime basina tek degrade)
    return [tuple(int(c0[j] + (c1[j] - c0[j]) * (i / max(1, n - 1))) for j in range(3)) for i in range(n)]
w1, w2 = a.baslik.split(" ", 1)
renk = (gecis(len(w1), (150, 70, 255), (255, 110, 235)) + [(255, 255, 255)] + gecis(len(w2), (255, 250, 70), (190, 255, 40)) if T3 else
        gecis(len(w1), (40, 230, 230), (150, 255, 40)) + [(255, 255, 255)] + gecis(len(w2), (255, 225, 40), (255, 100, 20)))
if T6:
    # REF-057 basligi: HUMAN maviden yesil-turkuaza, TETRIS pembeden sariya (kelime ici degrade), duz harf (kullanici 19 Eki karari)
    yz = baloncuk_baslik(w1, w2)        # kullanici 21 Eki 2026: referanstaki gibi baloncuk harf
elif T4:
    # 4. video: 3. videodaki kullanici karari (19 Eki 2026, "harfler asagida veya yukarida olmasin, normal duz") burada da;
    # REF-055 basligi kelime ici degrade -> TETRIS yakut->turuncu, MODE safir->acik mavi (videonun P1/P2 renkleri)
    renk = gecis(len(w1), (255, 45, 85), (255, 140, 60)) + [(255, 255, 255)] + gecis(len(w2), (47, 84, 255), (110, 190, 255))
    yz = parlak_yazi(a.baslik, yfont(160), renk, kontur=10, derinlik=15, dis=(40, 8, 60), parlama=(255, 190, 140), zipla=0, don=0)
elif T3:
    # kullanici 19 Eki 2026: "ayni yazi fontunda kalsin ama harfler asagida veya yukarida olmasin, normal duz olsun ... sigsin,
    # okunacak, dikkat cekecek" -> Titan One kalir; ziplama/donme 0, tek satir tam genislik, renkler video ile uyumlu
    renk = [(178, 92, 255)] * len(w1) + [(255, 255, 255)] + [(245, 255, 61)] * len(w2)
    yz = parlak_yazi(a.baslik, yfont(160), renk, kontur=10, derinlik=15, dis=(45, 8, 95), parlama=(200, 120, 255), zipla=0, don=0)
else:
    yz = parlak_yazi(a.baslik, yfont(160), renk, kontur=10, derinlik=15, dis=(20, 10, 60), parlama=(255, 236, 150), zipla=7, don=4)
if yz.width > 1240:
    yz = yz.resize((1240, int(yz.height * 1240 / yz.width)), Image.LANCZOS)
by = int(96 - yz.height / 2)
baslik_alt = by + int(yz.getchannel("A").point(lambda v: 255 if v > 200 else 0).getbbox()[3])
vs_kat, vs_engel = ((lambda m: vs_09((m[0], m[1] + 40), r=105)) if T9 else (lambda m: vs_08((m[0], m[1] + 70), r=125)) if T8 else vs_06 if T6 else vs_jole if T3 else vs)((640, 455))
m1 = yerlestir(a.p1, a.ayna1, 310, a.boy1, a.gen1, vs_engel, -1, baslik_alt + 4)
m2 = yerlestir(a.p2, a.ayna2, 970, a.boy2, a.gen2, vs_engel, +1, baslik_alt + 4)
print("siluet kutulari:", m1.getbbox(), m2.getbbox(), "baslik alti", baslik_alt)
siluetleri_ciz([m1, m2])                                      # 1) siluetler
im.alpha_composite(yz, (int(W / 2 - yz.width / 2), by))       # 2) baslik
im.alpha_composite(vs_kat)                                    # 3) VS en onde, siluete degmez
im.convert("RGB").save(a.cikti, quality=93)
print(a.cikti, os.path.getsize(a.cikti) // 1024, "KB")
