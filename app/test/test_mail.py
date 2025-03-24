from flask import Flask
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

with app.app_context():
    msg = Message("Prueba de correo", sender=app.config['MAIL_USERNAME'], recipients=["tife502@yopmail.com"])
    msg.body = "Este es un correo de prueba."

    try:
        mail.send(msg)
        print("✅ Correo enviado exitosamente.")
    except Exception as e:
        print("❌ Error al enviar correo:", str(e))
