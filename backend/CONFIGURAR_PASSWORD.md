# 🔐 Configurar Contraseña de PostgreSQL

## ⚠️ Problema Actual

Tu archivo `.env` tiene `DB_PASSWORD=` vacío. Necesitas agregar tu contraseña de PostgreSQL.

## ✅ Solución Rápida

### Opción 1: Editar manualmente el archivo .env

1. Abre el archivo: `backend/.env`
2. Busca la línea:
   ```
   DB_PASSWORD=
   ```
3. Cámbiala por tu contraseña de PostgreSQL:
   ```
   DB_PASSWORD=tu_password_aqui
   ```
4. Guarda el archivo

### Opción 2: Usar PowerShell (Windows)

```powershell
cd backend

# Reemplaza 'TU_PASSWORD' con tu contraseña real
(Get-Content .env) -replace 'DB_PASSWORD=', 'DB_PASSWORD=TU_PASSWORD' | Set-Content .env
```

### Opción 3: Si no tienes contraseña configurada en PostgreSQL

Si tu usuario de PostgreSQL no tiene contraseña, necesitas asignarle una:

1. Abre `psql` o tu cliente de PostgreSQL
2. Ejecuta:
```sql
ALTER USER postgres WITH PASSWORD 'nueva_password';
```

3. Luego actualiza tu `.env` con esa contraseña

## ✅ Verificar que Funciona

Después de actualizar el `.env`, ejecuta:

```bash
python verificar_env.py
```

Deberías ver:
```
DB_PASSWORD: ******** (X caracteres)
✅ Todas las variables están configuradas
```

Luego prueba la conexión:

```bash
python test_db.py
```

Deberías ver:
```
✅ Conexión a la base de datos: OK
```

## 📝 Ejemplo de .env Correcto

```env
# Configuración de Django
SECRET_KEY=tu-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración de Base de Datos PostgreSQL
DB_NAME=ruta_academica
DB_USER=postgres
DB_PASSWORD=tu_password_aqui  # ← IMPORTANTE: No debe estar vacío
DB_HOST=localhost
DB_PORT=5432
```

## 🔒 Seguridad

- El archivo `.env` ya está en `.gitignore`, así que no se subirá a Git
- Nunca compartas tu archivo `.env` con otros
- Usa contraseñas seguras en producción

