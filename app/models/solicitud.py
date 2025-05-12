from app import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

estado_enum = ENUM(
    'Pendiente', 
    'Aprobado', 
    'Rechazado', 
    'Aprobado Parcialmente', 
    name='estadoenum', 
    create_type=False  # se creará con la migración
)

class SolicitudMaterial(db.Model):
    __tablename__ = "solicitudes_material"

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    cantidad_pendiente = db.Column(db.Integer, nullable=False, default=0)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id"), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(estado_enum, nullable=False, default="Pendiente")
    fecha_solicitud = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
