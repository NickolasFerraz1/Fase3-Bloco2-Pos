# Aula 1

Primeiro contato com CI no GitHub Actions: um pipeline simples que valida o ambiente Python.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `validate_env.py` | Imprime a versão do Python e sai com erro (`exit 1`) se for menor que 3.8 |
| `ci-aula1.yaml` | Cópia do workflow de CI desta aula (o ativo fica em `.github/workflows/ci.yaml`) |

## Pipeline

Disparado em `push` e `pull_request` na `main`:

1. Checkout do repositório
2. Instalação do Python 3.10
3. Execução de `python Aula1/validate_env.py`

## Como rodar localmente

```bash
python Aula1/validate_env.py
```
