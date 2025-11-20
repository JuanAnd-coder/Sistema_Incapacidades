from flask import jsonify, request
from models.usuario_model import Usuario
from config.db import db

class UsuarioController:

    @staticmethod
    def listar_usuarios():
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
        data = request.json

        try:
            nuevo_id = Usuario.crear(data)
            return jsonify({
                "mensaje": "Usuario creado correctamente",
                "id_usuario": nuevo_id
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def actualizar_usuario(usuario_id):
        data = request.json
        actualizado = Usuario.actualizar(usuario_id, data)

        if not actualizado:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"mensaje": "Usuario actualizado correctamente"})

    @staticmethod
    def eliminar_usuario(usuario_id):
        eliminado = Usuario.eliminar(usuario_id)

        if not eliminado:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"mensaje": "Usuario eliminado correctamente"})
