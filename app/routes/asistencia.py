from flask import Blueprint, request, jsonify
from sqlalchemy.sql import func
from app import db
from app.models.zona import ZonaTrabajo
from app.models.usuario import Usuario 
from app.models.asistencia import Asistencia  # Asegúrate de importar el modelo de Asistencia
from math import radians, sin, cos, sqrt, atan2

asistencia_bp = Blueprint("asistencia", __name__)

# Función para calcular la distancia entre dos coordenadas geográficas
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371000  # Radio de la Tierra en metros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distancia en metros

# 📌 Ruta para registrar el Check-in
@asistencia_bp.route("/checkin", methods=["POST"])
def registrar_checkin():
    data = request.json
    trabajador_id = data.get("trabajador_id")
    lat_actual = float(data.get("latitud"))
    lon_actual = float(data.get("longitud"))

    trabajador = Usuario.query.get(trabajador_id)
    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404

    zona_trabajo = ZonaTrabajo.query.get(trabajador.id_zona)
    if not zona_trabajo or not zona_trabajo.ubicacion:
        return jsonify({"error": "Zona de trabajo no encontrada"}), 404

    lat_zona, lon_zona = map(float, zona_trabajo.ubicacion.split(","))
    distancia = calcular_distancia(lat_actual, lon_actual, lat_zona, lon_zona)

    if distancia > 100:
        return jsonify({"error": f"Fuera de la zona de trabajo. Distancia: {int(distancia)}m"}), 403

    nueva_asistencia = Asistencia(
        trabajador_id=trabajador_id,
        check_in=func.now(),
        ubicacion=f"{lat_actual},{lon_actual}"
    )
    db.session.add(nueva_asistencia)
    db.session.commit()

    return jsonify({"mensaje": "Check-in exitoso", "distancia": int(distancia)}), 200

# 📌 Ruta para registrar el Check-out
@asistencia_bp.route("/checkout", methods=["POST"])
def registrar_checkout():
    data = request.json
    trabajador_id = data.get("trabajador_id")
    lat_actual = float(data.get("latitud"))
    lon_actual = float(data.get("longitud"))

    asistencia = Asistencia.query.filter_by(trabajador_id=trabajador_id, check_out=None).first()
    if not asistencia:
        return jsonify({"error": "No hay check-in activo"}), 404

    trabajador = Usuario.query.get(trabajador_id)
    zona_trabajo = ZonaTrabajo.query.get(trabajador.zona_id)

    if not zona_trabajo or not zona_trabajo.ubicacion:
        return jsonify({"error": "Zona de trabajo no encontrada"}), 404

    lat_zona, lon_zona = map(float, zona_trabajo.ubicacion.split(","))
    distancia = calcular_distancia(lat_actual, lon_actual, lat_zona, lon_zona)

    if distancia > 100:
        return jsonify({"error": f"Fuera de la zona de trabajo. Distancia: {int(distancia)}m"}), 403

    asistencia.check_out = func.now()
    db.session.commit()

    return jsonify({"mensaje": "Check-out exitoso", "distancia": int(distancia)}), 200

# 📌 Ruta para obtener todas las asistencias
@asistencia_bp.route("/todas", methods=["GET"])
def obtener_asistencias():
    asistencias = Asistencia.query.all()
    
    resultado = [
        {
            "id": asistencia.id,
            "trabajador_id": asistencia.trabajador_id,
            "check_in": asistencia.check_in.strftime("%Y-%m-%d %H:%M:%S") if asistencia.check_in else None,
            "check_out": asistencia.check_out.strftime("%Y-%m-%d %H:%M:%S") if asistencia.check_out else None,
            "ubicacion": asistencia.ubicacion
        }
        for asistencia in asistencias
    ]
    
    return jsonify(resultado), 200
