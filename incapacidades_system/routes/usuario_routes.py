from flask import Blueprint
from controllers.usuario_controller import UsuarioController
from utils.decorators import rol_required

usuario_routes = Blueprint("usuario", __name__, url_prefix="/usuarios")

# Listar todos (Web y API)
@usuario_routes.route("/", methods=["GET"])
@rol_required("Administrador")
def listar():
    return UsuarioController.listar_usuarios()

# Obtener uno por ID (API)
@usuario_routes.route("/<int:usuario_id>", methods=["GET"])
@rol_required("Administrador")
def obtener(usuario_id):
    return UsuarioController.obtener_usuario(usuario_id)

# Crear usuario (Web y API)
@usuario_routes.route("/crear", methods=["GET", "POST"])
@rol_required("Administrador")
def crear():
    return UsuarioController.crear_usuario()

# Ruta alternativa para crear (API POST)
@usuario_routes.route("/", methods=["POST"])
@rol_required("Administrador")
def crear_api():
    return UsuarioController.crear_usuario()

# Actualizar usuario (Web y API)
@usuario_routes.route("/editar/<int:usuario_id>", methods=["GET", "POST"])
@rol_required("Administrador")
def editar(usuario_id):
    return UsuarioController.actualizar_usuario(usuario_id)

# Ruta alternativa para actualizar (API PUT)
@usuario_routes.route("/<int:usuario_id>", methods=["PUT"])
@rol_required("Administrador")
def actualizar_api(usuario_id):
    return UsuarioController.actualizar_usuario(usuario_id)

# Eliminar usuario (Web y API)
@usuario_routes.route("/eliminar/<int:usuario_id>", methods=["GET", "POST"])
@rol_required("Administrador")
def eliminar(usuario_id):
    return UsuarioController.eliminar_usuario(usuario_id)

# Ruta alternativa para eliminar (API DELETE)
@usuario_routes.route("/<int:usuario_id>", methods=["DELETE"])
@rol_required("Administrador")
def eliminar_api(usuario_id):
    return UsuarioController.eliminar_usuario(usuario_id)
