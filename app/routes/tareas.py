from flask import Blueprint, jsonify, request
from app import db
from app.models.zona import ZonaTrabajo
from app.models.usuario import Usuario 
from app.models.tarea import Tarea # Asegúrate de que el modelo Tarea esté importado correctamente

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route("/obtenertareas", methods=["GET"])
def obtener_tareas():
    tareas = Tarea.query.all()  # Recupera todas las tareas
    return jsonify([{
        "id": tarea.id,
        "descripcion": tarea.descripcion,
        "estado": tarea.estado,
        "trabajador_id": tarea.trabajador_id,
        "evidencia": tarea.evidencia,
        "id_zona": tarea.id_zona
    } for tarea in tareas]), 200

@tareas_bp.route("/creartareas", methods=["POST"])
def crear_tarea():
    data = request.json

    # Verificar si los campos obligatorios están presentes
    if not data.get('descripcion') or not data.get('trabajador_id'):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Verificar si el trabajador existe
    # En tu endpoint crear_tarea
    trabajador = Usuario.query.get(data['trabajador_id'])
    if not trabajador:
            return jsonify({"error": "Trabajador no encontrado"}), 404

    if data.get('id_zona') and str(trabajador.id_zona) != str(data['id_zona']):
            return jsonify({"error": "El trabajador no pertenece a la zona seleccionada"}), 400
    # Verificar si la zona de trabajo existe (opcional)
    zona_trabajo = None
    if data.get('id_zona'):
        zona_trabajo = ZonaTrabajo.query.get(data['id_zona'])
        if not zona_trabajo:
            return jsonify({"error": "Zona de trabajo no encontrada"}), 404

    # Crear la tarea
    tarea = Tarea(
        descripcion=data['descripcion'],
        trabajador_id=data['trabajador_id'],
        evidencia=data.get('evidencia'),
        id_zona=data.get('id_zona'),
        estado=bool(data.get('estado', False))  # Convertir a booleano, por defecto False
    )

    db.session.add(tarea)
    db.session.commit()

    return jsonify({
        "mensaje": "Tarea creada exitosamente",
        "id": tarea.id,
        "descripcion": tarea.descripcion,
        "trabajador_id": tarea.trabajador_id,
        "evidencia": tarea.evidencia,
        "id_zona": tarea.id_zona,
        "estado": tarea.estado
    }), 201


@tareas_bp.route("/modificartarea/<int:id>", methods=["PUT"])
def modificar_tarea(id):
    data = request.json
    tarea = Tarea.query.get(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Actualizar los campos si están presentes en el request
    tarea.descripcion = data.get("descripcion", tarea.descripcion)
    tarea.estado = bool(data.get("estado", tarea.estado))  # Convertir a booleano
    tarea.trabajador_id = data.get("trabajador_id", tarea.trabajador_id)
    tarea.evidencia = data.get("evidencia", tarea.evidencia)
    tarea.id_zona = data.get("id_zona", tarea.id_zona)

    db.session.commit()

    return jsonify({"mensaje": "Tarea modificada correctamente"}), 200

@tareas_bp.route("/eliminartarea/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    tarea = Tarea.query.get(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(tarea)
    db.session.commit()

    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200

@tareas_bp.route("/obtenertareas/<int:trabajador_id>", methods=["GET"])
def obtener_tareas_por_trabajador(trabajador_id):
    tareas = Tarea.query.filter_by(trabajador_id=trabajador_id).all()
    return jsonify([{
        "id": tarea.id,
        "descripcion": tarea.descripcion,
        "estado": tarea.estado,
        "trabajador_id": tarea.trabajador_id,
        "evidencia": tarea.evidencia,
        "id_zona": tarea.id_zona
    } for tarea in tareas]), 200

