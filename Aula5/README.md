# Aula 5

Containerização da API com Docker e CD que publica a imagem no GitHub Container Registry (GHCR).

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `api.py` | API FastAPI da Aula 4 |
| `Dockerfile` | Build multi-stage: o stage `builder` exporta as dependências do Poetry para `requirements.txt`, e a imagem final instala só isso e copia apenas o `api.py` |
| `Dockerfile-singlestage` | Versão de um único stage, usando Poetry dentro da imagem, para comparação |
| `pyproject.toml`, `poetry.lock` | Dependências da API, incluindo o `uvicorn` |
| `cd-aula5.yaml` | Cópia do workflow de CD (o ativo fica em `.github/workflows/cd.yaml`) |

## Pipeline de CD

Disparado em `push` na `main`:

1. Checkout e conversão do nome da imagem para minúsculas (exigência do GHCR)
2. Login no `ghcr.io` com o `GITHUB_TOKEN`
3. Build do contexto `Aula5/` e push com a tag do commit (`github.sha`)

## Como rodar localmente

```bash
cd Aula5
docker build -t api:latest .
docker run --rm -p 8000:8000 api:latest
```

A API fica em `http://localhost:8000` e a documentação em `/docs`. Para usar a versão de um stage: `docker build -f Dockerfile-singlestage -t api:single .`.
