from flask import jsonify
from models.empleado_model import Empleado

class EmpleadoController:

    @staticmethod
    def listar():
        empleados = Empleado.obtener_todos()
        return [EmpleadoController.serializar(e) for e in empleados]

    @staticmethod
    def obtener(id_empleado):
        empleado = Empleado.obtener_por_id(id_empleado)
        if not empleado:
            return None
        return EmpleadoController.serializar(empleado)

    @staticmethod
    def crear(data):
        nuevo_id = Empleado.crear(data)
        return nuevo_id

    @staticmethod
    def actualizar(id_empleado, data):
        return Empleado.actualizar(id_empleado, data)

    @staticmethod
    def eliminar(id_empleado):
        return Empleado.eliminar(id_empleado)

    @staticmethod
    def serializar(empleado):
        return {
            "id_empleado": empleado.id_empleado,
            "nombre": empleado.nombre,
            "cargo": empleado.cargo,
            "area": empleado.area,
            "cedula": empleado.cedula
        }
