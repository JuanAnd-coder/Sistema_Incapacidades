# Configurar Dominios Autorizados en Firebase

## Error: "This domain is not authorized for OAuth operations"

Si recibes este error, significa que el dominio desde el cual estás intentando autenticarte no está autorizado en tu proyecto de Firebase.

## Solución: Agregar Dominio Autorizado

### Paso 1: Ir a Firebase Console

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto: **incapacidades-system**

### Paso 2: Ir a Configuración de Autenticación

1. En el menú lateral, haz clic en **Authentication** (Autenticación)
2. Ve a la pestaña **Settings** (Configuración)
3. Desplázate hasta la sección **Authorized domains** (Dominios autorizados)

### Paso 3: Agregar Dominios

Debes agregar los siguientes dominios según donde estés ejecutando la aplicación:

#### Para Desarrollo Local:
- `localhost` (ya debería estar por defecto)
- `127.0.0.1` (si accedes por IP)

#### Para Producción:
- Tu dominio de producción (ej: `tudominio.com`)
- `www.tudominio.com` (si usas www)

### Paso 4: Guardar

1. Haz clic en **Add domain** (Agregar dominio)
2. Ingresa el dominio (ej: `localhost` o `127.0.0.1`)
3. Haz clic en **Add** (Agregar)
4. Espera unos segundos para que los cambios se apliquen

## Dominios Comunes para Desarrollo

Si estás desarrollando localmente, agrega:
- `localhost`
- `127.0.0.1`
- `localhost:5000` (si Firebase lo requiere)

## Verificar que Funciona

1. Recarga la página de login
2. Intenta iniciar sesión con Google nuevamente
3. El error debería desaparecer

## Nota Importante

- Los cambios pueden tardar unos minutos en aplicarse
- Asegúrate de que el dominio coincida exactamente (incluyendo el puerto si es necesario)
- No uses `http://` o `https://` al agregar el dominio, solo el nombre del dominio

## Ejemplo Visual

```
Authorized domains:
├── localhost ✅
├── 127.0.0.1 ✅
└── tudominio.com ✅ (para producción)
```

## Solución Rápida

Si estás en desarrollo local y el error persiste:

1. Verifica que `localhost` esté en la lista
2. Si no está, agrégalo manualmente
3. Espera 1-2 minutos
4. Recarga la página y prueba de nuevo

