// sahne13-kur.py: kartCiz icindeki parcalar (ESKI -> YENI, birebir metin degisimi)
//== ESKI
  } else if (kart.tip === 'yazi') {
    // mavi ışınlı zemin + pembe neon yazı (REF-057 açılış/geçiş kartları; metinler bizim)
    isinPatlamasi(t, TEMA.acilisZemin[0], TEMA.acilisZemin[1]);
    kivilcim(t, u);
    const satir = kart.alt ? [kart.metin, kart.alt] : [kart.metin];
    satir.forEach((m, j) => {
      const g = ease(kisit((u - j * 0.18) / 0.35, 0, 1)), zip = 1 + 0.18 * Math.sin(Math.min(1, g) * Math.PI);
      const px = (kart.px || (m.length > 14 ? 150 : 190)) * k * zip;
      yazi(m, W / 2, H * (satir.length > 1 ? 0.40 + j * 0.22 : 0.5), px, TEMA.acilisYazi, TEMA.acilisKontur, g, TEMA.acilisIsilti);
    });
//== YENI
  } else if (kart.tip === 'yazi') {
    // REF-067: mor izgara zemin + piksel yazi (pastel degrade, beyaz kontur, pembe golge); metinler bizim
    izgaraZemin(t);
    const satir = kart.alt ? [kart.metin, kart.alt] : [kart.metin];
    const RENKLER = [['#ffffff', '#ffd6f2', '#ff9ae0'], ['#ffffff', '#d6f6ff', '#7ad8ff'], ['#ffffff', '#fff6c0', '#ffd94a']];
    satir.forEach((m, j) => {
      const g = ease(kisit((u - j * 0.18) / 0.3, 0, 1)), zip = 1 + 0.15 * Math.sin(Math.min(1, g) * Math.PI);
      const px = (kart.px || (m.length > 13 ? 120 : 150)) * k * zip;
      pikselYazi(m, W / 2 + Math.sin(u * 5 + j) * 6 * k, H * (satir.length > 1 ? 0.40 + j * 0.2 : 0.5), px, RENKLER[(j + Math.round(kart.t)) % 3], g);
    });
//== ESKI
    const metin = ['3', '2', '1', 'GO!'][adim];
    const s2 = 1.35 - 0.35 * ease(Math.min(1, q / 0.3)), a2 = Math.min(1, (1 - q) / 0.25);
    cx.globalAlpha = a * a2;
    const renk = adim === 3 ? ['#ffffff', TEMA.p1acik, P1, TEMA.p1koyu] : ['#ffffff', ALTIN, '#ff7a00'];
    yazi(metin, W / 2, H * 0.47, (adim === 3 ? 300 : 340) * k * s2, renk, '#2a0a46', 1, adim === 3 ? P1 : ALTIN);
    if (adim === 0 && q < 0.6) yazi('GET READY!', W / 2, H * 0.2, 110 * k, '#ffffff', '#06122e', 1 - q / 0.6);
//== YENI
    // REF-067: 3-2-1-GO! tam ekran mor izgara kartinda, beyaz kalin rakam pembe isiltili
    const metin = ['3', '2', '1', 'GO!'][adim];
    const s2 = 1.35 - 0.35 * ease(Math.min(1, q / 0.3));
    izgaraZemin(t);
    if (adim < 3) yazi(metin, W / 2, H * 0.5, 380 * k * s2, ['#ffffff', '#fff0fa', '#ffd6f2'], '#c0168a', 1, '#ff7ad0');
    else pikselYazi('GO!', W / 2, H * 0.5, 300 * k * s2, ['#ffffff', '#ffd6f2', '#ff7ad0'], 1);
//== ESKI
  } else if (kart.tip === 'tur') {
    isinPatlamasi(t, TEMA.isin[0], TEMA.isin[1]);
    yazi(kart.metin, W / 2, H * (kart.alt ? 0.40 : 0.5), 200 * k * s, ['#ffffff', '#fff1a8', ALTIN], '#06122e', 1, ALTIN);
    if (kart.alt) yazi(kart.alt, W / 2, H * 0.62, 150 * k * s, ['#ffffff', TEMA.p1acik, P1], '#06122e', 1, P1);
//== YENI
  } else if (kart.tip === 'tur') {
    // REF-067: "ROUND 2" piksel + altinda zorluk adi (MEDIUM sari, HARD kirmizi) kalin kabarik yazi
    izgaraZemin(t);
    pikselYazi(kart.metin, W / 2, H * 0.36, 120 * k * s, ['#ffffff', '#ffd6f2', '#ff9ae0']);
    const zr = { EASY: ['#e6ffd6', '#7aea4a', '#2a9a10'], MEDIUM: ['#fffbd0', '#ffe23a', '#e8a000'], HARD: ['#ffe0e0', '#ff4a4a', '#b00018'] }[kart.alt] || ['#ffffff', ALTIN, '#e8a000'];
    if (kart.alt) yazi(kart.alt, W / 2, H * 0.6, 230 * k * s * (1 + 0.04 * Math.sin(u * 9)), zr, '#3a0a2a', 1, zr[1]);
//== ESKI
  } else if (kart.tip === 'abone') {
    isinPatlamasi(t, TEMA.isin[0], TEMA.isin[1]);
//== YENI
  } else if (kart.tip === 'abone') {
    izgaraZemin(t);
    maskotCiz(W * 0.2, H * 0.5 + Math.sin(u * 4) * 14 * k, 2.2, t);
