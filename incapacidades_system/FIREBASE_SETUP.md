# Configuración de Firebase para Autenticación con Google

Esta guía te ayudará a configurar Firebase para habilitar el login con Google en el sistema.

## Paso 1: Crear un Proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Haz clic en "Agregar proyecto" o selecciona un proyecto existente
3. Sigue los pasos para crear el proyecto

## Paso 2: Habilitar Autenticación con Google

1. En el panel de Firebase, ve a **Authentication** (Autenticación)
2. Haz clic en **Get Started** (Comenzar)
3. Ve a la pestaña **Sign-in method** (Método de inicio de sesión)
4. Haz clic en **Google**
5. Activa el toggle y configura:
   - **Support email**: Tu correo de soporte
   - **Project support email**: El correo del proyecto
6. Haz clic en **Save** (Guardar)

## Paso 3: Obtener las Credenciales del Cliente (Frontend)

1. En Firebase Console, ve a **Project Settings** (Configuración del proyecto)
2. Desplázate hasta **Your apps** (Tus aplicaciones)
3. Haz clic en el ícono de **Web** (`</>`)
4. Registra tu app con un nombre (ej: "Sistema Incapacidades Web")
5. Copia las credenciales que aparecen:

```javascript
const firebaseConfig = {
  apiKey: "TU_API_KEY",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};
```

## Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto o configura las variables de entorno:

```bash
FIREBASE_API_KEY=tu_api_key
FIREBASE_AUTH_DOMAIN=tu-proyecto.firebaseapp.com
FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_STORAGE_BUCKET=tu-proyecto.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abcdef
```

**O** edita directamente `config/config.py` y reemplaza los valores vacíos:

```python
FIREBASE_API_KEY = 'tu_api_key'
FIREBASE_AUTH_DOMAIN = 'tu-proyecto.firebaseapp.com'
# ... etc
```

## Paso 5: Obtener Credenciales del Servidor (Backend)

1. En Firebase Console, ve a **Project Settings** (Configuración del proyecto)
2. Ve a la pestaña **Service accounts** (Cuentas de servicio)
3. Haz clic en **Generate new private key** (Generar nueva clave privada)
4. Se descargará un archivo JSON
5. **Renombra** este archivo a `firebase-credentials.json`
6. **Mueve** el archivo a la carpeta `incapacidades_system/config/`

**Estructura esperada:**
```
incapacidades_system/
└── config/
    └── firebase-credentials.json  ← Aquí debe estar el archivo
```

## Paso 6: Configurar Dominios Autorizados

1. En Firebase Console, ve a **Authentication** > **Settings** (Configuración)
2. En **Authorized domains** (Dominios autorizados), agrega:
   - `localhost` (ya debería estar)
   - Tu dominio de producción (ej: `tudominio.com`)

## Paso 7: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará `firebase-admin` y `pyjwt`.

## Paso 8: Probar la Configuración

1. Inicia el servidor:
```bash
python app.py
```

2. Ve a `http://localhost:5000/auth/login`
3. Deberías ver el botón "Continuar con Google"
4. Haz clic y prueba el login con tu cuenta de Google

## Solución de Problemas

### Error: "Firebase no está configurado"
- Verifica que las variables de entorno estén configuradas
- O edita directamente `config/config.py`

### Error: "Archivo de credenciales no encontrado"
- Asegúrate de que `firebase-credentials.json` esté en `config/`
- Verifica que el archivo tenga el nombre correcto

### Error: "Token inválido"
- Verifica que el dominio esté autorizado en Firebase Console
- Asegúrate de que la autenticación con Google esté habilitada

### El botón de Google está deshabilitado
- Verifica la consola del navegador para ver errores
- Asegúrate de que las credenciales del frontend estén correctas

## Notas Importantes

- **Seguridad**: Nunca subas `firebase-credentials.json` a Git. Agrégalo a `.gitignore`
- **Producción**: Usa variables de entorno en producción, no hardcodees las credenciales
- **Roles**: Los usuarios que se registran con Google obtienen automáticamente el rol "Empleado"

## Archivos a Agregar a .gitignore

```
config/firebase-credentials.json
.env
```

