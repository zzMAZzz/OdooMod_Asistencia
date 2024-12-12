# API para la Gestion de la Asistencia, usando Odoo.

Este repositorio contiene los controladores personalizado para gestionar CRUD (Crear, Leer, Actualizar y Eliminar) de Estudiante, Docente, Clase y Asistencia dentro de un sistema basado en Odoo.

Está diseñado para interactuar con los modelos `school.class`, `school.attendance`, `school.docent` y `school.student`.

## Requisitos Previos

Antes de utilizar este módulo, asegúrate de que:

- Tienes una instalación funcional de Odoo.
- Los modelos `school.class`, `school.attendance`, `school.docent` y `school.student` están correctamente definidos.
- Estás autenticado como usuario para acceder a las rutas protegidas. 

## Instalación

1. Copia el módulo en la carpeta `addons` de tu instalación de Odoo.
2. Activa el modo desarrollador en Odoo.
3. Ve a **Apps** y actualiza la lista de aplicaciones.
4. Busca el módulo `RestAPI` y `Students Management`  y haz click en instalar.

### Inicia Sesión en Odoo
**Ruta:** `/web/session/authenticate`  
**Método:** `POST`

**Cuerpo del JSON:**
```json
{
    "jsonrpc": "2.0",
    "params":{
        "db": "prueba12",
        "login": "prueba12@gmail.com"
        "password": "hola123"
        }
}
```

## Rutas Disponibles
### Endpoint: Subida de Archivo

#### URL
`/upload/class_students`

#### Método
`POST`

#### Autenticación
Requiere un usuario autenticado con permisos adecuados.

#### Parámetros
- **xlsx**: Archivo Excel que contiene la información de los estudiantes.
- **class_id**: ID de la clase a la que se asociarán los estudiantes.

### Estructura del Archivo Excel
El archivo debe contener las siguientes columnas:
- `Nombre`: Nombre del estudiante (requerido).
- `Email`: Correo electrónico del estudiante (requerido y único).
- `Cuenta`: Número de cuenta del estudiante (requerido).
- `Edad`: Edad del estudiante (opcional).
- `Genero`: Género del estudiante (`M` para masculino, `F` para femenino; opcional).

### Respuestas
#### Éxito
```json
{
    "status": "success",
    "message": "Archivo procesado exitosamente.",
    "created": 5,
    "updated": 2
}
```

#### Error
- Si no se proporciona un archivo o el ID de la clase:
```json
{
    "status": "error",
    "message": "No se proporcionó un archivo Excel o el ID de la clase."
}
```

- Si el archivo no tiene el formato correcto:
```json
{
    "status": "error",
    "message": "Formato no válido. Solo se aceptan archivos .xlsx o .xls."
}
```

- Si el ID de la clase no existe:
```json
{
    "status": "error",
    "message": "No existe una clase con el ID 1."
}
```

- Si ocurre un error inesperado:
```json
{
    "status": "error",
    "message": "Error procesando el archivo: <mensaje_de_error>."
}
```

### Funcionalidades

1. **Creación de estudiantes**:
   - Si el correo electrónico no existe en el sistema, se crea un nuevo registro.

2. **Actualización de estudiantes existentes**:
   - Si el correo electrónico ya existe, se actualizan los datos del estudiante.

3. **Asociación con clases**:
   - Los estudiantes se añaden a la clase especificada mediante su `class_id`.

4. **Mapeo de géneros**:
   - Los valores `M` y `F` se convierten a `male` y `female`, respectivamente.### Crear un Estudiante

- **URL:** `/api/student/create`
- **Método:** `POST`
- **Autenticación:** Requerida (`auth='user'`)
- **Descripción:** Crea un nuevo estudiante.

#### Parámetros de Entrada (JSON):
```json
{
  "name": "Nombre del estudiante",
  "cuenta": "2020001234",
  "email": "ejemplo@unah.hn",
  "age": 20,
  "gender": "male"
}
```

#### Respuesta Exitosa:
```json
{
  "success": true,
  "student_id": 1
}
```

### Obtener Información de un Estudiante

- **URL:** `/api/student/<int:student_id>`
- **Método:** `GET`
- **Autenticación:** No requerida (`auth='public'`)
- **Descripción:** Obtiene los detalles de un estudiante por su ID.

#### Respuesta Exitosa:
```json
{
  "student": {
    "id": 1,
    "name": "Nombre del estudiante",
    "cuenta": "2020001234",
    "email": "ejemplo@unah.hn",
    "age": 20,
    "gender": "male"
  }
}
```

### Actualizar un Estudiante

- **URL:** `/api/student/update/<int:student_id>`
- **Método:** `PUT`
- **Autenticación:** Requerida (`auth='user'`)
- **Descripción:** Actualiza los datos de un estudiante existente.

#### Parámetros de Entrada (JSON):
```json
{
  "name": "Nuevo nombre del estudiante",
  "age": 21
}
```

#### Respuesta Exitosa:
```json
{
  "success": true,
  "student_id": 1
}
```

### Eliminar un Estudiante

- **URL:** `/api/student/delete/<int:student_id>`
- **Método:** `DELETE`
- **Autenticación:** Requerida (`auth='user'`)
- **Descripción:** Elimina un estudiante existente por su ID.

#### Respuesta Exitosa:
```json
{
  "success": true,
  "message": "Estudiante eliminado."
}
```

### Manejo de Errores

Todas las respuestas de error tienen el siguiente formato:
```json
{
  "error": "Mensaje de error descriptivo."
}
```

### Ejemplos de Errores:
1. **Estudiante no encontrado:**
   ```json
   {
     "error": "Estudiante no encontrado."
   }
   ```
2. **Faltan campos obligatorios:**
   ```json
   {
     "error": "Faltan campos obligatorios: 'name', 'age', 'grade'."
   }
   ```
   ### Crear Docente

**URL:** `/api/docent/create`  
**Método:** `POST`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "name": "Nombre del Docente",
  "email": "correo@ejemplo.com",
  "phone": "123456789",
  "subject_ids": [1, 2, 3],
  "active": true
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "docent_id": 1
}
```

### Leer Docente

**URL:** `/api/docent/<int:docent_id>`  
**Método:** `GET`  

**Respuesta Exitosa:**
```json
{
  "docent": {
    "id": 1,
    "name": "Nombre del Docente",
    "email": "correo@ejemplo.com",
    "phone": "123456789",
    "subject_ids": [1, 2, 3],
    "active": true
  }
}
```

### Actualizar Docente

**URL:** `/api/docent/update/<int:docent_id>`  
**Método:** `PUT`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "name": "Nuevo Nombre",
  "email": "nuevo@correo.com",
  "phone": "987654321",
  "subject_ids": [2, 4],
  "active": false
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "docent_id": 1
}
```

### Eliminar Docente

**URL:** `/api/docent/delete/<int:docent_id>`  
**Método:** `DELETE`

**Respuesta Exitosa:**
```json
{
  "success": true,
  "message": "Docente eliminado."
}
```
### Crear Clase

**URL:** `/api/class/create`  
**Método:** `POST`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "name": "Nombre de la Clase",
  "code": "CL001",
  "section": "A",
  "hour": "08:00",
  "year": 2024,
  "period": "1",
  "docent_id": 1,
  "student_ids": [1, 2, 3],
  "active": true
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "class_id": 1
}
```

### Leer Clase

**URL:** `/api/class/<int:class_id>`  
**Método:** `GET`  

**Respuesta Exitosa:**
```json
{
  "class": {
    "id": 1,
    "name": "Nombre de la Clase",
    "code": "CL001",
    "section": "A",
    "hour": "08:00",
    "year": 2024,
    "period": "1",
    "docent_id": 1,
    "student_ids": [1, 2, 3],
    "active": true
  }
}
```

### Actualizar Clase

**URL:** `/api/class/update/<int:class_id>`  
**Método:** `PUT`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "name": "Nuevo Nombre",
  "hour": "10:00",
  "active": false
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "class_id": 1
}
```

### Eliminar Clase

**URL:** `/api/class/delete/<int:class_id>`  
**Método:** `DELETE`  

**Respuesta Exitosa:**
```json
{
  "success": true,
  "message": "Clase eliminada."
}
```
### Crear Asistencia

**URL:** `/api/attendance/create`  
**Método:** `POST`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "date": "2024-12-11",
  "class_id": 1,
  "student_id": 42,
  "status": "present"
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "attendance_id": 1
}
```

### Leer Asistencia

**URL:** `/api/attendance/<int:attendance_id>`  
**Método:** `GET`  

**Respuesta Exitosa:**
```json
{
  "attendance": {
    "id": 1,
    "date": "2024-12-11",
    "class_id": 1,
    "student_id": 42,
    "status": "present"
  }
}
```

### Actualizar Asistencia

**URL:** `/api/attendance/update/<int:attendance_id>`  
**Método:** `PUT`  
**Headers:** `Content-Type: application/json`  

**Cuerpo del JSON:**
```json
{
  "date": "2024-12-12",
  "status": "absent"
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "attendance_id": 1
}
```

### Eliminar Asistencia

**URL:** `/api/attendance/delete/<int:attendance_id>`  
**Método:** `DELETE`

**Respuesta Exitosa:**
```json
{
  "success": true
}
```
