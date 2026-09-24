"""
Bolum 11 (motor 2, tel kafes) - muzigi uzatir ve tam bolum JSON'unu uretir.

Muzik ile cagri listesi AYNI olcu haritasindan cikar: kesim noktalari ve
cue'lar ayni sayilarla hesaplandigi icin ses ve siluet kaymaz.

Parca: 01-muzik/bob-and-weave-140.wav (Suno, 140,033 BPM olculdu, ilk vurus
-0,027 sn, 139,96 sn = 81,66 olcu). Kullanici: "surekli ayni muzigi kullanacaksin",
tempo duzeltilmez.

Dizilis (olcu, parcanin kendi izgarasinda):
  gecis 0 : parca [0, 80)            - bastan, giris dahil
  gecis 1-3: parca [16, 80)  x3      - govde (16 ve 80 sekizin kati: cumle siniri)
  gecis 4 : parca [16, sona kadar]   - sarkinin kendi bitisi
  toplam = 80 + 3*64 + 65,66 = 337,66 olcu = 578,7 sn (9:38,7)

Cagrilar: vokalin yogun oldugu bolumlerde 2 olcude bir (vokal izi, 23 Eyl 2026;
whisper kurulmadi -> kelime ayirt edilemiyor, siralama sarki sozundeki gibi).

Kullanim: python bolum11-kur.py
"""
import json, os
import numpy as np
import soundfile as sf

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KAYNAK = os.path.join(KOK, '01-muzik', 'bob-and-weave-140.wav')
CIKTI_WAV = os.path.join(KOK, '01-muzik', 'bob-and-weave-140-338olcu.wav')
CIKTI_JSON = os.path.join(KOK, 'bolumler', 'bolum-11-tel-kafes.json')

BPM = 140.033
ILK_VURUS = -0.027
OLCU = 60.0 / BPM * 4
TOPLAM_OLCU = 338          # render izgarasi (tam sayi); muzik 337,66'da biter

# parcadaki cagri olculeri ve hareketleri (her hareket parca basina 5 kez)
BW, LL, JR, TJ = 'bob-and-weave', 'lateral-lunge', 'jump-reach', 'tuck-jump'
PARCA_CAGRI = [(8, BW), (20, BW), (22, BW), (24, BW), (26, LL), (44, LL), (46, LL), (48, LL),
               (50, JR), (52, JR), (54, JR), (56, JR), (58, TJ), (60, TJ), (62, TJ), (68, TJ),
               (70, BW), (72, LL), (74, JR), (76, TJ)]
KUTU_SIRA = [3, 1, 2, 4, 0, 2, 3, 1, 4, 2, 0, 3]   # art arda ayni kutu yok

y, sr = sf.read(KAYNAK, always_2d=True)
son_sn = len(y) / sr
parca_olcu_son = (son_sn - ILK_VURUS) / OLCU

# (parca_bas_olcu, parca_bit_olcu | None=sona kadar, video_bas_olcu)
GECIS = [(0, 80, 0)]
for k in range(3):
    GECIS.append((16, 80, 80 + 64 * k))
GECIS.append((16, None, 80 + 64 * 3))

def ornek(olcu):
    return int(round((ILK_VURUS + olcu * OLCU) * sr))

parcalar = []
for bas, bit, _ in GECIS:
    a = max(0, ornek(bas))
    b = len(y) if bit is None else ornek(bit)
    parcalar.append(y[a:b].copy())
# dikislerde 5 ms capraz gecis (tik olmasin); uzunluk degismesin diye
# kesim noktasi etrafinda ic ice degil, kisa ses kisma-acma
F = int(0.005 * sr)
for i in range(len(parcalar)):
    p = parcalar[i]
    if i > 0: p[:F] *= np.linspace(0, 1, F)[:, None]
    if i < len(parcalar) - 1: p[-F:] *= np.linspace(1, 0, F)[:, None]
ses = np.concatenate(parcalar)
sf.write(CIKTI_WAV, ses, sr, subtype='PCM_16')
sure = len(ses) / sr

cuelar = []
n = 0
for bas, bit, vbas in GECIS:
    ust = parca_olcu_son if bit is None else bit
    for olcu, har in PARCA_CAGRI:
        if bas <= olcu < ust:
            v = vbas + (olcu - bas)
            if v + 2 <= TOPLAM_OLCU:
                cuelar.append({'olcu': v, 'vurus': 0, 'hareket': har, 'kutu': KUTU_SIRA[n % len(KUTU_SIRA)]})
                n += 1

bolum = {
    'ad': 'Bolum 11 - TEL KAFES (motor 2)',
    'not': 'Motor 2 (sahne2.html). REF-046 tel kafes, REF-045 muzik. HAR-006 A sikki. '
           'Muzik bolum11-kur.py ile uzatildi: parca [0,80) + [16,80)x3 + [16,son]. '
           'Cagrilar vokal izinden, 2 olcude bir; sira sarki sozundeki gibi.',
    'motor': 'sahne2.html',
    'bpm': BPM,
    'ilk_vurus': ILK_VURUS,
    'toplam_olcu': TOPLAM_OLCU,
    'bolum_olcu': TOPLAM_OLCU,
    'muzik': '01-muzik/bob-and-weave-140-338olcu.wav',
    'hareketler': [BW, LL, JR, TJ],
    'cuelar': cuelar,
}
with open(CIKTI_JSON, 'w', encoding='utf-8') as f:
    json.dump(bolum, f, ensure_ascii=False, indent=1)

print(f'muzik: {sure:.3f} sn ({(sure - ILK_VURUS) / OLCU:.2f} olcu) -> {CIKTI_WAV}')
print(f'render: {TOPLAM_OLCU} olcu = {TOPLAM_OLCU * OLCU:.2f} sn')
print(f'cue: {len(cuelar)}  ilk olcu {cuelar[0]["olcu"]}  son olcu {cuelar[-1]["olcu"]}')
for h in (BW, LL, JR, TJ):
    print(f'  {h}: {sum(c["hareket"] == h for c in cuelar)}')
dilim = TOPLAM_OLCU / 5
for L in range(5):
    print(f'  LEVEL {L+1}: olcu {L*dilim:.1f} - {(L+1)*dilim:.1f}  cue {sum(L*dilim <= c["olcu"] < (L+1)*dilim for c in cuelar)}')
