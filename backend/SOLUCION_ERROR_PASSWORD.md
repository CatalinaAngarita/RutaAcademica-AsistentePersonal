# 🔧 Solución: Error "no password supplied"

## ❌ Error que estás viendo:

```
connection to server at "localhost" (::1), port 5432 failed: fe_sendauth: no password supplied
```

## 🔍 Causa del Problema

El archivo `.env` tiene `DB_PASSWORD=` vacío. PostgreSQL necesita una contraseña para conectarse.

## ✅ Solución

### Opción 1: Editar el archivo .env manualmente

1. Abre el archivo `backend/.env` en tu editor
2. Busca la línea:
   ```
   DB_PASSWORD=
   ```
3. Cámbiala por tu contraseña de PostgreSQL:
   ```
   DB_PASSWORD=tu_password_de_postgres
   ```
4. Guarda el archivo

### Opción 2: Usar PowerShell para actualizar

```powershell
cd backend
# Reemplaza 'tu_password' con tu contraseña real
(Get-Content .env) -replace 'DB_PASSWORD=', 'DB_PASSWORD=tu_password' | Set-Content .env
```

### Opción 3: Si no tienes contraseña en PostgreSQL

Si tu usuario de PostgreSQL no tiene contraseña, puedes:

1. **Asignar una contraseña al usuario:**
```sql
ALTER USER postgres WITH PASSWORD 'nueva_password';
```

2. **O crear un nuevo usuario con contraseña:**
```sql
CREATE USER ruta_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE ruta_academica TO ruta_user;
```

Luego actualiza tu `.env`:
```env
DB_USER=ruta_user
DB_PASSWORD=tu_password
```

## ✅ Verificar que Funciona

Después de actualizar el `.env`, prueba la conexión:

```bash
python test_db.py
```

Deberías ver:
```
✅ Conexión a la base de datos: OK
```

## 📝 Ejemplo de archivo .env correcto

```env
# Configuración de Django
SECRET_KEY=tu-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración de PostgreSQL
DB_NAME=ruta_academica
DB_USER=postgres
DB_PASSWORD=tu_password_aqui  # ← IMPORTANTE: No debe estar vacío
DB_HOST=localhost
DB_PORT=5432
```

## 🆘 Si sigues teniendo problemas

1. **Verifica que PostgreSQL esté corriendo**
2. **Verifica que el usuario y contraseña sean correctos:**
   ```bash
   psql -U postgres -h localhost
   ```
3. **Verifica que la base de datos exista:**
   ```sql
   CREATE DATABASE ruta_academica;
   ```

