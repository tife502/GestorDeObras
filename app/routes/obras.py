from flask import Blueprint, request, jsonify
from app import db
from app.models.obra import Obra
from flask_jwt_extended import jwt_required
from app.utils.decorators import rol_requerido


obras_bp = Blueprint('obras', __name__)


@obras_bp.route('/mostrar', methods=['GET'])
@rol_requerido('administrador', 'arquitecto')
def mostrar_obras():
    obras = Obra.query.all()
    return jsonify([obra.to_dict() for obra in obras]), 200

@obras_bp.route('/crear', methods=['POST'])
@rol_requerido('administrador', 'arquitecto')
def crear_obra():
    data = request.get_json()
    obra = Obra(**data)
    db.session.add(obra)
    db.session.commit()
    return jsonify(obra.to_dict()), 201

@obras_bp.route('/editar/<int:id>', methods=['PUT'])
@rol_requerido('administrador', 'arquitecto')
def editar_obra(id):
    data = request.get_json()
    obra = Obra.query.get_or_404(id)
    obra.update(data)
    db.session.commit()
    return jsonify(obra.to_dict()), 200
