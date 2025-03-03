from fastapi import APIRouter, Body, Query, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.Models.Database import get_db
from app.config import token
from app.Services import process_message

router = APIRouter()

@router.get("/webhook")
async def verify_token(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode and hub_verify_token:
        if hub_mode == "subscribe" and hub_verify_token == token:
            print("[INFO] Webhook verificado com sucesso!")
            return PlainTextResponse(content=hub_challenge, status_code=200)
        else:
            print("[ERROR] Falha na verificação do webhook.")
            return PlainTextResponse(content="Verificação falhou", status_code=403)
    return PlainTextResponse(content="Nenhum parâmetro de verificação", status_code=400)


@router.post("/webhook")
async def receive_messages(
    payload: dict = Body(...),  # <- agora definimos que o corpo da requisição é um dict
    db: Session = Depends(get_db)
):
    """
    Endpoint para receber mensagens do WhatsApp (via JSON).
    """
    try:
        data = payload
        print("[DEBUG] JSON recebido:", data)
        
        # Mesmo fluxo de antes, mas agora data = payload
        if "entry" in data:
            for entry in data["entry"]:
                changes = entry.get("changes", [])
                for change in changes:
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            process_message.processar_mensagem(db, message)
        elif data.get("field") == "messages" and "value" in data:
            value = data["value"]
            if "messages" in value:
                for message in value["messages"]:
                    process_message.processar_mensagem(db, message)
        return JSONResponse(content={"status": "received"}, status_code=200)
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro: {e}")
        return JSONResponse(content={"error": "Erro interno do servidor"}, status_code=500)
