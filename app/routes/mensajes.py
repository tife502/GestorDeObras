from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from app import db
from app.models import Mensaje
from app.models import Usuario

# Crear el Blueprint
chat_bp = Blueprint("mensajes", __name__)

# Para trabajar con SocketIO
from app import socketio

from flask import Blueprint, request, jsonify
from app import db
from app.models import Mensaje, Usuario

# Crear el Blueprint
chat_bp = Blueprint("mensajes", __name__)

# Ruta para obtener los mensajes grupales
# Ruta para obtener los mensajes grupales
@chat_bp.route("/mensaje", methods=["POST"])
def enviar_mensaje_http():
    data = request.json
    usuario_id = data.get("usuario_id")  # Este es el ID que estás recibiendo del cliente
    mensaje = data.get("mensaje")

    # Buscar al usuario por su ID
    usuario = Usuario.query.get(usuario_id)  # No uses usuario.id, ya que usuario ya es un ID

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 400

    nuevo_mensaje = Mensaje(usuario_id=usuario_id, mensaje=mensaje)
    db.session.add(nuevo_mensaje)
    db.session.commit()

    # Añadir el nombre del usuario al mensaje antes de devolverlo
    mensaje_dict = nuevo_mensaje.to_dict()
    mensaje_dict['usuario_nombre'] = usuario.nombre  # Asegúrate de que 'nombre' esté disponible

    return jsonify(mensaje_dict), 201



# Evento para recibir y enviar mensajes en tiempo real (WebSocket)
@socketio.on("send_message")
def handle_message(data):
    """
    Evento que maneja el envío de mensajes en tiempo real a través de WebSocket.
    """
    usuario_id = data["usuario_id"]
    mensaje = data["mensaje"]

    nuevo_mensaje = Mensaje(
        usuario_id=usuario_id,
        mensaje=mensaje
    )

    db.session.add(nuevo_mensaje)
    db.session.commit()

    # Crear el diccionario para emitir el mensaje
    mensaje_dict = nuevo_mensaje.to_dict()

    # Emitir el mensaje a todos los clientes conectados (mensajes grupales)
    emit("receive_message", mensaje_dict, broadcast=True)

@chat_bp.route("/mensajes", methods=["GET"])
def obtener_mensajes_grupales():
    mensajes = Mensaje.query.order_by(Mensaje.fecha_envio).all()
    return jsonify([m.to_dict() for m in mensajes])
