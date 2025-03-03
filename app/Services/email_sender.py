import smtplib
from email.mime.text import MIMEText
from app.config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def enviar_codigo_email(destinatario: str, codigo: str):
    assunto = "Código de Verificação"
    corpo = f"Seu código de verificação é: {codigo}"
    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_SENDER
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        print(f"[INFO] E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"[ERROR] Falha ao enviar e-mail: {e}")
