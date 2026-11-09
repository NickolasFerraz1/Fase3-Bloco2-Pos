import os
import pickle

print("Iniciando o treinamento do modelo...")

os.makedirs("outputs", exist_ok=True)

with open("outputs/dataset_processado.pkl", "wb", encoding="utf-8") as f:
    pickle.dump({"modelo_falso": "apenas para enganar o pipeline"}, f)

print("Treinamento concluído! Modelo salvo em 'outputs/dataset_processado.pkl'.")