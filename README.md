# Ruta Académica – Asistente Personal

## 📚 Descripción del Proyecto

Plataforma web móvil desarrollada con Django para que los estudiantes gestionen su vida académica. Permite planificar la carrera, registrar notas y asistencias, y recibir alertas personalizadas.

## 🎯 Objetivo Personal

Crear una herramienta integral que ayude a los estudiantes a:
- Planificar su carrera académica
- Registrar y gestionar notas y asistencias
- Recibir alertas personalizadas sobre su rendimiento
- Visualizar su progreso académico

## 🧠 Conceptos Aplicados

### ➤ Grafos
Modelado de la malla curricular y prerequisitos usando la librería `networkx`.

### ➤ Probabilidad
Estimación del riesgo de reprobación basada en datos históricos.

### ➤ Variables
Notas, asistencias, créditos y ponderados como datos clave del sistema.

## 🛠️ Herramientas y Tecnologías

### Backend
- **Python 3**
- **Django** - Framework web
- **PostgreSQL** - Base de datos
- **Django REST Framework** - API REST

### Librerías Python
- **networkx** - Para modelado de grafos (malla curricular)
- **numpy** - Cálculos numéricos y estadísticos

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**
- **Chart.js** - Visualización de datos

## 📁 Estructura del Proyecto

```
RutaAcademica-AsistentePersonal/
├── backend/              # Aplicación Django
│   ├── apps/            # Apps del proyecto
│   │   ├── estudiantes/  # Gestión de estudiantes
│   │   ├── materias/    # Gestión de materias
│   │   ├── notas/       # Gestión de notas
│   │   ├── asistencias/ # Gestión de asistencias
│   │   └── alertas/     # Sistema de alertas
│   ├── core/            # Configuración principal
│   ├── manage.py
│   └── requirements.txt
├── frontend/            # Interfaz de usuario
│   ├── css/
│   ├── js/
│   └── index.html
├── docs/                # Documentación
└── README.md
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd RutaAcademica-AsistentePersonal
```

2. **Configurar el entorno virtual**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Ejecutar el servidor de desarrollo**
```bash
python manage.py runserver
```

## 📖 Documentación

La documentación detallada del proyecto se encuentra en la carpeta `docs/`.

## 👥 Contribución

Este es un proyecto personal de aprendizaje. Las contribuciones son bienvenidas.

## 📝 Licencia

Este proyecto es de uso educativo y personal.

