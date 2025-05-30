from flask import Blueprint, jsonify
from app import db
from app.models.estado_solicitud import EstadoSolicitud

estados_solicitud_bp = Blueprint("estados_solicitud", __name__)

# Listar todos los estados de solicitud
@estados_solicitud_bp.route("/listaestadosolicitud", methods=["GET"])
def listar_estados():
    estados = EstadoSolicitud.query.all()
    resultado = []
    for estado in estados:
        resultado.append({
            "id_nombre": estado.id_nombre,
            "nombre": estado.nombre
        })
    return jsonify(resultado), 200

# Obtener un estado de solicitud por ID
@estados_solicitud_bp.route("/estadosolicitud/<int:id_nombre>", methods=["GET"])
def obtener_estado(id_nombre):
    estado = EstadoSolicitud.query.get_or_404(id_nombre)
    return jsonify({
        "id_nombre": estado.id_nombre,
        "nombre": estado.nombre
    }), 200

