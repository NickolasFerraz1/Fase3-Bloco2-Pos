import pickle
from pathlib import Path

print("Iniciando o treinamento do modelo...")

# Caminho relativo ao script, para funcionar de qualquer pasta
# (o CI roda "python Aula7/train.py" a partir da raiz do repositório)
pasta_saida = Path(__file__).parent / "outputs"
pasta_saida.mkdir(exist_ok=True)
caminho_modelo = pasta_saida / "dataset_processado.pkl"

with open(caminho_modelo, "wb") as f:
    pickle.dump({"modelo_falso": "apenas para enganar o pipeline"}, f)

print(f"Treinamento concluído! Modelo salvo em '{caminho_modelo}'.")
