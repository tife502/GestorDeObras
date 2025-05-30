from flask import Blueprint, request, jsonify
from app import db
from app.models.unidadmedida import UnidadMedida

unidad_medida_bp = Blueprint("unidadmedida", __name__)

# Crear una unidad de medida
@unidad_medida_bp.route("/crearunidadmedida", methods=["POST"])
def crear_unidad():
    data = request.get_json()
    nombre = data.get("nombre")
    abreviatura = data.get("abreviatura")
    if not nombre or not abreviatura:
        return jsonify({"error": "Nombre y abreviatura son obligatorios"}), 400
    unidad = UnidadMedida(nombre=nombre, abreviatura=abreviatura)
    db.session.add(unidad)
    db.session.commit()
    return jsonify({"mensaje": "Unidad de medida creada", "id": unidad.id}), 201

# Listar todas las unidades de medida
@unidad_medida_bp.route("/listarunidadesmedida", methods=["GET"])
def listar_unidades():
    unidades = UnidadMedida.query.all()
    resultado = []
    for u in unidades:
        resultado.append({
            "id": u.id,
            "nombre": u.nombre,
            "abreviatura": u.abreviatura
        })
    return jsonify(resultado), 200

# Obtener una unidad de medida por ID
@unidad_medida_bp.route("/obtenerunidadmedida/<int:id>", methods=["GET"])
def obtener_unidad(id):
    unidad = UnidadMedida.query.get_or_404(id)
    return jsonify({
        "id": unidad.id,
        "nombre": unidad.nombre,
        "abreviatura": unidad.abreviatura
    }), 200

# Actualizar una unidad de medida
@unidad_medida_bp.route("/actualizarunidadmedida/<int:id>", methods=["PUT"])
def actualizar_unidad(id):
    unidad = UnidadMedida.query.get_or_404(id)
    data = request.get_json()
    unidad.nombre = data.get("nombre", unidad.nombre)
    unidad.abreviatura = data.get("abreviatura", unidad.abreviatura)
    db.session.commit()
    return jsonify({"mensaje": "Unidad de medida actualizada"}), 200

# Eliminar una unidad de medida
@unidad_medida_bp.route("/eliminarunidad/<int:id>", methods=["DELETE"])
def eliminar_unidad(id):
    unidad = UnidadMedida.query.get_or_404(id)
    db.session.delete(unidad)
    db.session.commit()
    return jsonify({"mensaje": "Unidad de medida eliminada"}), 200