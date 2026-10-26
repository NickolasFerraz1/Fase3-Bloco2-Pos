# Aula 6

Evolução do CD: deploy em produção com manifestos Kubernetes e autenticação na nuvem via OIDC. Como as permissões em cloud são limitadas, a parte da AWS foi só esboçada e o deploy no CD da raiz é simulado.

## Conteúdo

| Arquivo | Descrição |
|---|---|
| `k8s/deployment.yaml` | Deployment `anti-fraud-api` (2 réplicas, limites de CPU e memória, porta 8080) com placeholders `${API_ENV}` e `${LOG_LEVEL}` e imagem `nginx:latest` a ser substituída |
| `k8s/routing.yaml` | `VirtualService` com roteamento canário: 90% do tráfego para a v1 e 10% para a v2 |
| `cd-aula6.yaml` | Primeira versão do CD da aula: build e push da imagem no GHCR, seguido de login na AWS via OIDC (`configure-aws-credentials`) e `aws sts get-caller-identity` para validar a identidade |
| `cd-aula6.3.yaml` | Cópia do CD da raiz (`.github/workflows/cd.yaml`) ao final da aula, com o job de deploy |

## Pipelines

**`cd-aula6.yaml`**: job `build-and-push` (build do `Aula5/` e push no GHCR com a tag do commit), depois autenticação na AWS usando a role do secret `AWS_ROLE_ARN`. Fica como referência e não está ativo, porque não havia permissão para criar a role na conta de cloud.

**`cd-aula6.3.yaml` / `.github/workflows/cd.yaml`** (ativo), disparado em `push` na `main`:

1. `build-and-push`: login no GHCR, nome da imagem em minúsculas e push com a tag `github.sha`
2. `deploy-production` (`needs: build-and-push`, ambiente `production`):
   - define `API_ENV` e `LOG_LEVEL` como variáveis do job
   - com `sed`, troca no `deployment.yaml` a imagem pela recém-publicada (em minúsculas, como o GHCR exige) e os placeholders pelas variáveis
   - imprime o manifesto final com `cat`; o envio para o cluster é apenas simulado

## Limitações

- **Sem integração com a AWS no CD ativo:** o login OIDC e o `kubectl apply` não foram implementados por falta de permissões na conta. Para ativar, seria preciso criar a role, configurar o secret `AWS_ROLE_ARN` e dar acesso ao cluster.
- **Endpoint do OIDC:** o `cd-aula6.yaml` usa `audience: sts.amazonaws.com.cn`, que é o da AWS China. Para a conta global o valor é `sts.amazonaws.com`.
- **`routing.yaml`:** o `apiVersion` está como `networking.k8s.io/v1`. Para um `VirtualService` do Istio, o correto seria `networking.istio.io/v1`. O arquivo não é usado pelo CD.
