# Arquitetura: do sinal à ação e à ideia

[Índice](../README.md) · [Ambientes](ambientes-e-governanca.md) · [Estado real](estado-e-limites.md)

## Objetivo e fronteira

O problema original: um agente recebe informações em muitos lugares, mas não sabe responder com precisão **o que chegou, de onde veio, o que mudou e onde está o original**. Mais memória no prompt não resolve procedência, pendências contraditórias ou fontes ausentes.

A arquitetura divide responsabilidades. O motor de contexto preserva, localiza e organiza evidência. O motor de ideias lê esse contexto para encontrar material que mereça reflexão. A operação acompanha compromissos. A produção transforma uma escolha editorial em peça. Uma camada não deve simular a outra.

Este documento descreve um padrão derivado de uma instalação privada. A única parte executável distribuída aqui é o ledger de referência. Os demais componentes exigem implementação e autorização próprias.

## Camadas e perguntas

| Camada | Pergunta | Guarda | Não prova |
|---|---|---|---|
| Captura | O que a origem disponibilizou? | Payload, fonte, versão e estado da coleta | Que todo o histórico foi importado |
| Original privado | O que foi realmente dito ou recebido? | Transcrição, mensagem, resumo separado e metadados | Que a pessoa concordou com uma interpretação |
| Ledger | O que entrou, quando e de quem? | Referência curta por sinal | O volume integral da conversa |
| Catálogo de fontes | Onde está o corpo recuperável? | Metadados e índice derivado de texto | Completude histórica ou compreensão semântica |
| Classificação/propagação | O que este material muda? | Contexto, decisão ou obrigação com evidência | Permissão para enviar para outro ambiente |
| Fonte canônica | Qual é o estado operacional vigente? | Decisão, projeto, pessoa, prazo ou conhecimento | Que o índice de busca já atualizou |
| Memória nativa | O que precisa acompanhar toda sessão? | Poucos fatos estáveis e preferências | Corpus completo de vida e trabalho |
| Memória conversacional | O que foi discutido e aprendido sobre pessoas? | Histórico e representações consultáveis | Ingestão automática de todos os documentos |
| Busca documental | Qual documento curado trata disso? | Índice derivado e citações | Verdade superior ao documento original |
| Motor de ideias | O que merece aprofundamento? | Candidatos, evidência, hipótese e lacuna | Publicação aprovada |
| Produção | Como expressar a ideia escolhida? | Rascunho, revisão, versão e artefato | Envio ou publicação sem autorização |

Na implantação de referência, **Honcho** atende a memória conversacional e **GBrain** a recuperação documental. São papéis, não dependências do exemplo Python. O catálogo de fontes usa busca lexical FTS5 privada; não é o mesmo índice documental.

## Caminho completo de um item

Exemplo inteiramente sintético: numa conversa, uma pessoa diz que abandonou uma automação depois de perceber que precisava revisar toda saída.

1. **Capturar:** receber o corpo autorizado e guardar a referência estável da origem. Manter separado o resumo que o fornecedor gerou.
2. **Registrar:** adicionar um sinal ao ledger. Se a origem reenviar o mesmo evento, não criar outro sinal idêntico.
3. **Indexar:** atualizar o catálogo para localizar o texto. Se uma transcrição antes ausente aparecer depois, enriquecer a fonte sem reabrir automaticamente tarefas já processadas.
4. **Recuperar:** a pergunta sobre automações encontra o trecho; o agente abre a fonte para confirmar a fala e seu contexto.
5. **Interpretar:** separar fala original, hipótese do agente e eventual decisão explícita. A observação não vira automaticamente uma ordem para desligar outras automações.
6. **Destinar:** atualização operacional fica no cockpit correspondente. Conversa pessoal segue o destino pessoal acordado. Dúvida bloqueia a propagação, não a preservação privada autorizada.
7. **Extrair ideia:** a tensão entre economia aparente e custo de revisão pode gerar um candidato. A ficha guarda a origem, a autoria e o que falta para sustentar a tese.
8. **Escolher:** a pessoa pode escrever, aprofundar, guardar ou rejeitar. Nenhuma cota obriga a conversa a render post.
9. **Produzir:** aplicar voz, formato e revisão factual. Publicar somente dentro do escopo autorizado.
10. **Aprender:** guardar o feedback no procedimento pertinente, sem converter uma preferência pontual em lei permanente.

## Quatro deduplicações diferentes

**Evento:** mesma referência da origem, não repetir a entrada. Isso é o que o exemplo público demonstra.

**Gravação/fonte:** dois fornecedores podem registrar a mesma reunião. Preservar ambos como fontes, mantendo relações e diferenças; não descartar a transcrição mais completa só porque o título se parece.

**Fato/compromisso:** a mesma ação pode aparecer na reunião, no email e na mensagem seguinte. Propagar uma obrigação com múltiplas evidências. Não gerar três tarefas.

**Obra/ideia:** uma newsletter pode republicar artigo de outra autora. Contar recebimentos e obras separadamente; crédito pertence à autoria da obra. Duas propostas editoriais podem compartilhar um tema sem serem a mesma ideia.

Misturar essas deduplicações causa perda de evidência ou multiplicação de trabalho.

## Contexto online e offline

O transporte não determina a utilidade nem o destino. Uma gravação pode ser aula, memória pessoal, conversa profissional, recorte, demonstração do fornecedor ou material de terceiro. Transcrição disponível na conta é diferente de gravação ainda apenas no aparelho.

A proposta para classificar conversas usa **pessoal, profissional, misto e a confirmar**, pelo conteúdo e contexto. Em material misto, preservar o original inteiro e destinar apenas os recortes pertinentes. Essa separação ainda não estava implantada no checkpoint desta documentação. Não a deduza do classificador `who_kind`, que apenas tenta identificar tipo de remetente.

## Como o contexto entra na sessão

1. Carregar identidade, regras e mapa mínimos.
2. Identificar a pergunta real e o domínio.
3. Ler o mapa local e a fonte canônica pertinente.
4. Consultar histórico de conversas quando a pergunta depender de pessoa, preferência ou decisão anterior.
5. Consultar ledger para chegada, catálogo para fala original, índice documental para conhecimento curado.
6. Abrir a fonte escolhida e conferir atualidade, autoria e limites.
7. Responder ou agir com o menor conjunto suficiente de evidências.

Não existe um comando mágico que carregue todos os ambientes e resolva todos os conflitos. Contexto tem orçamento; dados desnecessários também aumentam o risco de confundir instruções com material de análise.

## Documentos de controle e procedimentos

Uma implementação pode usar arquivos como `AGENTS.md`, `SOUL.md`, `MAPA.md`, `TOOLS.md` e `PROPAGATION.md` para, respectivamente, governar execução, identidade, navegação, ferramentas e escrita. Esses nomes são uma convenção da implantação, não arquivos fornecidos pelo Hub.

**Skills** guardam o procedimento recorrente: quando usar, entradas, passos, gates, verificação e destino. Não são o lugar para despejar transcrições ou estado de projeto. O agente carrega a skill relevante e suas referências quando necessário; não injeta o catálogo inteiro de procedimentos em cada turno.

**Cockpits vivos** guardam estado: situação atual, próximo passo, responsável, prazo e evidência. Datas ou responsáveis ausentes ficam a definir. Diário registra cronologia; relatório guarda evidência; nenhum deles substitui silenciosamente o cockpit.

## Invariantes

- Preservar o original e sua procedência; resumo não substitui transcrição.
- Separar estado vigente de histórico e correções.
- Um responsável ativo por side effect. Leitura de um ambiente não concede escrita em outro.
- Falha de coleta não equivale a nenhuma novidade.
- Ideia, hipótese, conselho e desabafo não equivalem a decisão.
- Captura bem-sucedida não certifica classificação, propagação ou entrega.
- Um índice pode ser reconstruído; o original e o histórico de processamento precisam de proteção própria.
- Não publicar conteúdo privado para explicar a arquitetura que o processa.
