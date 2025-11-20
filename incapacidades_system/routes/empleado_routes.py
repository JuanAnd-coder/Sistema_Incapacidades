from flask import Blueprint, request, jsonify, render_template
# Importamos el decorador CORRECTO que usa functools.wraps
from utils.decorators import rol_required
# Asumo que EmpleadoController está en controllers/empleado_controller
from controllers.empleado_controller import EmpleadoController 
# Se eliminó la importación innecesaria/conflictiva de 'middleware.auth_required'


empleado_bp = Blueprint("empleado", __name__, url_prefix="/empleados")


# ------------------------------
#       DASHBOARD DE EMPLEADO (Acceso Empleado)
# ------------------------------
@empleado_bp.route("/dashboard") # Cambié el endpoint de "/login.html" a "/dashboard" para claridad
@rol_required(["Empleado", "RRHH", "Admin"]) # Puede ser accesible si está logueado, pero se muestra la vista de empleado
def dashboard():
    return render_template("empleado_dashboard.html")


# ------------------------------
#       LISTAR EMPLEADOS (Acceso RRHH y Admin)
# ------------------------------
@empleado_bp.get("/")
@rol_required(["Admin", "RRHH"]) # Solo Admin y RRHH pueden ver todos los empleados
def listar_empleados():
    empleados = EmpleadoController.listar()
    return jsonify(empleados), 200


# ------------------------------
#       OBTENER EMPLEADO POR ID (Acceso RRHH y Admin - El Empleado podría tener su propia ruta /me)
# ------------------------------
@empleado_bp.get("/<int:id_empleado>")
@rol_required(["Admin", "RRHH"])
def obtener_empleado(id_empleado):
    empleado = EmpleadoController.obtener(id_empleado)
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404
    return jsonify(empleado), 200


# ------------------------------
#       CREAR EMPLEADO (Acceso RRHH y Admin)
# ------------------------------
@empleado_bp.post("/")
@rol_required(["Admin", "RRHH"])
def crear_empleado():
    data = request.json

    if not data:
        return jsonify({"error": "JSON vacío o inválido"}), 400

    campos_obligatorios = ["nombre", "cargo", "area", "cedula"]
    faltantes = [c for c in campos_obligatorios if c not in data or not data[c]]

    if faltantes:
        return jsonify({"error": f"Faltan datos obligatorios: {faltantes}"}), 400

    try:
        nuevo_id = EmpleadoController.crear(data)
        return jsonify({"mensaje": "Empleado creado", "id": nuevo_id}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear empleado: {str(e)}"}), 500


# ------------------------------
#       ACTUALIZAR EMPLEADO (Acceso RRHH y Admin)
# ------------------------------
@empleado_bp.put("/<int:id_empleado>")
@rol_required(["Admin", "RRHH"])
def actualizar_empleado(id_empleado):
    data = request.json

    if not data:
        return jsonify({"error": "JSON vacío o inválido"}), 400

    try:
        actualizado = EmpleadoController.actualizar(id_empleado, data)
        if not actualizado:
            return jsonify({"error": "Empleado no encontrado"}), 404

        return jsonify({"mensaje": "Empleado actualizado"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al actualizar: {str(e)}"}), 500


# ------------------------------
#       ELIMINAR EMPLEADO (Acceso Admin - Muy sensible)
# ------------------------------
@empleado_bp.delete("/<int:id_empleado>")
@rol_required(["Admin"]) # Sólo el administrador puede eliminar empleados
def eliminar_empleado(id_empleado):
    try:
        eliminado = EmpleadoController.eliminar(id_empleado)
        if not eliminado:
            return jsonify({"error": "Empleado no encontrado"}), 404

        return jsonify({"mensaje": "Empleado eliminado"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar: {str(e)}"}), 500