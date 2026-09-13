# Captura e recuperação: da fonte à evidência consultável

> **Escopo:** este Hub publica um ledger de referência e documentação de arquitetura. Não distribui os coletores, o catálogo de transcrições, o classificador, o agendador ou as integrações de memória descritos abaixo. As práticas de produção vêm de uma implantação privada de referência, consultada em **13/09/2026**. Não são funcionalidades instaladas ao clonar este repositório.

O objetivo não é colocar todos os documentos no prompt. É permitir que o agente descubra **o que chegou**, localize **a evidência original** e use somente o trecho necessário: sem confundir captura com verdade aceita, nem acesso com autorização de divulgação.

## 1. O que cada camada responde

| Camada | Pergunta que responde | Conteúdo e responsabilidade | O que não comprova |
|---|---|---|---|
| Fonte | O que o fornecedor disponibiliza para esta conta? | API, MCP, exportação ou arquivo explicitamente autorizado | Todo o histórico da organização; gravação integral |
| Raw privado | Qual resposta foi preservada? | Payload nativo, metadados, páginas da transcrição, notas e revisões | Que tudo foi lido, que o conteúdo é verdadeiro ou que pode ser publicado |
| Summary do fornecedor | Como a ferramenta resumiu o material? | Resumo separado da transcrição | Existência de fala original; completude; concordância de todos |
| Queue e ack | O que está pendente ou foi reconhecido por um consumidor? | Estado mutável, lote congelado, finalidade e referências | Qualidade semântica da propagação; recebimento de um digest |
| Context Ledger | O que entrou, de qual origem e por qual referência? | Índice leve com seis campos | Transcrição completa; mecanismo universal de resolução; estado canônico |
| Catálogo local FTS | Em qual corpo aparece este termo? | Índice lexical derivado, com distinção entre resumo e transcrição | Busca semântica; cobertura total do acervo; atualização de outros índices |
| Estado canônico | O que foi aceito como decisão, compromisso ou contexto vigente? | Notas curadas, destinos de domínio e proveniência | Cópia integral do raw; fato irrevogável |
| GBrain | Onde está o conhecimento documental selecionado? | Recuperação sobre corpus curado e políticas explícitas de seleção | Que raw, queue ou ledger foram indexados |
| Honcho | Que contexto conversacional ou de pessoas está disponível? | Memória conversacional consultada pelas interfaces próprias | Crawl automático do arquivo privado de reuniões |

**Uma mesma informação pode aparecer em várias camadas sem que elas sejam equivalentes.** Um trecho útil de uma conversa pode sustentar uma nota canônica e um aprendizado editorial; ambos devem conservar a origem, mas nenhum substitui a gravação preservada.

### Implementado aqui versus descrito como referência

Neste repositório, o circuito executável é:

```text
produtor sintético → append_entry → JSONL de seis campos → consulta por janela
```

Na implantação privada estudada, o circuito de reuniões é mais amplo:

```text
APIs/MCP autorizados
  → captura limitada por fornecedor
  → raw privado + revisões
  ├─→ catálogo local FTS + referências no ledger
  └─→ envelope de reuniões + dedupe + lote pending
        ├─→ classificador único → destinos canônicos → ack de classificação
        └─→ digest separado → artefato local → consumidor de entrega

corpus documental selecionado → sincronização própria → GBrain
conversas do agente            → integração própria   → Honcho
```

As setas representam responsabilidades, não uma transação distribuída automática. Cada fronteira precisa de seu próprio recibo e teste. O procedimento de verificação está em [Operação e verificação](operacao-e-verificacao.md).

## 2. Capturar com fidelidade; interpretar depois

### Raw não é sinônimo de texto puro

Um raw pode conter a resposta JSON nativa, identificador do fornecedor, instante de coleta, metadados da gravação, páginas de transcrição e notas. Preservar o envelope permite corrigir o parser e reconstruir o índice **sem pedir novamente o material à origem**.

A normalização deve ser aditiva: extrair os campos úteis para a leitura comum sem destruir o payload nativo. É uma fronteira de parser, não licença para reescrever falas, completar participantes ausentes ou transformar prosa de status em transcrição.

Na referência, o desenho privado é equivalente a este esquema; os rótulos entre `<...>` são placeholders, não caminhos de instalação:

```text
<arquivo-privado>/
  granola/raw/
  granola/queue/
  fathom/raw/
  plaud/raw/
  catalog.sqlite
  catalog-health.json

<estado-privado>/
  classificacao/pending/
  classificacao/acked/
  digest/pending/
  digest/acked/
```

- **Raw:** preservação e revisões. O classificador não o edita.
- **Queue:** estado operacional mutável. Pode conter material sensível; não é pasta pública de intercâmbio.
- **Catálogo:** derivado e reconstruível. Também é sensível, pois contém texto indexado.
- **Ack:** reconhecimento de consumo por finalidade. Não substitui backup nem prova de destino.

A referência usa diretórios privados `0700` e arquivos `0600` nas rotas de arquivo e estado. O ledger público de demonstração **não implementa sozinho** esse contrato de permissões. Em uma implantação real, a localização, a política de acesso e os backups devem ser configurados explicitamente.

### Transcrição, resumo e recorte precisam manter seus nomes

Uma transcrição válida exige fala não vazia. Espaços, rótulos de speaker sem fala, um objeto contendo só resumo ou uma mensagem “ainda não disponível” não contam como conteúdo transcrito.

No catálogo privado, o tipo de corpo diferencia `transcript` de `summary`. A cobertura distingue presença, ausência, parcialidade e recorte manual. No coletor, podem existir estados mais detalhados, como conteúdo ainda não pronto, paginação inválida e erro de autenticação. A redução para um catálogo comum não pode apagar o diagnóstico do raw.

Um recorte manual continua sendo **recorte**. Completar uma paginação comprova que o conjunto retornado pelo fornecedor foi percorrido; não comprova que a transcrição cobre todo o áudio, que o reconhecimento de fala acertou ou que o speaker foi identificado corretamente.

### Privacidade não significa empobrecer a fonte privada

O arquivo privado pode preservar o contexto rico dentro do escopo autorizado. A minimização ocorre na saída: contexto de prompt, nota canônica, compartilhamento entre ambientes e publicação recebem apenas o necessário para sua finalidade.

Isso não elimina consentimento, retenção ou direito de exclusão. Também não autoriza enviar raw para ferramentas externas de parsing, embeddings ou criação de conteúdo só porque o agente consegue lê-lo. Exemplos públicos, testes e screenshots devem ser sintéticos.

## 3. O ledger é o mapa de entrada, não o arquivo completo

A implementação pública está em [`reference/context_ledger.py`](../reference/context_ledger.py). Cada linha tem exatamente:

| Campo | Significado prático | Cuidado |
|---|---|---|
| `ts` | Timestamp informado pelo produtor; na ausência, instante do append | Não presumir que seja o início da reunião |
| `source` | Nome da origem lógica | Não implica que exista um conector com esse nome neste repo |
| `who` | Remetente ou rótulo de origem informado pelo produtor | Pode conter informação privada |
| `who_kind` | `person`, `tool`, `transactional` ou `unknown` | Heurística de remetente, não identidade verificada nem classificação do conteúdo |
| `excerpt` | Texto com espaços normalizados e corte em 200 caracteres, acrescido de reticência quando necessário | Não é resumo de LLM; pode perder contexto e continua sensível |
| `ref` | Referência estável usada para dedupe | Deve permitir rastreabilidade no sistema integrador |

Exemplo exclusivamente sintético de referência: `meetings:demo-001`. Na referência privada há convenções por provedor, como `granola:<identificador>`, `fathom:<identificador>` e `plaud:<identificador>`. O CLI público não transforma essas strings automaticamente em chamadas de API.

### Três limitações que importam antes de adicionar produtores

1. **Dedupe é por `ref`, não por evento real.** Se dois fornecedores gravam a mesma conversa, são duas entradas legítimas de origem. Se duas contas usam IDs locais iguais, o integrador precisa de uma convenção de referência que as diferencie.
2. **Repetir uma referência não atualiza seu excerpt.** A versão pública ignora um append com `ref` não vazia já existente. Enriquecer o raw não altera automaticamente a linha histórica. Uma política de correção precisa de identidade própria e vínculo explícito com o evento anterior; não há protocolo completo de correção embutido no esquema.
3. **O toy não é um banco transacional.** Ele relê as referências para deduplicar, não contém lock multiprocesso e não valida todos os campos ou referências vazias. Reexecução serial idempotente não prova segurança com escritores concorrentes. O helper privado examinado tem proteções adicionais; elas não estão automaticamente presentes no código público.

O ledger é leve em comparação com o acervo, mas **não é anonimizado**. Seu excerpt pode conter fala original. Mesmo quando uma implantação o mantém junto ao cérebro privado, isso não autoriza copiá-lo para um repositório público ou incluí-lo no corpus semântico.

## 4. Recuperação por pergunta, não por “busca universal”

Escolha a camada pelo que precisa responder:

| Pergunta | Primeiro caminho | Verificação adicional |
|---|---|---|
| “O que entrou nesta semana?” | Consulta de ledger por janela | Checar se os produtores daquela fonte estão ativos |
| “Onde foi mencionada esta expressão?” | Catálogo FTS do corpo | Abrir raw, conferir origem, data e tipo do trecho |
| “Qual decisão está valendo?” | Fonte canônica do domínio | Revisar evidências e eventuais decisões posteriores |
| “Onde está o documento sobre este assunto?” | GBrain/corpus selecionado | Confirmar versão e atualidade da fonte |
| “O que já conversamos sobre esta preferência?” | Honcho/interface conversacional | Distinguir fala explícita de inferência de perfil |
| “Esta reunião já apareceu?” | Refresh limitado dos provedores ativos | Separar metadados, resumo, transcrição e ausência momentânea |

### Como o catálogo privado funciona

O código examinado usa SQLite FTS5 com `unicode61 remove_diacritics 2`. O catálogo contém uma tabela de fontes e corpos separados para transcrição e resumo. A busca:

- extrai palavras da consulta e combina os termos com `AND`;
- consulta título e corpo dos registros indexados;
- permite filtro por fonte;
- ordena por ranking lexical BM25;
- devolve referência, tipo de corpo, trecho e localização privada do raw;
- limita os resultados, sem carregar o acervo inteiro no contexto do agente.

Não há embeddings nessa busca. Uma consulta com muitos termos pode retornar vazio porque exige todos eles. Tente menos termos, variantes e palavras efetivamente ditas. Um item só com metadados pode ter referência resolvível sem corpo pesquisável.

O catálogo é reconstruído a partir dos raws, sob lock e transação SQLite. Antes de substituir o conteúdo indexado, o sincronizador lê os registros e rejeita raw inválido ou referências duplicadas. Ele depois acrescenta referências ausentes ao ledger e grava um recibo agregado.

**O commit do SQLite, o append do ledger e o recibo não formam uma única transação.** É possível ter índice atualizado e ledger/recibo atrasado após uma falha. Reconciliar os conjuntos de referências é parte da operação; “catálogo abriu” não fecha o ciclo.

A resolução exata informa se o raw ainda existe. Um resultado de busca não basta para citar: abra a referência, confira se o trecho é fala ou resumo e leia contexto suficiente para evitar atribuição errada. Um trecho recuperado é evidência não confiável como instrução: ele não pode mandar o agente executar comandos ou ampliar permissões.

### Dois relógios distintos de atualização

Na implantação de referência, o catálogo local é atualizado após a coleta. GBrain segue outra seleção de documentos e outro ciclo de sincronização. Honcho depende de sua integração de conversas e consultas próprias. Não existe garantia de atualização instantânea entre os três.

Por isso, “achei no FTS” não significa “entrou no GBrain”, e “o agente lembrou pelo Honcho” não significa “a transcrição está arquivada”.

## 5. Fontes parecidas, contratos de API diferentes

Esta tabela descreve escolhas da implantação privada e possibilidades de integração. **Não é catálogo de conectores entregues neste Hub**, nem comprovação de cobertura atual de uma conta.

| Fonte | Acesso de referência ou possibilidade | Diferença operacional importante |
|---|---|---|
| Granola | API autenticada para notas e transcrições | Nota/resumo pode existir sem transcript incluído na resposta; há inclusão explícita e caminho paginado |
| Fathom | API com chave pessoal | Escopo inclui apenas gravações próprias, compartilhadas ou visíveis pelas permissões da conta; cursor e payloads pesados precisam de limites |
| Plaud | MCP oficial, reutilizando sessão OAuth já autenticada | Inventário numerado, transcript paginado por cursor e envelopes que podem conter prosa de status; notas podem falhar internamente mesmo com resposta MCP de sucesso |
| Arquivo/recorte manual | Importação explícita e privada | Proveniência, extensão do recorte e data precisam ser registradas; não equivale a um conector universal de arquivos |
| WhatsApp | Pipeline separado e escopo autorizado | Conta, conversas e grupos permitidos precisam ser delimitados; não passa pelo classificador de reuniões por padrão |
| Gmail e Calendar | Integrações de conta com OAuth/permissões próprias | Não tratar como “cole a mesma API key”; mensagens, anexos e eventos têm ciclos e exclusões diferentes |
| Slack | Possibilidade de produto, captura desligada na implantação de referência | Ter um bot ou superfície de conversa não prova ingestão de histórico |
| Newsletters | Possível fonte editorial em outro fluxo | Não são capturadas pelo ledger operacional de referência; não inferir cobertura por haver integração de email |
| Outras ferramentas de reunião | Adaptadores futuros, mediante validação | API/MCP/exportação precisam provar escopo, IDs, corpo, paginação e direitos de acesso |

### Granola: nota não prova transcrição

A referência operacional utiliza `GET /v1/notes/{id}?include=transcript`. Para a resposta de tamanho excedido documentada como HTTP 413, o caminho é obter metadados e percorrer `/v1/notes/{id}/transcript` até o término verificável.

Essas rotas descrevem o contrato usado na implantação, não um comando deste Hub. Antes de portar o adaptador, confirme API, plano, schema e autenticação na documentação vigente do fornecedor.

O enriquecimento de notas antigas é separado da coleta de novas notas. O objetivo é preencher conteúdo ausente sem desfazer reconhecimento de processamento. Campos de status da fila não podem ser reinicializados por um backfill de transcript.

### Fathom: visibilidade e corpo são canários diferentes

O fluxo de referência usa listagem de reuniões, `include_transcript=true` quando pertinente e o endpoint específico `/recordings/{recording_id}/transcript`. A paginação usa `next_cursor` na resposta e `cursor` no pedido seguinte.

Uma chave válida não prova acesso a todas as reuniões de uma organização. Uma listagem bem-sucedida não prova acesso ao corpo. Metadados, transcrição, resumo e action items precisam ser inspecionados separadamente, sem imprimir seus conteúdos no diagnóstico.

### Plaud: MCP não é automaticamente arquivo durável

Na implementação privada, o coletor chama o servidor oficial por stdio e preserva as respostas. Não copia tokens, não cria novo login, não baixa áudio nem solicita geração de transcrição. O conteúdo precisa já estar disponível na origem.

Comportamentos importantes observados na implementação revisada:

- `list_files` usa páginas numeradas. Filtros locais só são aplicados depois do inventário; página curta sozinha não certifica fim. A coleta verifica término e contradições de paginação.
- `get_file` pode trazer JSON acompanhado de prosa. Preservar resposta integral e separar o objeto decodificado evita perder contexto de parsing.
- `get_transcript` retorna páginas com `block=transaction`. O coletor verifica identificador, offset, quantidade retornada, segmentos, total e cursor terminal.
- `[]`, conteúdo não pronto, resposta não estruturada e erro técnico são estados distintos. Prosa sem `isError` não vira fala.
- `get_note` pode trazer `data_content_error` por nota mesmo quando a chamada MCP foi aceita. Não contar essa nota como conteúdo válido.
- `transcript_complete=true` certifica a paginação reconhecida, não a qualidade do áudio ou a identidade de quem falou.

O inventário visível pode ser completo enquanto somente um lote limitado de corpos foi selecionado. “Inventário completo”, “corpos coletados” e “transcrições presentes” precisam de contagens separadas.

## 6. Dedupe em três níveis

### Nível 1: registro da fonte

Mesmo provedor + mesmo identificador não deve criar dois arquivos correntes para a mesma origem. Preserve o identificador literal e valide seu formato antes do acesso; não “conserte” silenciosamente um token inválido. Para múltiplas contas, a identidade precisa incluir o escopo da conta.

### Nível 2: evento representado por várias fontes

Mantenha os raws separados. Só depois agrupe a conversa para classificar uma vez e evitar duplicar decisões e compromissos.

**Comportamento real examinado, não algoritmo idealizado:**

- O agrupamento legado Granola/Fathom usa data local e título normalizado. Não implementa score completo de participantes, duração ou tolerância temporal. Isso pode produzir falsos agrupamentos ou separar o mesmo evento.
- Plaud exige corroboração adicional para aderir ao grupo legado: título normalizado não genérico, mesmo instante de início da gravação em todos os membros e candidato Plaud único para aquele grupo.
- Sem essa corroboração, Plaud fica separado com revisão de dedupe. Data e título sozinhos não autorizam fusão.

Participantes, duração, agenda e finalidade são sinais úteis de revisão ou evolução futura. Não devem ser apresentados como campos que o código atual já compara automaticamente.

### Nível 3: fato canônico

Mesmo após agrupar fontes, o classificador precisa procurar o fato nos destinos antes de escrever. Uma pendência já aberta deve ser atualizada, não recriada. Divergências de prazo, responsável ou decisão viram conflito explícito; não se escolhe a fonte mais conveniente silenciosamente.

O owner único da propagação de reuniões evita dois pipelines aceitando a mesma evidência separadamente. O digest permanece leitor: resumir e entregar não concede permissão para atualizar a memória canônica.

## 7. Refresh não é reprocessamento

Uma transcrição pode aparecer depois dos metadados, ou ser editada após o processamento. Há quatro operações diferentes:

| Operação | O que pode mudar | O que deve preservar |
|---|---|---|
| Fetch de novo registro | Novo raw, entrada de índice, candidato de processamento | Registros anteriores e escopo autorizado |
| Refresh/enriquecimento | Conteúdo corrente, cobertura, revisão, índice derivado | IDs e ack já existentes |
| Retry de lote pending | Continuação do mesmo lote congelado | Identidade do lote e fatos já escritos corretamente |
| Reprocessamento aprovado | Nova avaliação canônica de material atualizado | Histórico, justificativa e idempotência das escritas |

Na referência Plaud, o refresh compara conteúdo por hash semântico, ignorando campos operacionais e determinados links efêmeros para não criar revisões falsas. Conteúdo igual não reescreve o arquivo. Conteúdo alterado preserva snapshot anterior dentro do raw. O helper comum de arquivo também preserva revisões, mas em arquivos de revisão separados; os layouts não são idênticos.

Sem refresh, estados de ausência reconhecida podem ser apenas reutilizados. Um recibo com “existente ignorado” descreve cobertura conhecida, não uma nova consulta de disponibilidade na origem.

A preparação de reuniões filtra IDs já reconhecidos por finalidade. O batch pending é reproduzido antes de selecionar material novo. Logo, atualizar o raw **não reabre automaticamente ack nem reescreve o envelope congelado**. Se a mudança merece nova decisão, é necessário um fluxo explícito de revisão; não apagar ack como atalho.

## 8. Atribuição e fronteira pessoal/profissional

Uma conta pode conter demos, exemplos de onboarding e gravações importadas. Pertencer à conta não prova que seu dono participou, assumiu uma ação ou viveu aquela experiência. A referência Plaud marca atribuição ainda não verificada e exige revisão antes de afirmações pessoais no cérebro ou no digest.

Separar conversas **pessoais, profissionais, mistas e a confirmar** é uma direção de evolução, **ainda não implementada** no roteamento Plaud estudado. Não confundir esse desenho com uma proteção automatizada já validada.

Uma implementação futura deve manter o original privado, decidir o destino pelo conteúdo e finalidade, separar os trechos necessários sem multiplicar o raw e bloquear promoção ambígua até confirmação. Conversa casual não vira tarefa ou pauta automaticamente. O ambiente de empresa ou de conteúdo não recebe o íntimo por herança da conectividade.

## 9. Limites conhecidos e leitura responsável da evidência

- O Hub entrega o mecanismo mínimo de ledger; não entrega instalação de MCP, `doctor`, catálogo FTS, conectores reais, retenção, purge ou agendamento.
- A implantação privada possui captura e recuperação de raw verificadas nos seus recibos. **Classificador, digest e entrega não foram retestados ponta a ponta após a inclusão Plaud.** Código preparado e jobs configurados não fecham esse gate.
- Limites de janela, quantidade por execução e permissões podem deixar histórico fora da coleta. Um contador do catálogo não é uma prova de cobertura online/offline total.
- Busca lexical pode falhar por vocabulário. Resumo pode omitir um assunto presente no corpo. Os dois problemas pedem testes diferentes.
- A versão Plaud examinada não implementa retry exponencial interno nem retomada de cursor entre execuções. Paginação numerada não oferece snapshot transacional do inventário upstream.
- Silêncio de um coletor não prova ausência de novos fatos. Verifique último run, resultado, escopo e frescor do catálogo.
- A presença de um nome de ferramenta nas regras do classificador de remetentes não significa que ela está conectada.

Para transformar esta arquitetura em produto, a primeira expansão útil é um adaptador real, limitado e testável. Adicionar todas as fontes de uma vez sem provar autenticação, persistência, resolução, dedupe e exclusão só aumenta a quantidade de estados que parecem saudáveis sem estarem.
