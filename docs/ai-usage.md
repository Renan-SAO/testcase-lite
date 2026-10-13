# Uso de inteligência artificial

## Uso durante o desenvolvimento
A IA generativa pode apoiar planejamento, explicação de código, elaboração de cenários de teste, revisão do README e identificação de casos-limite. Todo conteúdo sugerido deve ser revisado, executado e validado antes de ser incorporado.

## Funcionalidade demonstrativa no produto
O menu “Assistente de sugestões” oferece sugestões iniciais locais a partir de um requisito. Esta versão não chama um modelo generativo: usa textos-modelo para demonstrar o fluxo sem depender de chave de API ou conexão externa. As sugestões não são consideradas verdade absoluta e devem ser revisadas por uma pessoa.

## Possível evolução
Integrar um provedor de IA generativa por meio de uma variável de ambiente para a chave de API, mantendo a funcionalidade isolada e opcional. Não enviar informações confidenciais para o provedor.

## Exemplos de prompts para registrar durante o trabalho
- “Sugira cenários positivos, negativos e casos-limite para este requisito, com pré-condições, passos e resultado esperado.”
- “Revise estes testes automatizados e identifique regras de negócio importantes que ainda não estão cobertas.”
- “Revise o README para que uma pessoa iniciante consiga instalar, executar e testar a aplicação.”

Registre quais sugestões foram aproveitadas, modificadas ou descartadas. Não declare que uma integração generativa existe enquanto ela não estiver implementada e validada.
