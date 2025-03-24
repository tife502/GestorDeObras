from app import db
from datetime import datetime
from sqlalchemy.sql import func

class Reporte(db.Model):
    __tablename__ = "reportes"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)  # Ej: 'Asistencia', 'Materiales'
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())