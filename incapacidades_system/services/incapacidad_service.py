import os
# Importamos 'date' para hacer la verificación de tipo correctamente
from datetime import datetime, date 
from werkzeug.utils import secure_filename
from config.config import Config
from config.db import db
from models.incapacidad_model import Incapacidad, Archivo
from utils.helpers import identificar_tipo_documento
from utils.constantes import DOCUMENTOS_REQUERIDOS


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
        tipos_documentos_subidos = []
        
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
                        tipos_documentos_subidos.append(tipo_doc)

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
        
        # ------------------------
        # Validación de documentos obligatorios básicos
        # ------------------------
        # Verificar que se haya subido al menos "Soporte incapacidad" o "Epicrisis"
        documentos_basicos = ["Soporte incapacidad", "Epicrisis"]
        tiene_documento_basico = any(doc in tipos_documentos_subidos for doc in documentos_basicos)
        
        if not tipos_documentos_subidos:
            raise ValueError(
                "❌ ERROR: Debes subir al menos un documento. "
                "Documentos obligatorios mínimos: 'Soporte incapacidad' o 'Epicrisis'. "
                "Asegúrate de que el nombre del archivo contenga palabras como 'incapacidad', 'soporte', 'epicrisis' o 'epic'."
            )
        
        if not tiene_documento_basico:
            # Si se subieron archivos pero ninguno es básico, advertir
            raise ValueError(
                "❌ ERROR: Debes subir al menos uno de estos documentos obligatorios: "
                "'Soporte incapacidad' o 'Epicrisis'. "
                "Los archivos subidos no fueron reconocidos como documentos válidos. "
                "Asegúrate de que el nombre del archivo contenga palabras como:\n"
                "- Para Soporte incapacidad: 'incapacidad', 'soporte', 'incap'\n"
                "- Para Epicrisis: 'epicrisis', 'epic'"
            )
        
        # Validación adicional: verificar documentos requeridos según el tipo
        tipo_incapacidad = data.get("tipo")
        if tipo_incapacidad and tipo_incapacidad in DOCUMENTOS_REQUERIDOS:
            docs_requeridos = DOCUMENTOS_REQUERIDOS[tipo_incapacidad]
            docs_faltantes = [doc for doc in docs_requeridos if doc not in tipos_documentos_subidos]
            
            if docs_faltantes:
                # Advertir pero no bloquear (pueden agregarse después)
                pass  # Se puede completar el registro y agregar documentos faltantes después

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
    
    @staticmethod
    def agregar_documentos(incapacidad_id, archivos):
        """
        Agrega documentos adicionales a una incapacidad existente
        """
        inc = Incapacidad.query.get_or_404(incapacidad_id)
        
        # Validación carpeta uploads
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        documentos_agregados = []
        tipos_documentos_nuevos = []
        
        if archivos:
            for archivo in archivos:
                if archivo and archivo.filename:
                    filename = secure_filename(archivo.filename)
                    
                    # Validación de extensión permitida
                    ext = filename.rsplit(".", 1)[-1].lower()
                    if ext not in ["pdf", "jpg", "jpeg", "png"]:
                        continue
                    
                    # Verificar si el archivo ya existe
                    ruta = os.path.join(Config.UPLOAD_FOLDER, filename)
                    if os.path.exists(ruta):
                        # Agregar timestamp para evitar conflictos
                        base, ext_file = os.path.splitext(filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{base}_{timestamp}{ext_file}"
                        ruta = os.path.join(Config.UPLOAD_FOLDER, filename)
                    
                    try:
                        archivo.save(ruta)
                        
                        tipo_doc = identificar_tipo_documento(filename)
                        tipos_documentos_nuevos.append(tipo_doc)
                        
                        nuevo_archivo = Archivo(
                            incapacidad_id=inc.id,
                            nombre_archivo=filename,
                            tipo_documento=tipo_doc
                        )
                        db.session.add(nuevo_archivo)
                        documentos_agregados.append(filename)
                        
                    except Exception as e:
                        db.session.rollback()
                        if os.path.exists(ruta):
                            os.remove(ruta)
                        raise Exception(f"Error al guardar archivo {filename}: {str(e)}")
        
        # Commit final
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al agregar documentos: {str(e)}")
        
        # Verificar que después de agregar documentos, existan los básicos
        # Obtener todos los documentos actuales de la incapacidad
        docs_actuales = [a.tipo_documento for a in inc.archivos]
        documentos_basicos = ["Soporte incapacidad", "Epicrisis"]
        tiene_documento_basico = any(doc in docs_actuales for doc in documentos_basicos)
        
        if not tiene_documento_basico:
            # Advertir pero no bloquear (ya que puede estar agregando documentos progresivamente)
            return {
                "documentos_agregados": documentos_agregados,
                "advertencia": "Aún falta subir al menos uno de estos documentos obligatorios: 'Soporte incapacidad' o 'Epicrisis'"
            }
        
        return {
            "documentos_agregados": documentos_agregados,
            "advertencia": None
        }