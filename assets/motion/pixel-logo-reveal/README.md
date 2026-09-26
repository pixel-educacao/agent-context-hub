# Pixel logo reveal

Animação de 6 s do logo da Pixel se formando: uma bolinha nasce no centro e se divide em quatro gerações (1, 4, 4, 4 e 8) até fechar as 21 do símbolo, o símbolo desliza para a esquerda, "pixel" entra letra por letra e o pingo do i cai por último.

| Arquivo | O que é |
|---|---|
| `index.html` | Animação ao vivo (SVG + Web Audio). Abra no navegador e clique em **Tocar**. |
| `pixel-logo-reveal-light.mp4` | Vídeo 1920×1080, 30 fps, com som, fundo off-white `#F2F1ED`. |
| `pixel-logo-reveal-dark.mp4` | Mesmo vídeo com fundo profundo `#05060F`. |
| `render.mjs` | Gera os MP4 a partir do `index.html`. |

## Fonte dos elementos

- Logo: SVG oficial de `aihub.pixeleducacao.com.br/assets/logos/logo-horizontal-dark.svg`. O símbolo foi separado nas 21 formas originais; nenhuma foi redesenhada.
- Cor `#FF5100`, fundos e ritmo (pulso 1 → 1,045 → 1, flash que sobe em 0,16 s e cai em 0,75 s) seguem o sistema de motion da marca.
- Sons sintetizados no próprio navegador: estalo de bolha por bolinha (a nota sobe a cada geração, escala pentatônica), brilho no fechamento, whoosh no deslize, marimba nas letras, queda e quique do pingo e um acorde final.

## Roteiro

| Tempo | Evento |
|---|---|
| 0,30 s | primeira bolinha nasce |
| 0,95 / 1,40 / 1,80 / 2,15 s | divisões: ×4, ×4, ×4, ×8 |
| 2,95 s | símbolo completo: pulso + flash |
| 3,20 s | símbolo desliza para a posição do lockup |
| 3,55 a 4,40 s | p, i, x, e, l |
| 4,45 s | pingo do i pousa, acorde final |
| até 6,00 s | logo parado |

## Regerar os vídeos

```bash
npm i -D playwright            # ou use um playwright global
node render.mjs light
node render.mjs dark
```

Variáveis opcionais: `FFMPEG` (caminho do ffmpeg) e `CHROMIUM` (caminho de um Chromium já instalado).
