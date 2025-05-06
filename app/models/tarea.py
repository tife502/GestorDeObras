from app import db

class Tarea(db.Model):
    __tablename__ = "tareas"

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), default="Pendiente")  # Cambiado a String para evitar problemas de compatibilidad
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    evidencia = db.Column(db.Text, nullable=True)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="SET NULL"), nullable=True)  

    usuario = db.relationship("Usuario", backref="tareas", lazy=True)
    zona = db.relationship("ZonaTrabajo", backref="tareas", lazy=True)
    