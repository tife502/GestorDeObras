from app import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False, default=0)