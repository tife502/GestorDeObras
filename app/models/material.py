from app import db

class Material(db.Model):
    __tablename__ = "materiales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_disponible = db.Column(db.Float, nullable=False, default=0)  # Cambiar a Float para manejar decimales
    unidad_medida = db.Column(db.String(20), nullable=False, default="kg")  # Unidad de medida (ejemplo: kg, g, t)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="SET NULL"), nullable=True)

