from app import db

class Tarea(db.Model):
    __tablename__ = "tareas"

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(50), default="Pendiente")
    trabajador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    zona_id = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="CASCADE"), nullable=False)