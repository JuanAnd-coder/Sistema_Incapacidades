from flask import Blueprint
from controllers.medico_controller import MedicoController

medico_routes = Blueprint("medico_routes", __name__)

# Listar todos
medico_routes.route("/medicos", methods=["GET"])(MedicoController.listar_medicos)

# Obtener uno por ID
medico_routes.route("/medicos/<int:id_medico>", methods=["GET"])(MedicoController.obtener_medico)

# Crear
medico_routes.route("/medicos", methods=["POST"])(MedicoController.crear_medico)

# Actualizar
medico_routes.route("/medicos/<int:id_medico>", methods=["PUT"])(MedicoController.actualizar_medico)

# Eliminar
medico_routes.route("/medicos/<int:id_medico>", methods=["DELETE"])(MedicoController.eliminar_medico)

