from flask import render_template, request, redirect, url_for, flash, send_from_directory, session
from services.incapacidad_service import IncapacidadService
from models.incapacidad_model import Incapacidad
from utils.constantes import DOCUMENTOS_REQUERIDOS
from config.config import Config
import datetime
import os

class IncapacidadController:

    @staticmethod
    def index():
        # Verificar autenticación
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        incapacidades = Incapacidad.query.all()
        return render_template("index.html", incapacidades=incapacidades)

    @staticmethod
    def nuevo():
        # Verificar autenticación
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        # Solo Empleados y Administradores pueden registrar incapacidades
        rol = session.get("rol")
        if rol not in ["Empleado", "Administrador"]:
            flash("Solo los empleados pueden registrar sus incapacidades. Los revisores y médicos solo pueden revisar y validar.", "error")
            return redirect(url_for("incapacidades_list"))
        
        if request.method == "POST":
            data = {
                "empleado": request.form["empleado"],
                "documento": request.form["documento"],
                "entidad": request.form["entidad"],
                "tipo": request.form["tipo"],
                "fecha": datetime.datetime.strptime(request.form["fecha"], "%Y-%m-%d").date(),
                "dias": int(request.form["dias"])
            }

            archivos = request.files.getlist("archivos")
            
            try:
                IncapacidadService.crear_incapacidad(data, archivos)
                flash("Incapacidad registrada exitosamente", "success")
                return redirect(url_for("incapacidades_list"))
            except ValueError as e:
                flash(str(e), "error")
                return render_template("nuevo.html")
            except Exception as e:
                flash(f"Error al registrar incapacidad: {str(e)}", "error")
                return render_template("nuevo.html")

        return render_template("nuevo.html")


    @staticmethod
    def ver(id):
        # Verificar autenticación
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        inc = Incapacidad.query.get_or_404(id)
        req = DOCUMENTOS_REQUERIDOS[inc.tipo]
        docs_presentes = [a.tipo_documento for a in inc.archivos]

        faltantes = [d for d in req if d not in docs_presentes]

        return render_template("ver.html", inc=inc, faltantes=faltantes)


    @staticmethod
    def descargar(nombre):
        return send_from_directory(Config.UPLOAD_FOLDER, nombre, as_attachment=True)


    @staticmethod
    def editar(id):
        # Verificar autenticación
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        inc = Incapacidad.query.get_or_404(id)
        rol = session.get("rol")
        
        # Solo Empleados (para sus propias incapacidades) y Administradores pueden editar
        # Los empleados solo pueden editar si el documento coincide con su sesión
        # Por ahora permitimos a Empleados y Administradores editar cualquier incapacidad
        # (En producción, podrías verificar que el empleado coincida con session)
        if rol not in ["Empleado", "Administrador"]:
            flash("Solo los empleados y administradores pueden agregar documentos a incapacidades", "error")
            return redirect(url_for("incapacidades_list"))
        
        if request.method == "POST":
            archivos = request.files.getlist("archivos")
            
            if not archivos or not any(f.filename for f in archivos):
                flash("Debes seleccionar al menos un archivo para agregar", "error")
                req = DOCUMENTOS_REQUERIDOS.get(inc.tipo, [])
                docs_presentes = [a.tipo_documento for a in inc.archivos]
                faltantes = [d for d in req if d not in docs_presentes]
                return render_template("editar_incapacidad.html", inc=inc, faltantes=faltantes, docs_presentes=docs_presentes)
            
            try:
                resultado = IncapacidadService.agregar_documentos(id, archivos)
                
                if isinstance(resultado, dict):
                    documentos_agregados = resultado.get("documentos_agregados", [])
                    advertencia = resultado.get("advertencia")
                    
                    if documentos_agregados:
                        flash(f"Se agregaron {len(documentos_agregados)} documento(s) exitosamente", "success")
                        if advertencia:
                            flash(advertencia, "error")
                    else:
                        flash("No se pudieron agregar los documentos. Verifica que sean PDF, JPG, JPEG o PNG", "error")
                else:
                    # Compatibilidad con versión anterior
                    if resultado:
                        flash(f"Se agregaron {len(resultado)} documento(s) exitosamente", "success")
                    else:
                        flash("No se pudieron agregar los documentos. Verifica que sean PDF, JPG, JPEG o PNG", "error")
            except Exception as e:
                flash(f"Error al agregar documentos: {str(e)}", "error")
            
            return redirect(url_for("ver_incapacidad", id=id))
        
        # GET: Mostrar formulario de edición
        req = DOCUMENTOS_REQUERIDOS.get(inc.tipo, [])
        docs_presentes = [a.tipo_documento for a in inc.archivos]
        faltantes = [d for d in req if d not in docs_presentes]
        
        return render_template("editar_incapacidad.html", inc=inc, faltantes=faltantes, docs_presentes=docs_presentes)

    @staticmethod
    def transcribir(id):
        # Verificar autenticación y rol (solo Revisor puede transcribir)
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        if session.get("rol") not in ["Revisor", "Administrador"]:
            flash("Solo los revisores pueden cambiar el estado de las incapacidades", "error")
            return redirect(url_for("incapacidades_list"))
        
        IncapacidadService.cambiar_estado(id, "Transcrita")
        flash("Estado cambiado a Transcrita")
        return redirect(url_for("ver_incapacidad", id=id))
