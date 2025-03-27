from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from app.models.usuario import Usuario

def rol_requerido(*rol):
    def decorador(func):
        @wraps(func)
        def decorador_function(*args, **kwargs):
            usuario_id = get_jwt_identity()
            usuario = Usuario.query.get(usuario_id)
            if usuario.rol != rol:
                return jsonify({"error": "No tienes permiso para realizar esta acción"}), 403
            return func(*args, **kwargs)
        return decorador_function
    return decorador