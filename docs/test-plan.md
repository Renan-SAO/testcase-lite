# Plano de testes — TestCase Lite

## Objetivo
Validar cadastro e manutenção de casos de teste, registro do histórico de execução e consistência dos indicadores do painel.

## Escopo
- Cadastro, edição, exclusão e consulta de casos.
- Validação dos campos obrigatórios.
- Registro de resultados permitidos.
- Preservação do histórico de execuções.
- Upload e validação de evidências em imagem.
- Remoção de evidências associadas à exclusão do caso.
- Indicadores do painel.
- Tratamento de identificadores inexistentes.

## Ambiente
Python 3.12, Flask, SQLite e pytest. Os testes automatizados utilizam um banco temporário separado dos dados locais.

## Cenários
| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| CT01 | Abrir painel sem dados | Página abre e indicadores ficam zerados | Integração |
| CT02 | Cadastrar caso válido | Caso persistido | Integração |
| CT03 | Cadastrar sem título | Cadastro rejeitado | Integração |
| CT04 | Cadastrar sem passos | Cadastro rejeitado | Integração |
| CT05 | Editar caso existente | Dados atualizados | Integração |
| CT06 | Excluir caso existente | Caso removido | Integração |
| CT07 | Registrar execução aprovada | Execução persistida | Integração |
| CT08 | Registrar resultado inválido pela regra de negócio | Erro de validação | Unitário |
| CT09 | Registrar duas execuções | Histórico mantém ambas | Integração |
| CT10 | Consultar caso inexistente | HTTP 404 | Integração |
| CT11 | Conferir indicadores com três resultados | Contagens correspondem aos dados | Unitário |
| CT12 | Consultar painel vazio | Indicadores zerados | Unitário |
| CT13 | Excluir caso com histórico | Caso e execuções removidos | Integração |
| CT14 | Registrar execução com imagem válida | Evidência salva e exibida no histórico | Integração |
| CT15 | Enviar extensão não permitida | Upload rejeitado sem registrar execução | Integração |
| CT16 | Excluir caso com evidência | Arquivo da evidência também removido | Integração |

## Critérios de aceite
- Todos os testes automatizados passam.
- Os campos obrigatórios não aceitam valores vazios.
- Apenas APROVADO, REPROVADO e BLOQUEADO são aceitos.
- Evidências aceitam PNG, JPG, JPEG, GIF ou WEBP até 5 MB.
- Excluir um caso remove o histórico e arquivos de evidência associados.
- Os indicadores refletem execuções registradas, não apenas casos cadastrados.
- Os testes não usam o banco de desenvolvimento.

## Limitações
Os testes automatizados validam regras e rotas, mas não substituem a inspeção manual da interface em navegador. A funcionalidade de sugestões é demonstrativa e não usa um modelo generativo externo nesta versão.
