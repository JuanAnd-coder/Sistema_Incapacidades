from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
# Importamos el decorador CORRECTO que usa functools.wraps
from utils.decorators import rol_required
# Asumo que EmpleadoController está en controllers/empleado_controller
from controllers.empleado_controller import EmpleadoController 
from models.empleado_model import Empleado
# Se eliminó la importación innecesaria/conflictiva de 'middleware.auth_required'


empleado_bp = Blueprint("empleado", __name__, url_prefix="/empleados")


# ------------------------------
#       DASHBOARD DE EMPLEADO (Acceso Empleado)
# ------------------------------
@empleado_bp.route("/dashboard") # Cambié el endpoint de "/login.html" a "/dashboard" para claridad
@rol_required("Empleado", "Administrador") # Puede ser accesible si está logueado, pero se muestra la vista de empleado
def dashboard():
    return render_template("empleado_dashboard.html")


# ------------------------------
#       LISTAR EMPLEADOS (Acceso RRHH y Admin)
# ------------------------------
@empleado_bp.get("/")
@rol_required("Administrador") # Solo Administrador puede ver todos los empleados
def listar_empleados():
    # Verificar si es una petición explícita de JSON (API)
    wants_json = (
        request.is_json or 
        request.args.get('format') == 'json' or
        (request.accept_mimetypes.accept_json and 
         not request.accept_mimetypes.accept_html)
    )
    
    empleados = EmpleadoController.listar()
    
    if wants_json:
        return jsonify(empleados), 200
    
    # Por defecto, devolver HTML (Web)
    return render_template("empleados/lista.html", empleados=empleados)


# ------------------------------
#       OBTENER EMPLEADO POR ID (Acceso RRHH y Admin - El Empleado podría tener su propia ruta /me)
# ------------------------------
@empleado_bp.get("/<int:id_empleado>")
@rol_required("Administrador")
def obtener_empleado(id_empleado):
    empleado = EmpleadoController.obtener(id_empleado)
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404
    return jsonify(empleado), 200


# ------------------------------
#       CREAR EMPLEADO (Web y API)
# ------------------------------
@empleado_bp.route("/crear", methods=["GET", "POST"])
@rol_required("Administrador")
def crear():
    if request.method == "POST":
        # Si es JSON (API)
        if request.is_json:
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
        
        # Si es formulario HTML (Web)
        nombre = request.form.get("nombre", "").strip()
        cargo = request.form.get("cargo", "").strip()
        area = request.form.get("area", "").strip()
        cedula = request.form.get("cedula", "").strip()
        
        if not nombre or not cargo or not area or not cedula:
            flash("Todos los campos son obligatorios", "error")
            return render_template("empleados/crear.html")
        
        # Verificar si la cédula ya existe
        empleado_existente = Empleado.query.filter_by(cedula=cedula).first()
        if empleado_existente:
            flash("La cédula ya está registrada", "error")
            return render_template("empleados/crear.html")
        
        try:
            data = {
                "nombre": nombre,
                "cargo": cargo,
                "area": area,
                "cedula": cedula
            }
            nuevo_id = EmpleadoController.crear(data)
            flash(f"Empleado creado exitosamente (ID: {nuevo_id})", "success")
            return redirect(url_for("empleado.listar_empleados"))
        except Exception as e:
            flash(f"Error al crear empleado: {str(e)}", "error")
            return render_template("empleados/crear.html")
    
    # GET: Mostrar formulario
    return render_template("empleados/crear.html")

# Ruta alternativa para crear (API POST)
@empleado_bp.post("/")
@rol_required("Administrador")
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
#       ACTUALIZAR EMPLEADO (Web y API)
# ------------------------------
@empleado_bp.route("/editar/<int:id_empleado>", methods=["GET", "POST"])
@rol_required("Administrador")
def editar(id_empleado):
    empleado_obj = Empleado.obtener_por_id(id_empleado)
    if not empleado_obj:
        flash("Empleado no encontrado", "error")
        return redirect(url_for("empleado.listar_empleados"))
    
    if request.method == "POST":
        # Si es JSON (API)
        if request.is_json:
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
        
        # Si es formulario HTML (Web)
        nombre = request.form.get("nombre", "").strip()
        cargo = request.form.get("cargo", "").strip()
        area = request.form.get("area", "").strip()
        cedula = request.form.get("cedula", "").strip()
        
        if not nombre or not cargo or not area or not cedula:
            flash("Todos los campos son obligatorios", "error")
            empleado = EmpleadoController.obtener(id_empleado)
            return render_template("empleados/editar.html", empleado=empleado)
        
        # Verificar si la cédula ya existe en otro empleado
        empleado_existente = Empleado.query.filter_by(cedula=cedula).first()
        if empleado_existente and empleado_existente.id_empleado != id_empleado:
            flash("La cédula ya está registrada en otro empleado", "error")
            empleado = EmpleadoController.obtener(id_empleado)
            return render_template("empleados/editar.html", empleado=empleado)
        
        try:
            data = {
                "nombre": nombre,
                "cargo": cargo,
                "area": area,
                "cedula": cedula
            }
            actualizado = EmpleadoController.actualizar(id_empleado, data)
            if actualizado:
                flash("Empleado actualizado exitosamente", "success")
                return redirect(url_for("empleado.listar_empleados"))
            else:
                flash("Error al actualizar empleado", "error")
        except Exception as e:
            flash(f"Error al actualizar empleado: {str(e)}", "error")
    
    # GET: Mostrar formulario de edición
    empleado = EmpleadoController.obtener(id_empleado)
    if not empleado:
        flash("Empleado no encontrado", "error")
        return redirect(url_for("empleado.listar_empleados"))
    return render_template("empleados/editar.html", empleado=empleado)

# Ruta alternativa para actualizar (API PUT)
@empleado_bp.put("/<int:id_empleado>")
@rol_required("Administrador")
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
#       ELIMINAR EMPLEADO (Web y API)
# ------------------------------
@empleado_bp.route("/eliminar/<int:id_empleado>", methods=["GET", "POST"])
@rol_required("Administrador")
def eliminar(id_empleado):
    # Si es JSON (API)
    if request.is_json or request.accept_mimetypes.accept_json:
        try:
            eliminado = EmpleadoController.eliminar(id_empleado)
            if not eliminado:
                return jsonify({"error": "Empleado no encontrado"}), 404
            return jsonify({"mensaje": "Empleado eliminado"}), 200
        except Exception as e:
            return jsonify({"error": f"Error al eliminar: {str(e)}"}), 500
    
    # Si es HTML (Web)
    try:
        eliminado = EmpleadoController.eliminar(id_empleado)
        if eliminado:
            flash("Empleado eliminado exitosamente", "success")
        else:
            flash("Empleado no encontrado", "error")
    except Exception as e:
        flash(f"Error al eliminar empleado: {str(e)}", "error")
    
    return redirect(url_for("empleado.listar_empleados"))

# Ruta alternativa para eliminar (API DELETE)
@empleado_bp.delete("/<int:id_empleado>")
@rol_required("Administrador")
def eliminar_empleado(id_empleado):
    try:
        eliminado = EmpleadoController.eliminar(id_empleado)
        if not eliminado:
            return jsonify({"error": "Empleado no encontrado"}), 404
        return jsonify({"mensaje": "Empleado eliminado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar: {str(e)}"}), 500