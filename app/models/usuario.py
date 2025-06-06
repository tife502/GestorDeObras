from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, default=4)
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime, nullable=True)
    activo = db.Column(db.Boolean, default=True)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="SET NULL"), nullable=True)
    
    rol = db.relationship("Rol", backref=db.backref("usuarios", lazy=True))
    zona_trabajo = db.relationship("ZonaTrabajo", backref="trabajador", uselist=False)

    def to_dict(self):
        return {
        "id": self.id,
        "nombre": self.nombre,
        "email": self.email,
        "rol": self.rol_id,
        "id_zona": self.id_zona,  # ID de la zona de trabajo
        "zona_trabajo": self.zona_trabajo.nombre if self.zona_trabajo else None  # Nombre de la zona si existe
    }
