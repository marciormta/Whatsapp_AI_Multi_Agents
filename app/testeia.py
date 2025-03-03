import os
from app.Services import ia_service
from dotenv import load_dotenv

load_dotenv()

def testar_ia():
    prompt = "Qual é a previsão do tempo hoje?"
    resultado = ia_service.modulo_ia(prompt, autenticado=True)
    print("Resposta da IA:", resultado["resposta"])

if __name__ == "__main__":
    testar_ia()
