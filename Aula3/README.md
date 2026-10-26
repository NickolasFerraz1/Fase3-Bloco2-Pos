# Aula 3

Pipeline de ML no CI: preparação de dados (ETL), treinamento de um modelo dummy e um passo simulado de governança com Model Registry.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `preparar_dados.py` | ETL: cria um DataFrame de exemplo e salva em `dataset_processado.csv` |
| `dummy_train.py` | Treina um `DecisionTreeClassifier` com o dataset e imprime a acurácia |
| `dummy_train_governance.py` | Igual ao anterior, mas salva `modelo_treinado.pkl` e simula o registro no Model Registry usando o `GITHUB_SHA` do commit |
| `pyproject.toml` | Dependências (pandas, scikit-learn) e dev (nbstripout, ruff) |
| `ci-aula3.yaml` | Cópia do workflow de CI (roda em `pull_request` na `main`) |
| `ml-pipeline-aula3.yaml` | Cópia do workflow de treinamento (roda em `push` na `main`) |

## Pipelines

**CI**: valida ambiente, notebook e linter, depois roda ETL, `dummy_train.py` e `dummy_train_governance.py`.

**Pipeline de treinamento**: dois jobs encadeados com `needs`. O job `preparando_dados` roda o ETL e publica o `dataset_processado.csv` como artefato. O job `treinamento` baixa o artefato e confere o conteúdo.

## Como rodar localmente

```bash
cd Aula3
poetry install
poetry run python preparar_dados.py
poetry run python dummy_train.py
poetry run python dummy_train_governance.py
```
