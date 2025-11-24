# Arquitectura del Sistema

## Visión General

Ruta Académica es una plataforma web que utiliza una arquitectura cliente-servidor con separación entre frontend y backend.

## Componentes Principales

### Backend (Django)

```
backend/
├── core/              # Configuración principal de Django
│   ├── settings.py    # Configuración del proyecto
│   ├── urls.py        # URLs principales
│   └── wsgi.py        # Configuración WSGI
├── apps/              # Aplicaciones Django
│   ├── estudiantes/   # Gestión de estudiantes
│   ├── materias/      # Gestión de materias y malla curricular
│   ├── notas/         # Gestión de notas
│   ├── asistencias/   # Gestión de asistencias
│   └── alertas/       # Sistema de alertas
└── manage.py          # Script de administración
```

### Frontend

```
frontend/
├── index.html         # Página principal
├── css/
│   └── styles.css     # Estilos
└── js/
    └── app.js         # Lógica del cliente
```

## Flujo de Datos

```
Usuario → Frontend (HTML/CSS/JS) → API REST (Django) → Base de Datos (PostgreSQL)
```

## Modelado de Datos

### Grafos (NetworkX)

La malla curricular se modela como un grafo dirigido:

- **Nodos**: Materias
- **Aristas**: Prerequisitos
- **Algoritmos**: Búsqueda de ruta académica, verificación de prerequisitos

### Probabilidades

Sistema de estimación de riesgo basado en:
- Análisis estadístico de notas históricas
- Porcentaje de asistencia
- Tendencias de rendimiento

## API REST

### Estructura de Endpoints

```
/api/
├── estudiantes/       # CRUD de estudiantes
├── materias/          # CRUD de materias
├── notas/             # CRUD de notas
├── asistencias/       # CRUD de asistencias
└── alertas/           # Gestión de alertas
```

### Autenticación

- Token-based authentication (Django REST Framework)
- Sesiones para el panel de administración

## Base de Datos

### Esquema Relacional

```
Estudiante (1) ──< (N) Nota
Estudiante (1) ──< (N) Asistencia
Estudiante (1) ──< (N) Alerta
Materia (1) ──< (N) Nota
Materia (1) ──< (N) Asistencia
Materia (N) ──< (N) Materia (prerequisitos)
```

## Seguridad

- CSRF protection
- SQL injection prevention (ORM de Django)
- XSS protection
- Validación de datos en frontend y backend

## Escalabilidad

- Separación de concerns (frontend/backend)
- API REST permite múltiples clientes
- Base de datos relacional para integridad de datos
- Caché para consultas frecuentes (futuro)

