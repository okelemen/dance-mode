# 03 — Motor

Three.js render motoru. **Henüz yazılmadı.**

## Ne olacak

Node + Three.js + Puppeteer. Girdi: `../spec/sabitler.json` + bir bölüm JSON'u.
Çıktı: kare akışı → doğrudan ffmpeg'e boru → mp4.

## Kurulacaklar (proje başlayınca)

```bash
npm init -y && npm i three puppeteer
```

Puppeteer, Chromium'u kendi indirir (~300 MB).

## İlk hedef: TEK ÖLÇÜ

Tam bölüm değil. **2 saniye, loop halinde:**
bir tünel + bir hız + bir nota + bir siluet hareketi + bir combo tiki.

> Bu 2 saniye doğru hissettiriyorsa geri kalan 9 dakika sadece tekrardır.
> Yanlış hissettiriyorsa 9 dakika yapmak hiçbir şeyi kurtarmaz.

## Değişmez tasarım kuralları

- Deterministik: `t = kare_no / fps`. Duvar saati YOK, ekran kaydı YOK.
- Kareler diske yazılmaz, ffmpeg'e boru ile gider.
- Yerel çalıştırma sadece 640x360 önizleme. Tam render GitHub Actions'ta.
- Blender pipeline'da yok. FBX/GLB doğrudan Three.js'e yüklenir.

## node_modules uyarısı

Bu klasör OneDrive dışında tutuluyor, sebebi tam olarak `node_modules`.
Projeyi asla OneDrive altına taşıma.
