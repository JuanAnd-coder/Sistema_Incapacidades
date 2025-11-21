"""
Configuración de Firebase para autenticación con Google
"""
import os

# Variable global para almacenar la app de Firebase
firebase_app = None

def init_firebase():
    """
    Inicializa Firebase Admin SDK
    Requiere un archivo de credenciales JSON de Firebase
    """
    global firebase_app
    
    if firebase_app is not None:
        return firebase_app
    
    # Intentar importar firebase_admin (puede no estar instalado)
    try:
        import firebase_admin
        from firebase_admin import credentials, auth
    except ImportError:
        print("⚠️  firebase-admin no está instalado. La autenticación con Google no funcionará.")
        print("   Instala con: pip install firebase-admin")
        return None
    
    # Calcular BASE_DIR (directorio base del proyecto)
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Ruta al archivo de credenciales de Firebase
    # Por defecto busca en la carpeta config/
    cred_path = os.path.join(BASE_DIR, "config", "firebase-credentials.json")
    
    # También verificar si está definido en variables de entorno
    cred_path_env = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if cred_path_env:
        cred_path = cred_path_env
    
    # Verificar si el archivo existe
    if not os.path.exists(cred_path):
        print(f"⚠️  ADVERTENCIA: Archivo de credenciales de Firebase no encontrado en: {cred_path}")
        print("   La autenticación con Google no funcionará hasta que agregues el archivo.")
        print("   Para obtener las credenciales:")
        print("   1. Ve a https://console.firebase.google.com/")
        print("   2. Selecciona tu proyecto")
        print("   3. Ve a Configuración del proyecto > Cuentas de servicio")
        print("   4. Haz clic en 'Generar nueva clave privada'")
        print("   5. Guarda el archivo JSON como 'firebase-credentials.json' en la carpeta config/")
        return None
    
    try:
        # Inicializar Firebase con las credenciales
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado correctamente")
        return firebase_app
    except Exception as e:
        print(f"❌ Error al inicializar Firebase: {str(e)}")
        return None

def verify_firebase_token(id_token):
    """
    Verifica un token de ID de Firebase y retorna la información del usuario
    
    Args:
        id_token: Token de ID obtenido del cliente Firebase
    
    Returns:
        dict: Información del usuario (uid, email, name, etc.) o None si el token es inválido
    """
    try:
        if firebase_app is None:
            print("⚠️  Firebase no está inicializado. Verifica que firebase-credentials.json esté en config/")
            return None
        
        # Importar auth si no está disponible
        try:
            from firebase_admin import auth
        except ImportError:
            print("⚠️  firebase_admin.auth no está disponible")
            return None
        
        if not id_token:
            print("⚠️  Token no proporcionado")
            return None
        
        # Verificar el token
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as verify_error:
            print(f"❌ Error al verificar token: {str(verify_error)}")
            print(f"   Tipo de error: {type(verify_error).__name__}")
            return None
        
        # Extraer información del usuario
        user_info = {
            'uid': decoded_token.get('uid'),
            'email': decoded_token.get('email'),
            'name': decoded_token.get('name'),
            'picture': decoded_token.get('picture'),
            'email_verified': decoded_token.get('email_verified', False)
        }
        
        print(f"✅ Token verificado correctamente para usuario: {user_info.get('email')}")
        return user_info
    except Exception as e:
        print(f"❌ Error inesperado al verificar token de Firebase: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def get_firebase_config():
    """
    Retorna la configuración de Firebase para el cliente
    Esta información se usa en el frontend para inicializar Firebase
    """
    # Estas son las credenciales públicas que se usan en el frontend
    # Debes reemplazarlas con las de tu proyecto Firebase
    config = {
        'apiKey': os.getenv('FIREBASE_API_KEY', ''),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN', ''),
        'projectId': os.getenv('FIREBASE_PROJECT_ID', ''),
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET', ''),
        'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID', ''),
        'appId': os.getenv('FIREBASE_APP_ID', '')
    }
    
    return config

