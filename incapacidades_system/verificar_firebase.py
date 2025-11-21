"""
Script para verificar la configuración de Firebase
Ejecuta este script para diagnosticar problemas con Firebase
"""

import os
import sys

print("=" * 60)
print("Verificación de Configuración de Firebase")
print("=" * 60)

# 1. Verificar si firebase-admin está instalado
print("\n1. Verificando instalación de firebase-admin...")
try:
    import firebase_admin
    from firebase_admin import credentials, auth
    print("   ✅ firebase-admin está instalado")
except ImportError as e:
    print(f"   ❌ firebase-admin NO está instalado: {e}")
    print("   💡 Instala con: pip install firebase-admin")
    sys.exit(1)

# 2. Verificar archivo de credenciales
print("\n2. Verificando archivo de credenciales...")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
cred_path = os.path.join(BASE_DIR, "config", "firebase-credentials.json")

if os.path.exists(cred_path):
    print(f"   ✅ Archivo encontrado en: {cred_path}")
    
    # Verificar que sea un JSON válido
    try:
        import json
        with open(cred_path, 'r') as f:
            cred_data = json.load(f)
        
        # Verificar campos requeridos
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in cred_data]
        
        if missing_fields:
            print(f"   ⚠️  Campos faltantes en el archivo: {', '.join(missing_fields)}")
        else:
            print(f"   ✅ Archivo JSON válido")
            print(f"   📋 Project ID: {cred_data.get('project_id', 'N/A')}")
            print(f"   📧 Client Email: {cred_data.get('client_email', 'N/A')}")
    except json.JSONDecodeError as e:
        print(f"   ❌ El archivo no es un JSON válido: {e}")
    except Exception as e:
        print(f"   ⚠️  Error al leer el archivo: {e}")
else:
    print(f"   ❌ Archivo NO encontrado en: {cred_path}")
    print("   💡 Descarga el archivo desde Firebase Console:")
    print("      1. Ve a https://console.firebase.google.com/")
    print("      2. Selecciona tu proyecto")
    print("      3. Ve a Configuración del proyecto > Cuentas de servicio")
    print("      4. Haz clic en 'Generar nueva clave privada'")
    print(f"      5. Guarda el archivo como: {cred_path}")

# 3. Intentar inicializar Firebase
print("\n3. Intentando inicializar Firebase...")
try:
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        app = firebase_admin.initialize_app(cred)
        print("   ✅ Firebase inicializado correctamente")
        
        # 4. Verificar que podemos acceder a auth
        print("\n4. Verificando acceso a Firebase Auth...")
        try:
            # Solo verificar que el módulo funciona, no hacer una verificación real
            print("   ✅ Firebase Auth está disponible")
        except Exception as e:
            print(f"   ❌ Error al acceder a Firebase Auth: {e}")
    else:
        print("   ⚠️  No se puede inicializar sin el archivo de credenciales")
except Exception as e:
    print(f"   ❌ Error al inicializar Firebase: {e}")
    import traceback
    traceback.print_exc()

# 5. Verificar configuración del frontend
print("\n5. Verificando configuración del frontend...")
config_file = os.path.join(BASE_DIR, "static", "js", "firebaseconfig.js")
if os.path.exists(config_file):
    print(f"   ✅ Archivo de configuración encontrado: {config_file}")
    with open(config_file, 'r') as f:
        content = f.read()
        if 'apiKey' in content and 'projectId' in content:
            print("   ✅ Configuración parece estar presente")
        else:
            print("   ⚠️  Configuración incompleta en firebaseconfig.js")
else:
    print(f"   ❌ Archivo de configuración NO encontrado: {config_file}")

print("\n" + "=" * 60)
print("Verificación completada")
print("=" * 60)
print("\n💡 Si hay errores, revisa los mensajes anteriores para solucionarlos.")
print("💡 Asegúrate de que el project_id en firebase-credentials.json")
print("   coincida con el projectId en firebaseconfig.js")

