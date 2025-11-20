from config.db import db
from werkzeug.security import generate_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, correo, password, rol):
        self.nombre = nombre
        self.correo = correo
        self.password = generate_password_hash(password)
        self.rol = rol

    # Obtener todos
    @staticmethod
    def obtener_todos():
        return Usuario.query.all()

    # Obtener por ID
    @staticmethod
    def obtener_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    # Obtener por correo
    @staticmethod
    def obtener_por_correo(correo):
        return Usuario.query.filter_by(correo=correo).first()

    # Crear
    @staticmethod
    def crear(data):
        nuevo = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            password=data["password"],
            rol=data["rol"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.id_usuario

    # Actualizar
    @staticmethod
    def actualizar(usuario_id, data):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return False

        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.correo = data.get("correo", usuario.correo)
        usuario.rol = data.get("rol", usuario.rol)

        db.session.commit()
        return True

    # Eliminar
    @staticmethod
    def eliminar(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return False

        db.session.delete(usuario)
        db.session.commit()
        return True
