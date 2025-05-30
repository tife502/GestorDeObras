from flask import Blueprint, jsonify
from app import db
from app.models.bodega import Bodega
from app.models.material import Material

bodega_bp = Blueprint("bodega", __name__)

# Listar todos los materiales en bodega con su cantidad
@bodega_bp.route("/listar", methods=["GET"])
def listar_bodega():
    materiales_bodega = Bodega.query.all()
    resultado = []
    for b in materiales_bodega:
        resultado.append({
            "id_material": b.id_material,
            "nombre_material": b.material.nombre if b.material else None,
            "cantidad": b.cantidad
        })
    return jsonify(resultado), 200

# Obtener un material de la bodega por id_material
@bodega_bp.route("/obtener/<int:id_material>", methods=["GET"])
def obtener_material_bodega(id_material):
    b = Bodega.query.get_or_404(id_material)
    return jsonify({
        "id_material": b.id_material,
        "nombre_material": b.material.nombre if b.material else None,
        "cantidad": b.cantidad
    }), 200

