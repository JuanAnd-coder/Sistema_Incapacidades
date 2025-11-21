import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = "clave-secreta"
    # Para desarrollo: usar SQLite (más fácil, no requiere MySQL)
    SQLALCHEMY_DATABASE_URI = "sqlite:///incapacidades.db"
    
    # Para producción: usar MySQL (descomentar y comentar la línea de arriba)
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/incapacidades_db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    
    # Configuración de Firebase (puedes usar variables de entorno)
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY', '')
    FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN', '')
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', '')
    FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', '')
    FIREBASE_MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID', '')
    FIREBASE_APP_ID = os.getenv('FIREBASE_APP_ID', '')
