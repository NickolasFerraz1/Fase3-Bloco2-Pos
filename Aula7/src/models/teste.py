"""Script de teste para validar o ml-pipeline.yaml.

Lê o dataset gerado pelo job de preparação de dados, "treina" um modelo
trivial (classe majoritária) e imprime as métricas. Usa só a biblioteca
padrão, então roda sem instalar dependências.

Uso:
    python teste.py [caminho_do_csv]
"""

import csv
import sys
from collections import Counter
from pathlib import Path


def carregar_dataset(caminho: Path) -> list[dict]:
    if not caminho.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {caminho}")
    with caminho.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def treinar(linhas: list[dict]) -> int:
    """'Treina' um modelo dummy: sempre prevê a classe mais comum."""
    contagem = Counter(int(linha["target"]) for linha in linhas)
    return contagem.most_common(1)[0][0]


def avaliar(modelo: int, linhas: list[dict]) -> float:
    acertos = sum(1 for linha in linhas if int(linha["target"]) == modelo)
    return acertos / len(linhas)


def main() -> None:
    caminho = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset_processado.csv")
    linhas = carregar_dataset(caminho)
    assert linhas, "Dataset vazio"
    print(f"Dataset carregado: {len(linhas)} linhas de {caminho}")

    modelo = treinar(linhas)
    acuracia = avaliar(modelo, linhas)
    print(f"Modelo treinado (classe prevista: {modelo})")
    print(f"Acurácia: {acuracia:.2%}")

    assert acuracia > 0, "Acurácia inválida"
    print("Treinamento de teste concluído com sucesso")


if __name__ == "__main__":
    main()
