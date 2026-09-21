# Workflows

Convenção: um workflow por aula, nomeado `aulaX.yml`, filtrando por `paths: - 'AulaX/**'` para não disparar as outras pipelines.

Exemplo de esqueleto:

```yaml
name: CI Aula1
on:
  push:
    paths:
      - 'Aula1/**'
jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: Aula1
    steps:
      - uses: actions/checkout@v4
      # ... build/test específico da aula
```
