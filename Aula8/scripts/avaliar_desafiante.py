from pathlib import Path


def gerar_relatorio_luta():
    # Na vida real, carregaríamos o modelo de prod e o 
    # recém-trienado e calcularíamos a acurácia usando um 
    # dataset de validação dourado (Hold-out)
    acuracia_champion = 0.82
    acuracia_challenger = 0.89

    # Decisão matemática
    vencedor = "challenger" if acuracia_challenger > acuracia_champion else "champion"

    relatorio_md = f"""
# Relatório da Batalha Champion vs Challenger

O Sistema Imunológico detectou falhas e treinou um novo modelo. Aqui estão os resultados da validação cruzada:
| Modelo | Papel | Acurácia | F1 Score | Status |
|--------|-------|----------|----------|--------|
| **V1 (Atual)** | Champion | {acuracia_champion:.2%} | 0.81 | {'🏆' if vencedor == 'champion' else '❌'} |
| **V2 (Novo)** | Challenger | {acuracia_challenger:.2%} | 0.88 | {'🏆' if vencedor == 'challenger' else '❌'} |

**VEREDITO DA MÁQUINA:** O modelo **{vencedor.upper()}** venceu a batalha e será promovido para produção.

**AÇÃO HUMANA REQUERIDA:** Por favor, revise o relatório e confirme a promoção do modelo vencedor.
"""

    # Salvar o relatório em um arquivo Markdown
    # Caminho relativo ao script (Aula8/relatorio.md), para funcionar de
    # qualquer pasta, inclusive da raiz do repositório como no CI
    caminho_relatorio = Path(__file__).parent.parent / "relatorio.md"
    with open(caminho_relatorio, "w", encoding="utf-8") as f:
        f.write(relatorio_md)

    print(f"Relatório Markdown gerado com sucesso: '{caminho_relatorio}'")

if __name__ == "__main__":
    gerar_relatorio_luta()