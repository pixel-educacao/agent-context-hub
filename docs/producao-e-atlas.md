# Produção editorial e Atlas: da ideia escolhida à peça, sem confundir as camadas

O [motor de ideias](motor-de-ideias.md) prepara matéria-prima. A produção começa quando o autor escolhe o que quer desenvolver. O Atlas é uma proposta de interface para consultar essas relações, não o responsável por decidir, publicar ou executar procedimentos.

Este repositório é uma referência pública. Não contém o acervo privado, um aplicativo Atlas instalável, um gerador de cadernos instalado nem conectores editoriais prontos.

## 1. Situação documentada

Estado em 13/09/2026:

| Frente | Estado | Limite |
|---|---|---|
| Motor de ideias | Piloto manual privado produzido para avaliação | Não há cron implementado do motor; frequência e seleção recorrente não foram fechadas |
| Caderno de criação | Modelos privados experimentados, com contexto e variações de copy | Modelo guardado não significa lote de posts aprovado |
| HTML | Formato principal escolhido para esse report; modelo privado com amostra guardada | Não equivale a aplicação com banco de dados nem entrega agendada |
| Voz | Revisões e uma amostra recalibrada no modelo | A v5 foi rejeitada como voz e formato de posts; não é exemplo aprovado |
| Atlas | Mockup navegável privado, com recorte ilustrativo | Sem acervo vivo conectado, persistência, publicação, métricas integradas ou servidor persistente |
| Newsletters | Captura complementar proposta | Não implantada como rotina editorial |
| Roteamento pessoal Plaud | Proposta com destino definido no contexto pessoal privado | Sem implantação desse encaminhamento pessoal |

Esses estados são independentes. A existência de captura de gravações em outro fluxo não comprova roteamento pessoal. Aprovar riqueza do contexto não aprova copy. Gostar de aparência não autoriza integrar dados ou expor um serviço.

## 2. Três objetos que não devem virar um só

### Ideia

É o aprendizado, pergunta ou reflexão com identidade estável, fontes, contexto e evolução. Pode começar bruta e ser lapidada. Continua existindo depois de gerar uma publicação, e pode receber novos contrapontos.

### Peça

É um texto, roteiro ou artefato concreto para um canal. Tem identidade própria, vínculo com a ideia, versões e estado editorial. Publicar uma peça não publica suas alternativas, nem conclui todos os desdobramentos da ideia.

### Skill

É um procedimento reutilizável, com escopo, pré-requisitos, passos e verificações. Pode orientar a execução de uma peça. Não é uma ideia em estágio avançado, não herda etapas editoriais e não se torna instalada por aparecer num grafo.

```text
Ideia ──origina──► Peça para um canal ──tem──► versões do texto
   └──origina──► Peça para outro canal

Skill ──pode orientar──► produção de uma peça
Fonte ──sustenta──► ideia e afirmações específicas
```

O diagrama é conceitual, não um schema ou uma API implementada.

## 3. Lifecycle proposto e registro canônico

| Objeto | Estado conceitual | Condição de passagem |
|---|---|---|
| Ideia | Bruta | Fragmento ou referência capturada, com origem identificada quando disponível |
| Ideia | Lapidada | Contexto, ângulo e valor para o leitor desenvolvidos; limites e autoria preservados |
| Peça | Draft | Texto ou roteiro concreto para um canal, ainda em elaboração ou revisão |
| Peça | Publicada | Publicação confirmada por rede, URL/ID e data; vínculo com a peça resolvido |
| Skill | Procedimento em camada própria | Validação e manutenção do procedimento, separadas de publicação editorial |

“Escolhida”, “em escrita”, “favorita” e “arquivada da seleção” podem ajudar a operação manual, mas não devem criar uma máquina de estados concorrente sem reconciliação. Favorito e tags são sinais independentes da maturidade. Arquivar da seleção não apaga a fonte.

Antes de implementar:

1. Identificar o registro que hoje é dono do estado editorial e seu responsável ativo.
2. Confirmar como se identificam pauta/ideia, peça, versões e publicação.
3. Reconciliar os documentos de contrato com a operação realmente viva.
4. Resolver conflitos antes de permitir escrita por uma nova interface.
5. Ler de volta o registro canônico depois de cada mudança.

No ambiente de origem, o contrato editorial inspecionado descreve uma peça por plataforma, vínculo comum de pauta e lifecycle num Kanban externo. Isso é evidência documental, não comprovação de sincronização em operação. Não criar outro Kanban por inferência, nem presumir que um arquivo sem URL nunca foi publicado. Correspondências duvidosas ficam a confirmar.

## 4. Caderno de ideias, caderno ampliado e posts são entregas diferentes

| Entrega | Para que serve | Conteúdo |
|---|---|---|
| Caderno de ideias | Ajudar o autor a compreender, refletir e escrever | Contexto, interpretação identificada, utilidade, perspectivas e fontes; não exige posts |
| Caderno de criação ampliado | Explorar a ideia e alternativas editoriais quando solicitado | Seção de contexto aprofundado e seção separada com variações completas |
| Peça para aprovação | Revisar uma proposta concreta de publicação | Copy ou roteiro do canal, fontes necessárias e status de revisão |
| Publicação | Tornar uma peça acessível na rede autorizada | Ato separado, com alvo, autorização e recibo verificável |

No experimento do caderno ampliado, o pedido foi contexto e três posts completos em percursos distintos por ideia. Essa configuração não é quota do motor de ideias e não torna obrigatório produzir três textos para cada fonte. Uma ideia não selecionada pode continuar sendo apenas aprendizado.

No HTML, “duas páginas por ideia” significa duas seções de leitura contínua, não folhas rígidas:

- **Contexto:** situação factual, ponto a desenvolver, leitura editorial, utilidade para a audiência e limites relevantes.
- **Variações:** textos completos com argumentos ou percursos diferentes, apenas quando pedidos. O nome do formato e a referência ficam fora da copy.

O caderno não deve dizer apenas “conte a cena”, “explique a lição” e “feche com CTA”. Precisa desenvolver a ideia para que o autor a reconheça e possa discordar. Em contrapartida, não preencher cenas, falas, emoções ou consequências que a fonte não registra.

## 5. Escolher a narrativa pela evidência

O arco problema → ação → resultado é útil para um case documentado. Não serve como formulário universal.

- **Pergunta de diagnóstico:** a contribuição pode estar numa pergunta melhor, mesmo sem desfecho do caso.
- **Critério de implementação:** explicar a distinção que muda a escolha sem inventar antes/depois.
- **Raciocínio de decisão:** mostrar alternativas e condições; terminar na escolha se ainda não há resultado.
- **Experiência com resultado:** descrever o observado e os limites da atribuição causal.
- **Reflexão aberta:** preservar a tensão sem fabricar conclusão.

Se não há alegação de eficácia, não é necessário acrescentar um bloco vazio de “resultado em aberto”. Se o texto promete eficácia, exige evidência ou qualificação. Notas de auditoria ficam no contexto de trabalho quando não são necessárias para qualificar a alegação pública.

## 6. Autoria, voz e adaptação por canal

### Antes de escrever em nome de alguém

Recuperar amostras reais aprovadas daquele autor no canal escolhido e o guia de voz vigente. Distinguir o posicionamento desejado de dados efetivamente medidos sobre a audiência. Relatório de uma rede não prova profissão, dores, demografia ou desempenho de outra.

Comparar concretamente:

- Como a opinião entra no texto.
- Tamanho e ritmo dos parágrafos.
- Uso de primeira pessoa, listas, setas e respiro.
- Relação entre cena, argumento e aplicação.
- Tipo de fechamento e convite à conversa.

No sistema documentado, setas `→`, listas autorais e parágrafos curtos são marcas a preservar. Retirar rótulos internos como “hook”, “desenvolvimento” e “CTA” não autoriza apagar a formatação do autor. Outra pessoa deve construir sua própria régua, não copiar essa identidade.

### Benchmark não é voz

Uma referência externa pode inspirar percurso narrativo. Não substitui a sintaxe, experiência e posição do autor. Informar o canal original e tratar a adaptação entre redes como hipótese. Título ou legenda de vídeo não prova sua estrutura interna; sucesso em uma rede não comprova eficácia em outra.

### Texto-mãe e derivados

Uma tese desenvolvida pode originar artigo, vídeo e peças curtas. É possível escrever e depois gravar, ou gravar uma explicação e lapidar o artigo a partir dela. Transcrição crua não é artigo nem newsletter: é preciso retirar repetições e reconstruir o argumento sem adulterar a fala.

Derivação deve ser nativa ao canal. LinkedIn e YouTube não têm o mesmo contrato de atenção; um raciocínio que depende de demonstração pode pedir vídeo. LinkedIn para X exige condensação, não cópia automática. No fluxo de curtos experimentado, lapidar LinkedIn antes de adaptar para Instagram; isso não impõe a mesma ordem a toda produção longa.

A tese vem antes da embalagem. Título, thumbnail e CTA não devem fabricar uma promessa que a peça não sustenta. Uma pauta escolhida não autoriza um pacote multicanal não pedido.

### A lição da v5

A v5 do caderno privado passou por testes técnicos e foi rejeitada em voz e formato dos posts. Ela permanece histórico de tentativa, não exemplo aprovado. Uma amostra posteriormente recalibrada foi guardada num modelo; isso não reescreve nem aprova o restante do lote.

Quando um lote falha na voz, corrigir uma amostra, comparar com textos reais e pedir avaliação antes de escalar a revisão. Lint, exportação íntegra e leitura confortável não validam identidade autoral.

## 7. Gates de qualidade e circulação

| Gate | Pergunta de verificação | Evidência esperada |
|---|---|---|
| Fidelidade | O texto diz apenas o que a fonte sustenta? | Conferência dos trechos, citações, autoria e cronologia |
| Raciocínio | A interpretação respeita alternativas, limites e causalidade? | Leitura semântica; distinguir observação, projeção e hipótese |
| Autoria | Primeira pessoa, opinião e experiência pertencem ao autor? | Fonte atribuível ou contribuição reconhecida por ele |
| Voz e canal | A peça parece escrita por esse autor para esse canal? | Comparação com amostras reais e avaliação editorial, não só lint |
| Privacidade | Este conteúdo pode circular para esse destinatário? | Escopo autorizado, revisão de identificação indireta e remoção do que não pode sair |
| Integridade do artefato | O arquivo contém o texto final sem cortes ou deformações? | Comparação textual e inspeção da renderização |
| Aprovação editorial | O autor aprovou esta versão concreta? | Registro de aprovação com escopo claro |
| Publicação | Foi publicado no alvo correto? | URL/ID, rede, data e leitura de volta da publicação |

Preservar o contexto completo nas fontes e no caderno privados já autorizados. Não apagar material valioso preventivamente só porque é sensível. Isso não concede circulação: para o time ou público, preparar um recorte autorizado. Remover nomes pode ser insuficiente se as circunstâncias identificam pessoas ou empresas. Credenciais nunca entram no caderno público ou no repositório.

Se uma revisão independente foi definida como gate, incorporar o parecer antes de apresentar o trabalho como pronto. Registrar o escopo realmente revisado. Revisão de parte do lote não valida o restante. Testes técnicos não substituem o parecer semântico.

## 8. Como reproduzir o caderno manualmente

1. Preencher uma [ficha de ideia](../templates/ficha-de-ideia.md) com material autorizado.
2. Separar o contexto de trabalho de qualquer copy para publicação.
3. Confirmar qual entrega foi pedida: ideias, variações ou peça final.
4. Desenvolver o texto conforme o raciocínio sustentado pela fonte.
5. Aplicar os gates editoriais e de privacidade antes de exportar.
6. Se for produzir HTML, usar arquivo autocontido, CSS embutido e texto selecionável. Não incluir fontes remotas, bibliotecas externas ou JavaScript obrigatório para ler.
7. Em telas menores, empilhar variações; não comprimir o texto para simular uma folha.
8. Testar em navegador real em desktop e mobile, inclusive largura estreita e JavaScript desligado. Conferir âncoras, expansões, overflow, chamadas externas e legibilidade em screenshots.
9. Comparar os textos renderizados com os aprovados, incluindo parágrafos e setas. Regenerar após correções.
10. Entregar no destino privado autorizado e registrar avaliação, sem presumir publicação.

PDF é exportação opcional. Quando solicitado, verificar todas as páginas, texto integral, margens e sobreposições; redistribuir conteúdo antes de reduzir fonte. Um hash confirma qual arquivo foi testado, não a verdade do conteúdo.

Este procedimento não pressupõe um renderer disponível neste repositório. Para o teste manual, a ficha Markdown já permite validar a utilidade editorial sem construir uma interface. A etapa HTML exige uma implementação própria e verificação do artefato resultante.

## 9. O que o Atlas pretende resolver

A proposta é uma interface permanente sobre o acervo existente, combinando:

- **Grafo:** explorar relações entre ideias, fontes, temas, peças e skills.
- **Biblioteca filtrável:** localizar e escolher sem depender da navegação visual.
- **Ficha de contexto:** entender a ideia, suas fontes, notas, peças derivadas e limites.
- **Sinais pessoais:** favoritos e tags independentes da etapa editorial.
- **Desempenho:** consultar resultados das publicações quando houver integração verificada.

O grafo não deve transformar cada arquivo em ideia nem esconder a origem de uma ligação. Uma conexão precisa dizer se é explícita na fonte, compartilhamento temático, sugestão editorial ou vínculo de derivação confirmado. Similaridade não prova causalidade nem endosso.

A representação explorada usa círculos para ideias, quadrados arredondados para peças e hexágonos para skills. Cor indica etapa; um halo pode destacar uma publicação. Formas e rótulos acompanham as cores para não depender só de percepção cromática. Essa convenção é desenho de interface, não contrato de backend.

## 10. Mockup versus sistema implementado

O mockup privado já existe e permite experimentar navegação, busca, filtros, favoritos, seleção, contexto e movimento do grafo. Usa um recorte ilustrativo; publicações, métricas, favoritos e relações demonstradas não são inventário real. Contém também uma amostra privada de rascunho, por isso o arquivo não acompanha este repositório público.

| No mockup | Em um sistema futuro, ainda a implementar e verificar |
|---|---|
| Dados incorporados ao HTML | Leitura de fontes oficiais com cobertura e atualização conhecidas |
| Favoritos e filtros em memória; recarregar restaura o início | Persistência privada com destino, identidade, autorização e leitura de volta |
| Publicações e métricas de demonstração | Correspondência verificável com publicações reais |
| Conexões ilustrativas | Relações explicáveis, com tipo e evidência |
| Seleção visual de uma skill | Distinção entre recomendar procedimento, comprovar uso e executá-lo |
| HTML offline com interações | Operação segura, acesso privado, autenticação quando necessária e observabilidade |
| QA de frontend registrado | Testes de ingestão, persistência, integração, reconciliação e falhas |

O mockup foi exercitado em navegador no ambiente privado; isso prova interações do protótipo, não integração com dados vivos. Não há servidor persistente, publicação automática, execução de skills ou escrita no cérebro por esse HTML. A prévia sem JavaScript é estática, ao contrário do caderno de leitura, cujo conteúdo deve continuar funcional sem JavaScript.

## 11. Desempenho não é atributo mágico da ideia

Métricas pertencem à publicação observada. Uma ideia pode ter uma peça com bom desempenho e outra ainda em draft. O destaque visual da ideia-mãe apenas indica que existe uma derivação em destaque, não que toda a ideia ou suas peças “viralizaram”.

Para uma integração futura:

- Resolver publicação por **rede + ID/URL**, nunca só título.
- Registrar fonte, data da coleta e janela da medição.
- Separar alcance, interação e conversão.
- Comparar dentro da mesma rede, formato, idade da postagem e histórico relevante.
- Mostrar métrica ausente ou atrasada como tal, não zero.
- Distinguir favorito pessoal, marcação manual de destaque e classificação calculada.
- Definir a regra antes de calcular; não há limiar universal aprovado de viralização.
- Ao relacionar resultados a tags, formatos ou skills, indicar amostra e período, sem inferir causa.

A cobertura de métricas por um agente de distribuição foi informada no contexto original, mas não foi verificada nem conectada ao Atlas nessa exploração. Uma skill sugerida não pode ser marcada como usada sem evidência de execução.

## 12. Ordem segura para evoluir

1. Validar manualmente a seleção de ideias e o caderno com o autor.
2. Fechar identidades e vínculos entre fonte, ideia, peça, versão e publicação.
3. Inventariar o escopo autorizado; explicitar fontes, períodos e pendências de ingestão.
4. Reconciliar o dono do lifecycle editorial antes de qualquer escrita de status.
5. Implementar primeiro leitura, busca e contexto; tratar o índice como reconstruível, não outro banco manual concorrente.
6. Aprovar separadamente persistência de favoritos, edição de notas e alteração de estado.
7. Conectar métricas por publicação e verificar atualização e correspondência.
8. Só então discutir automação, entrega recorrente e novas áreas do sistema pessoal.

Uma página em localhost não resolve por si só o acesso entre servidor remoto e computador do usuário. A futura implantação precisa de acesso privado apropriado; não deve expor portas públicas nem servir a raiz de um workspace. Aprovar o visual não autoriza migrar o cérebro, ampliar fontes, ativar crons ou incluir módulos pessoais adicionais.

**Critério final:** é possível reproduzir hoje a leitura, a ficha, a seleção e a revisão manual. O caderno automatizado recorrente e o Atlas conectado continuam sendo trabalho de implementação e validação, não funcionalidades entregues por este repositório.
