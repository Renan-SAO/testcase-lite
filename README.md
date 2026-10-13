# TestCase Lite

Aplicação web acadêmica para cadastrar casos de teste, registrar execuções e consultar indicadores básicos de qualidade.

## Funcionalidades
- Listagem, cadastro, edição e exclusão de casos de teste.
- Registro de execuções como `APROVADO`, `REPROVADO` ou `BLOQUEADO`.
- Histórico de execuções por caso, incluindo observações e evidências em imagem.
- Upload opcional de evidências PNG, JPG, JPEG, GIF ou WEBP (até 5 MB) por execução.
- Exclusão de casos com confirmação; a exclusão também remove o histórico e os arquivos de evidência associados.
- Painel com totais de casos e execuções por resultado.
- Assistente demonstrativo de sugestões iniciais de cenários a partir de um requisito.
- Testes automatizados com pytest e execução contínua via GitHub Actions.

## Tecnologias
Python, Flask, Flask-SQLAlchemy, SQLite, HTML, Bootstrap e pytest.

## Requisitos
- Python 3.12 recomendado (Python 3.10+ deve funcionar com as dependências declaradas).
- Git opcional para execução local; necessário para versionamento e publicação.

## Instalação no Windows
Abra o Prompt de Comando ou PowerShell na pasta do projeto.

1. Crie um ambiente virtual:

   ```powershell
   py -m venv .venv
   ```

2. Ative o ambiente:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Se estiver usando o Prompt de Comando (cmd.exe), use:

   ```bat
   .venv\Scripts\activate.bat
   ```

3. Instale as dependências:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```

4. Inicie a aplicação:

   ```powershell
   python run.py
   ```

5. Abra o navegador em http://127.0.0.1:5000

O banco de dados é criado automaticamente em `instance/testcase_lite.db`. Imagens enviadas ficam em `instance/evidence/`. Esses dados locais não devem ser publicados no GitHub.

Para encerrar, volte ao terminal e pressione `Ctrl+C`.

## Executar os testes
Com o ambiente virtual ativado:

```powershell
python -m pytest -v
```

Para ver uma estimativa de cobertura:

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

Os testes usam um banco temporário separado dos dados locais.

## Primeiro uso
1. Clique em **Novo caso de teste**.
2. Preencha título, passos de execução e resultado esperado.
3. Abra o caso cadastrado.
4. Registre uma execução com resultado aprovado, reprovado ou bloqueado.
5. Se quiser, selecione uma imagem no campo **Evidência em imagem** ao registrar a execução.
6. Volte ao painel para conferir os indicadores. A lista usa numeração visual sequencial; os IDs internos do banco não são alterados.
7. Abra **Assistente de sugestões** para experimentar o fluxo demonstrativo.
8. Para excluir um caso, use **Excluir** e confirme a mensagem. O caso, seu histórico e as evidências associadas serão removidos.

## Estrutura do projeto
- `app/routes.py`: rotas web.
- `app/models.py`: entidades de banco.
- `app/services.py`: validações, regras e métricas.
- `instance/`: banco de dados e arquivos de evidência locais (não versionar).
- `app/templates/`: páginas HTML.
- `tests/`: testes automatizados.
- `docs/test-plan.md`: plano de testes.
- `docs/ai-usage.md`: documentação do uso e limites da IA.
- `.github/workflows/tests.yml`: execução automática dos testes no GitHub.

## Uso de IA
A IA pode ser utilizada como apoio ao planejamento, implementação, revisão de testes e documentação, sempre com validação humana. O assistente incluído nesta versão usa sugestões locais demonstrativas; ele **não está conectado a um modelo generativo externo**. Veja `docs/ai-usage.md`.

## Critérios de aceite
- A aplicação inicia conforme as instruções.
- Os casos podem ser criados, editados, consultados e excluídos.
- O histórico de execução é preservado até a exclusão do caso correspondente.
- Evidências de imagem são associadas à execução e removidas quando o caso é excluído.
- Os indicadores refletem as execuções registradas.
- A suíte de testes automatizados passa.

## Limitações e evolução futura
Este é um MVP local e acadêmico. Não possui login, controle de acesso, integração com ferramentas externas ou execução automática de sistemas sob teste. Evoluções possíveis: integração opcional com um modelo generativo, exportação de relatórios e filtros adicionais.

## Atualizar uma cópia existente sem perder os dados

Antes de trocar de pasta ou usar uma versão atualizada, pare o servidor com `Ctrl+C` e faça uma cópia de segurança do arquivo `instance/testcase_lite.db`. Copie esse arquivo para a pasta `instance/` da nova versão antes de iniciar o aplicativo. Se você já tiver imagens de evidência, copie também a pasta `instance/evidence/`. Nunca envie o banco de dados nem evidências privadas ao repositório público.

## Publicação no GitHub

Antes de publicar, confirme que `instance/`, arquivos `.db`, ambientes virtuais, credenciais e imagens de teste privadas não estão incluídos no commit. O arquivo `.gitignore` já exclui `instance/` e `.env`.

## Licença
Projeto acadêmico. Pode ser reutilizado e adaptado para fins educacionais.
