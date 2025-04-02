from flask import Blueprint, request, jsonify
from app import db
from app.models.solicitud import SolicitudMaterial
from app.models.usuario import Usuario  # Asegúrate de importar el modelo correcto
from app.models.zona import ZonaTrabajo
from datetime import datetime
from app.models.material import Material  # Asegúrate de importar el modelo correcto

solicitudes_bp = Blueprint("solicitudes", __name__)

@solicitudes_bp.route("/crearsolicitud", methods=["POST"])
def crear_solicitud():
    data = request.get_json()

    trabajador_id = data.get("trabajador_id")
    cantidad = data.get("cantidad")
    id_zona = data.get("id_zona")
    nombre = data.get("nombre")  # Nuevo campo

    # Validación de datos obligatorios
    if not trabajador_id or not cantidad or not id_zona or not nombre:
        return jsonify({"error": "El trabajador, la cantidad, la zona y el nombre del material son obligatorios"}), 400

    # Verificar si el trabajador existe
    trabajador = Usuario.query.get(trabajador_id)
    if not trabajador:
        return jsonify({"error": "El trabajador no existe"}), 404

    # Verificar si la zona existe
    zona = ZonaTrabajo.query.get(id_zona)
    if not zona:
        return jsonify({"error": "La zona no existe"}), 404

    # Validación de cantidad
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser mayor a 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    # Crear solicitud
    nueva_solicitud = SolicitudMaterial(
        trabajador_id=trabajador_id,
        cantidad=cantidad,
        id_zona=id_zona,
        nombre=nombre,  # Asignar el nombre del material
        estado="Pendiente",
        fecha_solicitud=datetime.utcnow()
    )

    try:
        db.session.add(nueva_solicitud)
        db.session.commit()
        return jsonify({"mensaje": "Solicitud creada exitosamente", "id": nueva_solicitud.id}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error al crear la solicitud: {e}")  # Imprimir el error en la consola
        return jsonify({"error": f"Error al crear la solicitud: {str(e)}"}), 500

@solicitudes_bp.route("/mostrarsolicitudes", methods=["GET"])
def obtener_solicitudes():
    solicitudes = SolicitudMaterial.query.all()
    return jsonify([
        {
            "id": solicitud.id,
            "trabajador_id": solicitud.trabajador_id,
            "cantidad": solicitud.cantidad,
            "estado": solicitud.estado,
            "fecha_solicitud": solicitud.fecha_solicitud.isoformat(),
            "id_zona": solicitud.id_zona,
            "nombre": solicitud.nombre  # Incluir el nombre del material
        }
        for solicitud in solicitudes
    ]), 200

@solicitudes_bp.route("/modificarsolicitud/<int:solicitud_id>", methods=["PUT"])
def modificar_solicitud(solicitud_id):
    solicitud = SolicitudMaterial.query.get(solicitud_id)
    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    data = request.get_json()

    if "cantidad" in data:
        try:
            nueva_cantidad = int(data["cantidad"])
            if nueva_cantidad <= 0:
                return jsonify({"error": "La cantidad debe ser mayor a 0"}), 400
            solicitud.cantidad = nueva_cantidad
        except (ValueError, TypeError):
            return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    if "estado" in data:
        solicitud.estado = data["estado"]

    if "id_zona" in data:
        zona = ZonaTrabajo.query.get(data["id_zona"])
        if not zona:
            return jsonify({"error": "La zona no existe"}), 404
        solicitud.id_zona = data["id_zona"]

    if "nombre" in data:  # Actualizar el nombre del material
        solicitud.nombre = data["nombre"]

    try:
        db.session.commit()
        return jsonify({"mensaje": "Solicitud actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al modificar la solicitud: {e}")  # Imprimir el error en la consola
        return jsonify({"error": f"Error al modificar la solicitud: {str(e)}"}), 500

@solicitudes_bp.route("/eliminarsolicitud/<int:solicitud_id>", methods=["DELETE"])
def eliminar_solicitud(solicitud_id):
    solicitud = SolicitudMaterial.query.get(solicitud_id)
    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    try:
        db.session.delete(solicitud)
        db.session.commit()
        return jsonify({"mensaje": "Solicitud eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar la solicitud: {e}")  # Imprimir el error en la consola
        return jsonify({"error": f"Error al eliminar la solicitud: {str(e)}"}), 500
    
@solicitudes_bp.route("/aprobar-solicitud/<int:solicitud_id>", methods=["PUT"])
def aprobar_solicitud(solicitud_id):
    solicitud = SolicitudMaterial.query.get(solicitud_id)
    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    data = request.get_json()

    # Validar que el estado sea "Aprobado"
    estado = data.get("estado")
    if estado != "Aprobado":
        return jsonify({"error": "El estado debe ser 'Aprobado' para crear un material"}), 400

    try:
        # Actualizar el estado de la solicitud
        solicitud.estado = estado
        db.session.commit()

        # Crear un nuevo material basado en la solicitud
        nuevo_material = Material(
            nombre=solicitud.nombre,  # Nombre del material solicitado
            cantidad_disponible=solicitud.cantidad,  # Cantidad solicitada
            id_zona=solicitud.id_zona  # Zona asociada a la solicitud
        )

        db.session.add(nuevo_material)
        db.session.commit()

        return jsonify({
            "mensaje": "Solicitud aprobada y material creado exitosamente",
            "material": {
                "id": nuevo_material.id,
                "nombre": nuevo_material.nombre,
                "cantidad_disponible": nuevo_material.cantidad_disponible,
                "id_zona": nuevo_material.id_zona
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al aprobar la solicitud y crear el material: {e}")  # Imprimir el error en la consola
        return jsonify({"error": f"Error al aprobar la solicitud y crear el material: {str(e)}"}), 500
