from flask_mail import Mail, Message
from flask import current_app


mail = Mail()

def init_mail(app):
    mail.init_app(app)

def enviar_email(destinatario, asunto, mensaje):
    try:
        msg = Message(asunto, sender=current_app.config['MAIL_USERNAME'], recipients=[destinatario])
        msg.body = mensaje
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

