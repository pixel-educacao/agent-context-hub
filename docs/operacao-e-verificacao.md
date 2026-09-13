# Operação e verificação: provar cada fronteira

> **Dois escopos diferentes:** a seção 1 executa somente o ledger sintético deste repositório. As demais seções são runbooks de engenharia derivados de uma implantação privada consultada em **13/09/2026**. Exigem implementação, autorização e descoberta do ambiente; não são comandos de instalação deste Hub.

Veja [Captura e recuperação](captura-e-recuperacao.md) para os conceitos. Regra de operação: **um arquivo existente, um exit code zero ou um job configurado não comprovam o pipeline inteiro**.

## 1. Executar e verificar o que este repositório contém

### 1.1 Smoke do ledger

Na raiz deste checkout, com Python disponível:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 reference/test_ledger.py
```

O teste usa dados sintéticos e diretórios temporários. Examina a ordem de classificação de remetentes, corte de excerpt, append/dedupe/esquema e consulta por janela. Seu resultado não valida autenticação, concorrência, segurança de um conector real ou recuperação de transcrições.

### 1.2 Produtor, replay e consulta sem criar dados no repo

Este exemplo para shell POSIX cria um diretório temporário privado. Todos os conteúdos vêm de `fake_source_pull()`; nenhuma API é chamada.

```sh
umask 077
DEMO_DIR="$(mktemp -d)"
export LEDGER_PATH="$DEMO_DIR/ledger.jsonl"
export PYTHONDONTWRITEBYTECODE=1

python3 reference/example_producer.py
python3 reference/example_producer.py
python3 reference/ledger_query.py --since 7d --limit 10
```

No primeiro run, o produtor deve acrescentar suas entradas sintéticas; no segundo, deve ignorá-las por dedupe. Confirme os contadores produzidos pelas execuções, em vez de assumir que o comando funcionou.

Valide o arquivo sintético estruturalmente:

```sh
python3 -c 'import json, os; from pathlib import Path; rows=[json.loads(x) for x in Path(os.environ["LEDGER_PATH"]).read_text().splitlines() if x.strip()]; expected={"ts","source","who","who_kind","excerpt","ref"}; assert rows; assert all(set(r)==expected for r in rows); assert all(r["ref"] for r in rows); assert len({r["ref"] for r in rows})==len(rows); print("schema e unicidade: ok")'
```

Depois, remova somente o artefato criado por este exemplo e desfaça suas variáveis:

```sh
python3 -c 'import os; from pathlib import Path; p=Path(os.environ["LEDGER_PATH"]); p.unlink(); p.parent.rmdir()'
unset LEDGER_PATH DEMO_DIR PYTHONDONTWRITEBYTECODE
```

**Limitações do CLI:** `--since` usa a sintaxe `Nd`; `--who` filtra substrings de remetente e excerpt. A consulta percorre o arquivo local e restringe o resultado apresentado, mas não implementa FTS, resolver de fontes, cursor de API ou consulta semântica. Os itens são exibidos na ordem do arquivo, não ordenados automaticamente por relevância ou pelo timestamp mais recente. Linhas inválidas podem ser ignoradas pelo leitor: ausência no resultado não substitui validação de integridade.

A leitura por janela evita despejar o ledger inteiro no contexto do agente; não significa que o arquivo inteiro deixou de ser lido pelo processo Python.

### 1.3 Revisão documental

```sh
git diff --check
```

Esse comando verifica problemas de whitespace no diff. Não detecta sozinho segredos, afirmações falsas, links quebrados ou material pessoal. Também é preciso revisar os arquivos novos que ainda não estão no diff de arquivos rastreados.

### O que não executar como se existisse aqui

Os coletores privados, o sincronizador do catálogo, o preparador de batches e o guard de frescor GBrain **não estão em `reference/`**. Este Hub também não fornece `connect`, `doctor`, instalador de MCP, `purge`, cron ou mecanismo de entrega. As ações descritas adiante são contratos para a implementação de quem adotar o padrão, não CLIs disponíveis neste checkout.

## 2. A matriz de evidência

Use um recibo separado para cada capacidade. Uma coluna verde não torna a seguinte verde.

| Capacidade | Evidência mínima | Não aceitar como substituto |
|---|---|---|
| Autenticação | Chamada de metadados na conta/escopo autorizados | Credencial salva no cofre |
| Acesso ao corpo | Canário limitado com fala válida ou ausência explicitamente diagnosticada | Título ou resumo presente |
| Persistência | Raw parseável, privado e associado à referência literal | Resposta da API vista no terminal |
| Idempotência | Replay limitado sem duplicar registros; refresh igual sem revisão falsa | Arquivo existente antes do run |
| Indexação local | Referência no catálogo e termo do corpo recuperado | Contagem de linhas do ledger |
| Resolução | Resultado leva ao raw correto e legível | Snippet sem origem |
| Dedupe de evento | Grupo corroborado ou revisão explícita de ambiguidade | Títulos parecidos |
| Propagação | Leitura dos destinos canônicos depois da escrita | Ack, daily ou digest sozinho |
| Digest | Artefato gerado com origem e cobertura reconhecidas | Classificação concluída |
| Entrega | Leitura posterior do destino confirma a mensagem/artefato | Produtor retornou sucesso |
| GBrain | Sync final reconhecido, recibo fresco e recuperação documental | Serviço online ou exit zero |
| Scheduler | Execução observada, status, horário/fuso e próximo run coerentes | Arquivo de script ou tabela de horários |

O recibo público deve conter apenas estados e agregados. Mapeamentos de IDs, logs detalhados e referências que identifiquem pessoas pertencem ao ambiente privado autorizado.

## 3. Runbook: habilitar uma fonte sem abrir o acervo inteiro

**Aplicabilidade:** implantação própria; não realizado pelo toy público.

### Pré-condições

- [ ] Fonte, conta, dono da operação e finalidade definidos.
- [ ] Escopo de leitura autorizado: gravações próprias, compartilhadas, equipe ou seleção manual.
- [ ] Documentação vigente do fornecedor revisada: plano, auth, limites, paginação e acesso ao corpo.
- [ ] Destino privado fora do checkout público; política de permissões, backup e retenção definida.
- [ ] Nenhum coletor concorrente com a mesma responsabilidade.
- [ ] Janela e quantidade máxima de coleta escolhidas antes da execução.
- [ ] Caminho de pausa/rollback conhecido; nenhuma alteração implícita no scheduler.

### Autenticação sem expor segredos

Guarde credenciais em cofre ou mecanismo local aprovado. Não use argumentos de shell, exemplos versionados ou mensagens de chat para carregá-las. Logs não devem repetir headers, URLs assinadas, corpos de erro do fornecedor ou variáveis de ambiente.

Para API key, prove a credencial com uma chamada de leitura. Para OAuth/MCP, confirme conta e sessão apropriadas e use o fluxo oficial; não leia ou copie tokens para criar um segundo caminho de autenticação. Conexão MCP disponível não é autorização para login, instalação ou atualização automática de pacotes.

Uma implantação pública futura precisa oferecer onboarding próprio. Reutilizar uma sessão OAuth já existente na instalação privada não é um fluxo de instalação reproduzível para outra pessoa.

### Canário A: apenas metadados

1. Solicitar uma página pequena sem transcript/resumo pesado.
2. Verificar código de retorno, shape, IDs estáveis, paginação e janela de visibilidade.
3. Emitir apenas status e contagens, sem títulos, participantes ou links.
4. Confirmar que nenhum corpo foi buscado ou raw criado nesta modalidade.

**Gate:** autenticação e visibilidade do inventário provadas; corpo ainda não verificado.

### Canário B: corpo limitado

1. Selecionar um pequeno conjunto autorizado de registros.
2. Preservar a resposta nativa privadamente.
3. Validar conteúdo real: fala não vazia, ordem das páginas e campos de segmento quando disponíveis.
4. Tratar ausência, conteúdo ainda não pronto, erro de autorização e paginação incompleta como estados diferentes.
5. Não inferir completude quando bateu o limite de páginas ou apareceu cursor repetido.
6. Se o acervo de teste não tem transcrição longa, registrar essa lacuna; exercitar paginação longa com fixtures sintéticas.

**Gate:** acesso ao corpo e fidelidade do parser no escopo testado. Não prova qualidade da transcrição ou cobertura histórica total.

### Canário C: replay e recuperação

1. Reexecutar a mesma seleção.
2. Conferir que não surgem novas identidades para a mesma origem.
3. Fazer refresh controlado; conteúdo igual não deve criar revisão falsa.
4. Buscar uma expressão presente **no meio do corpo e ausente do título/resumo**.
5. Resolver o resultado e abrir o raw correto.
6. Conferir que o teste não vazou conteúdo em Git, stdout, logs ou recibos públicos.

**Gate:** captura → arquivo → catálogo → resolução no escopo do canário. Propagação e entrega continuam gates separados.

## 4. Runbook: “a reunião já apareceu?”

1. Resolver data, horário e contexto do evento sem confundir reuniões semelhantes do mesmo dia.
2. Consultar ou atualizar de modo limitado cada provedor ativo e autorizado.
3. Separar os resultados:
   - metadados encontrados;
   - resumo/nota disponível;
   - transcrição com fala não vazia;
   - nenhuma entrada independente visível ainda;
   - consulta inconclusiva por falha técnica.
4. Se transcript veio vazio, verificar parâmetro de inclusão, endpoint específico e paginação antes de afirmar ausência de acesso.
5. Se a reunião terminou há pouco e não apareceu, responder **“ainda não apareceu na consulta”**, não “não gravou”.
6. Não usar a presença da pessoa em outra reunião como prova sobre o evento perguntado.

A conclusão precisa informar o limite: fonte e janela verificadas, cobertura e falhas. Não revelar IDs, títulos privados ou participantes para demonstrar que a consulta aconteceu.

## 5. Runbook: enriquecer raw sem reabrir ack

### Antes

- [ ] Delimitar registros e motivo: transcript tardio, correção upstream ou falha de parser.
- [ ] Preservar backup privado e inventário de estado.
- [ ] Capturar uma comparação dos campos de processamento, referências reconhecidas e batches pending.
- [ ] Distinguir refresh de coleta, rebuild de índice e reprocessamento canônico.

### Durante

1. Atualizar só o conteúdo autorizado, preservando revisões anteriores.
2. Manter status de processamento e ack intactos.
3. Reconstruir o índice derivado com validação antes da substituição.
4. Reconciliar referências do catálogo e do ledger.
5. Não gerar um batch novo para substituir silenciosamente o pending existente.

### Depois

- [ ] Raw enriquecido parseável; original recuperável na política de revisões.
- [ ] Mesmo conjunto de IDs reconhecidos antes/depois.
- [ ] Pending existente idêntico; campos não relacionados ao enriquecimento preservados.
- [ ] Busca de termo do novo corpo retorna referência e tipo corretos.
- [ ] Reexecução controlada não gera mudança espúria.
- [ ] Se o conteúdo novo altera uma decisão, abrir revisão explícita; não apagar ack para “forçar o pipeline”.

**Detalhe da referência:** Plaud pode ignorar estados reconhecidos de ausência sem refresh. O job adicional usa refresh limitado justamente para reconciliar conteúdo antes indisponível. Isso não significa que todo o histórico é rechecado em cada run.

## 6. Runbook: classificar, propagar e reconhecer o lote

A preparação e o ack são mecanismos privados. O código estudado mantém estados separados para `classify` e `digest`, filtros por janela e limite de registros, além do lote pending congelado.

1. Conferir a finalidade. Um envelope de digest não autoriza escrita canônica.
2. Se há pending, reutilizar o lote existente; não selecionar outro por conveniência.
3. Conferir fonte, cobertura, atribuição e ambiguidades de dedupe.
4. Ler os destinos canônicos e procurar fatos já existentes.
5. Escrever somente fatos sustentados, com responsáveis/prazos explícitos ou incerteza indicada.
6. Manter divergências como conflito de revisão; não sobrescrever o estado vigente sem resolução.
7. Validar todos os destinos, ausência de duplicatas e nenhum raw ou alvo proibido alterado.
8. Só então reconhecer todas as referências contribuintes no ack de classificação.
9. Ler de volta o estado reconhecido e o destino do lote; emitir recibo local sem payload.

### O que o helper não verifica por você

O ack registra IDs processados e move o pending para o arquivo de reconhecidos. Ele **não inspeciona semanticamente** se a decisão foi salva no lugar certo. Essa validação pertence ao consumidor antes do ack.

Além disso, escrever o estado e mover o arquivo são operações separadas. Não há uma transação única envolvendo os documentos canônicos e o ack. Uma queda no intervalo exige reconciliação. No helper estudado, `already_acked_or_missing` também não distingue, sozinho, conclusão legítima de ausência inesperada; leia estado e arquivos antes de concluir.

A preparação com saída “somente estatísticas” pode criar pending: formato de output reduzido não significa dry-run. O preparador também não deve ser considerado uma proteção multiprocesso completa; a operação precisa garantir um único executor por finalidade.

### Se houver escrita parcial

Não reconhecer o lote. Registrar privadamente o ponto da falha, preservar pending e retomar de forma idempotente, lendo os destinos antes de inserir novamente. Se houver risco de vazamento ou duplicação recorrente, pausar o consumidor responsável até a correção.

## 7. Runbook: corrigir catálogo ou migração de fila

### Catálogo com falha

| Sinal | Diagnóstico a testar | Recuperação segura |
|---|---|---|
| Resultado vazio | Termos em `AND`, vocabulário diferente, falta de corpo ou índice ausente | Reduzir termos; conferir referência/cobertura; testar corpo conhecido |
| Resultado antigo | Coleta ou sincronização falhou | Conferir recibos por etapa; reconstruir a partir do raw válido |
| Referência resolve, raw não existe | Remoção/movimentação ou índice stale | Restaurar a origem autorizada ou reconciliar o catálogo, sem inventar evidência |
| Raw inválido | Escrita incompleta ou schema inesperado | Preservar arquivo para diagnóstico; corrigir parser/dado com revisão; não substituir índice bom por parcial |
| Catálogo atualizado, ledger atrasado | Falha após commit SQLite | Reexecutar reconciliação idempotente e comparar conjuntos de referências |
| Uma fonte falhou, catálogo passou | Índice reconstruído com dados antigos daquela fonte | Manter falha da fonte no status global; não chamar fetch de sucesso |

O orquestrador privado examinado tenta Fathom e Plaud independentemente e avalia seus resultados separadamente do catálogo. Isso contém falhas, mas não as apaga.

### Migração de queue para arquivo privado

1. Pausar escritores/coleta/classificação afetados e confirmar ausência de execuções em curso.
2. Fazer backup privado com mapa de origem/destino e verificação de integridade.
3. Copiar bytes e validar IDs antes de substituir caminhos de compatibilidade.
4. Confirmar que o destino não contém estado divergente; conflito deve interromper a migração.
5. Quando houver symlink de compatibilidade, escritores devem resolver o alvo antes de substituição atômica. Substituir o próprio symlink pode recriar uma fila paralela.
6. Reexecutar a migração para comprovar idempotência e verificar todos os destinos.
7. Retomar somente os owners aprovados e observar os próximos runs.

Um flag que afirma “escritores parados” é declaração do operador, não mecanismo que encerra processos.

**Rollback:** parar os escritores, preservar o estado privado mais recente, restaurar código/wrappers conforme o mapa de backup e reconciliar acknowledgements posteriores. Não restaurar cegamente uma fila antiga nem apagar raw enriquecido para voltar a uma versão anterior do código.

## 8. Runbook: verificar frescor documental no GBrain

GBrain é uma camada separada. Um guard privado examinado aplica gates antes/depois da sincronização:

1. **Corpus legível:** Markdown sem bytes NUL, encoding inválido ou frontmatter YAML quebrado. Erros expõem classe/localização privada, não conteúdo.
2. **Verdicto final reconhecido:** algumas ferramentas podem sair com código zero mesmo quando o resultado é parcial ou bloqueado. Inspecionar o resultado final esperado, não apenas o exit code.
3. **Checkpoint coerente:** quando o sync informa revisão, ela precisa corresponder à revisão pretendida.
4. **Recibo fresco:** identificar exatamente uma fonte, confirmar destino do corpus, páginas não vazias e timestamp de sync posterior ao início da operação, com timezone.
5. **Consulta real:** recuperar um documento escolhido para o teste e conferir a versão desejada.

Os quatro primeiros gates não substituem o quinto. Um recibo fresco não certifica qualidade de busca. Uma consulta que acerta um documento não comprova que todas as páginas foram indexadas.

Não incluir raw, queue ou ledger no corpus para corrigir uma busca documental que deveria ser resolvida pelo catálogo privado. Corrija a rota de recuperação sem ampliar silenciosamente a fronteira de dados.

## 9. Cadência e prova do scheduler

**Exemplo histórico da implantação de referência, registrado em setembro de 2026; não é default nem recomendação universal deste projeto.** Fuso: `America/Sao_Paulo`.

| Etapa | Cadência de referência |
|---|---|
| Fetch Granola | 20:45, dias úteis |
| Fetch adicional Fathom/Plaud e catálogo | 20:50, dias úteis |
| Classificação e propagação | 21:05, dias úteis |
| Produção local do digest | 21:25, dias úteis |
| Entrega por consumidor separado | 09:00, diário |
| Snapshot documental GBrain | 03:00, diário |

Esses horários não estão configurados neste repo. Antes de operar uma instalação, ler scheduler e responsável atuais. Não restaurar cron antigo a partir desta tabela e não criar duplicata porque um script existe.

Checklist de promoção para recorrência:

- [ ] Aprovação do escopo, frequência, conta e entrega.
- [ ] Um owner ativo por responsabilidade; consumidores de classificação/digest separados.
- [ ] Limites por execução e tratamento de rate limit documentados.
- [ ] Próximo run com timezone coerente.
- [ ] Execução observada pelo scheduler, não apenas manual.
- [ ] Resultado por provedor, catálogo e consumidor disponível sem payload sensível.
- [ ] Nenhum ack avançou sem validação canônica.
- [ ] Entrega verificada por leitura do destino, se fizer parte do aceite.
- [ ] Critérios de pausa e responsável de recuperação conhecidos.

**Situação da referência estudada:** captura e recuperação privada foram implantadas e verificadas. A inclusão Plaud não recebeu um novo teste completo de classificação, digest e entrega. Não apresentar a cadência configurada como prova de E2E aprovado.

## 10. Falhas, pausa e lacunas explícitas

| Falha/risco | Conduta |
|---|---|
| Autenticação inválida ou revogada | Interromper a fonte afetada, manter raws válidos e reconectar por fluxo autorizado; não repetir segredos no erro |
| Rate limit, timeout ou shape inesperado | Preservar cobertura parcial e recibo de erro; retry limitado conforme a implementação, nunca loop sem limite |
| Lock abandonado | Verificar owner/processo antes de remover; idade do arquivo não basta |
| Conteúdo ainda não pronto | Registrar estado e reconciliar via refresh autorizado; não marcar transcript presente |
| Demos/importados atribuídos ao usuário | Bloquear afirmações pessoais e levar a revisão de origem |
| Pessoal/profissional ambíguo | Manter privado e não promover ao ambiente de empresa/conteúdo por aproximação |
| Ack sem escrita completa | Pausar classificação, reconciliar estado e destinos, preservar o histórico |
| Duas automações escrevem os mesmos fatos | Pausar a duplicata e definir owner único antes de retomar |
| Raw, segredo ou PII em Git/log público | Conter acesso e jobs afetados; tratar remoção, histórico e eventual rotação conforme o incidente; não basta apagar a linha corrente |
| Falha de entrega | Manter geração e recebimento como estados distintos; evitar reenvio duplicado sem checar destino |

### Gaps que o operador precisa aceitar ou fechar

- O toy público não implementa autenticação, ACL, concorrência robusta, backup, rotação, retention/purge ou resolução externa.
- Separação automática Plaud pessoal/profissional/misto está pendente na referência. O marcador de atribuição não substitui esse roteamento.
- Histórico fora das janelas/limites pode nunca entrar sem backfill deliberado. Não chamar ausência de catálogo de ausência na vida real.
- Completude de paginação upstream não garante snapshot estável se o inventário muda durante a coleta.
- FTS e ledger não oferecem uma busca semântica universal; avaliar perguntas reais antes de adicionar embeddings.
- Retenção precisa cobrir raw, revisões, catálogo, fila, ledger, backups e material já promovido. Apagar uma cópia não prova exclusão global. Este repo não automatiza esse ciclo.

## 11. Aceite de uma implementação própria

Antes de afirmar “pronto para uso”, execute uma bateria com dados sintéticos e, separadamente, um canário real autorizado:

- [ ] Mesmo item repetido produz uma identidade; duas fontes da mesma conversa preservam os dois raws.
- [ ] Duas contas com IDs iguais não colidem.
- [ ] Falta de auth não gera escrita ou resultado de outra conta.
- [ ] JSON inválido, paginação repetida, fim contraditório e limite excedido falham sem falso complete.
- [ ] Resumo sem transcript não conta como fala; speaker sem conteúdo não conta como segmento útil.
- [ ] Frase exclusiva do corpo é recuperada e resolve para o raw correto.
- [ ] Refresh preserva revisão e não reabre ack; retry preserva pending.
- [ ] Falha após escrita parcial não avança reconhecimento indevido nem duplica fatos na retomada.
- [ ] Texto de prompt injection no material recuperado permanece dado inerte.
- [ ] Destinos fora do escopo, traversal e escape por symlink são rejeitados no importador próprio.
- [ ] Reinício preserva estado; rollback não reativa fila antiga sobre reconhecimentos novos.
- [ ] Catálogo, ledger e recibos são reconciliáveis após falha entre etapas.
- [ ] Scheduler e entrega têm provas independentes.
- [ ] Logs, árvore pública e histórico não contêm material privado.

Não transformar checkboxes desta documentação em testes “aprovados” sem executá-los. Os smokes do ledger são uma primeira verificação do mecanismo, não a certificação de uma plataforma de ingestão.

### Formato de encerramento sugerido

Use um recibo curto com estes campos, preenchidos com evidência real:

```text
Escopo autorizado e janela:
Autenticação/metadados:
Corpos coletados e ausências explícitas:
Persistência e replay:
Catálogo e resolução:
Propagação/ack:
Digest/entrega:
Scheduler/frescor:
Privacidade:
Gates pendentes:
```

Não incluir valores fictícios com aparência de execução real. Quando uma etapa não foi exercitada, escrever **“não testado”**. Quando falhou, registrar **“falhou”** e o limite da conclusão: sem esconder a falha atrás do sucesso de outra camada.
