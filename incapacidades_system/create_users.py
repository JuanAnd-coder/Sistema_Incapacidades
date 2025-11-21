"""
Script para crear usuarios de prueba en el sistema
Ejecutar: python create_users.py
"""
import sys
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from config.db import db
from models.usuario_model import Usuario
from config.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def crear_usuarios():
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        usuarios_prueba = [
            {
                "nombre": "Admin Principal",
                "correo": "admin@empresa.com",
                "password": "admin123",
                "rol": "Administrador"
            },
            {
                "nombre": "Juan Pérez",
                "correo": "empleado@empresa.com",
                "password": "empleado123",
                "rol": "Empleado"
            },
            {
                "nombre": "María García",
                "correo": "revisor@empresa.com",
                "password": "revisor123",
                "rol": "Revisor"
            },
            {
                "nombre": "Dr. Carlos López",
                "correo": "medico@empresa.com",
                "password": "medico123",
                "rol": "Médico"
            }
        ]
        
        print("=" * 50)
        print("Creando usuarios de prueba...")
        print("=" * 50)
        
        for usuario_data in usuarios_prueba:
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.query.filter_by(correo=usuario_data["correo"]).first()
            
            if usuario_existente:
                print(f"[!] Usuario {usuario_data['correo']} ya existe, omitiendo...")
            else:
                try:
                    nuevo_usuario = Usuario(
                        nombre=usuario_data["nombre"],
                        correo=usuario_data["correo"],
                        password=usuario_data["password"],
                        rol=usuario_data["rol"]
                    )
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    print(f"[OK] Usuario creado: {usuario_data['correo']} ({usuario_data['rol']})")
                except Exception as e:
                    print(f"[ERROR] Error al crear {usuario_data['correo']}: {str(e)}")
        
        print("=" * 50)
        print("Usuarios de prueba creados exitosamente!")
        print("=" * 50)
        print("\nCredenciales de acceso:")
        print("-" * 50)
        for usuario_data in usuarios_prueba:
            print(f"Rol: {usuario_data['rol']}")
            print(f"  Correo: {usuario_data['correo']}")
            print(f"  Contraseña: {usuario_data['password']}")
            print()

if __name__ == "__main__":
    crear_usuarios()

