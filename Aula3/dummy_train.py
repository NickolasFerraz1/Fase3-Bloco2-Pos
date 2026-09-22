import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import sys


def main():
    print("Iniciando treinamento do modelo")

    try:
        df = pd.read_csv('dataset_processado.csv')

        X = df.drop('target', axis=1)
        y = df['target']

        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X, y)

        score = clf.score(X, y)
        print(f"Modelo treinado com sucesso. Acurácia: {score:.2f}")
        sys.exit(0)

    except Exception as e:
        print(f"Erro durante o treinamento do modelo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()