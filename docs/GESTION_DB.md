# 🗄️ Gestión de Base de Datos

## Estado Actual

✅ **Conexión:** PostgreSQL  
✅ **Configuración:** Variables desde archivo `.env`  
✅ **Migraciones:** Todas aplicadas  
✅ **Datos de prueba:** Creados

## 📊 Datos Actuales

- **Estudiantes:** 3
- **Materias:** 5
- **Notas:** 12
- **Asistencias:** 20
- **Alertas:** 0

## 🔧 Comandos Útiles

### Verificar Conexión
```bash
python test_db.py
```

### Crear Datos de Prueba
```bash
python poblar_datos.py
```

### Aplicar Migraciones
```bash
python manage.py migrate
```

### Crear Nuevas Migraciones
```bash
python manage.py makemigrations
```

### Acceder al Shell de Django
```bash
python manage.py shell
```

### Ver Datos desde el Shell
```python
from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia
from apps.notas.models import Nota

# Ver todos los estudiantes
Estudiante.objects.all()

# Ver todas las materias
Materia.objects.all()

# Ver todas las notas
Nota.objects.all()

# Contar registros
Estudiante.objects.count()
```

## 🌐 Acceder a los Datos

### 1. Frontend (Interfaz Visual)
```
http://localhost:8000
```

### 2. Admin de Django
```
http://localhost:8000/admin
```
**Credenciales de prueba:**
- Usuario: `juan.perez`
- Contraseña: `password123`

### 3. API REST

#### Ver todos los estudiantes:
```
GET http://localhost:8000/api/estudiantes/
```

#### Ver todas las materias:
```
GET http://localhost:8000/api/materias/
```

#### Ver todas las notas:
```
GET http://localhost:8000/api/notas/
```

#### Ver estadísticas de un estudiante:
```
GET http://localhost:8000/api/estudiantes/1/estadisticas/
```

## 📝 Ejemplos de Consultas

### Desde el Shell de Django

```python
# Importar modelos
from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia
from apps.notas.models import Nota
from apps.asistencias.models import Asistencia

# Obtener un estudiante
estudiante = Estudiante.objects.get(codigo='2024001')

# Ver sus notas
notas = Nota.objects.filter(estudiante=estudiante)
for nota in notas:
    print(f"{nota.materia.nombre}: {nota.valor}")

# Calcular promedio
from django.db.models import Avg, Sum
notas = Nota.objects.filter(estudiante=estudiante)
suma_ponderada = sum(n.valor * (n.porcentaje / 100) for n in notas)
total_porcentaje = sum(n.porcentaje for n in notas)
promedio = (suma_ponderada / total_porcentaje) * 100 if total_porcentaje > 0 else 0
print(f"Promedio: {promedio:.2f}")

# Ver materias con prerequisitos
materia = Materia.objects.get(codigo='WEB101')
prerequisitos = materia.prerequisitos.all()
print(f"Prerequisitos de {materia.nombre}:")
for prereq in prerequisitos:
    print(f"  - {prereq.nombre}")
```

## ⚙️ Configuración de PostgreSQL

La aplicación está configurada para usar PostgreSQL. Las credenciales se configuran en el archivo `.env`:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

Ver `CONFIGURAR_POSTGRESQL.md` para más detalles.

## 🧹 Limpiar Base de Datos

Si quieres eliminar todos los datos y empezar de nuevo:

```python
# Desde el shell de Django
python manage.py shell

from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia
from apps.notas.models import Nota
from apps.asistencias.models import Asistencia
from apps.alertas.models import Alerta
from django.contrib.auth.models import User

# Eliminar todos los datos
Nota.objects.all().delete()
Asistencia.objects.all().delete()
Alerta.objects.all().delete()
Estudiante.objects.all().delete()
Materia.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
```

## 📦 Backup de Base de Datos

### PostgreSQL
```bash
# Crear backup
pg_dump -h localhost -U tu_usuario -d nombre_base_datos > backup.sql

# Restaurar desde backup
psql -h localhost -U tu_usuario -d nombre_base_datos < backup.sql
```

## ✅ Verificación Rápida

Ejecuta este comando para verificar que todo funciona:

```bash
python test_db.py
```

Deberías ver:
- ✅ Conexión a la base de datos: OK
- ✅ Todos los modelos funcionan correctamente
- 📊 Conteo de registros

