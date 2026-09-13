# Ambientes, agentes e governança

[Índice](../README.md) · [Arquitetura](arquitetura.md)

## Mapa lógico dos ambientes

O mapa abaixo descreve responsabilidades. Não revela hosts, credenciais, paths operacionais ou configurações de contas. Não é um manifesto de deploy.

| Ambiente | Responsabilidade | Fronteira |
|---|---|---|
| Agente principal / masterbrain | Orquestrar prioridades, contexto privado de negócios, decisões e destino das informações | Não espelhar seu cérebro inteiro no time |
| Agente pessoal | Família, relações, saúde, casa e demais assuntos pessoais | Receber somente contexto destinado e autorizado; não enviar intimidade para o editorial |
| Cérebro editorial / Content Wiki | Referências editoriais autorizadas, ideias, voz, briefings, versões e produção | Não é arquivo de contratos, credenciais ou raw de conversas privadas |
| Cérebro da empresa de educação | Conhecimento e operação compartilhável de produtos, comunidade e equipe | Só material adequado ao time e ao escopo aprovado |
| Cérebro da empresa de serviços | Operação compartilhável de execução e entrega a clientes | Não herdar acesso ao privado só porque participa do mesmo ecossistema |
| Runtime | Executar ferramentas, guardar sessão, filas, secrets e estado dos jobs | Estado de execução não é automaticamente fonte canônica versionada |
| Repositório de referência público | Explicar métodos com código mínimo e exemplos sintéticos | Não hospedar backups dos ambientes acima |
| Worktree/branch de trabalho | Desenvolver e revisar uma mudança isolada | Não substituir `main` como estado canônico do time |

O roteamento de conversas pessoais está **definido como direção**, mas a transferência automatizada do Plaud e a reconciliação dos mapas de leitura do ambiente pessoal ainda são pendências de implementação no checkpoint de 13/09/2026. O desenho não deve ser apresentado como conexão pronta.

## Fonte canônica, runtime e índice

- **Fonte canônica:** documento de domínio que contém o estado e sua evidência.
- **Git:** versionamento, revisão e distribuição desses artefatos, dentro do que pode ser versionado.
- **Runtime privado:** credenciais, transcrições, filas, sessões e logs sensíveis conforme a política de cada implantação.
- **Mirror de leitura:** cópia para consulta; não vira checkout de escrita por conveniência.
- **Índice:** estrutura derivada para localizar informação. Precisa declarar a versão da fonte e o último refresh.

Arquivo salvo localmente, commit publicado, PR aberto, merge em `main`, índice atualizado e mensagem entregue são eventos diferentes. O recibo deve dizer qual ocorreu. Um agente do time que lê apenas `main` não recebeu uma alteração que continua numa branch.

## Como enviar sem espelhar

Classificar o conteúdo antes da transferência:

1. **Nota leve compartilhável:** capturar no inbox aprovado do destino, com autoria e referência adequada. Não encaminhar anexos privados por reflexo.
2. **Artefato de equipe:** produzir na área de autoria, revisar em branch/PR e considerar canônico quando incorporado ao ramo que o time consome.
3. **Conteúdo sensível:** permanecer no ambiente privado autorizado. Quando houver necessidade operacional, compartilhar apenas o status mínimo permitido, não o corpo do documento.

Uma ideia editorial pode nascer de uma conversa privada sem exigir o envio da conversa. O agente pode preparar uma hipótese generalizada, manter a evidência privada e aguardar a decisão de exposição do autor. Se até a hipótese revelar identidade ou um caso reconhecível, não deve ser compartilhada sem revisão.

## Agentes especialistas e responsabilidade

O principal pode delegar pesquisa, implementação, edição e revisão. A delegação especifica:

- Objetivo e critério de aceite.
- Fontes que o especialista pode ler.
- Arquivos que pode alterar e destinos proibidos.
- Ferramentas/ações externas autorizadas.
- Formato de devolução, evidências e lacunas.

O especialista não ganha permissão adicional por ter uma ferramenta disponível. Uma afirmação de conclusão não basta: o principal abre o artefato, executa a verificação aplicável e confirma o efeito externo antes de relatar sucesso.

Para frentes independentes, usar arquivos ou worktrees com ownership explícito. Não pedir a dois agentes para editar o mesmo trecho simultaneamente. Um revisor independente procura contradições, vazamentos e critérios não atendidos, não apenas melhora a redação.

## Controle de side effects

Cada coletor, agendador, publicador ou sincronizador tem um responsável ativo. Na instalação que originou o padrão, Hermes é o runtime principal; OpenClaw permanece somente como histórico, sem fallback de automação. Outra instalação precisa declarar seu próprio owner, não copiar um nome de runtime como se fosse configuração válida.

Antes de ligar uma integração:

- Qual conta e qual escopo serão acessados?
- Qual processo já executa a mesma função?
- Quem guarda credenciais e como serão obtidas sem aparecer nos logs?
- A operação só lê ou também escreve, envia, agenda ou publica?
- Como impedir duas instâncias simultâneas?
- Onde fica o recibo de sucesso, falha e ausência de novidade?
- Qual é o rollback sem perda de dados novos?

Um cron documentado não prova cron ativo. Um token válido não autoriza novos grupos de mensagens, contas ou destinatários. Nunca fazer deploy de exemplo com credenciais da instalação original.

## Estado e correções

Informação nova pode alterar mais de um lugar, mas cada campo tem uma fonte de verdade. Exemplo sintético: uma data confirmada atualiza o cockpit do evento; agenda e deadline recebem a mudança pertinente; o diário registra a alteração. Cópias de contexto antigo não devem reabrir uma tarefa já encerrada.

Ao corrigir:

1. Encontrar a fonte vigente e o registro de origem.
2. Preservar o histórico necessário.
3. Atualizar o estado no destino correto.
4. Propagar somente os reflexos aplicáveis.
5. Invalidar ou atualizar caches que possam contradizer o novo estado.
6. Verificar a leitura do consumidor real.

## Política para dados pessoais e mistos

As quatro categorias propostas para conversas são pessoal, profissional, misto e a confirmar. O assunto e a intenção pesam mais que o nome do participante. Um amigo pode discutir trabalho; um colega pode compartilhar algo pessoal.

Quando houver dúvida, manter a fonte privada no local autorizado e perguntar antes de propagar. Em material misto, relacionar os recortes ao mesmo original sem criar uma cópia íntima em todos os cérebros. Uma história pode ser preservada sem virar tarefa, pauta ou perfil definitivo sobre alguém.

A classificação de remetente do exemplo público não faz esse trabalho. `who_kind=person` não significa contexto pessoal; `who_kind=tool` pode apontar para uma transcrição de conversa humana.

## Checklist de handoff entre ambientes

- [ ] Destino, escopo e responsável definidos.
- [ ] Corpo revisado para informações privadas e de terceiros.
- [ ] Referências permitem rastrear sem abrir permissões indevidas.
- [ ] Documento identifica hipótese, decisão, piloto e operação real.
- [ ] Arquivo está no checkout de autoria correto.
- [ ] Branch/PR e merge correspondem à política do destino.
- [ ] SHA remoto e conteúdo do alvo foram lidos após a escrita.
- [ ] Consumidor ou índice relevante enxerga a versão adequada.
- [ ] Recibo foi registrado no ambiente de origem, sem duplicar o corpo privado.
