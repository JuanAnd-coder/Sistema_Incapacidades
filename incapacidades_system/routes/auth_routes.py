from flask import Flask,Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from config.db import db
from models.usuario_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and check_password_hash(usuario.contrasena, contrasena):
            session["user_id"] = usuario.id
            session["rol"] = usuario.rol

            # Redirigir según el rol
            if usuario.rol == "Administrador":
                return redirect(url_for("admin_dashboard"))
            elif usuario.rol == "Empleado":
                return redirect(url_for("empleado_dashboard"))
            elif usuario.rol == "Revisor":
                return redirect(url_for("revisor_dashboard"))
        else:
            flash("Correo o contraseña incorrectos")
    return render_template("login.html")


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Sesión cerrada.")
    return redirect('/login')
