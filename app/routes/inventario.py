from flask import Blueprint, request, jsonify
from app import db
from app.models.inventario import Inventario
from app.models.material import Material
from app.models.zona import ZonaTrabajo

inventario_bp = Blueprint("inventario", __name__)

# Listar todo el inventario, agrupado por zona
@inventario_bp.route("/listar", methods=["GET"])
def listar_inventario():
    inventarios = Inventario.query.all()
    resultado = {}
    for inv in inventarios:
        zona = inv.zona.nombre if inv.zona else f"Zona {inv.id_zona}"
        if zona not in resultado:
            resultado[zona] = []
        resultado[zona].append({
            "id_inventario": inv.id_inventario,
            "id_material": inv.id_material,
            "nombre_material": inv.material.nombre if inv.material else None,
            "cantidad": inv.cantidad
        })
    return jsonify(resultado), 200

# Listar inventario de una zona específica
@inventario_bp.route("/zona/<int:id_zona>", methods=["GET"])
def inventario_por_zona(id_zona):
    inventarios = Inventario.query.filter_by(id_zona=id_zona).all()
    resultado = []
    for inv in inventarios:
        resultado.append({
            "id_inventario": inv.id_inventario,
            "id_material": inv.id_material,
            "nombre_material": inv.material.nombre if inv.material else None,
            "cantidad": inv.cantidad
        })
    return jsonify(resultado), 200

# Obtener un registro de inventario por ID
@inventario_bp.route("/obtener/<int:id_inventario>", methods=["GET"])
def obtener_inventario(id_inventario):
    inv = Inventario.query.get_or_404(id_inventario)
    return jsonify({
        "id_inventario": inv.id_inventario,
        "id_material": inv.id_material,
        "nombre_material": inv.material.nombre if inv.material else None,
        "id_zona": inv.id_zona,
        "nombre_zona": inv.zona.nombre if inv.zona else None,
        "cantidad": inv.cantidad
    }), 200

