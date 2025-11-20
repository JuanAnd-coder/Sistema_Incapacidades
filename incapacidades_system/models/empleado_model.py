from config.db import db

class Empleado(db.Model):
    __tablename__ = "empleados"

    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(150), nullable=False)
    area = db.Column(db.String(150), nullable=False)
    cedula = db.Column(db.String(50), unique=True, nullable=False)

    # ---- MÉTODOS CRUD ----

    @staticmethod
    def obtener_todos():
        return Empleado.query.all()

    @staticmethod
    def obtener_por_id(id_empleado):
        return Empleado.query.get(id_empleado)

    @staticmethod
    def crear(data):
        nuevo = Empleado(
            nombre=data["nombre"],
            cargo=data["cargo"],
            area=data["area"],
            cedula=data["cedula"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.id_empleado

    @staticmethod
    def actualizar(id_empleado, data):
        empleado = Empleado.query.get(id_empleado)
        if not empleado:
            return False

        empleado.nombre = data["nombre"]
        empleado.cargo = data["cargo"]
        empleado.area = data["area"]
        empleado.cedula = data["cedula"]

        db.session.commit()
        return True

    @staticmethod
    def eliminar(id_empleado):
        empleado = Empleado.query.get(id_empleado)
        if not empleado:
            return False

        db.session.delete(empleado)
        db.session.commit()
        return True
