# Fase3 - Bloco2 - Pós FIAP

Repositório com o material e os exercícios das aulas de CI/CD do Bloco 2.

## Estrutura

```
Bloco2/
├── .github/
│   └── workflows/      # 1 workflow por aula (aulaX.yml), disparado via paths: AulaX/**
├── Aula1/
├── Aula2/
├── Aula3/
├── Aula4/
├── Aula5/
├── Aula6/
├── Aula7/
└── Aula8/
```

Cada pasta `AulaX` contém o código referente àquela aula. O pipeline de CI/CD de cada aula fica isolado em `.github/workflows/aulaX.yml`, disparando apenas quando há mudanças dentro da respectiva pasta.
