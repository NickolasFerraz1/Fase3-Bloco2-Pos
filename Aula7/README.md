# Aula 7

Workflows reutilizáveis (`workflow_call`) para o CI e pipeline de treinamento de ML com gatilho por caminho (`paths`). O CI da raiz passou a chamar um template guardado em outro repositório, e o pipeline de ML só dispara quando o código de modelos muda.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `ci-workflow-call-aula7.yaml` | Cópia do workflow da raiz (`.github/workflows/ci-workflow-call.yaml`): chama o template de CI do repositório `Fase3-Bloco2-Pos-Integracao` |
| `ml-pipeline-aula7.yaml` | Cópia do workflow da raiz (`.github/workflows/ml-pipeline.yaml`): preparação de dados e treinamento de teste |
| `ci-aula7.yaml` | Cópia do CI da raiz (`.github/workflows/ci.yaml`): validações de ambiente, lint, testes, treino do `.pkl` e auditoria MLOps |
| `train.py` | Gera um modelo falso (`pickle`) em `outputs/dataset_processado.pkl`, usado pela auditoria do CI |
| `src/models/teste.py` | Script de treinamento de teste, usado para disparar e validar o `ml-pipeline` |

Na raiz também foram criados `backend/app.py` e `frontend/index.html`, só para conferir que mudanças fora de `Aula7/src/models/` não disparam o pipeline.

## Pipelines

**`ci-aula7.yaml` / `.github/workflows/ci.yaml`** (ativo), disparado em `pull_request` para a `main`. Job `validacao_ambiente`:

1. instala Poetry e Python 3.10 e roda `Aula1/validate_env.py`
2. verifica com `nbstripout --verify` que `Aula2/explorer.ipynb` não tem outputs
3. instala o Ruff na versão fixa `0.4.10` (a mesma dos `poetry.lock`) e roda `ruff check .` no repositório inteiro, por isso os arquivos novos da Aula7, do `backend/` e do `frontend/` também são checados
4. Aula3: `poetry install`, ETL (`preparar_dados.py`), `dummy_train.py` e `dummy_train_governance.py`
5. Aula4: `poetry install` e `pytest tests/`
6. roda `python Aula7/train.py` para gerar o modelo `.pkl`
7. **Auditoria MLOps:** usa a action `Fase3-Bloco2-Pos-Integracao/model-action@main` sobre `Aula7/outputs/dataset_processado.pkl`, com `nivel-alerta: 'WARNING'`

**`ci-workflow-call-aula7.yaml` / `.github/workflows/ci-workflow-call.yaml`** (ativo), disparado em `push` na `main`:

- usa `uses: .../template-ci-ml.yml@main`, do repositório `Fase3-Bloco2-Pos-Integracao`
- passa os inputs `PYTHON_VERSION: '3.10'`, `working-directory: Aula4` e `path-tests: tests/`
- repassa o token com `TOKEN_GITHUB: ${{ secrets.GITHUB_TOKEN }}`. Nomes que começam com `GITHUB_` são reservados e não podem ser declarados em `secrets:`, por isso o nome foi trocado. O `GITHUB_TOKEN` é criado automaticamente pelo GitHub e não precisa ser cadastrado no repositório

O template (job `validacao-ambiente`) instala Poetry e Python (com cache do `poetry.lock`), roda `ruff check .`, `poetry install` e `pytest`, tudo dentro da pasta indicada em `working-directory`.

**`ml-pipeline-aula7.yaml` / `.github/workflows/ml-pipeline.yaml`** (ativo), disparado em `push` na `main` apenas se mudar um destes caminhos: `Aula7/src/models/**`, `Aula3/pyproject.toml`, `Aula3/poetry.lock` ou o próprio workflow.

1. `preparando_dados`: instala Poetry e Python 3.10, roda `preparar_dados.py` (da `Aula3/`) e publica `dataset_processado.csv` como artefato `dataset-processado`
2. `treinamento` (`needs: preparando_dados`): baixa o artefato, mostra o conteúdo do CSV e executa `python Aula7/src/models/teste.py dataset_processado.csv`

O `teste.py` usa só a biblioteca padrão: lê o CSV, "treina" um modelo que sempre prevê a classe mais comum e imprime a acurácia.

## Como testar

- Alterar `Aula7/src/models/teste.py` e dar push: o `ml-pipeline` deve rodar
- Alterar só `backend/` ou `frontend/` e dar push: o `ml-pipeline` não deve aparecer na aba Actions (o `ci-workflow-call` roda em qualquer push na `main`)

## Limitações

- **`paths` e `paths-ignore` juntos:** o GitHub não aceita os dois no mesmo evento. O `paths-ignore` foi removido, porque o `paths` já restringe o disparo.
- **Dados na Aula3:** o pipeline de ML usa o `pyproject.toml` e o `preparar_dados.py` da `Aula3/`, pois a `Aula7/` não tem esses arquivos.
- **Treinamento simulado:** o `teste.py` não usa modelo real, serve apenas para validar o pipeline.
- **Template em outro repositório:** o chamador usa `@main`. Mudanças no template só valem depois de commit e push na `main` do repositório `Fase3-Bloco2-Pos-Integracao`.
- **`train.py` com erro:** `open(..., "wb", encoding="utf-8")` lança `ValueError`, porque o modo binário não aceita `encoding`. Basta remover o argumento.
- **Caminho do modelo:** o CI roda `python Aula7/train.py` na raiz, e o script grava em `outputs/` relativo à pasta atual. O arquivo vai para `outputs/` na raiz, mas a auditoria procura em `Aula7/outputs/`. É preciso ajustar o caminho no `train.py` ou o `path-model`.
- **Lint do CI:** rodando o ruff dentro de `Aula4/`, o pacote `Aula4` não é detectado como código do projeto. Por isso o `Aula4/pyproject.toml` ganhou `known-first-party = ["Aula4"]` em `[tool.ruff.lint.isort]`.
