import sys

import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def main():
    print("Iniciando treinamento do modelo")

    try:
        df = pd.read_csv('dataset_processado.csv')

        X = df.drop('target', axis=1)
        y = df['target']

        # Converte colunas de texto (ex.: feature2) em colunas numéricas 0/1
        X = pd.get_dummies(X)
        # Preenche valores ausentes nas colunas numéricas com a média da coluna
        X = X.fillna(X.mean(numeric_only=True))

        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X, y)

        score = clf.score(X, y)
        print(f"Modelo treinado com sucesso. Acurácia: {score:.2f}")
        sys.exit(0)

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Erro durante o treinamento do modelo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()