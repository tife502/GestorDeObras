from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False, default = 3)
    rol_id = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))


    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.email,
            "rol_id": self.rol_id
        }
