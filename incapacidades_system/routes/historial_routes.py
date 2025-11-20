from flask import Blueprint, jsonify, request, session
from controllers.historial_controller import HistorialController
from utils.decorators import rol_required

historial_bp = Blueprint("historial", __name__, url_prefix="/historial")


# -------------------------
#   Obtener historial del usuario autenticado
# -------------------------
@historial_bp.get("/")
@rol_required(["Usuario"])
def obtener_historial_usuario():
    usuario_id = session.get("usuario_id")
    historial = HistorialController.obtener_por_usuario(usuario_id)
    return jsonify(historial), 200


# -------------------------
#   Registrar un movimiento
# -------------------------
@historial_bp.post("/")
@rol_required(["Usuario"])
def registrar_historial():
    data = request.json

    campos = ["id_incapacidad", "descripcion"]
    if not all(c in data for c in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    usuario_id = session.get("usuario_id")

    movimiento_id = HistorialController.registrar(
        usuario_id,
        data["id_incapacidad"],
        data["descripcion"]
    )

    return jsonify({"mensaje": "Movimiento registrado", "id": movimiento_id}), 201
