from app.Services import auth_service, storage_service, ia_service, whatsapp_sender
from app.Models.Models import LogMensagem, Funcionario, Autenticacao
from sqlalchemy.orm import Session

def processar_mensagem(db: Session, message: dict):
    sender = message.get("from")
    
    if "text" in message:
        texto = message["text"]["body"].strip()
        print(f"[INFO] Texto recebido de {sender}: {texto}")
        
        # Registra a mensagem no log
        log = LogMensagem(
            id_user=sender,
            nome="Nome do Usuário",
            telefone=sender,
            mensagem_enviada=texto
        )
        db.add(log)
        db.commit()
        
        funcionario = db.query(Funcionario).filter(Funcionario.telefone == sender).first()
        if not funcionario:
            msg = "Usuário não cadastrado, por favor entre em contato com o RH para realizar a inclusão de cadastro."
            whatsapp_sender.enviar_mensagem_whatsapp(numero_destino=sender, mensagem=msg)
            print(f"[INFO] Número {sender} não cadastrado.")
            return
        sessao_autenticada = db.query(Autenticacao).filter(
            Autenticacao.telefone == sender,
            Autenticacao.verificado == "S"
        ).first()
        if sessao_autenticada:
            resultado_ia = ia_service.modulo_ia(texto, autenticado=True)
            msg = resultado_ia["resposta"]
            enviado = whatsapp_sender.enviar_mensagem_whatsapp(numero_destino=sender, mensagem=msg)
            if enviado:
                print(f"[INFO] Resposta da IA enviada para {sender}")
            else:
                print(f"[ERROR] Falha no envio da resposta para {sender}")
            return

        sessao = db.query(Autenticacao).filter(
            Autenticacao.telefone == sender,
            Autenticacao.verificado == "N"
        ).first()
        
        if sessao:
            if texto.isdigit() and len(texto) == 4:
                validado = auth_service.validar_codigo(db, telefone=sender, codigo_recebido=texto)
                if validado:
                    resultado_ia = ia_service.modulo_ia("Como posso ajudar?", autenticado=True)
                    msg = resultado_ia["resposta"]
                else:
                    msg = "Código inválido. Por favor, verifique o código enviado para seu e-mail."
                enviado = whatsapp_sender.enviar_mensagem_whatsapp(numero_destino=sender, mensagem=msg)
                if enviado:
                    print(f"[INFO] Resposta enviada para {sender}")
                else:
                    print(f"[ERROR] Falha no envio da resposta para {sender}")
                return
            else:
                msg = "Por favor, informe o código enviado para o seu e-mail para continuar."
                whatsapp_sender.enviar_mensagem_whatsapp(numero_destino=sender, mensagem=msg)
                return
        else:
            resultado_auth = auth_service.iniciar_autenticacao(db, telefone=sender, email=funcionario.email_corporativo)
            print(resultado_auth["mensagem"])
            whatsapp_sender.enviar_mensagem_whatsapp(
                numero_destino=sender,
                mensagem="Oi, estamos iniciando a etapa de verificação. Seu número está cadastrado, aguarde um momento."
            )
            whatsapp_sender.enviar_mensagem_whatsapp(
                numero_destino=sender,
                mensagem="Enviei um código para o seu e-mail. Por favor, informe o código recebido para continuar usando a IA."
            )
            return
        
    elif "image" in message or "audio" in message:
        file_id = message.get("image", {}).get("id") or message.get("audio", {}).get("id")
        print(f"[INFO] Arquivo recebido de {sender} com ID: {file_id}")
        file_bytes = b"conteudo do arquivo"
        url = storage_service.upload_arquivo(user_id=sender, file_bytes=file_bytes, filename=f"{file_id}.bin")
        print(f"[INFO] Arquivo armazenado em: {url}")
    else:
        print(f"[INFO] Tipo de mensagem não suportado de {sender}")
