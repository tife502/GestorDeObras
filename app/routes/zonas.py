from flask import Blueprint, request, jsonify
from app import db
from app.models.zona import ZonaTrabajo
from datetime import datetime


zonas_bp = Blueprint("zonas", __name__)


@zonas_bp.route("/mostrarzonas", methods=["GET"])
def mostrar_zonas():
    zonas = ZonaTrabajo.query.all()
    return jsonify([zona.to_dict() for zona in zonas]), 200

@zonas_bp.route("/crearzonas", methods=["POST"])
def crear_zona():
    data = request.get_json()
    nueva_zona = ZonaTrabajo(
        nombre=data.get("nombre", ""),
        descripcion=data.get("descripcion", ""),
        fecha_inicio=data.get("fecha_inicio"),
        fecha_fin=data.get("fecha_fin"),
    )
    db.session.add(nueva_zona)
    db.session.commit()
    return jsonify(nueva_zona.to_dict()), 201

@zonas_bp.route("/editarzonas/<int:id>", methods=["PUT"])
def editarzona(id):
    data = request.get_json()
    zona = ZonaTrabajo.query.get_or_404(id)

    # Solo actualizar los campos que se envían en la petición
    if "nombre" in data:
        zona.nombre = data["nombre"]
    if "descripcion" in data:
        zona.descripcion = data["descripcion"]
    if "fecha_inicio" in data:
        zona.fecha_inicio = data["fecha_inicio"]
    if "fecha_fin" in data:
        zona.fecha_fin = data["fecha_fin"]

    db.session.commit()
    return jsonify(zona.to_dict()), 200

@zonas_bp.route("/eliminarzona/<int:id>", methods=["DELETE"])
def eliminar_zona(id):
    zona = ZonaTrabajo.query.get_or_404(id)
    db.session.delete(zona)
    db.session.commit()
    return jsonify({"message": "Zona eliminada"}), 200



@zonas_bp.route("zonatrabajo/<int:zona_id>/check_out", methods=["POST"])
def check_out(zona_id):
    data = request.get_json()
    trabajador_id = data.get("trabajador_id")

    zona = ZonaTrabajo.query.get(zona_id)
    if not zona:
        return jsonify({"error": "Zona no encontrada"}), 404
    
    if zona.trabajador_id != trabajador_id:
        return jsonify({"error": "El trabajador no está asignado a esta zona"}), 400
    
    zona.check_out = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Check-out registrado exitosamente"}), 200

