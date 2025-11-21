# 📍 Ubicación de los Datos del Sistema

Este documento explica dónde se almacenan todos los datos del sistema de incapacidades.

## 🗄️ Base de Datos (SQLite)

### Ubicación del Archivo
```
incapacidades_system/
└── instance/
    └── incapacidades.db  ← Base de datos SQLite
```

**Ruta completa:**
```
C:\Users\andre\Desktop\Ing soft\Sistema-Incapacidades\incapacidades_system\instance\incapacidades.db
```

### ¿Qué contiene?
- ✅ **Usuarios**: Información de todos los usuarios del sistema (nombre, correo, contraseña hasheada, rol)
- ✅ **Empleados**: Datos de los empleados (nombre, cargo, área, cédula)
- ✅ **Médicos**: Información de médicos (nombre, especialidad, licencia)
- ✅ **Incapacidades**: Todas las incapacidades registradas (empleado, tipo, fechas, días, estado)
- ✅ **Archivos**: Referencias a los documentos subidos (nombre, tipo de documento, relación con incapacidad)
- ✅ **Historial**: Movimientos y registros del historial (si está implementado)

### Configuración
La base de datos está configurada en `config/config.py`:
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///incapacidades.db"
```

**Nota:** SQLite guarda todo en un solo archivo `.db`, por lo que es fácil de respaldar.

---

## 📁 Archivos Subidos (Documentos)

### Ubicación
```
incapacidades_system/
└── uploads/
    ├── epicrisis.pdf
    ├── soporte_incapacidad.pdf
    ├── furips.pdf
    └── ... (otros documentos)
```

**Ruta completa:**
```
C:\Users\andre\Desktop\Ing soft\Sistema-Incapacidades\incapacidades_system\uploads\
```

### ¿Qué contiene?
- ✅ **Documentos médicos**: PDFs, imágenes (JPG, PNG) de incapacidades
- ✅ **Epicrisis**: Documentos de epicrisis
- ✅ **FURIPS**: Formularios FURIPS
- ✅ **Certificados**: Certificados médicos y otros documentos

### Configuración
Definido en `config/config.py`:
```python
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
```

---

## 🔐 Credenciales de Firebase

### Ubicación
```
incapacidades_system/
└── config/
    └── firebase-credentials.json  ← Credenciales del servidor
```

**Ruta completa:**
```
C:\Users\andre\Desktop\Ing soft\Sistema-Incapacidades\incapacidades_system\config\firebase-credentials.json
```

### ¿Qué contiene?
- Credenciales de Firebase Admin SDK para verificar tokens de autenticación
- **⚠️ IMPORTANTE:** Este archivo NO debe subirse a Git (está en .gitignore)

---

## 📊 Resumen de Ubicaciones

| Tipo de Dato | Ubicación | Archivo/Carpeta |
|--------------|-----------|-----------------|
| **Base de Datos** | `instance/` | `incapacidades.db` |
| **Documentos** | `uploads/` | Varios archivos PDF/JPG/PNG |
| **Firebase Creds** | `config/` | `firebase-credentials.json` |
| **Configuración** | `config/` | `config.py` |

---

## 💾 Respaldo de Datos

### Para respaldar todo el sistema:

1. **Base de datos:**
   ```bash
   # Copiar el archivo
   copy instance\incapacidades.db backups\incapacidades_backup_YYYYMMDD.db
   ```

2. **Documentos:**
   ```bash
   # Copiar toda la carpeta
   xcopy uploads backups\uploads_backup_YYYYMMDD /E /I
   ```

3. **Configuración:**
   ```bash
   # Copiar archivos de configuración
   copy config\firebase-credentials.json backups\
   ```

---

## 🔄 Cambiar a MySQL (Producción)

Si quieres usar MySQL en lugar de SQLite:

1. Edita `config/config.py`:
   ```python
   # Comentar SQLite:
   # SQLALCHEMY_DATABASE_URI = "sqlite:///incapacidades.db"
   
   # Descomentar MySQL:
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://usuario:contraseña@localhost/incapacidades_db"
   ```

2. Los datos se guardarán en el servidor MySQL en lugar del archivo local.

---

## 📝 Notas Importantes

- ✅ **SQLite** es perfecto para desarrollo (un solo archivo, fácil de respaldar)
- ✅ **MySQL** es mejor para producción (mejor rendimiento, múltiples usuarios)
- ⚠️ El archivo `.db` puede crecer con el tiempo, respáldalo regularmente
- ⚠️ Los archivos en `uploads/` también ocupan espacio, considera limpiar archivos antiguos
- 🔒 Las credenciales de Firebase son sensibles, no las compartas

---

## 🛠️ Ver el Contenido de la Base de Datos

Puedes usar herramientas como:
- **DB Browser for SQLite** (gratis): https://sqlitebrowser.org/
- **SQLiteStudio** (gratis): https://sqlitestudio.pl/
- **VS Code Extension**: SQLite Viewer

Simplemente abre el archivo `instance/incapacidades.db` con cualquiera de estas herramientas.

