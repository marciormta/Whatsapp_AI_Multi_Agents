import os
import requests

def enviar_mensagem_whatsapp(numero_destino: str, mensagem: str) -> bool:
    """
    Envia uma mensagem de texto para o usuário via WhatsApp Graph API.
    """
    url = os.getenv("WHATSAPP_API_URL")
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in (200, 201):
            print(f"[INFO] Mensagem enviada para {numero_destino}")
            return True
        else:
            print(f"[ERROR] Erro ao enviar mensagem: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Exceção ao enviar mensagem: {e}")
        return False
