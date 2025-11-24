# Guía de Instalación

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd RutaAcademica-AsistentePersonal
```

### 2. Configurar el Entorno Virtual

#### Windows
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

1. Crear la base de datos:
```sql
CREATE DATABASE ruta_academica;
CREATE USER ruta_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE ruta_academica TO ruta_user;
```

2. Actualizar `backend/core/settings.py` con las credenciales de la base de datos.

### 5. Configurar Variables de Entorno

Crear un archivo `.env` en la carpeta `backend/`:

```
SECRET_KEY=tu-secret-key-generada
DEBUG=True
DATABASE_URL=postgresql://ruta_user:tu_password@localhost:5432/ruta_academica
```

### 6. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Configuración del Frontend

El frontend es estático y puede ser servido directamente desde la carpeta `frontend/` o integrado con Django.

### Opción 1: Servidor de Desarrollo Simple

Usar cualquier servidor HTTP simple:

```bash
cd frontend
python -m http.server 8080
```

### Opción 2: Integrar con Django

Configurar Django para servir los archivos estáticos del frontend.

## Verificación

1. Acceder a `http://localhost:8000/admin` y verificar que puedas iniciar sesión
2. Acceder a `http://localhost:8000/api/` y verificar que la API responda
3. Abrir `frontend/index.html` en el navegador

## Solución de Problemas

### Error: No se puede conectar a PostgreSQL

- Verificar que PostgreSQL esté ejecutándose
- Verificar las credenciales en `settings.py`
- Verificar que la base de datos exista

### Error: ModuleNotFoundError

- Asegurarse de que el entorno virtual esté activado
- Ejecutar `pip install -r requirements.txt` nuevamente

### Error: Port already in use

- Cambiar el puerto: `python manage.py runserver 8001`

