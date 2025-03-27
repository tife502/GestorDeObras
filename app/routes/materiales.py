from flask import Blueprint, request, jsonify, url_for
from app import db, bcrypt
from app.models.material import Material

materiales_bp = Blueprint("materiales", __name__)

