from functools import wraps
from flask import session, redirect, url_for, flash

def rol_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "rol" not in session or session["rol"] not in roles:
                flash("No tienes permisos para acceder a esta página")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
