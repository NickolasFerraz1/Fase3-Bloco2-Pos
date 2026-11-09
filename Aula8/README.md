# Aula 8

Monitoramento de modelos em produção: um workflow agendado roda diariamente um "cão de guarda" que verifica data drift e concept drift. Data drift gera só um alerta; concept drift faz o job falhar.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `monitoramento-diario-aula8.yaml` | Cópia do workflow da raiz (`.github/workflows/monitoramento-diario.yaml`) |
| `scripts/cao_de_guarda.py` | Script que analisa a saúde do modelo de promoção (detecção de data drift e concept drift) |

## Pipelines

**`monitoramento-diario-aula8.yaml` / `.github/workflows/monitoramento-diario.yaml`** (ativo), disparado por:

- `schedule`: todo dia à meia-noite UTC (`cron: '0 0 * * *'`)
- `workflow_dispatch`: execução manual pela aba Actions

Job `monitoramento-diario`:

1. faz o checkout do repositório
2. instala o Python 3.10
3. instala `pandas`, `scipy` e `scikit-learn` com `pip` (dentro de `Aula8/`)
4. roda `python scripts/cao_de_guarda.py` (dentro de `Aula8/`)

## O script `cao_de_guarda.py`

Usa dados simulados, escritos no próprio código:

1. **Data drift:** compara a distribuição histórica (`[100, 150, 200, 250, 300]`) com a de produção (`[400, 450, 500, 550, 600]`) pelo teste de Kolmogorov-Smirnov (`ks_2samp`). Com `p_value < 0.05`, registra um `WARNING`. Não falha o job.
2. **Concept drift:** compara o gabarito auditado com as predições do modelo usando `accuracy_score`. Se a acurácia ficar abaixo da meta de 0,85, registra dois `ERROR` e marca o problema.

No final, o script sai com `sys.exit(1)` se houve concept drift e com `sys.exit(0)` caso contrário. Com os dados simulados a acurácia é 0,60, então o job termina em falha, que é o comportamento esperado.

## Limitações

- **O código de saída é o que decide a cor do job:** na primeira versão o script terminava sempre com `sys.exit(0)`. O `logging.error` só escreve uma linha no log e não altera o código de saída, então o job ficava verde mesmo com concept drift. Por isso foi adicionada a variável `concept_drift`.
- **Dados simulados:** o histórico, a produção, o gabarito e as predições são listas fixas. Em um caso real viriam de uma base ou de logs de produção.
- **Dependências sem versão:** o `pip install` instala as versões mais recentes de `pandas`, `scipy` e `scikit-learn`, sem travar versões ou usar `poetry.lock`.
- **`pandas` não é usado:** o script só importa `scipy` e `scikit-learn`.
- **Agendamento:** o `schedule` só roda a partir do branch padrão (`main`) e o GitHub pode atrasar a execução em horários de pico.
