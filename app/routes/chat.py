from app import db, socketio
from app.models.mensajes import Mensaje
from app.models.usuario import Usuario
from flask_socketio import emit

# Solo eventos WebSocket, sin rutas HTTP

@socketio.on("send_message")
def handle_message(data):
    usuario_id = data["usuario_id"]
    mensaje = data["mensaje"]
    conversacion_id = data.get("conversacion_id", "grupal")
    destinatario_id = data.get("destinatario_id")

    nuevo_mensaje = Mensaje(
        usuario_id=usuario_id,
        mensaje=mensaje,
        conversacion_id=conversacion_id,
        destinatario_id=destinatario_id
    )
    db.session.add(nuevo_mensaje)
    db.session.commit()

    mensaje_dict = nuevo_mensaje.to_dict()
    usuario = Usuario.query.get(usuario_id)
    mensaje_dict['usuario_nombre'] = usuario.nombre if usuario else "Usuario"

    emit("receive_message", mensaje_dict, broadcast=True)