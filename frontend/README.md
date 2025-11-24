# Frontend - Ruta Académica

## Descripción

Interfaz de usuario para la plataforma Ruta Académica desarrollada con HTML, CSS y JavaScript vanilla.

## Estructura

```
frontend/
├── index.html      # Página principal
├── css/
│   └── styles.css  # Estilos principales
└── js/
    └── app.js      # Lógica de la aplicación
```

## Tecnologías

- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con variables CSS
- **JavaScript (ES6+)**: Lógica del cliente
- **Chart.js**: Visualización de datos y gráficos

## Funcionalidades

### Dashboard
- Vista general con estadísticas del estudiante
- Promedio general
- Materias en curso
- Asistencia promedio
- Alertas activas
- Gráficos de progreso

### Gestión de Materias
- Visualización de malla curricular
- Prerequisitos
- Estado de cada materia

### Registro de Notas
- Formulario para registrar notas
- Cálculo automático de promedios
- Visualización de historial

### Registro de Asistencias
- Formulario para registrar asistencias
- Cálculo de porcentaje de asistencia
- Historial de asistencias

### Sistema de Alertas
- Alertas personalizadas
- Notificaciones de riesgo
- Recordatorios importantes

## Configuración

### API Endpoint

Editar la constante `API_BASE_URL` en `js/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## Uso

### Desarrollo Local

1. Servir los archivos con un servidor HTTP simple:

```bash
cd frontend
python -m http.server 8080
```

2. Abrir en el navegador: `http://localhost:8080`

### Integración con Django

Los archivos del frontend pueden ser servidos directamente por Django configurando las rutas estáticas en `settings.py`.

## Personalización

### Colores

Los colores principales están definidos como variables CSS en `css/styles.css`:

```css
:root {
    --primary-color: #4a90e2;
    --secondary-color: #50c878;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
    /* ... */
}
```

### Estilos Responsive

El diseño es responsive y se adapta a diferentes tamaños de pantalla mediante media queries.

## Próximas Mejoras

- [ ] Integración completa con la API REST
- [ ] Autenticación de usuarios
- [ ] Visualización interactiva de la malla curricular
- [ ] Exportación de reportes
- [ ] Modo oscuro

