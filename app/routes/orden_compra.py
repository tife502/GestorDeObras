from flask import Blueprint, request, jsonify
from app import db
from app.models.orden_compra import OrdenCompra
from app.models.bodega import Bodega
from datetime import datetime

orden_compra_bp = Blueprint("orden_compra", __name__)

# Listar todas las órdenes de compra
@orden_compra_bp.route("/listarordenes", methods=["GET"])
def listar_ordenes():
    ordenes = OrdenCompra.query.all()
    resultado = []
    for o in ordenes:
        resultado.append({
            "id_orden": o.id_orden,
            "fecha": o.fecha,
            "id_material": o.id_material,
            "cantidad": o.cantidad,
            "es_material_nuevo": o.es_material_nuevo,
            "id_estado": o.id_estado,
            "usuario_solicitante": o.usuario_solicitante
        })
    return jsonify(resultado), 200


# Cambiar el estado de una orden de compra a ENTREGADO y actualizar bodega
@orden_compra_bp.route("/entregarorden/<int:id_orden>", methods=["PUT"])
def entregar_orden(id_orden):
    orden = OrdenCompra.query.get_or_404(id_orden)
    data = request.get_json()
    nueva_cantidad = data.get("cantidad")

    # Permitir modificar la cantidad antes de entregar
    if nueva_cantidad is not None:
        orden.cantidad = nueva_cantidad

    # Estado entregado (ajusta el valor según tu catálogo)
    ESTADO_ENTREGADO = 2
    orden.id_estado = ESTADO_ENTREGADO

    # Sumar la cantidad a la bodega
    if orden.id_material is not None:
        bodega = Bodega.query.filter_by(id_material=orden.id_material).first()
        if not bodega:
            bodega = Bodega(id_material=orden.id_material, cantidad=0)
            db.session.add(bodega)
        bodega.cantidad += orden.cantidad

    db.session.commit()
    return jsonify({"mensaje": "Orden de compra entregada y bodega actualizada"}), 200

# Cambiar el estado de una orden de compra a RECHAZADO
@orden_compra_bp.route("/rechazarorden/<int:id_orden>", methods=["PUT"])
def rechazar_orden(id_orden):
    orden = OrdenCompra.query.get_or_404(id_orden)
    # Estado rechazado (ajusta el valor según tu catálogo)
    ESTADO_RECHAZADO = 3
    orden.id_estado = ESTADO_RECHAZADO
    db.session.commit()
    return jsonify({"mensaje": "Orden de compra rechazada"}), 200

# Crear una orden de compra para un material seleccionado (botón "compra")
@orden_compra_bp.route("/crearorden", methods=["POST"])
def crear_orden_compra():
    data = request.get_json()
    id_material = data.get("id_material")
    cantidad = data.get("cantidad")
    usuario_solicitante = data.get("usuario_solicitante")  # id del usuario que solicita la compra

    if not id_material or not cantidad or not usuario_solicitante:
        return jsonify({"error": "id_material, cantidad y usuario_solicitante son obligatorios"}), 400

    orden = OrdenCompra(
        fecha=datetime.utcnow(),
        id_material=id_material,
        cantidad=cantidad,
        es_material_nuevo=False,
        id_estado=1,  # Estado inicial, por ejemplo "Pendiente"
        usuario_solicitante=usuario_solicitante
    )
    db.session.add(orden)
    db.session.commit()
    return jsonify({"mensaje": "Orden de compra creada", "id_orden": orden.id_orden}), 201
