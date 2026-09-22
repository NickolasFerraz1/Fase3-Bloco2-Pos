import os
import pandas as pd


def test_schema_dados_processados():
    # O teste espera que o preparar_dados.py tenha sido executado e que o arquivo dataset_processado.csv exista
    caminho_arquivo = 'dataset_processado.csv'

    assert os.path.exists(caminho_arquivo), f"Arquivo {caminho_arquivo} não encontrado. Execute preparar_dados.py primeiro."

    # Lê o arquivo CSV
    df = pd.read_csv(caminho_arquivo)
    colunas_esperadas = ['feature1', 'feature2', 'target']

    # 1. Contrato de Colunas
    for col in colunas_esperadas:
        assert col in df.columns, f"Coluna esperada '{col}' não encontrada no DataFrame."

    # 2. Contrato de Qualidade
    assert df.isnull().sum().sum() == 0, "Existem valores nulos no DataFrame."

    # 3. Contrato de Regra de Negócio
    valores_target = set(df['target'].unique())
    assert valores_target.issubset({0, 1}), f"Valores inesperados na coluna 'target': {valores_target}. Esperado apenas 0 e 1."