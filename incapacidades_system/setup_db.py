"""
Script para crear la base de datos MySQL si no existe
Ejecutar: python setup_db.py
"""
import pymysql

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambiar si tienes contraseña
    'charset': 'utf8mb4'
}

DB_NAME = 'incapacidades_db'

try:
    # Conectar a MySQL (sin especificar base de datos)
    connection = pymysql.connect(**DB_CONFIG)
    
    with connection.cursor() as cursor:
        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Base de datos '{DB_NAME}' creada o ya existe")
    
    connection.close()
    print("✓ Configuración de base de datos completada")
    
except pymysql.Error as e:
    print(f"✗ Error al conectar con MySQL: {e}")
    print("\nAsegúrate de que:")
    print("1. MySQL esté instalado y corriendo")
    print("2. El usuario 'root' tenga acceso (o modifica la configuración)")
    print("3. Si tienes contraseña, actualiza 'password' en este script")
except Exception as e:
    print(f"✗ Error inesperado: {e}")

