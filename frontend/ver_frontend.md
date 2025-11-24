# Cómo Ver el Frontend

## Opción 1: Servidor HTTP Simple (Rápido)

### Con Python:
```bash
cd frontend
python -m http.server 8080
```

Luego abre en tu navegador: `http://localhost:8080`

### Con Node.js (si tienes instalado):
```bash
cd frontend
npx http-server -p 8080
```

## Opción 2: Integrado con Django (Recomendado)

El frontend está integrado con Django. Para verlo:

1. **Asegúrate de que el servidor Django esté corriendo:**
```bash
cd backend
python manage.py runserver
```

2. **Abre en tu navegador:**
```
http://localhost:8000
```

El frontend se servirá desde la raíz del sitio y la API estará disponible en `/api/`

## Nota Importante

El frontend está configurado para conectarse a la API en `http://localhost:8000/api`. Asegúrate de que:
- El servidor Django esté corriendo
- Las migraciones estén aplicadas
- Tengas algunos datos de prueba en la base de datos

## Datos de Prueba

Para probar el frontend, puedes crear datos de prueba desde el admin de Django:
- Accede a: `http://localhost:8000/admin/`
- Crea algunos estudiantes, materias, notas, etc.

