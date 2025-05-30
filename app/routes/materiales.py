import unicodedata
import re
from flask import Blueprint, request, jsonify
from app import db
from app.models.material import Material
from app.models.unidadmedida import UnidadMedida
from app.models.orden_compra import OrdenCompra
from app.models.bodega import Bodega


materiales_bp = Blueprint("materiales", __name__)

def limpiar_nombre(nombre):
    nfkd = unicodedata.normalize('NFKD', nombre)
    solo_ascii = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    limpio = re.sub(r'[^a-zA-Z0-9\s]', '', solo_ascii)
    return limpio.lower().strip()

# Crear un material
@materiales_bp.route("/crearmaterial", methods=["POST"])
def crear_material():
    data = request.get_json()
    nombre = data.get("nombre")
    id_unidad = data.get("id_unidad")
    if not nombre or not id_unidad:
        return jsonify({"error": "Nombre e id_unidad son obligatorios"}), 400

    nombre_limpio = limpiar_nombre(nombre)
    material_existente = Material.query.filter(
        db.func.lower(db.func.unaccent(Material.nombre)) == nombre_limpio
    ).first()
    if material_existente:
        return jsonify({"error": "Ya existe un material con ese nombre"}), 400

    material = Material(nombre=nombre_limpio, id_unidad=id_unidad)
    db.session.add(material)
    db.session.commit()
    return jsonify({"mensaje": "Material creado", "id": material.id}), 201

# Listar todos los materiales
@materiales_bp.route("/listarmateriales", methods=["GET"])
def listar_materiales():
    materiales = Material.query.filter_by(activo=True).all()
    resultado = []
    for m in materiales:
        unidad = UnidadMedida.query.get(m.id_unidad)
        resultado.append({
            "id": m.id,
            "nombre": m.nombre,
            "id_unidad": m.id_unidad,
            "unidad_nombre": unidad.nombre if unidad else "",
            "unidad_abreviatura": unidad.abreviatura if unidad else ""
        })
    return jsonify(resultado), 200

# Obtener un material por ID
@materiales_bp.route("/obtenermaterial/<int:id>", methods=["GET"])
def obtener_material(id):
    material = Material.query.get_or_404(id)
    return jsonify({
        "id": material.id,
        "nombre": material.nombre,
        "id_unidad": material.id_unidad
    }), 200

# Actualizar un material
@materiales_bp.route("/actualizarmaterial/<int:id>", methods=["PUT"])
def actualizar_material(id):
    material = Material.query.get_or_404(id)
    data = request.get_json()
    nombre = data.get("nombre", material.nombre)
    id_unidad = data.get("id_unidad", material.id_unidad)

    nombre_limpio = limpiar_nombre(nombre)
    material_existente = Material.query.filter(
        db.func.lower(db.func.unaccent(Material.nombre)) == nombre_limpio,
        Material.id != id
    ).first()
    if material_existente:
        return jsonify({"error": "Ya existe un material con ese nombre"}), 400

    material.nombre = nombre_limpio
    material.id_unidad = id_unidad
    db.session.commit()
    return jsonify({"mensaje": "Material actualizado"}), 200

# Eliminar un material
@materiales_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_material(id):
    material = Material.query.get_or_404(id)
    material.activo = False
    db.session.commit()
    return jsonify({"mensaje": "Material ocultado"}), 200









