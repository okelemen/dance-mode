# SUNO BRIEF

> Suno sekmesi açıkken bu sayfayı yanında tut.

---

## Önce ayarlar

- [ ] **Ücretli plana geç (Pro yeterli).**
      Ücretsiz katman ticari kullanım hakkı **vermez**. Free ile üretilen müzikle
      video yayınlanırsa bütün proje boşa gider. Bu, pazarlık edilebilir bir madde değil.
- [ ] **Instrumental modu AÇIK.**
      Vokal istemiyoruz: dikkat dağıtır, ayrıca söz telifi ayrı bir baş ağrısıdır.
- [ ] **İndirme formatı: WAV.** MP3 değil.
      Üstüne zaman esnetme uygulayacağız, kayıpsız kaynak şart.
- [ ] Uzun tek parça peşinde koşma. **2-4 dakikalık parçalar** üret;
      ölçü sınırında birleştirilir, dikiş duyulmaz.

---

## Prompt

Style / açıklama alanına:

```
instrumental synthwave house, 120 BPM, four-on-the-floor kick,
driving arpeggiated bassline, neon retro-futuristic, steady groove,
consistent tempo throughout, no vocals, no tempo changes,
no ambient intro, minimal fills
```

**Sondaki üç negatif kritik.** Izgarayı bozan üç şey:
- tempo değişimi → kafes çöker
- uzun ambient giriş → ilk vuruş nerede belli olmaz
- aşırı fill → vuruş hissi kaybolur

---

## Biyom varyantları

Sadece **ilk satır** değişir, gerisi aynı kalır:

| Biyom | İlk satır |
|---|---|
| Neon Grid | `instrumental synthwave house` |
| Uzay | `instrumental deep space progressive house, wide pads` |
| Retro CRT | `instrumental 80s electro chiptune house` |
| Sıvı zemin | `instrumental liquid drum-free deep house, flowing pads` |

---

## İLK İŞ — tam bölüm üretme YOK

Önce **tek bir 2 dakikalık test parçası** üret. Neon Grid promptu. WAV indir.

`01-muzik/` klasörüne koy ve Claude'a haber ver. Ölçülecekler:

1. Gerçek BPM ne çıktı (120'ye ne kadar yakın)
2. Tempo parça boyunca sabit mi, sürükleniyor mu
3. İlk vuruş nerede başlıyor
4. Fill/breakdown ızgarayı bozacak kadar var mı

Bu ölçümlere göre prompt kalibre edilir. **Ondan sonra** 264 ölçülük tam bölüme geçilir.

Neden böyle: bir bölümlük müzik üretip sonra tempo tutmadığını görmek, hem kredi
hem zaman israfı olur. Tek parçayla kalibre etmek ucuz.

---

## Suno sonrası tempo düzeltme (Claude yapar)

Suno tam 120,000 BPM vermez, yaklaşık verir. Sen bir şey yapmayacaksın, süreç şu:

1. Gerçek BPM ölçülür
2. ffmpeg ile mikroskobik zaman esnetme uygulanır (yaklaşık %0,2 — kulakla duyulmaz)
   → tam 120,000 olur
3. İlk vuruş t=0 noktasına gelecek şekilde kırpılır
4. Düzeltilmiş dosya `-120bpm` ekiyle kaydedilir, ham dosya da saklanır

Bundan sonra ızgara matematiksel olarak kusursuz ve render tamamen deterministik.

---

## Dosya adlandırma

`01-muzik/` içine:

```
bolum-01-neon-grid-HAM.wav        <- Suno'dan indiği hali
bolum-01-neon-grid-120bpm.wav     <- düzeltilmiş, motor bunu kullanır
```

Ham dosyayı asla silme — düzeltmeyi baştan yapmak gerekirse lazım olur.
