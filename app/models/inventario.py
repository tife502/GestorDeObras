from app import db

class Inventario(db.Model):
    __tablename__ = "inventario"

    id_inventario = db.Column(db.Integer, primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey("materiales.id"), nullable=False)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)

    material = db.relationship("Material", backref="inventarios")
    zona = db.relationship("ZonaTrabajo", backref="inventarios")