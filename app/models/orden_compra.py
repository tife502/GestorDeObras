from app import db
from datetime import datetime

class OrdenCompra(db.Model):
    __tablename__ = "orden_compra"

    id_orden = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_material = db.Column(db.Integer, db.ForeignKey("materiales.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    es_material_nuevo = db.Column(db.Boolean, nullable=False, default=False)
    id_estado = db.Column(db.Integer, db.ForeignKey("estados_compra.id"), nullable=False)
    usuario_solicitante = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    material = db.relationship("Material", backref="ordenes_compra")
    estado = db.relationship("EstadosCompra", backref="ordenes_compra")
    usuario = db.relationship("Usuario", backref="ordenes_compra")