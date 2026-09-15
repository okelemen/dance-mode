"""Bir fotografi MOTORDA KULLANILABILIR dokuya cevirir.

   python foto-hazirla.py <girdi> <cikti.png> [--esik 0.14] [--zemin koyu|acik] [--boy 1024]

13 Eylul 2026 kullanici karari: bundan sonraki videolarda mekan nesneleri
gercek fotograflardan kurulacak. Bu betik o boru hattinin ilk adimi.

ADIMLAR ve NEDENLERI (hepsi bir kez hata yapilarak bulundu):

1. ARKA PLANI KES. Duz zeminde parlaklik esigi yetiyor. Ama esik TEK BASINA
   kenarda tirtik birakir; maske once kapatilip aciliyor, en buyuk baglantili
   parca aliniyor (sagda solda kalan lekeler gitsin), sonra ici dolduruluyor.

2. KENARI YUMUSAT. Alfa tek pikselde 0'dan 255'e kirilirsa acik gokyuzunde
   testere disi gorunur. Hafif bulaniklik gecisi yumusatir.

3. RENK TASMASI (en cok atlanan adim). Saydam piksellerin RGB'si komsu opak
   renkle dolduruluyor. Yapilmazsa GPU kenarda saydam pikselin (cogu zaman
   siyah) rengini karistirir ve nesnenin etrafinda KOYU HALE cikar; kesim
   dogru olsa bile "yapistirilmis" gorunur.

4. KIRP + PAY. Nesnenin kutusuna kirpilip %6 pay birakiliyor.

5. KARE + IKININ USSU. 1024x1024. Ikinin ussu olmayan doku mipmap uretemiyor
   ve uzaktaki ornekler titriyor - tarlada 1600 ornek varken bu goze batar.

Cikti: alfa kanalli PNG + yanina '-onizleme.png' (dama tahtasi uzerinde).

SONRAKI ADIM motorda: dokuyu billboard duzleme koy, BOY ORANINI OLC.
Olculdu (REF-008): billboard boyu kure capinin 2,35 kati alininca tarlanin
silueti yukseldi ve ufuk %38 cikti (kural %42-50); 1,78'de %45 oldu.
Fotograf sahneye girdiginde olc-mekan.py yeniden kosar.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def hazirla(girdi, cikti, esik=0.14, zemin='koyu', boy=1024, pay_oran=0.06):
    im = Image.open(girdi).convert('RGB')
    a = np.asarray(im).astype(np.float32) / 255
    print('kaynak:', im.size)

    parlak = a.max(2)
    maske = parlak > esik if zemin == 'koyu' else parlak < (1.0 - esik)

    maske = ndimage.binary_closing(maske, np.ones((9, 9)))
    maske = ndimage.binary_opening(maske, np.ones((5, 5)))
    et, n = ndimage.label(maske)
    if n > 1:
        boylar = ndimage.sum(maske, et, range(1, n + 1))
        maske = et == (int(np.argmax(boylar)) + 1)
        print('  %d parca bulundu, en buyugu alindi' % n)
    maske = ndimage.binary_fill_holes(maske)
    print('  maske doluluk: %%%.1f' % (maske.mean() * 100))
    if maske.mean() < 0.01:
        raise SystemExit('HATA: maske bos - esik yanlis ya da zemin duz degil')

    alfa = Image.fromarray((maske * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(1.2))

    ys, xs = np.where(maske)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    pay = int(max(x1 - x0, y1 - y0) * pay_oran)
    y0 = max(0, y0 - pay); x0 = max(0, x0 - pay)
    y1 = min(maske.shape[0] - 1, y1 + pay); x1 = min(maske.shape[1] - 1, x1 + pay)

    rgba = np.dstack([np.asarray(im), np.asarray(alfa)])[y0:y1, x0:x1]

    op = rgba[:, :, 3] > 8
    if (~op).any():
        ind = ndimage.distance_transform_edt(~op, return_distances=False,
                                             return_indices=True)
        for k in range(3):
            rgba[:, :, k] = rgba[:, :, k][tuple(ind)]

    kes = Image.fromarray(rgba)
    kw, kh = kes.size
    yan = max(kw, kh)
    tuval = Image.new('RGBA', (yan, yan), (0, 0, 0, 0))
    tuval.paste(kes, ((yan - kw) // 2, (yan - kh) // 2))
    son = tuval.resize((boy, boy), Image.LANCZOS)
    son.save(cikti)
    print('yazildi:', cikti, son.size, ' en/boy orani kaynakta %.3f' % (kw / kh))

    dama = Image.new('RGBA', (boy, boy), (210, 210, 210, 255))
    px = dama.load()
    kare = boy // 16
    for y in range(0, boy, kare):
        for x in range(0, boy, kare):
            if ((x // kare) + (y // kare)) % 2:
                for yy in range(y, min(y + kare, boy)):
                    for xx in range(x, min(x + kare, boy)):
                        px[xx, yy] = (170, 170, 170, 255)
    on = cikti.rsplit('.', 1)[0] + '-onizleme.png'
    Image.alpha_composite(dama, son).convert('RGB').save(on)
    print('yazildi:', on)
    return kw / kh


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('girdi')
    ap.add_argument('cikti')
    ap.add_argument('--esik', type=float, default=0.14,
                    help='zemin ayirma esigi (0-1)')
    ap.add_argument('--zemin', choices=['koyu', 'acik'], default='koyu',
                    help='arka plan koyu mu acik mi')
    ap.add_argument('--boy', type=int, default=1024, help='cikti kenari (ikinin ussu)')
    k = ap.parse_args()
    hazirla(k.girdi, k.cikti, k.esik, k.zemin, k.boy)
