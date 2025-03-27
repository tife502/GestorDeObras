from flask import Blueprint, request, jsonify
from app import db
from app.models.rol import Rol

roles_bp = Blueprint("roles", __name__)