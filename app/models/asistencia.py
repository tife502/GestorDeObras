from app import db
from sqlalchemy.sql import func

class Asistencia(db.Model):
    __tablename__ = "asistencia"

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    check_in = db.Column(db.DateTime, default=func.now(), nullable=False)
    check_out = db.Column(db.DateTime, nullable=True)
    ubicacion = db.Column(db.String(200))