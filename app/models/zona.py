from app import db
from datetime import datetime

class ZonaTrabajo(db.Model):
    __tablename__ = "zonas_trabajo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    ubicacion = db.Column(db.String(255), nullable=True)
    finalizada = db.Column(db.Boolean, default=False, nullable=False)  



