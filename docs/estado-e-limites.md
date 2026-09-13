# Estado, limites e próximos gates

[Índice](../README.md) · [Operação](operacao-e-verificacao.md)

**Checkpoint documental: 13/09/2026.** Esta página distingue o que pode ser executado a partir deste GitHub do que existe na implantação privada ou ainda está em discussão. Não é uma consulta em tempo real ao scheduler.

## Legenda

- **Disponível aqui:** código ou documento incluído neste repositório.
- **Implantado na referência privada:** há código e recibos internos; não distribuído aqui.
- **Piloto manual:** houve execução assistida, sem aprovação de automação recorrente.
- **Proposto:** direção ou desenho registrado, sem implementação correspondente comprovada.
- **Não revalidado neste checkpoint:** existe uma etapa anterior, mas falta teste para a nova combinação.

## Matriz de cobertura

| Componente | Estado no checkpoint | O que o leitor recebe |
|---|---|---|
| Ledger com seis campos e produtor sintético | Disponível aqui | Código Python e smoke tests |
| Consulta por janela e filtro textual | Disponível aqui | CLI e teste de integração |
| Captura Granola/Fathom/Plaud em raiz privada comum | Implantado na referência privada | Contrato e procedimentos; sem conectores distribuídos |
| Separação raw/resumo/transcrição/fila | Implantado na referência privada | Explicação do modelo e cuidados de migração |
| Catálogo lexical FTS5 e resolução até o raw | Implantado na referência privada | Fluxo de recuperação, não banco nem serviço |
| Backfill e refresh de transcrições | Implantado na referência privada | Invariantes, falhas e verificação; cobertura limitada ao inventário consultado |
| Busca documental curada e freshness | Implantado na referência privada | Arquitetura e gates; sem corpus/indexador implantável |
| Memória nativa e Honcho | Usados na referência privada | Divisão de responsabilidades; sem histórico ou configuração de contas |
| Classificação/digest integrado após a nova coleta | Não revalidado neste checkpoint | A coleta foi testada; não alegar novo E2E de entrega |
| Plaud pessoal/profissional/misto/a confirmar | Proposto | Gate de interpretação e destino, sem classificador instalado |
| Encaminhamento ao agente pessoal | Direção definida; implementação pendente | Destino lógico e necessidade de reconciliar os mapas de leitura |
| Novas newsletters selecionadas | Pesquisa/proposta | Critério de seleção e autoria, sem captura recorrente nova |
| Motor de ideias e caderno | Piloto manual | Método, template e critérios; sem cron novo |
| Voz/template final do caderno | Em refinamento | Gates editoriais, sem tratar versão experimental como aprovada |
| Atlas visual | Mockup | Conceito, não painel conectado à operação |
| Publicação editorial | Não autorizada por esta documentação | Nenhum publicador, agendamento ou postagem |
| Captura Slack na instalação de referência | Desligada | Não é fonte ativa por aparecer numa lista de integrações possíveis |

**Relatórios de investidas e operação não são newsletters.** Podem compartilhar transporte por email, mas têm destinos e critérios distintos. Ler um relatório e atualizar um cockpit manualmente não comprova captura recorrente de todos os reports.

## Limites do código `reference/`

A implementação é propositalmente pequena. Nesta atualização, a lógica foi preservada e um fixture nominal herdado foi substituído por identidade fictícia com domínio de exemplo. Serve para entender e exercitar o contrato, não para copiar um backend de produção pronto.

### Concorrência e durabilidade

- `append_entry` lê referências e depois escreve. Não há lock envolvendo essa transação; dois processos concorrentes podem inserir duplicatas.
- Não há append transacional com recuperação garantida de escrita parcial, `fsync`, rotação ou backup implementados.
- `load_refs` ignora linhas JSON inválidas; isso não é relatório de corrupção nem reparo seguro. JSON válido com estrutura inadequada também não recebe validação de schema completa.
- Uma `ref` vazia não é rejeitada e não garante dedupe. Produtores reais devem validar a referência antes de gravar.
- Dedupe é exato por `ref`, sem verificar divergência de conteúdo numa mesma referência.

### Consulta e custo

- O arquivo inteiro é lido por append e por consulta. A janela limita o resultado entregue ao agente, **não a leitura em disco**.
- A CLI exibe itens na ordem do arquivo; não ordena por mais recente primeiro. `--limit` corta a exibição após essa ordem.
- O digest da CLI não exibe `ref` nem timestamp de cada item. Para seguir até a fonte, o integrador precisa ler esses campos na linha correspondente do JSONL sem despejar o arquivo inteiro no contexto. Não há resolver externo incluído.
- O filtro `--who` procura substring no remetente **e no excerpt**. Não é resolução de entidade nem busca vetorial.
- O teste de janela não transforma a CLI num mecanismo de retenção. Nenhum arquivo é expurgado automaticamente.
- O volume aproximado citado nas lições antigas não é benchmark nem limite universal seguro.

### Classificação e correções

- `who_kind` usa substrings e heurísticas. Pode errar nomes e domínios; não é classificador de segurança ou privacidade.
- Não identifica se uma gravação é pessoal/profissional, demonstração ou fala do titular da conta.
- `ts` usa hora do append por padrão. Para refletir o horário real da origem, o produtor precisa fornecê-lo.
- Correção append-only precisa de referência nova/versionada e semântica de reconciliação fora deste exemplo. Reusar a mesma `ref` não atualiza o conteúdo.

### Segurança e integrações

- Sem autenticação, ACLs, cifragem, rate limit, paginação, retry de fornecedor, API de produção ou scheduler.
- Criar arquivos privados com permissões adequadas é responsabilidade da implantação; o exemplo usa permissões do processo/umask.
- Nenhum comando desta documentação autoriza ligar coleta de mensagens, gravações ou email.
- Não há transferência entre cérebros, classificação por LLM ou sistema de produção editorial executável neste repo.

## O que foi verificado nesta atualização

O protocolo de revisão usa dados sintéticos e não chama APIs de coleta:

1. Smoke tests do ledger original.
2. Integração CLI: primeiro append, replay sem duplicata, leitura do mesmo arquivo, filtro, janela temporal e argumento inválido.
3. Links locais da documentação.
4. Revisão dos documentos para distinguir capacidade real, piloto e proposta.
5. Inspeção de privacidade e higiene básica, sem transformar busca por padrões em garantia absoluta de ausência de segredos.
6. Após publicação, comparação do commit e da árvore remota com o conjunto revisado.

Os recibos específicos da publicação ficam no PR correspondente. Esse protocolo não reexecuta os coletores privados, a entrega no Desktop ou o rebuild documental de produção.

## Gates antes de expandir a operação

**Conversas pessoais:** reconciliar o destino interno, implementar classificador e confirmação humana, testar material misto e impedir vazamento no digest profissional antes de ativar encaminhamento.

**Newsletters:** aprovar fontes e escopo, escolher owner, coletar corpo autorizado, preservar autoria/republicação, verificar profundidade e testar destinos. Não marcar como lido nem arquivar como efeito colateral da captura.

**Motor de ideias recorrente:** validar o piloto e a voz, definir critérios e cadência, limitar fontes ao escopo autorizado, construir recibos de execução e entrega. Não começar por cron quando o resultado editorial ainda está sendo refinado.

**Atlas vivo:** substituir mocks por fontes autorizadas, mostrar origem/freshness/limitações, testar permissões e leitura real. Um grafo bonito sem essas propriedades continua sendo demonstração.

**Ledger em produção:** implementar e testar validação, lock/atomicidade adequados ao ambiente, falhas e replay, permissões, backup e recuperação. Medir volume real antes de escolher banco ou complexidade adicional.
