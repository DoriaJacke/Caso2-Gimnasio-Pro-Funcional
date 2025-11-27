# 📚 Documentación API - Gimnasio Pro Funcional

## 🚀 Acceso a Swagger UI

Una vez que el backend esté corriendo, puedes acceder a la documentación interactiva de Swagger en:

**URL:** http://127.0.0.1:5000/api/docs

## 📋 Características de Swagger

✅ **Interfaz interactiva** - Prueba los endpoints directamente desde el navegador  
✅ **Documentación automática** - Especificaciones OpenAPI 2.0  
✅ **Ejemplos de requests/responses** - Ver formato esperado de datos  
✅ **Filtros por tags** - Endpoints organizados por categorías  
✅ **Modelos de datos** - Schemas de entrada y salida  

## 🏷️ Tags de Endpoints

### Autenticación
- `POST /api/registro` - Registro de nuevos usuarios
- `POST /api/login` - Login de usuarios (cliente, entrenador, admin)
- `POST /api/admin/login` - Login específico para administradores

### Usuarios
- `GET /api/usuarios/<user_id>` - Obtener información de usuario
- `PUT /api/usuarios/<user_id>` - Actualizar información de usuario

### Reservas
- `GET /api/reservas/<user_id>` - Obtener reservas activas de un usuario
- `POST /api/reservas` - Crear nueva reserva (con pago Webpay)
- `DELETE /api/reservas/<reserva_id>` - Cancelar reserva
- `POST /api/reservas/<reserva_id>/reagendar` - Reagendar una reserva existente

### Bloques
- `GET /api/bloques` - Listar bloques horarios (con filtros opcionales)
- `POST /api/bloques` - Crear nuevo bloque horario
- `DELETE /api/bloques/<bloque_id>` - Eliminar bloque horario

### Entrenadores
- `GET /api/entrenadores` - Listar todos los entrenadores
- `PUT /api/entrenadores/<entrenador_id>` - Actualizar especialidad
- `GET /api/entrenador/<nombre>/alumnos` - Ver alumnos de un entrenador

### Cupos
- `GET /api/cupos/disponibles` - Obtener cupos disponibles a futuro

### Pagos (Webpay Plus)
- `POST /api/iniciar-pago` - Iniciar transacción de pago
- `GET /api/confirmar-pago` - Confirmar pago después de redirección
- `GET /api/transaccion/<reserva_id>` - Obtener estado de transacción

## 🔧 Cómo usar Swagger UI

### 1. Iniciar el Backend
```bash
python backend.py
```

### 2. Abrir Swagger UI
Navega a: http://127.0.0.1:5000/api/docs

### 3. Probar un Endpoint

#### Ejemplo: Registro de Usuario

1. Click en `POST /api/registro` bajo el tag **Autenticación**
2. Click en **"Try it out"**
3. Modifica el JSON de ejemplo:
```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan.perez@gmail.com",
  "telefono": "912345678",
  "username": "juanperez",
  "password": "password123",
  "fecha_nacimiento": "1990-01-15",
  "role": "cliente"
}
```
4. Click en **"Execute"**
5. Ver respuesta en la sección **"Server response"**

#### Ejemplo: Listar Entrenadores

1. Click en `GET /api/entrenadores` bajo el tag **Entrenadores**
2. Click en **"Try it out"**
3. Click en **"Execute"**
4. Ver lista de entrenadores en la respuesta

#### Ejemplo: Filtrar Bloques por Fecha

1. Click en `GET /api/bloques` bajo el tag **Bloques**
2. Click en **"Try it out"**
3. Ingresar parámetros opcionales:
   - `fecha`: 2025-11-27
   - `actividad`: Cardio
4. Click en **"Execute"**

## 📊 Especificación OpenAPI

La especificación completa en formato JSON está disponible en:

**URL:** http://127.0.0.1:5000/apispec.json

Puedes importar este JSON en herramientas como:
- Postman
- Insomnia
- Swagger Editor
- OpenAPI Generator

## 🎯 Filtros Disponibles

### GET /api/bloques
```
?fecha=2025-11-27          # Filtrar por fecha específica
?actividad=Cardio          # Filtrar por tipo de actividad
?entrenador=Ricardo%20Meruane  # Filtrar por entrenador
```

Combina múltiples filtros:
```
/api/bloques?fecha=2025-11-27&actividad=Fuerza&entrenador=George%20Harris
```

## 🔐 Autenticación

Actualmente la API **no requiere autenticación** para propósitos de desarrollo.

En producción se recomienda implementar:
- JWT (JSON Web Tokens)
- OAuth 2.0
- API Keys

## 📝 Modelos de Datos

### Usuario
```json
{
  "id": 1,
  "username": "juanperez",
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan.perez@gmail.com",
  "telefono": "912345678",
  "fecha_nacimiento": "1990-01-15",
  "rol": "cliente",
  "fecha_registro": "2025-11-27T10:00:00"
}
```

### Bloque Horario
```json
{
  "id": 1,
  "actividad": "Cardio",
  "fecha": "2025-11-27",
  "hora": "10:00:00",
  "entrenador_id": 1,
  "nombre_entrenador": "Ricardo Meruane",
  "cupos_totales": 10,
  "cupos_disponibles": 8
}
```

### Reserva
```json
{
  "id": 1,
  "usuario_id": 5,
  "actividad": "Fuerza",
  "fecha": "2025-11-28",
  "hora": "15:00:00",
  "entrenador_id": 2,
  "nombre_entrenador": "George Harris",
  "estado": "activa"
}
```

### Entrenador
```json
{
  "id": 1,
  "nombre": "Ricardo Meruane",
  "especialidad": "Entrenamiento Funcional",
  "fecha_registro": "2025-11-24T20:53:10"
}
```

## 🛠️ Extensiones Recomendadas

Para desarrollo, instala estas extensiones de VS Code:
- **Swagger Viewer** - Previsualizar specs OpenAPI
- **REST Client** - Probar APIs sin salir de VS Code
- **Thunder Client** - Cliente API integrado

## 📱 Integración con Frontend

Desde tu aplicación frontend (JavaScript), puedes consumir la API así:

```javascript
// Registro de usuario
const response = await fetch('http://127.0.0.1:5000/api/registro', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: "Juan",
    apellido: "Pérez",
    email: "juan@example.com",
    telefono: "912345678",
    username: "juanperez",
    password: "pass123",
    fecha_nacimiento: "1990-01-15",
    role: "cliente"
  })
});
const data = await response.json();
console.log(data);
```

## 🔄 Versionamiento

Actualmente en **v1.0.0**

Futuros cambios breaking se publicarán en versiones mayores (v2.0.0, v3.0.0, etc.)

## 📞 Soporte

Para reportar problemas con la API:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo

---

**Última actualización:** 27 de Noviembre, 2025
