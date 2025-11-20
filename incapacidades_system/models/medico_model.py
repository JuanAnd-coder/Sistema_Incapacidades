from config.db import db

class Medico(db.Model):
    __tablename__ = "medicos"

    id_medico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, especialidad, licencia):
        self.nombre = nombre
        self.especialidad = especialidad
        self.licencia = licencia

    # Obtener todos
    @staticmethod
    def obtener_todos():
        return Medico.query.all()

    # Obtener por ID
    @staticmethod
    def obtener_por_id(id_medico):
        return Medico.query.get(id_medico)

    # Crear
    @staticmethod
    def crear(data):
        nuevo = Medico(
            nombre=data.get("nombre"),
            especialidad=data.get("especialidad"),
            licencia=data.get("licencia")
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.id_medico

    # Actualizar
    @staticmethod
    def actualizar(id_medico, data):
        medico = Medico.query.get(id_medico)
        if not medico:
            return False

        medico.nombre = data.get("nombre", medico.nombre)
        medico.especialidad = data.get("especialidad", medico.especialidad)
        medico.licencia = data.get("licencia", medico.licencia)

        db.session.commit()
        return True

    # Eliminar
    @staticmethod
    def eliminar(id_medico):
        medico = Medico.query.get(id_medico)
        if not medico:
            return False

        db.session.delete(medico)
        db.session.commit()
        return True
