from flask import Blueprint, request, jsonify
from app import db
from app.models.material import Material

materiales_bp = Blueprint("materiales", __name__)

UNIDADES_VALIDAS = ["kg", "g", "t", "lb", "und"]  # Kilogramos, gramos, toneladas, libras

def validar_unidad_medida(unidad):
    if unidad not in UNIDADES_VALIDAS:
        raise ValueError(f"Unidad de medida no válida. Las unidades válidas son: {', '.join(UNIDADES_VALIDAS)}")

@materiales_bp.route("/crearmateriales", methods=["POST"])
def crear_material():
    data = request.get_json()

    nombre = data.get("nombre")
    cantidad_disponible = data.get("cantidad_disponible", 0)
    unidad_medida = data.get("unidad_medida", "kg")  # Valor predeterminado: kg
    id_zona = data.get("id_zona")

    if not nombre:
        return jsonify({"error": "El nombre del material es obligatorio"}), 400

    if not id_zona:
        return jsonify({"error": "El ID de la zona es obligatorio"}), 400

    try:
        cantidad_disponible = float(cantidad_disponible)
        if cantidad_disponible < 0:
            return jsonify({"error": "La cantidad disponible no puede ser negativa"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    try:
        validar_unidad_medida(unidad_medida)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    nuevo_material = Material(
        nombre=nombre,
        cantidad_disponible=cantidad_disponible,
        unidad_medida=unidad_medida,
        id_zona=id_zona
    )

    db.session.add(nuevo_material)
    db.session.commit()

    return jsonify({"mensaje": "Material creado exitosamente", "id": nuevo_material.id}), 201

@materiales_bp.route("/mostrarmateriales", methods=["GET"])
def obtener_materiales():
    materiales = Material.query.all()
    return jsonify([{
        "id": material.id,
        "nombre": material.nombre,
        "cantidad_disponible": material.cantidad_disponible,
        "unidad_medida": material.unidad_medida,
        "id_zona": material.id_zona
    } for material in materiales]), 200

@materiales_bp.route("/modificarmateriales/<int:material_id>", methods=["PUT"])
def modificar_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404

    data = request.get_json()

    if "nombre" in data:
        material.nombre = data["nombre"]

    if "cantidad_disponible" in data:
        try:
            nueva_cantidad = float(data["cantidad_disponible"])
            if nueva_cantidad < 0:
                return jsonify({"error": "La cantidad disponible no puede ser negativa"}), 400
            material.cantidad_disponible = nueva_cantidad
        except (ValueError, TypeError):
            return jsonify({"error": "La cantidad debe ser un número válido"}), 400

    if "unidad_medida" in data:
        try:
            validar_unidad_medida(data["unidad_medida"])
            material.unidad_medida = data["unidad_medida"]
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if "id_zona" in data:
        material.id_zona = data["id_zona"]

    db.session.commit()
    return jsonify({"mensaje": "Material actualizado exitosamente"}), 200

@materiales_bp.route("/eliminarmateriales/<int:material_id>", methods=["DELETE"])
def eliminar_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material no encontrado"}), 404

    db.session.delete(material)
    db.session.commit()

    return jsonify({"mensaje": "Material eliminado exitosamente"}), 200

@materiales_bp.route("/unidadesmedida", methods=["GET"])
def obtener_unidades_medida():
    return jsonify({"unidades": UNIDADES_VALIDAS}), 200







