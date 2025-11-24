# Documentación del Proyecto

## 📋 Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Modelado de Grafos](#modelado-de-grafos)
3. [Sistema de Probabilidades](#sistema-de-probabilidades)
4. [API REST](#api-rest)
5. [Frontend](#frontend)
6. [Base de Datos](#base-de-datos)

## 🏗️ Arquitectura del Sistema

### Backend (Django)

El backend está estructurado en aplicaciones Django:

- **estudiantes**: Gestión de estudiantes y perfiles
- **materias**: Gestión de materias y malla curricular
- **notas**: Registro y cálculo de notas
- **asistencias**: Registro de asistencias
- **alertas**: Sistema de alertas personalizadas

### Frontend

Interfaz web responsive desarrollada con HTML, CSS y JavaScript vanilla, utilizando Chart.js para visualización de datos.

## 📊 Modelado de Grafos

### Malla Curricular

La malla curricular se modela como un grafo dirigido usando `networkx`, donde:

- **Nodos**: Representan las materias
- **Aristas**: Representan los prerequisitos (si la materia A es prerequisito de B, existe una arista de A a B)

### Ejemplo de Uso

```python
import networkx as nx

# Crear grafo dirigido
G = nx.DiGraph()

# Agregar materias (nodos)
G.add_node("Matemáticas I")
G.add_node("Matemáticas II")
G.add_node("Programación I")

# Agregar prerequisitos (aristas)
G.add_edge("Matemáticas I", "Matemáticas II")
G.add_edge("Matemáticas I", "Programación I")

# Verificar si una materia puede ser cursada
def puede_cursar(materia, materias_aprobadas):
    prerequisitos = list(G.predecessors(materia))
    return all(prereq in materias_aprobadas for prereq in prerequisitos)
```

## 🎲 Sistema de Probabilidades

### Estimación de Riesgo de Reprobación

El sistema calcula la probabilidad de reprobación basándose en:

1. **Notas históricas**: Promedio de notas anteriores
2. **Asistencias**: Porcentaje de asistencia actual
3. **Tendencia**: Análisis de tendencia de notas

### Fórmula de Cálculo

```
P(reprobación) = f(nota_actual, asistencia, historial)
```

Donde:
- `nota_actual`: Promedio actual de la materia
- `asistencia`: Porcentaje de asistencia
- `historial`: Promedio histórico del estudiante

## 🔌 API REST

### Endpoints Principales

#### Estudiantes
- `GET /api/estudiantes/` - Listar estudiantes
- `POST /api/estudiantes/` - Crear estudiante
- `GET /api/estudiantes/{id}/` - Detalle de estudiante

#### Materias
- `GET /api/materias/` - Listar materias
- `GET /api/materias/{id}/` - Detalle de materia
- `GET /api/materias/{id}/prerequisitos/` - Ver prerequisitos

#### Notas
- `GET /api/notas/` - Listar notas
- `POST /api/notas/` - Crear nota
- `GET /api/notas/{id}/` - Detalle de nota

#### Asistencias
- `GET /api/asistencias/` - Listar asistencias
- `POST /api/asistencias/` - Registrar asistencia

#### Alertas
- `GET /api/alertas/` - Listar alertas del estudiante
- `POST /api/alertas/` - Crear alerta

## 🎨 Frontend

### Estructura de Archivos

```
frontend/
├── index.html      # Página principal
├── css/
│   └── styles.css  # Estilos principales
└── js/
    └── app.js      # Lógica de la aplicación
```

### Funcionalidades

1. **Dashboard**: Vista general con estadísticas
2. **Materias**: Visualización de malla curricular
3. **Notas**: Registro y visualización de notas
4. **Asistencias**: Registro de asistencias
5. **Alertas**: Sistema de notificaciones

## 🗄️ Base de Datos

### Modelos Principales

#### Estudiante
- id
- nombre
- email
- carrera
- semestre_actual

#### Materia
- id
- nombre
- codigo
- creditos
- prerequisitos (relación many-to-many)

#### Nota
- id
- estudiante (FK)
- materia (FK)
- valor
- porcentaje
- fecha

#### Asistencia
- id
- estudiante (FK)
- materia (FK)
- fecha
- asistio (boolean)

#### Alerta
- id
- estudiante (FK)
- tipo
- titulo
- mensaje
- fecha_creacion
- activa (boolean)

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del backend:

```
SECRET_KEY=tu-secret-key
DEBUG=True
DATABASE_URL=postgresql://usuario:password@localhost:5432/ruta_academica
```

## 📚 Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [NetworkX Documentation](https://networkx.org/)
- [Chart.js Documentation](https://www.chartjs.org/)

