from flask import Blueprint, request, jsonify
from datetime import date
from app import db
from app.models.obra import Obra

obras_bp = Blueprint('obras', __name__)

@obras_bp.route('/mostrar', methods=['GET'])
def mostrar_obras():
    obras = Obra.query.all()
    return jsonify([obra.to_dict() for obra in obras]), 200

@obras_bp.route('/crear', methods=['POST'])
def crear_obra():
    data = request.get_json()

    fecha_inicio = data.get("fecha_inicio", date.today())  # Fecha actual si no se envía
    fecha_final = data.get("fecha_fin")  # Puede ser None

    if fecha_final and fecha_final < fecha_inicio:
        return jsonify({"error": "La fecha de fin no puede ser anterior a la fecha de inicio"}), 400

    # Asignar valores predeterminados si no se envían
    nueva_obra = Obra(
        nombre=data.get("nombre", ""),
        descripcion=data.get("descripcion", ""),
        fecha_inicio=fecha_inicio,
        fecha_fin= fecha_final
    )

    db.session.add(nueva_obra)
    db.session.commit()
    return jsonify(nueva_obra.to_dict()), 201

@obras_bp.route('/editar/<int:id>', methods=['PUT'])
def editar_obra(id):
    data = request.get_json()
    obra = Obra.query.get_or_404(id)

    # Solo actualizar los campos que se envían en la petición
    if "nombre" in data:
        obra.nombre = data["nombre"]
    if "descripcion" in data:
        obra.descripcion = data["descripcion"]
    if "fecha_inicio" in data:
        obra.fecha_inicio = data["fecha_inicio"]
    if "fecha_fin" in data:
        obra.fecha_fin = data["fecha_fin"]

    db.session.commit()
    return jsonify(obra.to_dict()), 200

@obras_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar_obra(id):
    obra = Obra.query.get_or_404(id)
    db.session.delete(obra)
    db.session.commit()
    return jsonify({"message": "Obra eliminada con éxito"}), 200


