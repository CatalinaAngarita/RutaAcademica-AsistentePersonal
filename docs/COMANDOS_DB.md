# 🗄️ Comandos para Configurar PostgreSQL

## 📋 Pasos para Conectar la Base de Datos

### 1. Verificar que el archivo .env esté configurado

Asegúrate de que `backend/.env` tenga estas variables con tus credenciales:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Crear la base de datos en PostgreSQL (si no existe)

Abre `psql` o tu cliente de PostgreSQL y ejecuta:

```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

O desde la terminal:
```bash
psql -U postgres -c "CREATE DATABASE nombre_de_tu_base_de_datos;"
```

### 3. Verificar la conexión

```bash
cd backend
python test_db.py
```

**Resultado esperado:**
```
✅ Conexión a la base de datos: OK
   Base de datos: nombre_de_tu_base_de_datos
   Motor: django.db.backends.postgresql
```

### 4. Aplicar las migraciones (crear las tablas)

```bash
python manage.py migrate
```

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: admin, alertas, asistencias, auth, contenttypes, estudiantes, materias, notas, sessions
Running migrations:
  Applying estudiantes.0001_initial... OK
  Applying materias.0001_initial... OK
  ...
```

### 5. Crear un superusuario (para acceder al admin)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear el usuario admin.

### 6. Crear datos de prueba (opcional)

```bash
python poblar_datos.py
```

**Resultado esperado:**
```
✅ ¡Datos de prueba creados exitosamente!
📊 Resumen:
  - Estudiantes: 3
  - Materias: 5
  - Notas: 12
  - Asistencias: 20
```

### 7. Verificar que todo funciona

```bash
python test_db.py
```

Deberías ver los datos creados.

---

## 🔄 Comandos Útiles Adicionales

### Ver el estado de las migraciones

```bash
python manage.py showmigrations
```

### Crear nuevas migraciones (si cambias los modelos)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Acceder al shell de Django (para consultas)

```bash
python manage.py shell
```

Dentro del shell:
```python
from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia

# Ver todos los estudiantes
Estudiante.objects.all()

# Contar estudiantes
Estudiante.objects.count()

# Ver todas las materias
Materia.objects.all()
```

### Iniciar el servidor

```bash
python manage.py runserver
```

Luego accede a:
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api/

---

## 🆘 Solución de Problemas

### Error: "could not connect to server"

**Verifica que PostgreSQL esté corriendo:**
- Windows: Servicios → Busca "PostgreSQL"
- Linux: `sudo systemctl status postgresql`
- Mac: `brew services list`

**Prueba la conexión manualmente:**
```bash
psql -h localhost -U tu_usuario -d nombre_de_tu_base
```

### Error: "password authentication failed"

**Verifica las credenciales en `.env`**

**Prueba conectarte manualmente:**
```bash
psql -h localhost -U tu_usuario -d postgres
```

### Error: "database does not exist"

**Crea la base de datos:**
```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

### Error: "relation does not exist"

**Aplica las migraciones:**
```bash
python manage.py migrate
```

---

## ✅ Checklist de Configuración

- [ ] Archivo `.env` configurado con credenciales correctas
- [ ] Base de datos creada en PostgreSQL
- [ ] Conexión probada con `python test_db.py`
- [ ] Migraciones aplicadas con `python manage.py migrate`
- [ ] Superusuario creado (opcional)
- [ ] Datos de prueba creados (opcional)
- [ ] Servidor iniciado y funcionando

---

## 📝 Resumen de Comandos en Orden

```bash
# 1. Ir al directorio backend
cd backend

# 2. Verificar conexión
python test_db.py

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario (opcional)
python manage.py createsuperuser

# 5. Crear datos de prueba (opcional)
python poblar_datos.py

# 6. Iniciar servidor
python manage.py runserver
```

¡Listo! Tu base de datos PostgreSQL está conectada y configurada. 🎉

