from functools import wraps
from flask import session, redirect, url_for, flash

def rol_required(*roles):
    """
    Decorador para requerir roles específicos.
    Uso: @rol_required("Administrador") o @rol_required("Empleado", "Revisor")
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Si no hay sesión, redirigir al login
            if "user_id" not in session or "rol" not in session:
                flash("Debes iniciar sesión para acceder a esta página", "error")
                return redirect(url_for("auth.login"))
            
            # Si el rol no está en la lista de roles permitidos
            if session["rol"] not in roles:
                flash("No tienes permisos para acceder a esta página", "error")
                return redirect(url_for("auth.no_autorizado"))
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
