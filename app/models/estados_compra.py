from app import db

class EstadosCompra(db.Model):
    __tablename__ = "estados_compra"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    