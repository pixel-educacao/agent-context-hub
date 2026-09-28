# Empresa agêntica

Vídeo de 38,5 s (1920×1080, 30 fps, com som) que mostra agentes de IA operando cada área da empresa com um humano no comando.

| Arquivo | O que é |
|---|---|
| `empresa-agentica.mp4` | O vídeo final. |
| `index.html` | Fonte da animação (SVG + JavaScript, fontes embutidas, funciona offline). Abra no navegador e clique em **Tocar com som**. |
| `render.mjs` | Gera o MP4 a partir do `index.html`. |

## Roteiro

| Tempo | O que acontece |
|---|---|
| 0 a 2 s | logo Pixel laranja |
| 2 a 3,4 s | a palavra sai e a câmera aproxima do símbolo |
| 3,4 a 4,6 s | as quatro bolinhas dos cantos ganham a cor da área: Marketing, Conteúdo, Financeiro e Operações |
| 4,6 a 12 s | mergulho em Marketing |
| 12 a 19,4 s | mergulho em Conteúdo |
| 19,4 a 26,8 s | mergulho em Financeiro |
| 26,8 a 34,6 s | mergulho em Operações e volta ao logo |
| 34,6 a 38,5 s | "Agentes em todas as áreas. Humanos no comando." |

Em cada área, a câmera entra pela bolinha e ela "abre" na cena:

- quatro agentes (orbe com robô, na cor da área) trabalhando ao mesmo tempo, cada um com um anel de progresso da tarefa;
- ligações entre eles com pacotes de dados circulando;
- um contador de tarefas concluídas que sobe a cada entrega;
- o humano embaixo, ligado a todos os agentes. Chega um pedido de aprovação, o cursor clica em **Aprovar** e a aprovação sobe até o agente que pediu.

## Fonte do conteúdo

- As mensagens dos agentes de Marketing, Financeiro e Operações foram adaptadas dos exemplos da página do Pixel AI Hub (CPL de R$ 8,40 pra R$ 6,10, ROAS 4,2, margem em 32%, 4 assinaturas duplicadas canceladas, reposição chegando quarta). Conteúdo não tem exemplo na página; as tarefas dessa área são ilustrativas.
- "Humanos no comando" segue a tese da estratégia Pixel 2.0: agentes em todas as áreas, humanos como orquestradores.
- Cores por área do sistema de motion da marca: Marketing `#D8B3FD`, Financeiro `#606FEF`, Operações `#FE5000`; Conteúdo usa o laranja claro `#FFA38D`.

## Como editar

Os textos ficam no array `AREAS` do `index.html` (nome da área, agentes com até duas linhas de tarefa e o pedido de aprovação). Os tempos ficam nas constantes `Z0`, `BLOCK`, `ZIN`, `HOLD` e `ZOUT`.

```bash
npm i -D playwright
node render.mjs
```

Variáveis opcionais: `FFMPEG` (caminho do ffmpeg) e `CHROMIUM` (caminho de um Chromium já instalado).
