"""
Bir parcayi hedef olcu sayisina uzatir (BPM'den bagimsiz).

muzik-bolum.py'nin genellestirilmisi: o dosya 120 BPM / 122 olculuk / mp3
kaynaga gomuluydu (OLCU_SN=2.0, ATEMPO, KAYNAK_OLCU sabitleri). Bolum-05'in
muzigi 130 BPM, 168 olcu ve wav - o yuzden ayri bir dosya.

NEDEN duz tekrar degil (gerekce muzik-bolum.py'den devraliniyor):
  Parcayi bastan sona iki kez calmak GIRIS bolumunu ikinci kez duyurur ve
  "bu tekrar" hissi verir. Giris ve cikis birer kez kullanilir, ortadaki
  GOVDE tekrarlanir; govde zaten kendi icinde dongusel oldugu icin tekrar
  fark edilmez.

Kesimler tam olcu sinirinda. 130 BPM'de bir olcu 24/13 sn; bu tam sayi
ornek etmiyor (88615,4 ornek), yani kesim noktasi en fazla yarim ornek
(~10 mikrosaniye) kayabiliyor. 120 BPM'deki tam-ornek garantisi burada yok
ama hata duyulabilir olmanin cok altinda ve BIRIKMIYOR: her kesim kaynaktaki
mutlak konumdan hesaplaniyor, oncekinin uzerine eklenmiyor.

Kullanim:
  python muzik-uzat.py <kaynak.wav> <cikti.wav> <bpm> <kaynak_olcu> <hedef_olcu>
"""
import subprocess
import sys
import os
import tempfile

GIRIS = 16
CIKIS = 16


def parcala(kaynak_olcu, hedef_olcu):
    """[(baslangic_olcu, uzunluk_olcu), ...] uretir."""
    if hedef_olcu <= kaynak_olcu:
        return [(0, hedef_olcu)]
    govde_bas = GIRIS
    govde_uz = kaynak_olcu - GIRIS - CIKIS
    cikis_bas = kaynak_olcu - CIKIS
    parcalar = [(0, GIRIS)]
    kalan = hedef_olcu - GIRIS - CIKIS
    while kalan > 0:
        al = min(govde_uz, kalan)
        parcalar.append((govde_bas, al))
        kalan -= al
    parcalar.append((cikis_bas, CIKIS))
    return parcalar


def main():
    kaynak, cikti, bpm, kaynak_olcu, hedef_olcu = sys.argv[1:6]
    bpm = float(bpm)
    kaynak_olcu = int(kaynak_olcu)
    hedef_olcu = int(hedef_olcu)
    olcu_sn = 4 * 60.0 / bpm
    parcalar = parcala(kaynak_olcu, hedef_olcu)

    gecici = tempfile.mkdtemp(prefix='muzik-')
    liste = os.path.join(gecici, 'liste.txt')
    satirlar = []
    for i, (bas, uz) in enumerate(parcalar):
        yol = os.path.join(gecici, 'p%02d.wav' % i)
        subprocess.run(['ffmpeg', '-v', 'error', '-y',
                        '-ss', '%.6f' % (bas * olcu_sn),
                        '-t', '%.6f' % (uz * olcu_sn),
                        '-i', kaynak, yol], check=True)
        satirlar.append("file '" + yol.replace(chr(92), '/') + "'")
        print('  parca %d: olcu %d..%d (%.2f sn)' % (i, bas, bas + uz, uz * olcu_sn))
    with open(liste, 'w', encoding='utf-8') as f:
        f.write(chr(10).join(satirlar) + chr(10))

    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                    '-i', liste, '-c', 'copy', cikti], check=True)
    sure = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                           'format=duration', '-of', 'csv=p=0', cikti],
                          capture_output=True, text=True).stdout.strip()
    print('cikti: %s  %s sn  (hedef %.3f)' % (cikti, sure, hedef_olcu * olcu_sn))


if __name__ == '__main__':
    main()
