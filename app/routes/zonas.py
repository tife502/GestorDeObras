from flask import Blueprint, request, jsonify
from app import db
from app.models.zona import ZonaTrabajo
from flask_jwt_extended import jwt_required


zonas_bp = Blueprint("zonas", __name__)