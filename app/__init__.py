from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.services.email_service import mail
    mail.init_app(app)
    
    # Registrar rutas
    from app.routes.main import main_bp  # Importa la nueva ruta principal
    app.register_blueprint(main_bp)  # Ruta principal
    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    from app.routes.zonas import zonas_bp
    app.register_blueprint(zonas_bp, url_prefix="/api/zonas")
    from app.routes.materiales import materiales_bp
    app.register_blueprint(materiales_bp, url_prefix="/api/materiales")
    from app.routes.roles import roles_bp
    app.register_blueprint(roles_bp, url_prefix="/api/roles")


    return app