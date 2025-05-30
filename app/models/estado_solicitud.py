from app import db

class EstadoSolicitud(db.Model):
    __tablename__ = "estado_solicitud"

    id_nombre = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)