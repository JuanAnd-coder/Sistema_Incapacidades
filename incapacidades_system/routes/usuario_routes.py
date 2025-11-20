from flask import Blueprint
from controllers.usuario_controller import UsuarioController

usuario_routes = Blueprint("usuario_routes", __name__)

# Listar todos
usuario_routes.route("/usuarios", methods=["GET"])(UsuarioController.listar_usuarios)

# Obtener uno por ID
usuario_routes.route("/usuarios/<int:usuario_id>", methods=["GET"])(UsuarioController.obtener_usuario)

# Crear
usuario_routes.route("/usuarios", methods=["POST"])(UsuarioController.crear_usuario)

# Actualizar
usuario_routes.route("/usuarios/<int:usuario_id>", methods=["PUT"])(UsuarioController.actualizar_usuario)

# Eliminar
usuario_routes.route("/usuarios/<int:usuario_id>", methods=["DELETE"])(UsuarioController.eliminar_usuario)
