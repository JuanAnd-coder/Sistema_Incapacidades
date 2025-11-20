from functools import wraps
from flask import session, jsonify, redirect, url_for, request

def _is_api_request():
    """Detecta si la petición es API o HTML."""
    return request.is_json or (
        request.accept_mimetypes.accept_json and
        not request.accept_mimetypes.accept_html
    )



def rol_requerido(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if "rol" not in session:
                if _is_api_request():
                    return jsonify({"error": "Debe iniciar sesión"}), 401
                return redirect(url_for("auth.login"))

            if session["rol"] not in roles:
                if _is_api_request():
                    return jsonify({"error": "Permiso denegado"}), 403
                return redirect(url_for("auth.no_autorizado"))

            return f(*args, **kwargs)
        return wrapper
    return decorator
