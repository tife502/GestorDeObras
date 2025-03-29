from flask import Blueprint, request, jsonify, url_for
from app import db, bcrypt
from app.models.usuario import Usuario
from app.models import Usuario, Rol

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from app.services.email_service import enviar_email
import secrets
from datetime import datetime, timedelta
from app.utils.decorators import rol_requerido
from flask_cors import CORS
reset_tokens = {}

usuarios_bp = Blueprint("usuarios", __name__)
CORS(usuarios_bp) 


def es_email_valido(email):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, email)

@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data["email"]).first()

    if usuario:
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta > datetime.utcnow():
            return jsonify({"error": "Cuenta bloqueada. Intenta más tarde."}), 403

        if bcrypt.check_password_hash(usuario.password, data["password"]):
            usuario.intentos_fallidos = 0
            db.session.commit()
            token = create_access_token(identity=usuario.id)
            return jsonify({"token": token}), 200
        else:
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= 3:
                usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=15)
                # Envía un correo para recuperación de contraseña
                token = secrets.token_urlsafe(20)
                reset_tokens[token] = usuario.email
                enlace = url_for("usuarios.resetear_contrasena", token=token, _external=True)
                enviar_email(usuario.email, "Recuperación de contraseña", f"Enlace para restablecer: {enlace}")
            db.session.commit()
            return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify({"error": "Credenciales inválidas"}), 401

@usuarios_bp.route("/registro", methods=["POST"])
def registrar_usuario():
    data = request.json
    
    # Verificar que el email sea válido
    if not es_email_valido(data["email"]):
        return jsonify({"error": "Formato de correo inválido"}), 400
    
    # Verificar que el email no esté registrado
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El correo ya está en uso"}), 400
    
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        password=hashed_password
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@usuarios_bp.route("/recuperar", methods=["POST"])
def recuperar_contrasena():
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "Se requiere un email"}), 400

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Generar token de recuperación
        token = secrets.token_urlsafe(20)
        reset_tokens[token] = email

        # Simulación de envío de email
        enlace = url_for("usuarios.resetear_contrasena", token=token, _external=True)
        enviado = enviar_email(email, "Recuperación de contraseña", f"Enlace para restablecer: {enlace}")

        if not enviado:
            return jsonify({"error": "Error al enviar el correo"}), 500

        return jsonify({"mensaje": "Correo enviado con instrucciones"}), 200

    except Exception as e:
        print("Error en el servidor:", str(e))  # 🔹 Esto imprimirá el error en la terminal
        return jsonify({"error": "Error interno del servidor"}), 500

@usuarios_bp.route("/resetear/<token>", methods=["POST"])
def resetear_contrasena(token):
    data = request.json
    nueva_password = data.get("password")
    email = reset_tokens.get(token)
    if not email:
        return jsonify({"error": "Token inválido o expirado"}), 400
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    hashed_password = bcrypt.generate_password_hash(nueva_password).decode("utf-8")
    usuario.password = hashed_password
    db.session.commit()
    del reset_tokens[token]

    return jsonify({"mensaje": "Contraseña actualizada exitosamente"}), 200

@usuarios_bp.route("/perfil", methods=["GET"])
def perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return jsonify({
        "nombre": usuario.nombre,
        "email": usuario.email
    }), 200

@usuarios_bp.route("/usuarios/<int:id>/desactivar", methods=["PUT"])
@rol_requerido('administrador')
def desactivar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario.activo = False
    db.session.commit()
    return jsonify({"mensaje": "Usuario desactivado exitosamente"}), 200

@usuarios_bp.route("/mostrarusuarios", methods=["GET"])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200



@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
@rol_requerido('administrador')
def modificar_roles(id):
    data = request.json
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if usuario.rol.nombre == 'administrador':
        return jsonify({"error": "No se puede modificar el rol de un administrador"}), 403

    nuevo_rol = data.get("rol")
    if not nuevo_rol:
        return jsonify({"error": "Se requiere un rol"}), 400

    usuario.rol_id = nuevo_rol
    db.session.commit()
    return jsonify({"mensaje": "Rol modificado exitosamente"}), 200

# Eliminar usuario por ID
@usuarios_bp.route("/eliminarusuario/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200

# Modificar usuario por ID
@usuarios_bp.route("/modificarusuario/<int:id>", methods=["OPTIONS", "PATCH"])
def modificar_usuario(id):
    if request.method == "OPTIONS":
        return '', 204  # Respuesta para preflight request

    usuario = db.session.get(Usuario, id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    datos = request.json
    usuario.nombre = datos.get("nombre", usuario.nombre)
    usuario.email = datos.get("email", usuario.email)

    rol_id = datos.get("rol")
    if rol_id:
        try:
            rol_id = int(rol_id)
        except ValueError:
            return jsonify({"error": "El rol debe ser un número"}), 400

        rol_obj = db.session.get(Rol, rol_id)
        if rol_obj:
            usuario.rol = rol_obj
        else:
            return jsonify({"error": "Rol no encontrado"}), 400

    try:
        db.session.commit()
        return jsonify({"mensaje": "Usuario modificado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

