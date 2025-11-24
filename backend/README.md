# Backend - Ruta Académica

## Descripción

Backend desarrollado con Django y Django REST Framework para la plataforma Ruta Académica.

## Estructura

```
backend/
├── apps/                 # Aplicaciones Django
│   ├── estudiantes/      # Gestión de estudiantes
│   ├── materias/         # Gestión de materias
│   ├── notas/            # Gestión de notas
│   ├── asistencias/      # Gestión de asistencias
│   └── alertas/          # Sistema de alertas
├── core/                 # Configuración principal
│   ├── settings.py       # Configuración del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── manage.py             # Script de administración
├── requirements.txt      # Dependencias Python
└── .env.example          # Ejemplo de variables de entorno
```

## Aplicaciones

### estudiantes
Gestión de estudiantes y perfiles académicos.

### materias
Gestión de materias, malla curricular y prerequisitos usando grafos (networkx).

### notas
Registro y cálculo de notas, promedios y ponderados.

### asistencias
Registro y seguimiento de asistencias.

### alertas
Sistema de alertas personalizadas basado en probabilidades y análisis de riesgo.

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. Ejecutar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor:
```bash
python manage.py runserver
```

## Dependencias Principales

- **Django 5.2.8**: Framework web
- **Django REST Framework 3.16.1**: API REST
- **psycopg2-binary 2.9.9**: Driver de PostgreSQL
- **networkx 3.2.1**: Modelado de grafos
- **numpy 1.26.4**: Cálculos numéricos

## API REST

La API está disponible en `/api/` y utiliza Django REST Framework.

### Endpoints Principales

- `/api/estudiantes/` - Gestión de estudiantes
- `/api/materias/` - Gestión de materias
- `/api/notas/` - Gestión de notas
- `/api/asistencias/` - Gestión de asistencias
- `/api/alertas/` - Gestión de alertas

Para documentación detallada de la API, ver [API.md](API.md)

## Modelado de Grafos

La malla curricular se modela usando `networkx` como un grafo dirigido donde:
- Los nodos representan materias
- Las aristas representan prerequisitos

## Base de Datos

El proyecto utiliza PostgreSQL como base de datos principal. Configurar la conexión en `settings.py` o mediante variables de entorno.

## Desarrollo

### Crear una nueva aplicación

```bash
python manage.py startapp nombre_app
```

### Crear migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar tests

```bash
python manage.py test
```

## Características Implementadas

### Modelos de Datos
- **Estudiante**: Perfiles de estudiantes con información académica
- **Materia**: Materias con prerequisitos (relaciones many-to-many)
- **Nota**: Registro de notas con valores y porcentajes
- **Asistencia**: Registro de asistencias por materia
- **Alerta**: Sistema de alertas personalizadas

### Funcionalidades Especiales

#### Grafos (NetworkX)
- Modelado de malla curricular como grafo dirigido
- Verificación de prerequisitos
- Ordenamiento topológico para ruta académica
- Endpoint `/api/materias/malla_curricular/` para obtener el grafo completo

#### Probabilidades
- Cálculo de riesgo de reprobación basado en:
  - Promedio de notas actuales
  - Porcentaje de asistencia
  - Análisis estadístico
- Generación automática de alertas según el riesgo

#### Estadísticas
- Promedios generales y por materia
- Porcentajes de asistencia
- Dashboard con métricas clave

## Documentación

- **API REST**: Ver [API.md](API.md) para documentación completa de endpoints
- **Proyecto**: Ver la carpeta `../docs/` para documentación detallada del proyecto

