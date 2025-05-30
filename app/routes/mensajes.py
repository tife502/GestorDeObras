from flask import Blueprint, request, jsonify
from app import db
from app.models.mensajes import Mensaje
from app.models.usuario import Usuario

mensajes_bp = Blueprint("mensajes", __name__)

# Obtener mensajes filtrados por conversacion_id (grupal o privado)
@mensajes_bp.route("/mensajes", methods=["GET"])
def obtener_mensajes():
    conversacion_id = request.args.get("conversacion_id", "grupal")
    mensajes = Mensaje.query.filter_by(conversacion_id=conversacion_id).order_by(Mensaje.fecha_envio).all()
    resultado = []
    for m in mensajes:
        d = m.to_dict()
        usuario = Usuario.query.get(m.usuario_id)
        d["usuario_nombre"] = usuario.nombre if usuario else "Usuario"
        resultado.append(d)
    return jsonify(resultado), 200

# Enviar mensaje (grupal o privado)
@mensajes_bp.route("/mensaje", methods=["POST"])
def enviar_mensaje_http():
    data = request.json
    usuario_id = data.get("usuario_id")
    mensaje = data.get("mensaje")
    conversacion_id = data.get("conversacion_id", "grupal")
    destinatario_id = data.get("destinatario_id")

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 400

    nuevo_mensaje = Mensaje(
        usuario_id=usuario_id,
        mensaje=mensaje,
        conversacion_id=conversacion_id,
        destinatario_id=destinatario_id
    )
    db.session.add(nuevo_mensaje)
    db.session.commit()

    mensaje_dict = nuevo_mensaje.to_dict()
    mensaje_dict['usuario_nombre'] = usuario.nombre

    return jsonify(mensaje_dict), 201
