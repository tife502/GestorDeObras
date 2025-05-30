from app.models.inventario import Inventario
from app.models.bodega import Bodega
from app.models.solicitud import SolicitudMaterial
from app.models.orden_compra import OrdenCompra
from app.models.material import Material
from app import db
from flask import Blueprint, request, jsonify
from datetime import datetime

solicitudes_bp = Blueprint("solicitudes", __name__)

# Crear solicitud (material existente o nuevo)
@solicitudes_bp.route("/crearsolicitud", methods=["POST"])
def crear_solicitud():
    data = request.get_json()
    cantidad = data.get("cantidad")
    id_usuario = data.get("id_usuario")
    id_zona = data.get("id_zona")
    id_estado = data.get("id_estado")
    es_nuevo = data.get("es_nuevo", False)

    if es_nuevo:
        # Solicitud de nuevo material
        nombre_material = data.get("nombre_material")
        id_unidad = data.get("id_unidad")
        if not nombre_material or not id_unidad:
            return jsonify({"error": "Faltan datos para nuevo material"}), 400
        # Crear el material primero
        nuevo_material = Material(nombre=nombre_material, id_unidad=id_unidad)
        db.session.add(nuevo_material)
        db.session.commit()

        # Ahora puedes usar nuevo_material.id
        solicitud = SolicitudMaterial(
            cantidad=cantidad,
            es_nuevo=True,
            id_material=nuevo_material.id,
            nombre_material=nombre_material,
            id_unidad=id_unidad,
            fecha_solicitud=datetime.utcnow(),
            id_estado=id_estado,
            id_usuario=id_usuario,
            id_zona=id_zona
        )
        db.session.add(solicitud)
        db.session.commit()

        orden = OrdenCompra(
            fecha=datetime.utcnow(),
            id_material=nuevo_material.id,
            cantidad=cantidad,
            es_material_nuevo=True,
            id_estado=1,  # Estado inicial, por ejemplo "Pendiente"
            usuario_solicitante=id_usuario
        )
        db.session.add(orden)
        db.session.commit()
        return jsonify({"mensaje": "Solicitud y orden de compra creadas para nuevo material", "id": solicitud.id_solicitud}), 201

    else:
        # Solicitud de material existente
        id_material = data.get("id_material")
        if not id_material:
            return jsonify({"error": "Debe seleccionar un material existente"}), 400

        # Verificar cantidad en bodega
        bodega = Bodega.query.filter_by(id_material=id_material).first()
        cantidad_bodega = bodega.cantidad if bodega else 0

        solicitud = SolicitudMaterial(
            cantidad=cantidad,
            es_nuevo=False,
            id_material=id_material,
            id_unidad=None,
            fecha_solicitud=datetime.utcnow(),
            id_estado=id_estado,
            id_usuario=id_usuario,
            id_zona=id_zona
        )
        db.session.add(solicitud)
        db.session.commit()

        if cantidad_bodega < cantidad:
            # Crear orden de compra si no hay suficiente en bodega
            orden = OrdenCompra(
                fecha=datetime.utcnow(),
                id_material=id_material,
                cantidad=cantidad - cantidad_bodega,
                es_material_nuevo=False,
                id_estado=1,  # Estado inicial, por ejemplo "Pendiente"
                usuario_solicitante=id_usuario
            )
            db.session.add(orden)
            db.session.commit()
            return jsonify({"mensaje": "Solicitud creada y orden de compra generada por falta de stock", "id": solicitud.id_solicitud}), 201

        return jsonify({"mensaje": "Solicitud creada", "id": solicitud.id_solicitud}), 201

# Listar todas las solicitudes
@solicitudes_bp.route("/mostrarsolicitudes", methods=["GET"])
def listar_solicitudes():
    solicitudes = SolicitudMaterial.query.all()
    resultado = []
    for s in solicitudes:
        resultado.append({
            "id_solicitud": s.id_solicitud,
            "cantidad": s.cantidad,
            "es_nuevo": s.es_nuevo,
            "id_material": s.id_material,
            "nombre_material": s.nombre_material,
            "id_unidad": s.id_unidad,
            "fecha_solicitud": s.fecha_solicitud,
            "id_estado": s.id_estado,
            "id_usuario": s.id_usuario,
            "id_zona": s.id_zona
        })
    return jsonify(resultado), 200

# Obtener una solicitud por ID
@solicitudes_bp.route("/obtenersolicitud/<int:id_solicitud>", methods=["GET"])
def obtener_solicitud(id_solicitud):
    s = SolicitudMaterial.query.get_or_404(id_solicitud)
    return jsonify({
        "id_solicitud": s.id_solicitud,
        "cantidad": s.cantidad,
        "es_nuevo": s.es_nuevo,
        "id_material": s.id_material,
        "nombre_material": s.nombre_material,
        "id_unidad": s.id_unidad,
        "fecha_solicitud": s.fecha_solicitud,
        "id_estado": s.id_estado,
        "id_usuario": s.id_usuario,
        "id_zona": s.id_zona
    }), 200


# Eliminar una solicitud
@solicitudes_bp.route("/eliminarsolicitud/<int:id_solicitud>", methods=["DELETE"])
def eliminar_solicitud(id_solicitud):
    s = SolicitudMaterial.query.get_or_404(id_solicitud)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"mensaje": "Solicitud eliminada"}), 200

# Asignar solicitud (estado 2)
@solicitudes_bp.route("/asignarsolicitud/<int:id_solicitud>", methods=["PUT"])
def asignar_solicitud(id_solicitud):
    solicitud = SolicitudMaterial.query.get_or_404(id_solicitud)
    if solicitud.id_estado == 2:
        return jsonify({"error": "La solicitud ya está asignada"}), 400

    bodega = Bodega.query.filter_by(id_material=solicitud.id_material).first()
    if not bodega or bodega.cantidad < solicitud.cantidad:
        return jsonify({"error": "No hay suficiente cantidad del material en bodega para asignar la solicitud"}), 400

    # Asignar al inventario de la zona
    inventario = Inventario.query.filter_by(id_material=solicitud.id_material, id_zona=solicitud.id_zona).first()
    if not inventario:
        inventario = Inventario(id_material=solicitud.id_material, id_zona=solicitud.id_zona, cantidad=0)
        db.session.add(inventario)
    inventario.cantidad += solicitud.cantidad
    bodega.cantidad -= solicitud.cantidad
    solicitud.id_estado = 2  # Asignado
    db.session.commit()
    return jsonify({"mensaje": "Material asignado y solicitud actualizada"}), 200

# Rechazar solicitud (estado 3)
@solicitudes_bp.route("/rechazarsolicitud/<int:id_solicitud>", methods=["PUT"])
def rechazar_solicitud(id_solicitud):
    solicitud = SolicitudMaterial.query.get_or_404(id_solicitud)
    if solicitud.id_estado == 3:
        return jsonify({"error": "La solicitud ya está rechazada"}), 400
    solicitud.id_estado = 3  # Rechazado
    db.session.commit()
    return jsonify({"mensaje": "Solicitud rechazada"}), 200


