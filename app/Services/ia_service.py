import os
from langchain_openai import OpenAI

def modulo_ia(mensagem: str, autenticado: bool) -> dict:
    if not autenticado:
        resposta = "Você não está autenticado para utilizar o serviço multiagentes. Por favor, realize a autenticação."
        return {"agente": "Sem acesso", "resposta": resposta}

    mensagem_lower = mensagem.lower()
    if "jurídico" in mensagem_lower:
        agente = "Agente Jurídico"
        resposta = "Encaminhando sua dúvida para o setor jurídico..."
    elif "rh" in mensagem_lower:
        agente = "Agente de RH"
        resposta = "Encaminhando sua dúvida para o RH..."
    else:
        agente = "IA Geral"
        llm = OpenAI(temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))
        resposta = llm.invoke(mensagem)
    return {"agente": agente, "resposta": resposta}
