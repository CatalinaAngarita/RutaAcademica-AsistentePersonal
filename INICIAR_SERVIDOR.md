# 🚀 Cómo Ver el Frontend de Ruta Académica

## Opción 1: Integrado con Django (Recomendado) ⭐

El frontend está integrado con Django, así que puedes verlo directamente desde el servidor de Django.

### Pasos:

1. **Abre una terminal y navega al backend:**
```bash
cd backend
```

2. **Inicia el servidor Django:**
```bash
python manage.py runserver
```

3. **Abre tu navegador en:**
```
http://localhost:8000
```

¡Listo! Verás el frontend completo con todas sus secciones:
- Dashboard
- Materias
- Notas
- Asistencias
- Alertas

### Ventajas:
- ✅ El frontend está conectado directamente a la API
- ✅ Todo funciona en un solo servidor
- ✅ No necesitas configurar CORS
- ✅ Puedes probar la funcionalidad completa

---

## Opción 2: Servidor HTTP Simple (Solo Visualización)

Si solo quieres ver el diseño sin conectarte a la API:

### Con Python:
```bash
cd frontend
python -m http.server 8080
```

Luego abre: `http://localhost:8080`

### Con Node.js (si lo tienes):
```bash
cd frontend
npx http-server -p 8080
```

### Nota:
Con esta opción, el frontend mostrará datos de ejemplo pero no se conectará a la API real.

---

## 📋 Estructura de URLs

Cuando uses la Opción 1 (Django):

- **Frontend:** `http://localhost:8000/`
- **API Estudiantes:** `http://localhost:8000/api/estudiantes/`
- **API Materias:** `http://localhost:8000/api/materias/`
- **API Notas:** `http://localhost:8000/api/notas/`
- **API Asistencias:** `http://localhost:8000/api/asistencias/`
- **API Alertas:** `http://localhost:8000/api/alertas/`
- **Admin Django:** `http://localhost:8000/admin/`

---

## 🎨 Características del Frontend

El frontend incluye:

1. **Dashboard**
   - Promedio general
   - Materias cursando
   - Asistencia promedio
   - Alertas activas
   - Gráficos de progreso (Chart.js)

2. **Gestión de Materias**
   - Visualización de malla curricular
   - Prerequisitos

3. **Registro de Notas**
   - Formulario para registrar notas
   - Historial de notas
   - Cálculo automático de promedios

4. **Registro de Asistencias**
   - Formulario para registrar asistencias
   - Historial de asistencias
   - Cálculo de porcentaje

5. **Sistema de Alertas**
   - Alertas personalizadas
   - Notificaciones de riesgo

---

## 🔧 Solución de Problemas

### El CSS no se carga
- Verifica que el servidor Django esté corriendo
- Asegúrate de estar accediendo a `http://localhost:8000` (no a un puerto diferente)

### La API no responde
- Verifica que las migraciones estén aplicadas: `python manage.py migrate`
- Revisa la consola del navegador (F12) para ver errores

### No se ven datos
- Crea algunos datos de prueba desde el admin: `http://localhost:8000/admin/`
- O usa la API directamente para crear datos

---

## 📝 Próximos Pasos

1. Crea un superusuario para acceder al admin:
```bash
python manage.py createsuperuser
```

2. Accede al admin y crea algunos datos de prueba:
   - Estudiantes
   - Materias
   - Notas
   - Asistencias

3. Recarga el frontend y verás los datos reflejados

¡Disfruta explorando tu aplicación! 🎉

