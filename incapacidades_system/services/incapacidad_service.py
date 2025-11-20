import os
# Importamos 'date' para hacer la verificación de tipo correctamente
from datetime import datetime, date 
from werkzeug.utils import secure_filename
from config.config import Config
from config.db import db
from models.incapacidad_model import Incapacidad, Archivo
from utils.helpers import identificar_tipo_documento


class IncapacidadService:

    @staticmethod
    def crear_incapacidad(data, archivos):
        # ------------------------
        # Validación de datos
        # ------------------------
        campos_obligatorios = ["empleado", "documento", "entidad", "tipo", "fecha", "dias"]
        faltantes = [c for c in campos_obligatorios if c not in data]

        if faltantes:
            raise ValueError(f"Faltan campos obligatorios: {faltantes}")

        # Validación y conversión de fecha
        fecha_data = data["fecha"]
        
        if isinstance(fecha_data, str):
            # Si el dato es una cadena (str), intentamos parsearla.
            try:
                fecha_inicio = datetime.strptime(fecha_data, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("El formato de 'fecha' debe ser YYYY-MM-DD")
        
        elif isinstance(fecha_data, date):
            # Si el dato ya es un objeto date o datetime (como indica la traza de error), lo usamos directamente.
            # Nos aseguramos de obtener solo la parte de la fecha si es un objeto datetime completo.
            fecha_inicio = fecha_data.date() if isinstance(fecha_data, datetime) else fecha_data
        
        else:
            # Manejo de cualquier otro tipo inesperado.
            raise TypeError(f"Tipo de dato inesperado para 'fecha': {type(fecha_data)}. Se esperaba str o date.")
        
        # ------------------------
        # Crear incapacidad
        # ------------------------
        inc = Incapacidad(
            empleado=data["empleado"],
            documento=data["documento"],
            entidad=data["entidad"],
            tipo=data["tipo"],
            fecha_inicio=fecha_inicio,
            dias=data["dias"],
            estado="Pendiente"
        )

        try:
            db.session.add(inc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al guardar incapacidad: {str(e)}")

        # ------------------------
        # Validación carpeta uploads
        # ------------------------
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        # ------------------------
        # Guardar documentos
        # ------------------------
        if archivos:
            for archivo in archivos:
                if archivo and archivo.filename:

                    filename = secure_filename(archivo.filename)

                    # Validación de extensión permitida
                    ext = filename.rsplit(".", 1)[-1].lower()
                    if ext not in ["pdf", "jpg", "jpeg", "png"]:
                        continue  # O raise Exception si deseas bloquear

                    ruta = os.path.join(Config.UPLOAD_FOLDER, filename)

                    try:
                        archivo.save(ruta)

                        tipo_doc = identificar_tipo_documento(filename)

                        nuevo_archivo = Archivo(
                            incapacidad_id=inc.id,
                            nombre_archivo=filename,
                            tipo_documento=tipo_doc
                        )
                        db.session.add(nuevo_archivo)

                    except Exception as e:
                        db.session.rollback()
                        if os.path.exists(ruta):
                            os.remove(ruta)
                        raise Exception(f"Error al guardar archivo: {str(e)}")

        # Commit final
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error final al guardar archivos: {str(e)}")

        return inc

    @staticmethod
    def cambiar_estado(id, estado):
        inc = Incapacidad.query.get_or_404(id)

        inc.estado = estado

        try:
            db.session.commit()
            return inc
        except Exception as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el estado: {str(e)}")