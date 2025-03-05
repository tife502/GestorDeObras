from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/helo', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API"}), 200
