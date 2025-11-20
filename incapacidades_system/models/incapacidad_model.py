from config.db import db
from datetime import datetime

class Incapacidad(db.Model):
    __tablename__ = "incapacidad"

    id = db.Column(db.Integer, primary_key=True)
    empleado = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    entidad = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default="Registrada")
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    archivos = db.relationship("Archivo", backref="incapacidad",
                               cascade="all, delete-orphan")


class Archivo(db.Model):
    __tablename__ = "archivo"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidad.id"))
    nombre_archivo = db.Column(db.String(200), nullable=False)
    tipo_documento = db.Column(db.String(100), nullable=False)
