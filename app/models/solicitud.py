from app import db
from datetime import datetime

class SolicitudMaterial(db.Model):
    __tablename__ = "solicitudes_material"

    id_solicitud = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.Integer, nullable=False)
    es_nuevo = db.Column(db.Boolean, nullable=False, default=False)
    id_material = db.Column(db.Integer, db.ForeignKey("materiales.id"), nullable=True)
    nombre_material = db.Column(db.String(100), nullable=True)
    id_unidad = db.Column(db.Integer, db.ForeignKey("unidades_medida.id"), nullable=True)  # Puede ser nulo
    fecha_solicitud = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_estado = db.Column(db.Integer, db.ForeignKey("estado_solicitud.id_nombre"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id"), nullable=False)  # Nueva FK a zona

    material = db.relationship("Material", backref="solicitudes")
    estado = db.relationship("EstadoSolicitud", backref="solicitudes")
    usuario = db.relationship("Usuario", backref="solicitudes")
    unidad = db.relationship("UnidadMedida", backref="solicitudes")
    zona = db.relationship("ZonaTrabajo", backref="solicitudes")  # Relación con zona