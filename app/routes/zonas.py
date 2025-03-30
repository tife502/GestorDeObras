from flask import Blueprint, request, jsonify
from app import db
from app.models.zona import ZonaTrabajo
from app.models.usuario import Usuario  # Importamos el modelo de Usuario
from datetime import datetime

zonas_bp = Blueprint("zonas", __name__)

@zonas_bp.route("/mostrarzonas", methods=["GET"])
def mostrar_zonas():
    zonas = ZonaTrabajo.query.all()
    return jsonify([{
        "id": zona.id,
        "nombre": zona.nombre,
        "descripcion": zona.descripcion,
        "obra_id": zona.obra_id,
        "trabajador_id": zona.trabajador_id,
        "check_in": zona.check_in.isoformat() if zona.check_in else None,
        "check_out": zona.check_out.isoformat() if zona.check_out else None
    } for zona in zonas]), 200

@zonas_bp.route("/crearzonas", methods=["POST"])
def crear_zona():
    data = request.get_json()
    nueva_zona = ZonaTrabajo(
        nombre=data.get("nombre", ""),
        descripcion=data.get("descripcion", ""),
        obra_id=data.get("obra_id"),
        trabajador_id=data.get("trabajador_id"),
        check_in=datetime.utcnow() if data.get("check_in") else None,
        check_out=datetime.utcnow() if data.get("check_out") else None,
    )
    db.session.add(nueva_zona)
    db.session.commit()
    return jsonify({"message": "Zona creada exitosamente", "id": nueva_zona.id}), 201

@zonas_bp.route("/editarzonas/<int:id>", methods=["PUT"])
def editarzona(id):
    data = request.get_json()
    zona = ZonaTrabajo.query.get_or_404(id)

    if "nombre" in data:
        zona.nombre = data["nombre"]
    if "descripcion" in data:
        zona.descripcion = data["descripcion"]
    if "obra_id" in data:
        zona.obra_id = data["obra_id"]
    if "trabajador_id" in data:
        zona.trabajador_id = data["trabajador_id"]
    if "check_in" in data:
        zona.check_in = datetime.utcnow() if data["check_in"] else None
    if "check_out" in data:
        zona.check_out = datetime.utcnow() if data["check_out"] else None

    db.session.commit()
    return jsonify({"message": "Zona actualizada exitosamente"}), 200

@zonas_bp.route("/eliminarzona/<int:id>", methods=["DELETE"])
def eliminar_zona(id):
    zona = ZonaTrabajo.query.get_or_404(id)
    db.session.delete(zona)
    db.session.commit()
    return jsonify({"message": "Zona eliminada exitosamente"}), 200

@zonas_bp.route("/trabajadores", methods=["GET"])
def obtener_trabajadores():
    trabajadores = Usuario.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in trabajadores]), 200

@zonas_bp.route("/zonatrabajo/<int:zona_id>/check_in", methods=["POST"])
def check_in(zona_id):
    data = request.get_json()
    trabajador_id = data.get("trabajador_id")

    trabajador = Usuario.query.get(trabajador_id)
    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    zona = ZonaTrabajo.query.get(zona_id)
    if not zona:
        return jsonify({"error": "Zona no encontrada"}), 404

    if zona.trabajador_id != trabajador.id:
        return jsonify({"error": "El trabajador no está asignado a esta zona"}), 400

    if zona.check_in:
        return jsonify({"error": "El check-in ya fue registrado"}), 400

    zona.check_in = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Check-in registrado exitosamente"}), 200
    
@zonas_bp.route("/zonatrabajo/<int:zona_id>/check_out", methods=["POST"])
def check_out(zona_id):
    data = request.get_json()
    trabajador_id = data.get("trabajador_id")

    trabajador = Usuario.query.get(trabajador_id)
    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    zona = ZonaTrabajo.query.get(zona_id)
    if not zona:
        return jsonify({"error": "Zona no encontrada"}), 404
    
    if zona.trabajador_id != trabajador.id:
        return jsonify({"error": "El trabajador no está asignado a esta zona"}), 400
    
    zona.check_out = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Check-out registrado exitosamente"}), 200

