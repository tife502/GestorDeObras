from flask import Blueprint, request, jsonify
from app import db
from app.models.material import Material
from app.models.usuario import Usuario
from app.models.solicitud import SolicitudMaterial

materiales_bp = Blueprint("materiales", __name__)

# Obtener todos los materiales
@materiales_bp.route("/materiales", methods=["GET"])
def obtener_materiales():
    materiales = Material.query.all()
    materiales_json = [{"id": m.id, "nombre": m.nombre, "cantidad_disponible": m.cantidad_disponible} for m in materiales]
    return jsonify(materiales_json), 200

# Obtener un material por ID
@materiales_bp.route("/materiales/<int:material_id>", methods=["GET"])
def obtener_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404
    return jsonify({"id": material.id, "nombre": material.nombre, "cantidad_disponible": material.cantidad_disponible}), 200

# Crear un nuevo material
@materiales_bp.route("/crearmateriales", methods=["POST"])
def crear_material():
    data = request.get_json()
    nombre = data.get("nombre")
    cantidad_disponible = data.get("cantidad_disponible", 0)

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    try:
        cantidad_disponible = int(cantidad_disponible)
        if cantidad_disponible < 0:  # Validar que la cantidad inicial no sea negativa
            return jsonify({"error": "La cantidad disponible no puede ser negativa"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    nuevo_material = Material(nombre=nombre, cantidad_disponible=cantidad_disponible)
    db.session.add(nuevo_material)
    db.session.commit()

    return jsonify({"message": "Material creado exitosamente", "id": nuevo_material.id}), 201

# Actualizar un material
@materiales_bp.route("/materiales/<int:material_id>", methods=["PUT"])
def actualizar_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404

    data = request.get_json()

    if "cantidad_disponible" in data:
        try:
            nueva_cantidad = int(data["cantidad_disponible"])
            if nueva_cantidad < 0:  # Validar que la cantidad no sea negativa
                return jsonify({"error": "La cantidad disponible no puede ser negativa"}), 400
            material.cantidad_disponible = nueva_cantidad
        except (ValueError, TypeError):
            return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    material.nombre = data.get("nombre", material.nombre)
    db.session.commit()
    return jsonify({"message": "Material actualizado exitosamente"}), 200

# Eliminar un material
@materiales_bp.route("/materiales/<int:material_id>", methods=["DELETE"])
def eliminar_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404

    db.session.delete(material)
    db.session.commit()
    return jsonify({"message": "Material eliminado exitosamente"}), 200

# Obtener todas las solicitudes


# Crear nueva solicitud
@materiales_bp.route("/materiales/solicitudes", methods=["POST"])
def crear_solicitud():
    data = request.json

    if "material_id" not in data or "cantidad" not in data or "trabajador_id" not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    material = Material.query.get(data["material_id"])
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404

    trabajador = Usuario.query.get(data["trabajador_id"])
    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    try:
        cantidad_solicitada = int(data["cantidad"])
        if cantidad_solicitada <= 0:  # Validar que la cantidad sea positiva
            return jsonify({"error": "La cantidad solicitada debe ser un número positivo"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    if cantidad_solicitada > material.cantidad_disponible:
        return jsonify({"error": "Cantidad solicitada excede el inventario"}), 400

    # Restar la cantidad del inventario
    material.cantidad_disponible -= cantidad_solicitada
    db.session.commit()

    return jsonify({"mensaje": "Solicitud procesada exitosamente"}), 201

# Actualizar estado de solicitud
@materiales_bp.route("/materiales/solicitudes/<int:id>", methods=["PUT"])
def actualizar_solicitud(id):
    solicitud = SolicitudMaterial.query.get(id)
    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    data = request.json
    solicitud.estado = data.get("estado", solicitud.estado)
    db.session.commit()

    return jsonify({"mensaje": "Solicitud actualizada"}), 200

# Eliminar solicitud y devolver material al inventario si estaba aprobada
@materiales_bp.route("/materiales/solicitudes/<int:id>", methods=["DELETE"])
def eliminar_solicitud(id):
    solicitud = SolicitudMaterial.query.get(id)
    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    material = Material.query.get(solicitud.material_id)
    if solicitud.estado == "Aprobada":
        material.cantidad_disponible += solicitud.cantidad

    db.session.delete(solicitud)
    db.session.commit()

    return jsonify({"mensaje": "Solicitud eliminada"}), 200

@materiales_bp.route("/trabajadores", methods=["GET"]) 
def obtener_trabajadores():
    trabajadores = Usuario.query.all()
    return jsonify([{"id": t.id, "nombre": t.nombre} for t in trabajadores]), 200

# Obtener todas las solicitudes

@materiales_bp.route("/mostrarsolicitudes", methods=["GET"])
def obtener_solicitudes():
    solicitudes = SolicitudMaterial.query.all()
    solicitudes_json = [
        {
            "id": s.id,
            "trabajador_id": s.trabajador_id,
            "material_id": s.material_id,
            "cantidad": s.cantidad,
            "estado": s.estado,
            "fecha_solicitud": s.fecha_solicitud.strftime("%Y-%m-%d %H:%M:%S")
        }
        for s in solicitudes
    ]
    return jsonify(solicitudes_json), 200

