# app/models.py

from app import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'mensajes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    # Si usas conversaciones, descomenta esta línea:
    # conversacion_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "mensaje": self.mensaje,
            "fecha_envio": self.fecha_envio.isoformat(),  # para que sea serializable por JSON
            # "conversacion_id": self.conversacion_id  # solo si está en tu modelo
        }
