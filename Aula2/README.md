# Aula 2

Gerenciamento de dependências com Poetry e qualidade de código no CI (linter e notebooks limpos).

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `pyproject.toml` | Dependências do projeto (pandas, scikit-learn) e dev (nbstripout, ruff) |
| `processamento.py` | Função `limpa_dados(df)`: remove nulos e duplicados de um DataFrame |
| `explorer.ipynb` | Notebook de teste, sem outputs, usado para validar o `nbstripout` |
| `validate_env.py` | Validação de versão do Python (mesmo script da Aula 1) |
| `ci-aula2.yml` | Cópia do workflow de CI desta aula |

## Pipeline

Disparado em `push` e `pull_request` na `main`:

1. Instala Poetry e Python 3.10 (com cache do Poetry)
2. Valida o ambiente (`validate_env.py`)
3. `nbstripout --verify`: falha se o notebook tiver células com output
4. `ruff check .`: linter
5. `poetry install` na pasta `Aula2`

## Como rodar localmente

```bash
cd Aula2
poetry install
poetry run ruff check .
poetry run nbstripout --verify explorer.ipynb
```
