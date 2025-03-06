from app import db
from datetime import datetime

class SolicitudMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    trabajador = db.relationship('Usuario', backref=db.backref('solicitudes', lazy=True))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    material = db.relationship('Material', backref=db.backref('solicitudes', lazy=True))
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)