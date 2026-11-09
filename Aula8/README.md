# Aula 8

Monitoramento de modelos em produção e retreinamento automático: um workflow agendado roda diariamente um "cão de guarda" que verifica data drift e concept drift, um script dispara um webhook (`repository_dispatch`) quando há anomalia, e o pipeline de ML o recebe, treina um novo modelo e abre um PR com o resultado da disputa Champion vs Challenger.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `monitoramento-diario-aula8.yaml` | Cópia do workflow da raiz (`.github/workflows/monitoramento-diario.yaml`) |
| `ml-pipeline-aula8.yaml` | Cópia do workflow da raiz (`.github/workflows/ml-pipeline.yaml`), agora com o gatilho de webhook e o PR automático |
| `scripts/cao_de_guarda.py` | Analisa a saúde do modelo de promoção (detecção de data drift e concept drift) |
| `scripts/disparar_webhook.py` | Envia o evento `anomalia-detectada` para a API do GitHub |
| `scripts/avaliar_desafiante.py` | Compara Champion e Challenger e gera o relatório em Markdown (`Aula8/relatorio.md`) |

## Pipelines

**`monitoramento-diario-aula8.yaml` / `.github/workflows/monitoramento-diario.yaml`** (ativo), disparado por:

- `schedule`: todo dia à meia-noite UTC (`cron: '0 0 * * *'`)
- `workflow_dispatch`: execução manual pela aba Actions

Job `monitoramento-diario`:

1. faz o checkout do repositório
2. instala o Python 3.10
3. instala `pandas`, `scipy` e `scikit-learn` com `pip` (dentro de `Aula8/`)
4. roda `python scripts/cao_de_guarda.py` (dentro de `Aula8/`)

**`ml-pipeline-aula8.yaml` / `.github/workflows/ml-pipeline.yaml`** (ativo), disparado por:

- `push` na `main`, apenas se mudar `Aula7/src/models/**`, `Aula3/pyproject.toml`, `Aula3/poetry.lock` ou o próprio workflow
- `repository_dispatch` com o tipo `anomalia-detectada`

Jobs, em sequência (`needs`):

1. `anomalia-detect`: imprime o `motivo` e a `acuracia_atual` recebidos no payload do webhook e simula o início do retreinamento
2. `preparando_dados`: instala Poetry e Python 3.10, roda `preparar_dados.py` (da `Aula3/`) e publica `dataset_processado.csv` como artefato
3. `treinamento` (com `permissions: contents: write` e `pull-requests: write`):
   - baixa o artefato e executa `Aula7/src/models/teste.py`
   - roda `Aula8/scripts/avaliar_desafiante.py` (Champion vs Challenger)
   - lê `Aula8/relatorio.md` para a variável `BODY`
   - cria um PR com `peter-evans/create-pull-request` (branch `bot-pr-model`, base `main`, labels `mlops`, `machine-learning` e `automated-pr`) com o relatório no corpo

## Os scripts

**`cao_de_guarda.py`** usa dados simulados, escritos no código:

1. **Data drift:** compara a distribuição histórica (`[100, 150, 200, 250, 300]`) com a de produção (`[400, 450, 500, 550, 600]`) pelo teste de Kolmogorov-Smirnov (`ks_2samp`). Com `p_value < 0.05`, registra um `WARNING`. Não falha o job.
2. **Concept drift:** compara o gabarito auditado com as predições do modelo usando `accuracy_score`. Se a acurácia ficar abaixo da meta de 0,85, registra dois `ERROR` e marca o problema.

No final, sai com `sys.exit(1)` se houve concept drift e com `sys.exit(0)` caso contrário. Com os dados simulados a acurácia é 0,60, então o job termina em falha, que é o comportamento esperado.

**`disparar_webhook.py`** faz um `POST` em `https://api.github.com/repos/{owner}/{repo}/dispatches` com `event_type: anomalia-detectada` e um `client_payload` (`motivo` e `acuracia_atual`). Autentica com um PAT lido da variável de ambiente `GITHUB_PAT`. Responde `204` em caso de sucesso.

**`avaliar_desafiante.py`** compara as acurácias (valores fixos: Champion 0,82 e Challenger 0,89), decide o vencedor e grava a tabela de resultados em `Aula8/relatorio.md`, com o caminho calculado a partir do próprio script para funcionar de qualquer pasta. Com os valores fixos o Challenger sempre vence.

## Limitações

- **O código de saída é o que decide a cor do job:** na primeira versão o `cao_de_guarda.py` terminava sempre com `sys.exit(0)`. O `logging.error` só escreve uma linha no log e não altera o código de saída, então o job ficava verde mesmo com concept drift. Por isso foi adicionada a variável `concept_drift`.
- **O vencedor não barra o PR:** o `avaliar_desafiante.py` sempre termina com sucesso, e os passos seguintes não checam o vencedor. Se o Champion vencesse, o PR seria criado do mesmo jeito. Hoje isso não acontece porque os valores são fixos e o Challenger sempre vence. Para valer a regra "só promove se o Challenger vencer", o script teria que gravar o vencedor em `$GITHUB_OUTPUT` e o passo do PR usar `if: steps.<id>.outputs.vencedor == 'challenger'`.
- **Repositório do webhook:** o `disparar_webhook.py` aponta para `Fase3-Bloco2-Pos-Integracao`, mas o `ml-pipeline.yaml` está no `Fase3-Bloco2-Pos`. O `repository_dispatch` é entregue ao repositório da URL, então o pipeline deste repositório só recebe o evento se o `repo` do script for ajustado.
- **`repository_dispatch` só na `main`:** o evento dispara a versão do workflow que está na branch padrão, então não dá para testá-lo a partir de outra branch.
- **PAT necessário:** o disparo exige um token pessoal com permissão no repositório. O PR criado com o `GITHUB_TOKEN` não dispara o `ci.yaml`, e a opção "Allow GitHub Actions to create and approve pull requests" precisa estar ativa em Settings → Actions → General.
- **O PR leva arquivos a mais:** o `create-pull-request` faz commit de tudo que é novo, então o `dataset_processado.csv` baixado na raiz vai junto com o `relatorio.md`. Para só o relatório, use `add-paths: Aula8/relatorio.md`.
- **Dados simulados:** o histórico, a produção, o gabarito, as predições e as acurácias são valores fixos. Em um caso real viriam de uma base, de logs de produção e de um dataset de validação.
- **Dependências sem versão:** o `pip install` do monitoramento instala as versões mais recentes de `pandas`, `scipy` e `scikit-learn`, sem travar versões ou usar `poetry.lock`.
- **`pandas` não é usado:** o `cao_de_guarda.py` só importa `scipy` e `scikit-learn`.
- **Agendamento:** o `schedule` só roda a partir do branch padrão (`main`) e o GitHub pode atrasar a execução em horários de pico.
