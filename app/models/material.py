from app import db

class Material(db.Model):
    __tablename__ = "materiales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_disponible = db.Column(db.Integer, default=0, nullable=False)
    id_zona = db.Column(db.Integer, db.ForeignKey("zonas_trabajo.id", ondelete="CASCADE"), nullable=False)