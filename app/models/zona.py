from app import db
from datetime import datetime

class ZonaTrabajo(db.Model):
    __tablename__ = "zonas_trabajo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    obra_id = db.Column(db.Integer, db.ForeignKey("obras.id", ondelete="CASCADE"), nullable=False)
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), unique=True, nullable=True)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)

    tareas = db.relationship("Tarea", backref="zona", cascade="all, delete", lazy=True)