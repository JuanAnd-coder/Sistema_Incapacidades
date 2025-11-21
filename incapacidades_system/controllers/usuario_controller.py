from flask import jsonify, request, render_template, redirect, url_for, flash
from models.usuario_model import Usuario
from config.db import db

class UsuarioController:

    @staticmethod
    def listar_usuarios():
        # Verificar si es una petición explícita de JSON (API)
        # Solo devolver JSON si:
        # 1. El Content-Type es application/json
        # 2. O si hay un parámetro ?format=json
        # 3. O si el header Accept solo acepta JSON (sin HTML)
        wants_json = (
            request.is_json or 
            request.args.get('format') == 'json' or
            (request.accept_mimetypes.accept_json and 
             not request.accept_mimetypes.accept_html)
        )
        
        if wants_json:
            usuarios = Usuario.obtener_todos()
            data = []
            for u in usuarios:
                data.append({
                    "id_usuario": u.id_usuario,
                    "nombre": u.nombre,
                    "correo": u.correo,
                    "rol": u.rol
                })
            return jsonify(data)
        
        # Por defecto, devolver HTML (Web) - cuando se accede desde navegador
        usuarios = Usuario.obtener_todos()
        return render_template("usuarios/lista.html", usuarios=usuarios)

    @staticmethod
    def obtener_usuario(usuario_id):
        usuario = Usuario.obtener_por_id(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol
        })

    @staticmethod
    def crear_usuario():
        # Si es una petición JSON (API)
        if request.is_json:
            data = request.json
            try:
                nuevo_id = Usuario.crear(data)
                return jsonify({
                    "mensaje": "Usuario creado correctamente",
                    "id_usuario": nuevo_id
                }), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Si es una petición HTML (Web)
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            correo = request.form.get("correo", "").strip()
            password = request.form.get("password", "")
            rol = request.form.get("rol", "").strip()
            
            # Validaciones
            if not nombre or not correo or not password or not rol:
                flash("Todos los campos son obligatorios", "error")
                return render_template("usuarios/crear.html")
            
            # Verificar si el correo ya existe
            usuario_existente = Usuario.obtener_por_correo(correo)
            if usuario_existente:
                flash("El correo electrónico ya está registrado", "error")
                return render_template("usuarios/crear.html")
            
            try:
                data = {
                    "nombre": nombre,
                    "correo": correo,
                    "password": password,
                    "rol": rol
                }
                nuevo_id = Usuario.crear(data)
                flash(f"Usuario creado exitosamente (ID: {nuevo_id})", "success")
                return redirect(url_for("usuario.listar"))
            except Exception as e:
                flash(f"Error al crear usuario: {str(e)}", "error")
                return render_template("usuarios/crear.html")
        
        # GET: Mostrar formulario
        return render_template("usuarios/crear.html")

    @staticmethod
    def actualizar_usuario(usuario_id):
        # Si es una petición JSON (API)
        if request.is_json:
            data = request.json
            actualizado = Usuario.actualizar(usuario_id, data)
            if not actualizado:
                return jsonify({"error": "Usuario no encontrado"}), 404
            return jsonify({"mensaje": "Usuario actualizado correctamente"})
        
        # Si es una petición HTML (Web)
        usuario = Usuario.obtener_por_id(usuario_id)
        if not usuario:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("usuario.listar"))
        
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            correo = request.form.get("correo", "").strip()
            rol = request.form.get("rol", "").strip()
            
            # Validaciones
            if not nombre or not correo or not rol:
                flash("Todos los campos son obligatorios", "error")
                return render_template("usuarios/editar.html", usuario=usuario)
            
            # Verificar si el correo ya existe en otro usuario
            usuario_existente = Usuario.obtener_por_correo(correo)
            if usuario_existente and usuario_existente.id_usuario != usuario_id:
                flash("El correo electrónico ya está registrado en otro usuario", "error")
                return render_template("usuarios/editar.html", usuario=usuario)
            
            try:
                data = {
                    "nombre": nombre,
                    "correo": correo,
                    "rol": rol
                }
                actualizado = Usuario.actualizar(usuario_id, data)
                if actualizado:
                    flash("Usuario actualizado exitosamente", "success")
                    return redirect(url_for("usuario.listar"))
                else:
                    flash("Error al actualizar usuario", "error")
            except Exception as e:
                flash(f"Error al actualizar usuario: {str(e)}", "error")
        
        # GET: Mostrar formulario de edición
        return render_template("usuarios/editar.html", usuario=usuario)

    @staticmethod
    def eliminar_usuario(usuario_id):
        # Si es una petición JSON (API)
        if request.is_json or request.accept_mimetypes.accept_json:
            eliminado = Usuario.eliminar(usuario_id)
            if not eliminado:
                return jsonify({"error": "Usuario no encontrado"}), 404
            return jsonify({"mensaje": "Usuario eliminado correctamente"})
        
        # Si es una petición HTML (Web)
        try:
            eliminado = Usuario.eliminar(usuario_id)
            if eliminado:
                flash("Usuario eliminado exitosamente", "success")
            else:
                flash("Usuario no encontrado", "error")
        except Exception as e:
            flash(f"Error al eliminar usuario: {str(e)}", "error")
        
        return redirect(url_for("usuario.listar"))
