from app import db

class Bodega(db.Model):
    __tablename__ = "bodega"

    id_material = db.Column(db.Integer, db.ForeignKey("materiales.id"), primary_key=True, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)

    material = db.relationship("Material", backref=db.backref("bodega", uselist=False))