from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO  # Importamos SocketIO
from app.config import Config

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")  # Configuración de SocketIO

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Inicializamos el servicio de email
    from app.services.email_service import mail
    mail.init_app(app)
    
    # Registrar rutas (BluePrints)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)  # Ruta principal
    
    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    
    from app.routes.zonas import zonas_bp
    app.register_blueprint(zonas_bp, url_prefix="/api/zonas")
    
    from app.routes.materiales import materiales_bp
    app.register_blueprint(materiales_bp, url_prefix="/api/materiales")
    
    from app.routes.roles import roles_bp
    app.register_blueprint(roles_bp, url_prefix="/api/roles")
    
    from app.routes.solicitud import solicitudes_bp
    app.register_blueprint(solicitudes_bp, url_prefix="/api/solicitudes")
    
    from app.routes.asistencia import asistencia_bp
    app.register_blueprint(asistencia_bp, url_prefix="/api/asistencia")
    
    from app.routes.tareas import tareas_bp
    app.register_blueprint(tareas_bp, url_prefix="/api/tareas")
    
    from app.routes.mensajes import mensajes_bp
    app.register_blueprint(mensajes_bp, url_prefix="/api/mensajes")

    from app.routes.bodega import bodega_bp
    app.register_blueprint(bodega_bp, url_prefix="/api/bodega")

    from app.routes.inventario import inventario_bp
    app.register_blueprint(inventario_bp, url_prefix="/api/inventario")

    from app.routes.orden_compra import orden_compra_bp
    app.register_blueprint(orden_compra_bp, url_prefix="/api/orden_compra")

    from app.routes.unidadmedida import unidad_medida_bp
    app.register_blueprint(unidad_medida_bp, url_prefix="/api/unidades_medida")

    from app.routes.estados_compra import estados_compra_bp
    app.register_blueprint(estados_compra_bp, url_prefix="/api/estados_compra")

    from app.routes.estados_solicitud import estados_solicitud_bp
    app.register_blueprint(estados_solicitud_bp, url_prefix="/api/estados_solicitud")


    # Inicializar SocketIO
    socketio.init_app(app)

    return app
