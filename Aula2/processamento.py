import pandas as pd
import os # Import não utilizado 
import sys # Import não utilizado 

def limpa_dados(df):
    """
    Limpa os dados do DataFrame, removendo valores nulos e duplicados.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser limpo.

    Retorna:
    pd.DataFrame: O DataFrame limpo.
    """
    #Variável não utilizada
    x = 10
    df = df.dropna()  # Remove linhas com valores nulos
    df = df.drop_duplicates()  # Remove linhas duplicadas
    return df