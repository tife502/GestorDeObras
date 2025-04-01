from app import db
from datetime import datetime

class ZonaTrabajo(db.Model):
    __tablename__ = "zonas_trabajo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), unique=True, nullable=True)
    ubicacion = db.Column(db.Integer, nullable=True)
    finalizada = db.Column(db.Boolean, default=False, nullable=False)  


    usuarios = db.relationship("Usuario", backref="zona", cascade="all, delete", lazy=True)
