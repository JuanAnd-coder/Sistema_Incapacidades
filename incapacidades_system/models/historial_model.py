from config.db import db
from datetime import datetime

class Historial(db.Model):
    __tablename__ = "historial"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_incapacidad = db.Column(db.Integer, db.ForeignKey("incapacidad.id"), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación ORM con incapacidad
    incapacidad = db.relationship("Incapacidad", backref="movimientos")
