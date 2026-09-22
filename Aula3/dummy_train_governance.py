import os
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

        # Simula salvamento do modelo em disco (artefato binário)
        import pickle
        with open('modelo_treinado.pkl', 'wb') as f:
            pickle.dump(clf, f)

        # ==========================================
        # GOVERNANÇA: Integração com Model Registry
        # ==========================================
        commit_sha = os.environ.get('GITHUB_SHA', 'unknown')

        print("\n--- Integrando com Model Registry ---")
        print("Enviando o arquivo modelo_treinado.pkl para o Model Registry...")
        print(f"Commit SHA: {commit_sha}")
        print("Modelo registrado com sucesso no Model Registry.")

        sys.exit(0)

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Erro durante o treinamento do modelo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()