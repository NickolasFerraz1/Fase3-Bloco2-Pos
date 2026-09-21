def limpa_dados(df):
    """
    Limpa os dados do DataFrame, removendo valores nulos e duplicados.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser limpo.

    Retorna:
    pd.DataFrame: O DataFrame limpo.
    """
    df = df.dropna()  # Remove linhas com valores nulos
    df = df.drop_duplicates()  # Remove linhas duplicadas
    return df