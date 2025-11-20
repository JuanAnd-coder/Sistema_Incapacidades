from flask import Blueprint, render_template
from utils.decorators import rol_required

revisor_bp = Blueprint("revisor", __name__, url_prefix="/revisor")

@revisor_bp.route("/login.html")
@rol_required(["Revisor"])
def dashboard():
    return render_template("login.html")
