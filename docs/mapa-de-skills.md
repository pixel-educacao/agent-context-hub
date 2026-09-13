# Mapa de procedimentos: captura, análise e conteúdo

[Índice](../README.md) · [Motor de ideias](motor-de-ideias.md)

## Por que usar skills

Uma skill é um procedimento recuperável, não uma tarefa em andamento nem uma coleção de textos. Ela explica quando usar, quais fontes consultar, quais decisões tomar, o que verificar e onde registrar o resultado. O agente escolhe a habilidade conforme o pedido, em vez de carregar todas as instruções sempre.

Os nomes abaixo identificam procedimentos consultados na implantação de referência. **Os arquivos privados de skills não estão distribuídos neste repo.** As explicações públicas permitem reconstruir o método, mas não instalam ferramentas, prompts de identidade, credenciais ou automações.

## Cadeia de trabalho

| Procedimento de referência | Quando entra | Resultado | Gate indispensável |
|---|---|---|---|
| `agent-context-ingestion-systems` | Desenhar ingestão de múltiplas fontes | Contratos de captura, memória, recuperação e ownership | Inventariar produtores existentes antes de criar novos |
| `meeting-transcript-ingestion` | Integrar e operar fontes de transcrição | Original privado, coleta rastreável e recuperação | Transcrição real separada de resumo/metadados |
| `meetings-transcript` | Analisar fontes de reuniões em conjunto | Fatos deduplicados, contexto e digest conforme escopo | Não confundir coleta, classificação e entrega |
| `context-ledger` | Responder o que chegou ou integrar um produtor | Índice curto, ref estável e consulta por janela | O ledger não contém toda a conversa |
| `long-form-source-ingest` | Ler fonte longa e extrair conhecimento | Fonte preservada, inventário, lições e aplicações atribuídas | Cobertura da fonte antes de alegar leitura integral |
| `personal-content-production` | Transformar contexto em material para escrita pessoal | Ideias, aprofundamento e caderno editorial | Não gerar post final quando o pedido é pensar e escolher |
| `content-wiki-operations` | Ler ou registrar no destino editorial autorizado | Artefato editorial canônico, com versão e links | Separar authoring, branch e `main`; revisar privacidade |
| `humanizer` | Revisar uma peça em nome do autor | Texto sem padrões artificiais, preservando sentido | Ler voz do canal; lint não substitui revisão editorial |
| Skills do formato | Produzir a peça escolhida | Post, roteiro, newsletter, carrossel ou outra peça | Ideia escolhida, formato e autorização definidos |

Esta é a cadeia pertinente ao motor, não um inventário de todas as skills existentes no ecossistema. A existência de uma skill não comprova que esteja ativa num cron.

## Como analisar uma fonte longa sem achatá-la

1. **Inventário:** identificar exatamente quais documentos, vídeos, páginas ou segmentos compõem a fonte. Declarar exclusões e o que está ausente.
2. **Preservação:** guardar original e extração legível, com autoria, origem, data e referência estável. Se houver conversão, conferir integridade e limites.
3. **Leitura:** ler o conteúdo completo em partes delimitadas. Um resumo anterior serve como pista, nunca como prova de cobertura.
4. **Extração por fonte:** registrar situação original, problema, mecanismo explicado, sequência prática, exemplos, alternativas e limites. Uma lição precisa ser compreensível sem abrir várias notas.
5. **Síntese transversal:** agrupar temas e eliminar repetições de formulação, sem apagar diferenças entre casos. Contagem de lições por fonte não é contagem de ensinamentos únicos.
6. **Aplicação:** dizer por que o mecanismo poderia servir ao contexto atual, qual o primeiro experimento e o que ainda não se sabe. Nossa proposta não vira ensinamento atribuído ao autor.
7. **Revisão independente:** comparar síntese e fontes. Verificação numérica de cobertura ajuda, mas não certifica interpretação.
8. **Propagação:** guardar no destino pedido e atualizar apenas compromissos ou decisões sustentados pelo material. Estudo não autoriza execução da estratégia estudada.

### Ficha mínima de uma lição

```text
Fonte e localizador:
Contexto original:
Problema ou decisão:
Mecanismo explicado:
Exemplo concreto:
Sequência de aplicação:
Limites/contraexemplos:
O que é afirmação do autor:
O que é nossa interpretação:
Aplicação proposta no contexto atual:
Evidência que ainda falta:
```

Não impor cota de lições para aparentar profundidade. Uma aula curta pode ter um mecanismo forte; uma transcrição longa pode repetir o mesmo ponto.

## Diferenciar quatro saídas

**Resumo de fonte:** explica o que a fonte diz, sem introduzir um plano operacional próprio como se fosse parte dela.

**Aprendizado reutilizável:** explica um mecanismo e suas condições de aplicação, mantendo procedência.

**Atualização operacional:** muda estado, compromisso ou decisão em uma fonte canônica. Requer evidência de que essa mudança ocorreu ou foi assumida.

**Ideia editorial:** propõe uma pergunta, tensão, tese ou história a desenvolver. Pode combinar fontes, mas preserva autoria e lacunas.

Uma análise pode produzir mais de uma saída. Cada uma precisa de rótulo, destino e evidência próprios.

## Voz e revisão de uma peça

Aprovar a arquitetura do motor não aprova um template final nem a voz de uma peça. Antes de produzir:

- Ler amostras e regras reais do canal, não inventar uma voz genérica de fundador.
- Carregar o procedimento do formato escolhido.
- Conferir fatos, citações, números e origem dos exemplos.
- Revisar padrões de linguagem artificial sem enfraquecer a tese.
- Manter bloqueios de revisão visíveis. Um lint verde não prova que o texto representa a pessoa.
- Separar aprovação do rascunho, aprovação da arte e autorização de publicação.

## Aprendizado do sistema

Correções recorrentes pertencem à skill correspondente. Estado de cliente pertence ao cockpit do cliente. Preferências estáveis podem integrar memória compacta; o contexto aprofundado continua na fonte apropriada.

Ao melhorar uma skill, registrar a regra aplicável e a forma de verificar. Evitar relatos de sessão, segredos e regras tão específicas que só funcionam uma vez. Revisar se a mudança altera permissão ou escopo antes de incorporá-la.

## Como recriar uma skill em outro ambiente

Use esta estrutura, sem copiar instruções privadas:

```text
Nome e finalidade
Gatilhos e quando não usar
Pré-requisitos e permissão
Entradas e fontes de verdade
Passos com decisão e tratamento de falhas
Saída e destino
Critérios de aceite
Verificação e recibo
Limites conhecidos
Referências de aprofundamento
```

Comece pelo procedimento manual testável. Automatize somente depois de entender entradas, exceções e qualidade de saída. O motor precisa ajudar a decidir e agir, não apenas produzir mais arquivos.
