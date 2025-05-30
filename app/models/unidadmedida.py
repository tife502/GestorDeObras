from app import db

class UnidadMedida(db.Model):
    __tablename__ = "unidades_medida"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    abreviatura = db.Column(db.String(10), nullable=False)