# Como estudar, avaliar e reproduzir o sistema

[Índice](../README.md)

## Roteiro para o sócio

1. Leia [arquitetura](arquitetura.md) para entender os problemas que cada camada resolve.
2. Leia [ambientes](ambientes-e-governanca.md) para entender quem pode ler, escrever e receber cada tipo de conteúdo.
3. Leia [captura e recuperação](captura-e-recuperacao.md) para entender como encontrar o original, lidar com ausência de transcrição e evitar duplicidade.
4. Leia [motor de ideias](motor-de-ideias.md) e [produção](producao-e-atlas.md) para entender como contexto se transforma em matéria-prima editorial sem virar post automaticamente.
5. Leia [estado e limites](estado-e-limites.md) antes de concluir o que já funciona ou estimar implementação.
6. Rode o exemplo do README. Depois use uma fonte sintética na [ficha de ideia](../templates/ficha-de-ideia.md), sem ligar contas reais.
7. Consulte [operação e verificação](operacao-e-verificacao.md) para avaliar custo de manutenção, canários, falhas e rollback.

O resultado esperado dessa leitura é conseguir explicar **quem captura, onde guarda, como encontra, quem interpreta, para onde vai e quem autoriza uma ação**.

## Roteiro copiável para outro agente

O bloco abaixo é uma solicitação de análise do repositório, não uma instalação ou concessão de acesso a sistemas privados.

```text
Analise este repositório como documentação técnica de um sistema de contexto
conectado a um motor de ideias. Leia README, docs/, templates/ e reference/.

Responda em português do Brasil:
1. Explique o fluxo completo desde uma fonte autorizada até uma ação ou ideia.
2. Diferencie raw, resumo, fila, ledger, catálogo lexical, fonte canônica,
   memória nativa, memória conversacional e busca documental.
3. Mapeie os ambientes e as fronteiras de leitura, escrita e privacidade.
4. Explique critérios de seleção de ideias, autoria, dedupe e revisão editorial.
5. Separe código executável aqui, implantação privada documentada, piloto,
   mockup e proposta. Cite arquivos e trechos que sustentam cada conclusão.
6. Execute somente os testes locais sem rede, se o ambiente permitir.
   Não simule saídas. Não conecte contas nem crie automações.
7. Liste inconsistências e lacunas por impacto concreto.
8. Proponha o menor experimento seguro para validar a próxima hipótese.

Não trate exemplo sintético como fato real. Não confunda disponibilidade de
uma ferramenta com autorização. Não modifique arquivos, faça deploy ou
publique nada sem novo pedido. Se uma informação não estiver aqui, marque
como não documentada em vez de reconstruir o ambiente privado por suposição.
```

## Experimento manual de ponta a ponta do método

Este exercício valida entendimento, não substitui um teste de produção integrado.

**Entrada sintética:** uma transcrição inventada em que duas pessoas discutem por que uma automação foi abandonada. Inclua uma frase exata, uma hipótese não confirmada e um compromisso explícito. Não use nomes ou falas reais.

**Passos:**

1. Preserve o texto num diretório temporário privado e atribua uma referência sintética estável.
2. Use o produtor de exemplo para exercitar chegada/replay, ou adapte uma cópia em ambiente descartável para o formato sintético escolhido.
3. Faça a pergunta de chegada ao ledger. Depois abra o corpo: o excerpt sozinho não basta para responder sobre toda a conversa.
4. Separe frase, hipótese e obrigação. Para o compromisso, registre ação, responsável e prazo; se o prazo não existe, marque a definir.
5. Classifique o destino manualmente. Um comentário sobre família no meio da conversa não deve aparecer automaticamente no documento compartilhado de trabalho.
6. Preencha uma ficha de ideia: tensão, evidência, interpretação, aplicação e lacunas. É válido concluir que não há ideia forte.
7. Peça revisão: a tese está sustentada? A autoria foi preservada? A recomendação extrapola a fonte? A ideia é diferente de um resumo de reunião?
8. Registre o resultado como exercício. Não publique nem configure cron.

**Aceite:** outra pessoa consegue seguir a referência até a evidência, distingue o que aconteceu do que foi inferido e sabe qual etapa ainda precisa de decisão humana.

## Perguntas de análise crítica

- Se uma coleta retorna zero, como distinguir ausência de novidade de credencial expirada?
- Se o fornecedor disponibiliza a transcrição dias depois, como enriquecer a fonte sem duplicar tarefa?
- Se o mesmo compromisso aparece em três canais, onde está a obrigação única?
- Se uma busca não encontra um trecho, qual a alternativa antes de dizer que não existe?
- Se uma conversa mistura pessoal e profissional, o que bloqueia o encaminhamento errado?
- Se uma ideia parece boa mas a fonte é resumo de terceiro, como a limitação aparece?
- Se o caderno sai semanalmente, como provar que ajudou a escrever e não apenas aumentou leitura?
- Se um painel exibe status, de qual fonte e de qual horário ele veio?
- Se uma branch não foi incorporada a `main`, quem realmente enxerga a mudança?
- Se o runtime muda, quais permissões, owners e recibos precisam ser revalidados?

## Lacunas deliberadas deste repositório público

Não distribuímos dados pessoais, transcrições, catálogos privados, configurações de serviços, prompts de identidade privados ou inventário de credenciais. Também não distribuímos como se fossem genéricos os wrappers específicos da instalação original.

Para implementar em outro ambiente, o responsável precisa escolher fontes, obter autorização, definir destino e retenção, implementar conectores e testar o caminho completo. A documentação reduz a ambiguidade; não elimina esse trabalho nem o substitui por um `install` fictício.
