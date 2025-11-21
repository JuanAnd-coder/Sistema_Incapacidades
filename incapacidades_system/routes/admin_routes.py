from flask import Blueprint, render_template
from utils.decorators import rol_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@rol_required("Administrador")
def dashboard():
    return render_template("admin_dashboard.html")
