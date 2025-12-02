# ✅ Verificar Conexión a PostgreSQL

## Pasos Rápidos

### 1. Verificar que el archivo .env existe y tiene las variables correctas

Asegúrate de que tu archivo `backend/.env` tenga estas variables:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Probar la conexión

```bash
cd backend
python test_db.py
```

Deberías ver:
```
✅ Conexión a la base de datos: OK
   Base de datos: [nombre_de_tu_base]
   Motor: django.db.backends.postgresql
```

### 3. Aplicar migraciones (si es la primera vez)

```bash
python manage.py migrate
```

### 4. Crear datos de prueba (opcional)

```bash
python poblar_datos.py
```

## 🔍 Solución de Problemas

### Error: "could not connect to server"

**Solución:**
1. Verifica que PostgreSQL esté corriendo
2. Verifica las credenciales en `.env`
3. Verifica que la base de datos exista:
```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

### Error: "password authentication failed"

**Solución:**
- Verifica el usuario y contraseña en `.env`
- Prueba conectarte manualmente:
```bash
psql -h localhost -U tu_usuario -d nombre_de_tu_base
```

### Error: "database does not exist"

**Solución:**
Crea la base de datos:
```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

## ✅ Todo Listo

Una vez que `test_db.py` muestre "✅ Conexión a la base de datos: OK", 
tu aplicación está lista para usar PostgreSQL.

