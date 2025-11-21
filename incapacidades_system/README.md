# Sistema de Gestión de Incapacidades

## Requisitos Previos

- Python 3.8 o superior
- MySQL Server (para producción) o SQLite (para desarrollo)
- pip (gestor de paquetes de Python)

## Instalación y Configuración

### 1. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# En Windows (CMD):
venv\Scripts\activate.bat

# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

#### Opción A: MySQL (Producción)

1. Asegúrate de que MySQL esté instalado y corriendo
2. Ejecuta el script de configuración:
```bash
python setup_db.py
```

3. Si tienes contraseña en MySQL, edita `config/config.py`:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:TU_CONTRASEÑA@localhost/incapacidades_db"
```

#### Opción B: SQLite (Desarrollo - Más fácil)

Si no tienes MySQL instalado, puedes usar SQLite. Edita `config/config.py`:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///incapacidades.db"
```

**Nota:** Con SQLite no necesitas crear la base de datos manualmente, se crea automáticamente.

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Estructura del Proyecto

```
incapacidades_system/
├── app.py                 # Aplicación principal
├── config/                # Configuración
│   ├── config.py         # Configuración de la app
│   └── db.py             # Configuración de base de datos
├── controllers/          # Controladores
├── models/               # Modelos de datos
├── routes/               # Rutas/Endpoints
├── services/             # Lógica de negocio
├── templates/            # Plantillas HTML
├── utils/                # Utilidades
└── uploads/              # Archivos subidos
```

## Funcionalidades

- ✅ Registro de incapacidades
- ✅ Subida de documentos (PDF, JPG, PNG)
- ✅ Validación automática de documentos requeridos
- ✅ Gestión de empleados, médicos y usuarios
- ✅ Sistema de autenticación con roles (Admin, Empleado, Revisor)
- ✅ Historial de incapacidades

## Solución de Problemas

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté instalado y corriendo
- Verifica las credenciales en `config/config.py`
- Usa SQLite para desarrollo (más fácil)

### Error: "No module named 'flask'"
- Asegúrate de haber activado el entorno virtual
- Ejecuta: `pip install -r requirements.txt`

### Error al crear tablas
- Verifica que la base de datos exista
- Verifica los permisos del usuario de MySQL

## Desarrollo

Para desarrollo, se recomienda usar SQLite ya que no requiere configuración adicional.

## Producción

Para producción, usa MySQL y configura:
- SECRET_KEY seguro en `config/config.py`
- Contraseña de base de datos
- Configuración de servidor web (Nginx, Apache, etc.)

