from fastapi.testclient import TestClient
from Aula4.api import app


client = TestClient(app)

def test_predict_endpoint_sucesso():
    # Simula uma requisição POST para o endpoint /predict com dados válidos
    response = client.post("/predict", json={"feature1": 0.8, "feature2": "A"})

    assert response.status_code == 200
    assert response.json()["aprovado"] == 1  # Espera que o score seja maior que 0.5

def test_predict_endpoint_erro_validacao():
    # Simula uma requisição POST para o endpoint /predict com dados inválidos
    response = client.post("/predict", json={"feature1": "invalid", "feature2": "A"})

    assert response.status_code == 422  # Espera que a validação falhe e retorne status 422