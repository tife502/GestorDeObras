from app import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'mensajes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Para mensajes privados
    conversacion_id = db.Column(db.String(50), nullable=False, default="grupal")
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "destinatario_id": self.destinatario_id,
            "conversacion_id": self.conversacion_id,
            "mensaje": self.mensaje,
            "fecha_envio": self.fecha_envio.isoformat(),
        }
