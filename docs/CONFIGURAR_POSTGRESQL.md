# 🐘 Configuración de PostgreSQL

## 📋 Requisitos Previos

1. **PostgreSQL instalado** en tu sistema
2. **Base de datos creada** (o crear una nueva)
3. **Usuario con permisos** para la base de datos

## 🔧 Pasos de Configuración

### 1. Crear la Base de Datos en PostgreSQL

Abre `psql` o tu cliente de PostgreSQL favorito y ejecuta:

```sql
-- Crear la base de datos
CREATE DATABASE ruta_academica;

-- Crear un usuario (opcional, puedes usar postgres)
CREATE USER ruta_user WITH PASSWORD 'tu_password_seguro';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE ruta_academica TO ruta_user;

-- Si usas PostgreSQL 15+, también necesitas:
\c ruta_academica
GRANT ALL ON SCHEMA public TO ruta_user;
```

### 2. Configurar Variables de Entorno

#### Opción A: Archivo .env (Recomendado)

1. Copia el archivo de ejemplo:
```bash
cd backend
cp .env.example .env
```

2. Edita el archivo `.env` con tus credenciales:
```env
DB_NAME=ruta_academica
DB_USER=ruta_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432
```

#### Opción B: Variables de Entorno del Sistema

**Windows (PowerShell):**
```powershell
$env:DB_NAME="ruta_academica"
$env:DB_USER="ruta_user"
$env:DB_PASSWORD="tu_password"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
```

**Linux/Mac:**
```bash
export DB_NAME=ruta_academica
export DB_USER=ruta_user
export DB_PASSWORD=tu_password
export DB_HOST=localhost
export DB_PORT=5432
```

### 3. Verificar la Conexión

Ejecuta el script de prueba:
```bash
python test_db.py
```

Deberías ver:
```
✅ Conexión a la base de datos: OK
   Base de datos: ruta_academica
   Motor: django.db.backends.postgresql
```

### 4. Aplicar Migraciones

```bash
python manage.py migrate
```

Esto creará todas las tablas en PostgreSQL.

### 5. Crear Datos de Prueba (Opcional)

```bash
python poblar_datos.py
```

## 🔍 Solución de Problemas

### Error: "could not connect to server"

**Causa:** PostgreSQL no está corriendo o la configuración es incorrecta.

**Solución:**
1. Verifica que PostgreSQL esté corriendo:
   - Windows: Servicios → PostgreSQL
   - Linux: `sudo systemctl status postgresql`
   - Mac: `brew services list`

2. Verifica la conexión manualmente:
```bash
psql -h localhost -U tu_usuario -d ruta_academica
```

### Error: "password authentication failed"

**Causa:** Usuario o contraseña incorrectos.

**Solución:**
1. Verifica las credenciales en `.env`
2. Prueba conectarte manualmente con `psql`

### Error: "database does not exist"

**Causa:** La base de datos no ha sido creada.

**Solución:**
```sql
CREATE DATABASE ruta_academica;
```

### Error: "permission denied"

**Causa:** El usuario no tiene permisos.

**Solución:**
```sql
GRANT ALL PRIVILEGES ON DATABASE ruta_academica TO tu_usuario;
\c ruta_academica
GRANT ALL ON SCHEMA public TO tu_usuario;
```

## 📊 Verificar la Configuración

### Desde Django Shell

```bash
python manage.py shell
```

```python
from django.db import connection
print(connection.settings_dict)
```

### Desde psql

```bash
psql -h localhost -U tu_usuario -d ruta_academica
```

```sql
-- Ver todas las tablas
\dt

-- Ver estructura de una tabla
\d estudiantes_estudiante

-- Contar registros
SELECT COUNT(*) FROM estudiantes_estudiante;
```

## 🔄 Migrar Datos

Si necesitas migrar datos desde otra fuente:

### Usar dumpdata y loaddata

```bash
# 1. Exportar datos
python manage.py dumpdata > datos_backup.json

# 2. Aplicar migraciones en PostgreSQL
python manage.py migrate

# 3. Importar datos
python manage.py loaddata datos_backup.json
```

## ✅ Checklist de Configuración

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `ruta_academica` creada
- [ ] Usuario con permisos configurado
- [ ] Archivo `.env` creado con credenciales
- [ ] Conexión probada con `test_db.py`
- [ ] Migraciones aplicadas con `python manage.py migrate`
- [ ] Datos de prueba creados (opcional)

## 📝 Notas Importantes

1. **Seguridad:** Nunca subas el archivo `.env` a Git. Ya está en `.gitignore`
2. **Producción:** Usa variables de entorno del sistema en producción
3. **Backup:** Haz backups regulares de tu base de datos PostgreSQL
4. **Performance:** PostgreSQL es más robusto que SQLite para producción

## 🆘 Ayuda Adicional

Si tienes problemas, verifica:
- Logs de PostgreSQL: `/var/log/postgresql/` (Linux) o en la instalación de Windows
- Logs de Django: Revisa la consola donde ejecutas `runserver`
- Configuración de firewall: Asegúrate de que el puerto 5432 esté abierto

