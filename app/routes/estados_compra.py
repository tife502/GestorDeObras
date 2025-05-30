from flask import Blueprint, request, jsonify
from app import db
from app.models.estados_compra import EstadosCompra

estados_compra_bp = Blueprint("estados_compra", __name__)

# Listar todos los estados de compra
@estados_compra_bp.route("/listarestadocompra", methods=["GET"])
def listar_estados_compra():
    estados = EstadosCompra.query.all()
    resultado = []
    for estado in estados:
        resultado.append({
            "id": estado.id,
            "nombre": estado.nombre
        })
    return jsonify(resultado), 200

# Obtener un estado de compra por ID
@estados_compra_bp.route("/estadocompra/<int:id>", methods=["GET"])
def obtener_estado_compra(id):
    estado = EstadosCompra.query.get_or_404(id)
    return jsonify({
        "id": estado.id,
        "nombre": estado.nombre
    }), 200