from models.historial_model import Historial
from models.incapacidad_model import Incapacidad
from config.db import db

class HistorialController:

    @staticmethod
    def obtener_por_usuario(usuario_id):
        historial = (
            db.session.query(Historial)
            .filter(Historial.id_usuario == usuario_id)
            .order_by(Historial.fecha_registro.desc())
            .all()
        )

        resultado = []
        for h in historial:
            inc = h.incapacidad
            resultado.append({
                "id": h.id,
                "descripcion": h.descripcion,
                "fecha_registro": h.fecha_registro,
                "incapacidad": {
                    "id": inc.id,
                    "empleado": inc.empleado,
                    "documento": inc.documento,
                    "entidad": inc.entidad,
                    "tipo": inc.tipo,
                    "fecha_inicio": inc.fecha_inicio,
                    "dias": inc.dias,
                    "estado": inc.estado,
                }
            })

        return resultado

    @staticmethod
    def registrar(id_usuario, id_incapacidad, descripcion):
        nuevo = Historial(
            id_usuario=id_usuario,
            id_incapacidad=id_incapacidad,
            descripcion=descripcion
        )

        db.session.add(nuevo)
        db.session.commit()
        return nuevo.id
