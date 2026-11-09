import os 
import requests
import logging

logging.basicConfig(level=logging.INFO)

def enviar_webhook_para_github():
    logging.info("Enviando webhook para o GitHub...")

    #Para interagir com a API do GitHub, você precisa de um 
    #token de acesso pessoal (PAT) com permissões adequadas. 
    token = os.environ.get("GITHUB_PAT")
    owner = "NickolasFerraz1"
    repo = "Fase3-Bloco2-Pos-Integracao"

    # Endpoint oficial do GitHub para criar um dispatch event
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "event_type": "anomalia-detectada",
        "client_payload": {
            "motivo": "Concept Drift crítico identificado",
            "acuracia_atual": "72%"
        }
    }

    resposta = requests.post(url, json=payload, headers=headers)

    if resposta.status_code == 204:
        logging.info("Webhook enviado com sucesso!")
    else:
        logging.error(f"Falha ao enviar webhook. Status code: {resposta.status_code}, Resposta: {resposta.text}")

if __name__ == "__main__":
    enviar_webhook_para_github()