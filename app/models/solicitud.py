from app import db
from sqlalchemy.sql import func

class SolicitudMaterial(db.Model):
    __tablename__ = "solicitudes_materiales"

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default="Pendiente")
    fecha_solicitud = db.Column(db.DateTime, default=func.now())
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="SET NULL"), nullable=True)