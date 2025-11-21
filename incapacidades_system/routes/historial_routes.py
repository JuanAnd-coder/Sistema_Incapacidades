from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for
from controllers.historial_controller import HistorialController
from models.incapacidad_model import Incapacidad
from utils.decorators import rol_required
from config.db import db

historial_bp = Blueprint("historial", __name__, url_prefix="/historial")


# -------------------------
#   Ver historial de incapacidades del empleado
# -------------------------
@historial_bp.route("/")
@rol_required("Empleado", "Administrador")
def ver_historial():
    """
    Muestra el historial de incapacidades del empleado autenticado.
    Para empleados: solo sus propias incapacidades
    Para administradores: todas las incapacidades
    """
    rol = session.get("rol")
    
    if rol == "Administrador":
        # Administradores ven todas las incapacidades
        incapacidades = Incapacidad.query.order_by(Incapacidad.fecha_registro.desc()).all()
    else:
        # Empleados ven solo sus incapacidades (por documento)
        # Nota: En producción, deberías relacionar incapacidades con usuarios
        # Por ahora, mostramos todas pero podrías filtrar por documento si tienes esa relación
        incapacidades = Incapacidad.query.order_by(Incapacidad.fecha_registro.desc()).all()
    
    # Intentar obtener historial detallado si existe
    try:
        user_id = session.get("user_id")
        historial_detallado = HistorialController.obtener_por_usuario(user_id)
    except:
        historial_detallado = []
    
    return render_template("historial.html", incapacidades=incapacidades, historial_detallado=historial_detallado)


# -------------------------
#   API: Obtener historial del usuario autenticado (JSON)
# -------------------------
@historial_bp.route("/api")
@rol_required("Empleado", "Administrador")
def obtener_historial_api():
    """API endpoint para obtener historial en formato JSON"""
    user_id = session.get("user_id")
    historial = HistorialController.obtener_por_usuario(user_id)
    return jsonify(historial), 200


# -------------------------
#   API: Registrar un movimiento
# -------------------------
@historial_bp.route("/api", methods=["POST"])
@rol_required("Empleado", "Administrador")
def registrar_historial_api():
    """API endpoint para registrar un movimiento en el historial"""
    data = request.json

    campos = ["id_incapacidad", "descripcion"]
    if not all(c in data for c in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    user_id = session.get("user_id")

    movimiento_id = HistorialController.registrar(
        user_id,
        data["id_incapacidad"],
        data["descripcion"]
    )

    return jsonify({"mensaje": "Movimiento registrado", "id": movimiento_id}), 201
