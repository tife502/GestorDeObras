from flask import Blueprint, request, jsonify
from app import db
from app.models.zona import ZonaTrabajo
from app.models.usuario import Usuario  
from app.models.tarea import Tarea
from datetime import datetime

zonas_bp = Blueprint("zonas", __name__)

@zonas_bp.route("/crearzonas", methods=["POST"])
def crear_zona():
    data = request.get_json()

    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "")
    ubicacion = data.get("ubicacion", None)
    finalizada = data.get("finalizada", False)

    if not nombre:
        return jsonify({"error": "El nombre de la zona es obligatorio"}), 400

    nueva_zona = ZonaTrabajo(
        nombre=nombre,
        descripcion=descripcion,
        ubicacion=ubicacion,
        finalizada=finalizada
    )

    db.session.add(nueva_zona)
    db.session.commit()

    return jsonify({"mensaje": "Zona de trabajo creada exitosamente", "id": nueva_zona.id}), 201

@zonas_bp.route("/mostrarzonas", methods=["GET"])
def obtener_zonas():
    zonas = ZonaTrabajo.query.all()
    resultado = []

    for zona in zonas:
        # Obtener todas las tareas relacionadas con esta zona
        tareas = Tarea.query.filter_by(id_zona=zona.id).all()

        total_tareas = len(tareas)
        tareas_completadas = len([t for t in tareas if t.estado.strip().lower() == "completada"])

        # Calcular el avance
        avance = round((tareas_completadas / total_tareas) * 100) if total_tareas > 0 else 0

        # Verificar si todas las tareas están completadas para actualizar el estado de 'finalizada'
        zona.finalizada = True if tareas_completadas == total_tareas else False
        
        # Guardar los cambios en la base de datos si el estado de finalizada cambió
        db.session.commit()

        # Construir el diccionario con el campo "avance" y "finalizada"
        resultado.append({
            "id": zona.id,
            "nombre": zona.nombre,
            "descripcion": zona.descripcion,
            "ubicacion": zona.ubicacion,
            "finalizada": zona.finalizada,  
            "avance": avance  
        })

    return jsonify(resultado), 200



@zonas_bp.route("/modificarzonas/<int:id>", methods=["PUT"])
def modificar_zona(id):
    zona = ZonaTrabajo.query.get(id)
    if not zona:
        return jsonify({"error": "Zona de trabajo no encontrada"}), 404

    data = request.get_json()

    zona.nombre = data.get("nombre", zona.nombre)
    zona.descripcion = data.get("descripcion", zona.descripcion)
    zona.ubicacion = data.get("ubicacion", zona.ubicacion)
    zona.finalizada = data.get("finalizada", zona.finalizada)

    db.session.commit()

    return jsonify({"mensaje": "Zona de trabajo actualizada exitosamente"}), 200

@zonas_bp.route("/eliminarzonas/<int:id>", methods=["DELETE"])
def eliminar_zona(id):
    zona = ZonaTrabajo.query.get(id)
    if not zona:
        return jsonify({"error": "Zona de trabajo no encontrada"}), 404

    db.session.delete(zona)
    db.session.commit()

    return jsonify({"mensaje": "Zona de trabajo eliminada exitosamente"}), 200





