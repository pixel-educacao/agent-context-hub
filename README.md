# Agent Context Hub

**Guia técnico do motor de contexto e de sua conexão com memória, motor de ideias e produção de conteúdo.** Para quem precisa entender a arquitetura, discutir decisões e reproduzir o método sem receber o cérebro privado de uma pessoa.

O projeto começou com o **Context Ledger**, um índice append-only de sinais. Agora documenta o fluxo completo ao redor dele. O código distribuído continua sendo uma referência pequena do ledger, com produtor sintético e consulta local. Os coletores de produção, os agentes, a infraestrutura de busca e o motor editorial **não são instalados por este repositório**.

> Estado documentado em **13/09/2026**. Diferenciamos implementação privada verificada, exemplo executável neste repo, piloto manual e proposta ainda não implantada. Não há promessa de captura universal, tempo real ou publicação automática.

## Visão em uma tela

```text
Fontes autorizadas online/offline
  reuniões · mensagens · email · agenda · gravações · acervo
                  |
        captura e original privado
                  |
       +----------+--------------+
       |                         |
 ledger: o que entrou     catálogo: localizar o corpo
       +------------+------------+
                    |
       abrir fonte e interpretar com evidência
                    |
       +------------+-----------------------+
       |            |                       |
 operação       contexto pessoal       conhecimento/ideia
 dono/prazo     destino separado       autoria + hipótese
       |            |                       |
 fonte canônica e memória          caderno para pensar/escrever
                                            |
                               escolha humana + produção + revisão
                                            |
                                  publicação autorizada e verificada
```

A seta entre contextos **não representa permissão automática de transferência**. Uma conversa pode ter várias utilidades; isso não autoriza espelhar seu corpo entre ambientes.

## Por onde começar

- **Sócio ou liderança:** [arquitetura e decisões](docs/arquitetura.md), [motor de ideias](docs/motor-de-ideias.md) e [o que está pronto](docs/estado-e-limites.md).
- **Quem vai implementar:** [captura e recuperação](docs/captura-e-recuperacao.md), [ambientes e governança](docs/ambientes-e-governanca.md), [operação e verificação](docs/operacao-e-verificacao.md).
- **Quem vai editar conteúdo:** [motor de ideias](docs/motor-de-ideias.md), [produção e Atlas](docs/producao-e-atlas.md), [ficha de ideia](templates/ficha-de-ideia.md).
- **Quem quer entender as habilidades de análise:** [mapa de skills e extração de aprendizados](docs/mapa-de-skills.md).
- **Quem quer executar o código disponível:** o exemplo abaixo e [limites do ledger de referência](docs/estado-e-limites.md).
- **Quem vai usar outro agente para estudar o repo:** [roteiro de leitura e avaliação](docs/como-estudar-e-reproduzir.md).

## Experimento local reproduzível

Requisito recomendado: **Python 3.10+**, biblioteca padrão. A revisão desta atualização foi executada com Python 3.11; não é uma matriz de compatibilidade de todas as versões.

Na raiz de um clone, em shell POSIX:

```sh
git clone https://github.com/pixel-educacao/agent-context-hub.git
cd agent-context-hub
export CONTEXT_LEDGER_TZ=UTC
DEMO_DIR="$(mktemp -d)"
export LEDGER_PATH="$DEMO_DIR/demo-ledger.jsonl"
python3 reference/example_producer.py
python3 reference/example_producer.py
python3 reference/ledger_query.py --since 7d
python3 reference/test_ledger.py
python3 -m unittest discover -s tests -v
python3 tools/check_docs.py
```

O produtor usa **três registros sintéticos**, não lê nenhuma conta. A primeira execução deve adicionar três; a segunda deve ignorar os mesmos três por `ref`. A consulta usa exatamente o arquivo das duas execuções, fora do Git. O teste de integração confere esses resultados, o contrato de seis campos, a janela temporal e o filtro de consulta.

Não coloque tokens no exemplo. Para uma integração real, primeiro implemente autenticação, escopo, paginação, armazenamento privado e recuperação de falhas. O exemplo não contém esses controles.

## O contrato original do ledger

Seis campos por entrada:

| Campo | Significado |
|---|---|
| `ts` | Timestamp ISO com timezone. No exemplo, horário do append se não informado. |
| `source` | Identificador do produtor. |
| `who` | Remetente ou rótulo fornecido pelo produtor, sem inventar identidade. |
| `who_kind` | `person`, `tool`, `transactional` ou `unknown`. Heurística determinística. |
| `excerpt` | Trecho sem interpretação, truncado em aproximadamente 200 caracteres. |
| `ref` | Referência estável para dedupe e rastreamento até a fonte. |

- Capturar sem interpretação editorial. Identificar o tipo de remetente não equivale a decidir assunto, destino ou mérito.
- Não carregar o ledger inteiro no contexto do agente. Consultar janela e depois abrir as fontes necessárias.
- Não adicionar campos só porque parecem úteis; exigir uma consulta real que precise deles.
- Deduplicar eventos não resolve sozinho dedupe de fatos, pessoas, obras ou versões de transcrição.
- Append-only conserva a trilha. Correções precisam de nova referência versionada e relação explícita com o registro anterior no sistema que as consome; este exemplo não reconcilia correções automaticamente.

## O que há neste repo

- `reference/`: ledger, consulta e produtor sintético, com smoke tests.
- `docs/`: arquitetura, ambientes, ingestão, memória, operação, ideias, produção e limites.
- `templates/`: ficha vazia para testar o método editorial manualmente.
- `tests/`: integração do exemplo via CLI, sem rede.
- `tools/check_docs.py`: validação de links locais e higiene básica dos arquivos de documentação. Não substitui revisão de privacidade nem scanner especializado de segredos.
- `lessons/`: lições originais do ledger, preservadas como contexto histórico.

## Lições originais

1. [Ordem do classificador](lessons/01-classifier-order.md): transacional antes de regras genéricas de ferramentas.
2. [Hooks nos produtores](lessons/02-producer-hooks.md): capturar a referência junto da escrita do original.
3. [Orçamento de contexto](lessons/03-context-budget.md): recuperar recortes, não despejar arquivos inteiros.
4. [Higiene do índice](lessons/04-index-hygiene.md): raw e fila não entram por acidente no índice documental.
5. [Crescimento](lessons/05-growth.md): há custo na leitura integral por append; o número aproximado da nota não é benchmark ou SLA.
6. [Consulta primeiro](lessons/06-query-first.md): um índice precisa responder uma pergunta desde o primeiro dia.

Essas notas tratam da referência inicial, não certificam segurança de concorrência ou cobertura dos novos componentes. Consulte [estado e limites](docs/estado-e-limites.md) antes de reutilizar o código em produção.

## Segurança e permissão

Este é um repo **público** de padrões e exemplos. Não recebe transcrições privadas, identidades de participantes, contratos, chaves, configurações de servidores ou corpora pessoais. A matéria-prima privada pode ser preservada com riqueza no ambiente autorizado; a divulgação de qualquer trecho é uma decisão separada.

Capturar não autoriza publicar. Código presente não comprova job ativo. Job ativo não comprova entrega. Cada resultado precisa de recibo proporcional ao risco.

## Licença

MIT. Veja [LICENSE](LICENSE).
