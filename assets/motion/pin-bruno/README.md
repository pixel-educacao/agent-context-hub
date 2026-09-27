# Pin do Bruno

Vídeo em loop para o pin com tela redonda que o Bruno usa nas palestras. Logo Pixel AI Hub em cima, QR no centro exato e o robozinho embaixo. O QR e o logo ficam parados; só o robô se mexe.

| Arquivo | O que é |
|---|---|
| `pin-bruno.mp4` | 1080×1080, 30 fps, 8 s, sem áudio. Loop sem emenda (o último quadro volta para o primeiro). QR para `https://aihub.pixeleducacao.com.br`. |
| `index.html` | Versão ao vivo. Tem campo para trocar o link do QR e botão para ver quadrado ou recortado como pin. |
| `render.mjs` | Gera um MP4 novo com outro link no QR. |

## Composição

Tudo cabe dentro de um círculo de raio 475 px centrado no quadrado de 1080, então o pin pode cortar as bordas sem pegar em nada. O fundo `#05060F` preenche o quadrado inteiro, para não aparecer borda se o recorte do aparelho for um pouco diferente.

- **QR:** 360 px centrado em (540, 540), módulos `#05060F` sobre placa off-white `#F2F1ED`, correção de erro M. Confirmado que decodifica a partir do vídeo, inclusive com o quadro reduzido a 300 px.
- **Logo:** arquivo oficial `pixel ai hub logo white.png` do site do AI Hub.
- **Robô:** desenhado em SVG com as cores da marca (casco off-white, visor escuro, olhos em laranja claro `#FFB08F`, orelhas e antena em `#FF5100`).

## Roteiro do loop (8 s)

| Tempo | Robô |
|---|---|
| 0 a 2,3 s | digita, olhando o painel de código |
| 2,7 a 3,9 s | olha para cima, para o QR (pisca em 3,3 s) |
| 4,25 a 5,3 s | ergue a cabeça até o logo e sorri (^^) |
| 5,7 a 8 s | volta a digitar (pisca em 6,8 s) |

A antena e a luz do peito pulsam a cada 1 s e o corpo respira a cada 2 s. Todos os ciclos dividem 8 s, por isso o loop fecha.

## Gerar para outra palestra

```bash
npm i -D playwright qrcode-generator
node render.mjs "https://link-da-palestra" pin-palestra-x.mp4
```

Variáveis opcionais: `FFMPEG` (caminho do ffmpeg) e `CHROMIUM` (caminho de um Chromium já instalado). Links curtos geram QR com módulos maiores, que leem melhor de longe.
