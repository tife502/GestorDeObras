from app import db

class Material(db.Model):
    __tablename__ = "materiales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_unidad = db.Column(db.Integer, db.ForeignKey("unidades_medida.id"), nullable=False)  # FK a la tabla unidad de medida
    activo = db.Column(db.Boolean, default=True)
