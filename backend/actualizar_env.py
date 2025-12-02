#!/usr/bin/env python
"""
Script para actualizar el archivo .env con los nombres correctos de variables
según lo que espera settings.py
"""
from pathlib import Path
import re

def actualizar_env():
    """Actualiza el archivo .env con los nombres correctos"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ Archivo .env no encontrado")
        print("   Creando archivo .env de ejemplo...")
        crear_env_ejemplo(env_path)
        return
    
    print("📝 Leyendo archivo .env...")
    contenido = env_path.read_text(encoding='utf-8')
    
    # Mapeo de nombres antiguos a nuevos
    reemplazos = {
        r'^DB_NAME=': 'DATABASE_NAME=',
        r'^DB_USER=': 'DATABASE_USER=',
        r'^DB_HOST=': 'DATABASE_HOST=',
        r'^DB_PORT=': 'DATABASE_PORT=',
        # DB_PASSWORD se mantiene igual
    }
    
    contenido_actualizado = contenido
    cambios = []
    
    for patron_antiguo, nuevo_nombre in reemplazos.items():
        if re.search(patron_antiguo, contenido_actualizado, re.MULTILINE):
            contenido_actualizado = re.sub(
                patron_antiguo, 
                nuevo_nombre, 
                contenido_actualizado, 
                flags=re.MULTILINE
            )
            cambios.append(f"  - {patron_antiguo.strip('^=')} → {nuevo_nombre.strip('=')}")
    
    if cambios:
        # Crear backup
        backup_path = env_path.with_suffix('.env.backup')
        backup_path.write_text(contenido, encoding='utf-8')
        print(f"💾 Backup creado: {backup_path}")
        
        # Escribir archivo actualizado
        env_path.write_text(contenido_actualizado, encoding='utf-8')
        print("✅ Archivo .env actualizado")
        print()
        print("📋 Cambios realizados:")
        for cambio in cambios:
            print(cambio)
    else:
        print("✅ El archivo .env ya tiene los nombres correctos")
    
    # Verificar si DB_PASSWORD está vacío
    if re.search(r'^DB_PASSWORD=\s*$', contenido_actualizado, re.MULTILINE):
        print()
        print("⚠️  ADVERTENCIA: DB_PASSWORD está vacío")
        print("   Necesitas configurar la contraseña de PostgreSQL")
        print()
        print("💡 Para configurarla:")
        print("   1. Abre el archivo .env")
        print("   2. Busca la línea: DB_PASSWORD=")
        print("   3. Cámbiala por: DB_PASSWORD=tu_password_de_postgres")
        print("   4. Guarda el archivo")


def crear_env_ejemplo(env_path):
    """Crea un archivo .env de ejemplo"""
    contenido_ejemplo = """# Configuración de Django
SECRET_KEY=django-insecure-cambia-esta-clave-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración de Base de Datos PostgreSQL
# IMPORTANTE: Actualiza estos valores con tus credenciales de PostgreSQL
DATABASE_NAME=ruta_academica
DATABASE_USER=postgres
DB_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432
"""
    env_path.write_text(contenido_ejemplo, encoding='utf-8')
    print(f"✅ Archivo .env creado: {env_path}")
    print()
    print("⚠️  IMPORTANTE: Edita el archivo .env y configura:")
    print("   - SECRET_KEY: Genera una clave secreta única")
    print("   - DB_PASSWORD: Tu contraseña de PostgreSQL")


if __name__ == '__main__':
    print("🔧 ACTUALIZADOR DE ARCHIVO .ENV")
    print("=" * 60)
    print()
    actualizar_env()
    print()
    print("=" * 60)
    print("✅ Proceso completado")
    print()
    print("📝 Próximo paso: Ejecuta python verificar_conexion_db.py")

