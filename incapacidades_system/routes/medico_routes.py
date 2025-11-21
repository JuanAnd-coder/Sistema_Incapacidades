from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from controllers.medico_controller import MedicoController
from utils.decorators import rol_required
from models.medico_model import Medico

medico_routes = Blueprint("medico", __name__, url_prefix="/medicos")

# Dashboard de médico
@medico_routes.route("/dashboard")
@rol_required("Médico")
def dashboard():
    return render_template("medico_dashboard.html")

# Listar médicos (Web y API)
@medico_routes.route("/", methods=["GET"])
@rol_required("Administrador")
def listar():
    # Verificar si es una petición explícita de JSON (API)
    wants_json = (
        request.is_json or 
        request.args.get('format') == 'json' or
        (request.accept_mimetypes.accept_json and 
         not request.accept_mimetypes.accept_html)
    )
    
    medicos = Medico.obtener_todos()
    
    if wants_json:
        data = []
        for m in medicos:
            data.append({
                "id_medico": m.id_medico,
                "nombre": m.nombre,
                "especialidad": m.especialidad,
                "licencia": m.licencia
            })
        return jsonify(data), 200
    
    # Por defecto, devolver HTML (Web)
    return render_template("medicos/lista.html", medicos=medicos)

# Obtener médico por ID (API)
@medico_routes.route("/<int:id_medico>", methods=["GET"])
@rol_required("Administrador")
def obtener(id_medico):
    return MedicoController.obtener_medico(id_medico)

# Crear médico (Web y API)
@medico_routes.route("/crear", methods=["GET", "POST"])
@rol_required("Administrador")
def crear():
    if request.method == "POST":
        # Si es JSON (API)
        if request.is_json:
            return MedicoController.crear_medico()
        
        # Si es formulario HTML (Web)
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        licencia = request.form.get("licencia", "").strip()
        
        if not nombre or not especialidad or not licencia:
            flash("Todos los campos son obligatorios", "error")
            return render_template("medicos/crear.html")
        
        # Verificar si la licencia ya existe
        medico_existente = Medico.query.filter_by(licencia=licencia).first()
        if medico_existente:
            flash("La licencia ya está registrada", "error")
            return render_template("medicos/crear.html")
        
        try:
            data = {
                "nombre": nombre,
                "especialidad": especialidad,
                "licencia": licencia
            }
            data = {
                "nombre": nombre,
                "especialidad": especialidad,
                "licencia": licencia
            }
            nuevo_medico = Medico(
                nombre=nombre,
                especialidad=especialidad,
                licencia=licencia
            )
            from config.db import db
            db.session.add(nuevo_medico)
            db.session.commit()
            flash(f"Médico creado exitosamente (ID: {nuevo_medico.id_medico})", "success")
            return redirect(url_for("medico.listar"))
        except Exception as e:
            flash(f"Error al crear médico: {str(e)}", "error")
            return render_template("medicos/crear.html")
    
    # GET: Mostrar formulario
    return render_template("medicos/crear.html")

# Ruta alternativa para crear (API POST)
@medico_routes.route("/", methods=["POST"])
@rol_required("Administrador")
def crear_api():
    return MedicoController.crear_medico()

# Editar médico (Web y API)
@medico_routes.route("/editar/<int:id_medico>", methods=["GET", "POST"])
@rol_required("Administrador")
def editar(id_medico):
    medico_obj = Medico.obtener_por_id(id_medico)
    if not medico_obj:
        flash("Médico no encontrado", "error")
        return redirect(url_for("medico.listar"))
    
    if request.method == "POST":
        # Si es JSON (API)
        if request.is_json:
            return MedicoController.actualizar_medico(id_medico)
        
        # Si es formulario HTML (Web)
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        licencia = request.form.get("licencia", "").strip()
        
        if not nombre or not especialidad or not licencia:
            flash("Todos los campos son obligatorios", "error")
            return render_template("medicos/editar.html", medico=medico_obj)
        
        # Verificar si la licencia ya existe en otro médico
        medico_existente = Medico.query.filter_by(licencia=licencia).first()
        if medico_existente and medico_existente.id_medico != id_medico:
            flash("La licencia ya está registrada en otro médico", "error")
            return render_template("medicos/editar.html", medico=medico_obj)
        
        try:
            data = {
                "nombre": nombre,
                "especialidad": especialidad,
                "licencia": licencia
            }
            actualizado = Medico.actualizar(id_medico, data)
            if actualizado:
                flash("Médico actualizado exitosamente", "success")
                return redirect(url_for("medico.listar"))
            else:
                flash("Error al actualizar médico", "error")
        except Exception as e:
            flash(f"Error al actualizar médico: {str(e)}", "error")
    
    # GET: Mostrar formulario de edición
    return render_template("medicos/editar.html", medico=medico_obj)

# Ruta alternativa para actualizar (API PUT)
@medico_routes.route("/<int:id_medico>", methods=["PUT"])
@rol_required("Administrador")
def actualizar_api(id_medico):
    return MedicoController.actualizar_medico(id_medico)

# Eliminar médico (Web y API)
@medico_routes.route("/eliminar/<int:id_medico>", methods=["GET", "POST"])
@rol_required("Administrador")
def eliminar(id_medico):
    # Si es JSON (API)
    if request.is_json or request.accept_mimetypes.accept_json:
        return MedicoController.eliminar_medico(id_medico)
    
    # Si es HTML (Web)
    try:
        eliminado = Medico.eliminar(id_medico)
        if eliminado:
            flash("Médico eliminado exitosamente", "success")
        else:
            flash("Médico no encontrado", "error")
    except Exception as e:
        flash(f"Error al eliminar médico: {str(e)}", "error")
    
    return redirect(url_for("medico.listar"))

# Ruta alternativa para eliminar (API DELETE)
@medico_routes.route("/<int:id_medico>", methods=["DELETE"])
@rol_required("Administrador")
def eliminar_api(id_medico):
    return MedicoController.eliminar_medico(id_medico)

