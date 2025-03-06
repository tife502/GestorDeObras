from app import db
from datetime import datetime

class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    trabajador = db.relationship('Usuario', backref=db.backref('asistencias', lazy=True))
    check_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out = db.Column(db.DateTime, nullable=True)
    ubicacion = db.Column(db.String(200), nullable=True)