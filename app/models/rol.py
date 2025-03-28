from app import db

class Rol(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    nombrerol = db.Column(db.String(50), unique=True, nullable=False)
