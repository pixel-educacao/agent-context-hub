# Pin Instagram do Bruno

Vídeo em loop para o pin redondo: foto do Bruno com anel de story, `obrunookamoto` com selo de verificado, nome, QR para o perfil e "Siga no Instagram" com o ícone.

| Arquivo | O que é |
|---|---|
| `pin-instagram-bruno.mp4` | 1080×1080, 30 fps, 8 s, sem áudio. O anel de story gira uma volta por loop; o resto fica parado. |
| `index.html` | Fonte do vídeo (foto e fonte Manrope embutidas, funciona offline). |
| `render.mjs` | Gera o MP4. Aceita outro link: `node render.mjs "https://www.instagram.com/outro" saida.mp4`. |

- QR para `https://www.instagram.com/obrunookamoto`, módulos em gradiente roxo/rosa do Instagram sobre placa branca. Confirmado que decodifica a partir do vídeo reduzido a 360 px.
- Foto: `bruno-okamoto.webp` do site do AI Hub (800×800). A foto atual do perfil do Instagram não pôde ser baixada porque o Instagram exige login; para trocar, substitua a imagem embutida em `index.html` e rode o render de novo.
- Tudo fica dentro de um círculo de raio 475 px, como no `pin-bruno`.
