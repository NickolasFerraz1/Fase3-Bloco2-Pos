from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Aula 4 - FastAPI", version="0.1.0")

# O Contrato de Entrada
class Transacao(BaseModel):
    feature1: float
    feature2: str

@app.post("/predict")
def predict(dados: Transacao):
    # Aqui você implementaria a lógica de previsão usando um modelo treinado
    # Para fins de demonstração, vamos apenas retornar uma resposta simulada
    # feature2 é categórica (texto); aqui tratamos só a presença de valor (0 ou 1)
    feature2_presente = int(bool(dados.feature2))
    score = dados.feature1 * 0.5 + feature2_presente * 0.5  # Simulação de cálculo de score
    aprovado = int(score > 0.5)

    return {"score": score, "aprovado": aprovado}