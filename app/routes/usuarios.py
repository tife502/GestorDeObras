from flask import Blueprint, request, jsonify, url_for
from app import db, bcrypt
from app.models.usuario import Usuario
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from app.services.email_service import enviar_email
import secrets
from datetime import datetime, timedelta
from app.utils.decorators import rol_requerido

reset_tokens = {}

usuarios_bp = Blueprint("usuarios", __name__)


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

    # Verificar si el token es válido
    email = reset_tokens.get(token)
    if not email:
        return jsonify({"error": "Token inválido o expirado"}), 400

    # Buscar usuario
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Hashear la nueva contraseña y actualizar en la base de datos
    hashed_password = bcrypt.generate_password_hash(nueva_password).decode("utf-8")
    usuario.password = hashed_password
    db.session.commit()

    # Eliminar el token usado
    del reset_tokens[token]

    return jsonify({"mensaje": "Contraseña actualizada exitosamente"}), 200

@usuarios_bp.route("/perfil", methods=["GET"])
@jwt_required()
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
@jwt_required()
@rol_requerido('administrador')
def desactivar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario.activo = False
    db.session.commit()
    return jsonify({"mensaje": "Usuario desactivado exitosamente"}), 200


@usuarios_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    usuario_id = get_jwt_identity()
    usuario_actual = Usuario.query.get(usuario_id)
    
    if usuario_actual.rol.nombre == 'administrador':
        usuarios = Usuario.query.filter_by(activo=True).all()
    elif usuario_actual.rol.nombre == 'arquitecto':
        usuarios = Usuario.query.filter(Usuario.activo == True, Usuario.rol.has(nombre='supervisor') | Usuario.rol.has(nombre='trabajador')).all()
    elif usuario_actual.rol.nombre == 'supervisor':
        usuarios = Usuario.query.filter(Usuario.activo == True, Usuario.rol.has(nombre='trabajador')).all()
    elif usuario_actual.rol.nombre == 'trabajador':
        usuarios = [usuario_actual]
    else:
        return jsonify({"error": "Rol no reconocido"}), 403

    return jsonify([{
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol.nombre
    } for usuario in usuarios]), 200

@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
@jwt_required()
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

