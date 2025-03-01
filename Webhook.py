from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn

app = FastAPI()

import os
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@app.get("/webhook")
async def verify_token(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Endpoint GET usado pelo WhatsApp para verificar o webhook.
    Se os parâmetros estiverem corretos, retorna o hub.challenge.
    """
    if hub_mode and hub_verify_token:
        if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
            print("[INFO] Webhook verificado com sucesso!")
            return PlainTextResponse(content=hub_challenge, status_code=200)
        else:
            print("[ERROR] Falha na verificação do webhook.")
            return PlainTextResponse(content="Verificação falhou", status_code=403)
    return PlainTextResponse(content="Nenhum parâmetro de verificação", status_code=400)

@app.post("/webhook")
async def receive_messages(request: Request):
    try:
        data = await request.json()
        print("[DEBUG] JSON recebido:", data)
        # Verifica se vem no formato "entry/changes"
        if "entry" in data:
            for entry in data["entry"]:
                changes = entry.get("changes")
                if changes:
                    for change in changes:
                        value = change.get("value")
                        if value and value.get("messages"):
                            for message in value["messages"]:
                                process_message(message)
        # Verifica se vem direto com "field" e "value"
        elif data.get("field") == "messages" and "value" in data:
            value = data["value"]
            if value.get("messages"):
                for message in value["messages"]:
                    process_message(message)
        return JSONResponse(content={"status": "received"}, status_code=200)
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro: {e}")
        return JSONResponse(content={"error": "Erro interno do servidor"}, status_code=500)

    
def process_message(message):
    """
    Processa a mensagem conforme o seu tipo (texto, imagem ou áudio).
    """
    sender = message.get("from")
    if "text" in message:
        text = message["text"]["body"]
        print(f"[INFO] Mensagem de texto recebida de {sender}: {text}")
    elif "image" in message:
        image_id = message["image"]["id"]
        print(f"[INFO] Mensagem de imagem recebida de {sender}. ID da imagem: {image_id}")
    elif "audio" in message:
        audio_id = message["audio"]["id"]
        print(f"[INFO] Mensagem de áudio recebida de {sender}. ID do áudio: {audio_id}")
    else:
        print(f"[INFO] Tipo de mensagem não suportado recebido de {sender}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
