from flask import jsonify, request
from models.medico_model import Medico
from config.db import db

class MedicoController:

    @staticmethod
    def listar_medicos():
        medicos = Medico.obtener_todos()
        data = []

        for m in medicos:
            data.append({
                "id_medico": m.id_medico,
                "nombre": m.nombre,
                "especialidad": m.especialidad,
                "licencia": m.licencia
            })

        return jsonify(data)

    @staticmethod
    def obtener_medico(id_medico):
        medico = Medico.obtener_por_id(id_medico)
        if not medico:
            return jsonify({"error": "Médico no encontrado"}), 404

        return jsonify({
            "id_medico": medico.id_medico,
            "nombre": medico.nombre,
            "especialidad": medico.especialidad,
            "licencia": medico.licencia
        })

    @staticmethod
    def crear_medico():
        data = request.json

        nuevo_id = Medico.crear(data)
        return jsonify({
            "mensaje": "Médico creado exitosamente",
            "id_medico": nuevo_id
        }), 201

    @staticmethod
    def actualizar_medico(id_medico):
        data = request.json

        actualizado = Medico.actualizar(id_medico, data)
        if not actualizado:
            return jsonify({"error": "Médico no encontrado"}), 404

        return jsonify({"mensaje": "Médico actualizado exitosamente"})

    @staticmethod
    def eliminar_medico(id_medico):
        eliminado = Medico.eliminar(id_medico)
        if not eliminado:
            return jsonify({"error": "Médico no encontrado"}), 404

        return jsonify({"mensaje": "Médico eliminado correctamente"})
