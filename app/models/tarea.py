from app import db

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')
    trabajador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    trabajador = db.relationship('Usuario', backref=db.backref('tareas', lazy=True))
    zona_id = db.Column(db.Integer, db.ForeignKey('zona_trabajo.id'), nullable=False)
    zona = db.relationship('ZonaTrabajo', backref=db.backref('tareas', lazy=True))