"""
Script simple para crear un usuario personalizado
Ejecutar: python crear_usuario.py
"""
from config.db import db
from models.usuario_model import Usuario
from config.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def crear_usuario_personalizado():
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        print("=" * 60)
        print("CREAR NUEVO USUARIO")
        print("=" * 60)
        print()
        
        # Solicitar datos al usuario
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo electrónico: ").strip()
        password = input("Contraseña: ").strip()
        
        print("\nRoles disponibles:")
        print("1. Administrador")
        print("2. Empleado")
        print("3. Revisor")
        print("4. Médico")
        
        opcion_rol = input("\nSeleccione el rol (1-4): ").strip()
        
        roles = {
            "1": "Administrador",
            "2": "Empleado",
            "3": "Revisor",
            "4": "Médico"
        }
        
        rol = roles.get(opcion_rol, "Empleado")
        
        # Validaciones
        if not nombre or not correo or not password:
            print("\n❌ Error: Todos los campos son obligatorios")
            return
        
        if len(password) < 6:
            print("\n❌ Error: La contraseña debe tener al menos 6 caracteres")
            return
        
        # Verificar si el correo ya existe
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            print(f"\n❌ Error: El correo {correo} ya está registrado")
            return
        
        # Crear el usuario
        try:
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                password=password,
                rol=rol
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("✅ USUARIO CREADO EXITOSAMENTE")
            print("=" * 60)
            print(f"Nombre: {nombre}")
            print(f"Correo: {correo}")
            print(f"Rol: {rol}")
            print(f"ID: {nuevo_usuario.id_usuario}")
            print("\nAhora puedes iniciar sesión con estas credenciales.")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error al crear usuario: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    crear_usuario_personalizado()

