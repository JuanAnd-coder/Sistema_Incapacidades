from flask import render_template, request, redirect, url_for, flash, send_from_directory
from services.incapacidad_service import IncapacidadService
from models.incapacidad_model import Incapacidad
from utils.constantes import DOCUMENTOS_REQUERIDOS
from config.config import Config
import datetime
import os

class IncapacidadController:

    @staticmethod
    def index():
        incapacidades = Incapacidad.query.all()
        return render_template("index.html", incapacidades=incapacidades)

    @staticmethod
    def nuevo():
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
            IncapacidadService.crear_incapacidad(data, archivos)

            flash("Incapacidad registrada exitosamente")
            return redirect(url_for("index"))

        return render_template("nuevo.html")


    @staticmethod
    def ver(id):
        inc = Incapacidad.query.get_or_404(id)
        req = DOCUMENTOS_REQUERIDOS[inc.tipo]
        docs_presentes = [a.tipo_documento for a in inc.archivos]

        faltantes = [d for d in req if d not in docs_presentes]

        return render_template("ver.html", inc=inc, faltantes=faltantes)


    @staticmethod
    def descargar(nombre):
        return send_from_directory(Config.UPLOAD_FOLDER, nombre, as_attachment=True)


    @staticmethod
    def transcribir(id):
        IncapacidadService.cambiar_estado(id, "Transcrita")
        flash("Estado cambiado a Transcrita")
        return redirect(url_for("ver", id=id))
