import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.Models.Models import Funcionario, Autenticacao
from app.Services.email_sender import enviar_codigo_email



def gerar_codigo_verificacao() -> str:
    return str(random.randint(1000, 9999))

def iniciar_autenticacao(db: Session, telefone: str, email: str):
    funcionario = db.query(Funcionario).filter(Funcionario.telefone == telefone).first()
    if not funcionario:
        print(f"[INFO] Telefone {telefone} não cadastrado.")
        return {"status": "erro", "mensagem": "Seu número não está cadastrado na empresa e, portanto, você não está habilitado a utilizar o sistema."}
    
    codigo = gerar_codigo_verificacao()
    autenticacao = Autenticacao(
        telefone=telefone, 
        codigo_verificacao=codigo, 
        verificado="N", 
        data_solicitacao=datetime.utcnow()
    )
    db.add(autenticacao)
    db.commit()

    enviar_codigo_email(email, codigo)
    return {"status": "sucesso", "mensagem": "Código enviado para o seu e-mail corporativo. Por favor, verifique seu e-mail e informe o código recebido."}

def validar_codigo(db: Session, telefone: str, codigo_recebido: str) -> bool:
    autenticacao = db.query(Autenticacao).filter(
        Autenticacao.telefone == telefone,
        Autenticacao.codigo_verificacao == codigo_recebido
    ).first()
    if autenticacao:
        autenticacao.verificado = "S"
        db.commit()
        return True
    return False
