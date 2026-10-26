# Aula 4

Testes automatizados para ML: contratos de dados e testes de uma API FastAPI, rodando no CI com Pytest.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `api.py` | API FastAPI com `POST /predict`, que recebe `feature1` (float) e `feature2` (str) e devolve `score` e `aprovado` (cálculo simulado) |
| `preparar_dados.py` | ETL da Aula 3, agora removendo linhas com nulos |
| `tests/test_api.py` | Testa o endpoint com entrada válida (200) e inválida (422) |
| `tests/test_dados.py` | Contratos de dados: colunas esperadas, ausência de nulos e `target` apenas 0 ou 1 |
| `pyproject.toml` | Adiciona fastapi, pydantic e, no grupo dev, pytest e httpx |
| `ci-aula4.yaml`, `ml-pipeline-aula4.yaml` | Cópias dos workflows desta aula |

## Pipeline

No CI, depois dos passos das aulas anteriores, roda `poetry install` e `poetry run pytest tests/ -v` dentro de `Aula4`.

## Como rodar localmente

```bash
cd Aula4
poetry install
poetry run python preparar_dados.py   # gera o dataset que o test_dados.py valida
poetry run pytest tests/ -v
```

Para subir a API: `poetry run uvicorn api:app --reload` (a documentação interativa fica em `/docs`).
