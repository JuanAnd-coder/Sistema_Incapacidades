from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.usuario_model import Usuario
from config.db import db
from config.firebase_config import verify_firebase_token, get_firebase_config, init_firebase

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, redirigir al dashboard correspondiente
    if "user_id" in session:
        rol = session.get("rol")
        if rol == "Administrador":
            return redirect(url_for("admin.dashboard"))
        elif rol == "Empleado":
            return redirect(url_for("empleado.dashboard"))
        elif rol == "Revisor":
            return redirect(url_for("revisor.dashboard"))
        elif rol == "Médico":
            return redirect(url_for("medico.dashboard"))
    
    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not correo or not contrasena:
            flash("Por favor, completa todos los campos", "error")
            return render_template("login.html")

        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario and usuario.verificar_password(contrasena):
            session["user_id"] = usuario.id_usuario
            session["rol"] = usuario.rol
            session["nombre"] = usuario.nombre
            flash(f"Bienvenido, {usuario.nombre}!", "success")

            # Redirigir según el rol
            if usuario.rol == "Administrador":
                return redirect(url_for("admin.dashboard"))
            elif usuario.rol == "Empleado":
                return redirect(url_for("empleado.dashboard"))
            elif usuario.rol == "Revisor":
                return redirect(url_for("revisor.dashboard"))
            elif usuario.rol == "Médico":
                return redirect(url_for("medico.dashboard"))
            else:
                flash("Rol no reconocido", "error")
        else:
            flash("Correo o contraseña incorrectos", "error")
    
    return render_template("login.html")


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Ruta para registrar nuevos usuarios"""
    # Si ya está logueado, redirigir al dashboard
    if "user_id" in session:
        rol = session.get("rol")
        if rol == "Administrador":
            return redirect(url_for("admin.dashboard"))
        elif rol == "Empleado":
            return redirect(url_for("empleado.dashboard"))
        elif rol == "Revisor":
            return redirect(url_for("revisor.dashboard"))
        elif rol == "Médico":
            return redirect(url_for("medico.dashboard"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")
        confirmar_password = request.form.get("confirmar_password", "")
        rol = request.form.get("rol", "Empleado").strip()  # Por defecto Empleado
        
        # Validaciones
        if not all([nombre, correo, password, confirmar_password]):
            flash("Por favor, completa todos los campos", "error")
            return render_template("registro.html")
        
        if password != confirmar_password:
            flash("Las contraseñas no coinciden", "error")
            return render_template("registro.html")
        
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "error")
            return render_template("registro.html")
        
        # Verificar si el correo ya existe
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash("Este correo electrónico ya está registrado. Por favor, usa otro correo o inicia sesión.", "error")
            return render_template("registro.html")
        
        # Validar rol (solo permitir ciertos roles en el registro público)
        roles_permitidos = ["Empleado"]  # Solo permitir registro como Empleado
        if rol not in roles_permitidos:
            rol = "Empleado"  # Forzar rol Empleado para registros públicos
        
        # Crear nuevo usuario
        try:
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                password=password,
                rol=rol
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            flash(f"¡Registro exitoso! Bienvenido, {nombre}. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar usuario: {str(e)}", "error")
            return render_template("registro.html")
    
    return render_template("registro.html")


@auth_bp.route('/google/callback', methods=['POST'])
def google_callback():
    """
    Maneja el callback de autenticación con Google/Firebase
    Recibe el token de ID de Firebase y crea/autentica al usuario
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        id_token = data.get('idToken')
        
        if not id_token:
            print("⚠️  No se recibió idToken en la petición")
            return jsonify({'error': 'Token no proporcionado'}), 400
        
        print(f"📝 Token recibido (primeros 20 caracteres): {id_token[:20]}...")
        
        # Verificar el token con Firebase
        user_info = verify_firebase_token(id_token)
        
        if not user_info:
            print("❌ No se pudo verificar el token. Verifica los logs anteriores.")
            return jsonify({
                'error': 'Token inválido',
                'message': 'No se pudo verificar el token. Verifica que Firebase esté configurado correctamente.'
            }), 401
        
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])  # Usar email si no hay nombre
        uid = user_info.get('uid')
        
        if not email:
            return jsonify({'error': 'Email no disponible'}), 400
        
        # Buscar si el usuario ya existe
        usuario = Usuario.query.filter_by(correo=email).first()
        
        if not usuario:
            # Crear nuevo usuario con rol Empleado por defecto
            # Para usuarios de Google, no necesitamos password
            nuevo_usuario = Usuario(
                nombre=name,
                correo=email,
                password="google_auth",  # Placeholder, no se usará
                rol="Empleado"
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            usuario = nuevo_usuario
        
        # Iniciar sesión
        session["user_id"] = usuario.id_usuario
        session["rol"] = usuario.rol
        session["nombre"] = usuario.nombre
        session["auth_provider"] = "google"  # Marcar que viene de Google
        
        return jsonify({
            'success': True,
            'message': f'Bienvenido, {usuario.nombre}!',
            'redirect': get_dashboard_url(usuario.rol)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en autenticación: {str(e)}'}), 500


@auth_bp.route('/firebase-config')
def firebase_config():
    """
    Retorna la configuración de Firebase para el frontend
    """
    config = get_firebase_config()
    return jsonify(config)


def get_dashboard_url(rol):
    """Helper para obtener la URL del dashboard según el rol"""
    if rol == "Administrador":
        return url_for("admin.dashboard")
    elif rol == "Empleado":
        return url_for("empleado.dashboard")
    elif rol == "Revisor":
        return url_for("revisor.dashboard")
    elif rol == "Médico":
        return url_for("medico.dashboard")
    else:
        return url_for("auth.login")


@auth_bp.route('/no-autorizado')
def no_autorizado():
    return render_template("no_autorizado.html"), 403
