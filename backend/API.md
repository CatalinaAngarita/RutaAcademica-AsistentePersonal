# Documentación de la API REST

## Base URL
```
http://localhost:8000/api/
```

## Endpoints Disponibles

### Estudiantes

#### Listar estudiantes
```
GET /api/estudiantes/
```

#### Obtener estudiante por ID
```
GET /api/estudiantes/{id}/
```

#### Crear estudiante
```
POST /api/estudiantes/
Content-Type: application/json

{
    "codigo": "2024001",
    "carrera": "Ingeniería de Sistemas",
    "semestre_actual": 3,
    "username": "estudiante1",
    "email": "estudiante1@example.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

#### Obtener estadísticas del estudiante
```
GET /api/estudiantes/{id}/estadisticas/
```

**Respuesta:**
```json
{
    "estudiante": {...},
    "promedio_general": 15.5,
    "asistencia_promedio": 85.2,
    "total_notas": 10,
    "total_asistencias": 50
}
```

### Materias

#### Listar materias
```
GET /api/materias/
```

#### Obtener materia por ID
```
GET /api/materias/{id}/
```

#### Crear materia
```
POST /api/materias/
Content-Type: application/json

{
    "codigo": "MAT101",
    "nombre": "Matemáticas I",
    "creditos": 4,
    "descripcion": "Curso introductorio de matemáticas",
    "prerequisitos": [],
    "activa": true
}
```

#### Obtener prerequisitos de una materia
```
GET /api/materias/{id}/prerequisitos/
```

#### Obtener malla curricular (grafo)
```
GET /api/materias/malla_curricular/
```

**Respuesta:**
```json
{
    "nodos": [
        {"id": 1, "codigo": "MAT101", "nombre": "Matemáticas I", "creditos": 4}
    ],
    "aristas": [
        {"source": 1, "target": 2}
    ]
}
```

#### Verificar prerequisitos
```
POST /api/materias/verificar_prerequisitos/
Content-Type: application/json

{
    "materias": [2, 3],
    "materias_aprobadas": [1]
}
```

### Notas

#### Listar notas
```
GET /api/notas/?estudiante={id}&materia={id}
```

#### Crear nota
```
POST /api/notas/
Content-Type: application/json

{
    "estudiante": 1,
    "materia": 1,
    "valor": 15.5,
    "porcentaje": 30,
    "descripcion": "Parcial 1"
}
```

#### Obtener promedio de estudiante
```
GET /api/notas/promedio_estudiante/?estudiante={id}
```

#### Obtener promedio de materia
```
GET /api/notas/promedio_materia/?materia={id}
```

### Asistencias

#### Listar asistencias
```
GET /api/asistencias/?estudiante={id}&materia={id}
```

#### Crear asistencia
```
POST /api/asistencias/
Content-Type: application/json

{
    "estudiante": 1,
    "materia": 1,
    "fecha": "2024-01-15",
    "asistio": true,
    "justificada": false,
    "observaciones": ""
}
```

#### Obtener estadísticas de asistencia del estudiante
```
GET /api/asistencias/estadisticas_estudiante/?estudiante={id}
```

#### Obtener estadísticas de asistencia de la materia
```
GET /api/asistencias/estadisticas_materia/?materia={id}
```

### Alertas

#### Listar alertas
```
GET /api/alertas/?estudiante={id}&activa=true&leida=false
```

#### Crear alerta
```
POST /api/alertas/
Content-Type: application/json

{
    "estudiante": 1,
    "tipo": "warning",
    "titulo": "Asistencia baja",
    "mensaje": "Tu porcentaje de asistencia es bajo",
    "fecha_vencimiento": "2024-12-31T23:59:59Z",
    "activa": true
}
```

#### Marcar alerta como leída
```
POST /api/alertas/{id}/marcar_leida/
```

#### Generar alertas automáticas
```
POST /api/alertas/generar_automaticas/
Content-Type: application/json

{
    "estudiante": 1
}
```

## Tipos de Alertas

- `info`: Información general
- `warning`: Advertencia
- `danger`: Peligro/Riesgo alto
- `success`: Éxito/Logro

## Autenticación

Actualmente la API está configurada con `AllowAny` para desarrollo. Para producción, se recomienda implementar autenticación por tokens.

## Paginación

Las respuestas de listado están paginadas con 20 elementos por página. Puedes usar los parámetros `?page=2` para navegar.

## Ejemplos de Uso con cURL

### Crear un estudiante
```bash
curl -X POST http://localhost:8000/api/estudiantes/ \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "2024001",
    "carrera": "Ingeniería de Sistemas",
    "semestre_actual": 3,
    "username": "estudiante1",
    "email": "estudiante1@example.com",
    "password": "password123"
  }'
```

### Obtener estadísticas
```bash
curl http://localhost:8000/api/estudiantes/1/estadisticas/
```

### Crear una nota
```bash
curl -X POST http://localhost:8000/api/notas/ \
  -H "Content-Type: application/json" \
  -d '{
    "estudiante": 1,
    "materia": 1,
    "valor": 15.5,
    "porcentaje": 30,
    "descripcion": "Parcial 1"
  }'
```

## Notas Importantes

1. Todos los valores de notas están en escala 0-20
2. Los porcentajes deben sumar hasta 100% por materia
3. Las fechas deben estar en formato ISO 8601 (YYYY-MM-DD)
4. Los prerequisitos se manejan como relaciones many-to-many entre materias

