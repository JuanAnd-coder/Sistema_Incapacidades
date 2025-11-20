# -----------------------------------------------------------
#   Sistema de Gestión de Incapacidades - Release 1.2
#   Tecnologías: Python, Flask, SQLAlchemy, MySQL
#   Funcionalidad:
#     ✔ Registrar incapacidad
#     ✔ Subir documentos
#     ✔ Validación automática
#     ✔ Listar incapacidades
#     ✔ Gestión de empleados
#     ✔ Gestión de médicos
#     ✔ Gestión de usuarios
#     ✔ Autenticación
# -----------------------------------------------------------

from flask import Flask, redirect, url_for # <-- AGREGADO: redirect y url_for
from flask_cors import CORS
from config.config import Config
from config.db import db

# Importar Blueprints de cada módulo
from routes.usuario_routes import usuario_routes
from routes.empleado_routes import empleado_bp # Ajusté la ruta de importación de empleado_routes
from routes.medico_routes import medico_routes
from routes.incapacidad_routes import init_incapacidad_routes
from routes.auth_routes import auth_bp # Ajusté la ruta de importación de auth_controller
from routes.admin_routes import admin_bp
from routes.revisor_routes import revisor_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Activar CORS (permite peticiones desde frontend)
    CORS(app)

    # Inicializar base de datos
    db.init_app(app)

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    # Registrar blueprints (con sus prefijos ya definidos)
    app.register_blueprint(usuario_routes)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(medico_routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(revisor_bp)



    init_incapacidad_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)