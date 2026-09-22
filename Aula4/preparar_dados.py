import pandas as pd


def main():
    print("Iniciando preparação de dados")
    # Simulando a criação de um DataFrame com dados de exemplo
    dados = {
        'feature1': [1, 2, None, 4, 5],
        'feature2': ['A', 'B', 'C', None, 'E'],
        'target': [0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(dados)

    # Remove linhas com valores ausentes: test_dados.py exige um dataset
    # sem nulos (Contrato de Qualidade)
    df = df.dropna()

    # Salvando o DataFrame em um arquivo CSV
    df.to_csv('dataset_processado.csv', index=False)
    print("Dados processados e salvos em dataset_processado.csv")

if __name__ == "__main__":
    main()