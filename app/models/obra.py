from app import db

class Obra(db.Model):
    __tablename__ = "obras"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)

    zonas = db.relationship("ZonaTrabajo", backref="obra", cascade="all, delete", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": self.fecha_fin.strftime("%Y-%m-%d") if self.fecha_fin else None
        }
    