# Permisos y Funcionalidades por Rol

Este documento describe qué puede hacer cada rol en el sistema de gestión de incapacidades.

## 🔐 Roles Disponibles

1. **Administrador**
2. **Empleado**
3. **Revisor**
4. **Médico**

---

## 👨‍💼 Administrador

**Acceso completo al sistema**

### Funcionalidades:
- ✅ **Gestión de Usuarios**: Crear, editar y eliminar usuarios del sistema
- ✅ **Gestión de Empleados**: Administrar información de todos los empleados
- ✅ **Gestión de Médicos**: Crear, editar y eliminar médicos
- ✅ **Ver Todas las Incapacidades**: Acceso a todas las incapacidades registradas
- ✅ **Registrar Incapacidades**: Puede registrar incapacidades para cualquier empleado
- ✅ **Cambiar Estados**: Puede cambiar el estado de cualquier incapacidad
- ✅ **Transcribir Incapacidades**: Puede marcar incapacidades como "Transcrita"
- ✅ **Reportes y Estadísticas**: Acceso completo a reportes del sistema
- ✅ **Eliminar Empleados**: Solo el administrador puede eliminar empleados

### Rutas Accesibles:
- `/admin/dashboard` - Dashboard principal
- `/usuarios` - Gestión de usuarios
- `/empleados` - Gestión de empleados
- `/medicos` - Gestión de médicos
- `/` - Lista de incapacidades
- `/nuevo` - Registrar nueva incapacidad
- `/ver/<id>` - Ver detalle de incapacidad
- `/transcribir/<id>` - Cambiar estado a "Transcrita"

---

## 👤 Empleado

**Rol principal para registrar incapacidades - El empleado es quien registra su propia incapacidad**

### Funcionalidades:
- ✅ **Registrar Incapacidades**: **PRINCIPAL** - Puede registrar sus propias incapacidades cuando tiene un accidente, enfermedad o necesita licencia médica
- ✅ **Ver Sus Incapacidades**: Ver el estado de sus incapacidades registradas
- ✅ **Subir Documentos**: Subir documentos relacionados con sus incapacidades (certificados médicos, epicrisis, etc.)
- ✅ **Ver Historial**: Consultar su historial de incapacidades
- ❌ **NO puede** ver incapacidades de otros empleados
- ❌ **NO puede** cambiar estados de incapacidades (solo Revisores y Administradores)
- ❌ **NO puede** gestionar usuarios, empleados o médicos

### Flujo de Trabajo:
1. El **Empleado** registra su incapacidad con los documentos médicos
2. El **Revisor** revisa y valida la documentación
3. El **Médico** valida los aspectos médicos si es necesario
4. El sistema cambia el estado según el proceso de revisión

### Rutas Accesibles:
- `/empleados/dashboard` - Dashboard principal
- `/nuevo` - Registrar nueva incapacidad
- `/` - Ver sus incapacidades (filtradas)
- `/ver/<id>` - Ver detalle de su incapacidad
- `/historial` - Ver historial personal

---

## ✅ Revisor

**Acceso para revisar y validar incapacidades registradas por empleados**

### Funcionalidades:
- ✅ **Revisar Incapacidades**: Ver todas las incapacidades registradas por los empleados
- ✅ **Validar Documentos**: Verificar que los documentos estén completos y correctos
- ✅ **Cambiar Estados**: Cambiar el estado de incapacidades (Transcrita, Aprobada, Rechazada)
- ✅ **Transcribir**: Marcar incapacidades como "Transcrita" cuando se procesan
- ✅ **Ver Reportes**: Acceso a reportes de revisión
- ❌ **NO puede** registrar incapacidades (solo los empleados registran sus propias incapacidades)
- ❌ **NO puede** gestionar usuarios, empleados o médicos
- ❌ **NO puede** eliminar incapacidades

### Rutas Accesibles:
- `/revisor/dashboard` - Dashboard principal
- `/` - Lista de incapacidades para revisar
- `/ver/<id>` - Ver detalle de incapacidad
- `/transcribir/<id>` - Cambiar estado a "Transcrita"

---

## 👨‍⚕️ Médico

**Acceso para gestionar información médica de incapacidades registradas por empleados**

### Funcionalidades:
- ✅ **Ver Incapacidades Asignadas**: Ver incapacidades que requieren revisión médica
- ✅ **Validar Documentos Médicos**: Validar documentos médicos de incapacidades registradas por empleados
- ✅ **Emitir Certificados**: Emitir certificados médicos cuando sea necesario
- ✅ **Revisar Información Médica**: Acceso a información médica de incapacidades
- ❌ **NO puede** registrar incapacidades (solo los empleados registran sus propias incapacidades)
- ❌ **NO puede** cambiar estados administrativos (solo Revisores y Administradores)
- ❌ **NO puede** gestionar usuarios, empleados o médicos

### Rutas Accesibles:
- `/medico/dashboard` - Dashboard principal
- `/` - Ver incapacidades asignadas
- `/ver/<id>` - Ver detalle de incapacidad con información médica

---

## 🔒 Protección de Rutas

Todas las rutas están protegidas con el decorador `@rol_required()` que verifica:
1. Que el usuario esté autenticado (tiene sesión activa)
2. Que el rol del usuario esté en la lista de roles permitidos

Si un usuario intenta acceder a una ruta sin permisos:
- Se muestra un mensaje de error
- Se redirige a la página de "No Autorizado" o al login

---

## 📝 Notas Importantes

- **Autenticación requerida**: Todas las funcionalidades requieren iniciar sesión
- **Sesión activa**: La sesión se mantiene mientras el navegador esté abierto
- **Cerrar sesión**: Disponible en el menú superior de todas las páginas
- **Seguridad**: Las contraseñas se almacenan con hash (no en texto plano)

---

## 🚀 Usuarios de Prueba

Para crear usuarios de prueba, ejecuta:
```bash
python create_users.py
```

Esto creará usuarios con los siguientes roles:
- **Administrador**: admin@empresa.com / admin123
- **Empleado**: empleado@empresa.com / empleado123
- **Revisor**: revisor@empresa.com / revisor123
- **Médico**: medico@empresa.com / medico123

