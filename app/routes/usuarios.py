from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.usuario import Usuario
from flask_jwt_extended import create_access_token

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/registro", methods=["POST"])
def registrar_usuario():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    nuevo_usuario = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        password=hashed_password,
        rol_id=data["rol_id"]
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@usuarios_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data["email"]).first()
    
    if usuario and bcrypt.check_password_hash(usuario.password, data["password"]):
        token = create_access_token(identity=usuario.id)
        return jsonify({"token": token}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

@usuarios_bp.route("/helo", methods=["GET"])
def prueba():
    data = request.json
    return jsonify({"mensaje": "Hola mundo"}), 200
    
@usuarios_bp.route("/mostrar", methods=["GET"])
def obtenerusuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [usuario.to_dict() for usuario in usuarios]  # Convertir a JSON
    return jsonify(usuarios_json), 200