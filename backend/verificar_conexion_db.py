#!/usr/bin/env python
"""
Script para verificar la conexión a PostgreSQL usando la configuración de Django
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.conf import settings
from decouple import config

def verificar_variables_env():
    """Verifica que las variables de entorno estén configuradas"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("=" * 60)
    print()
    
    # Verificar si el archivo .env existe
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        print(f"✅ Archivo .env encontrado: {env_path}")
    else:
        print(f"❌ Archivo .env NO encontrado en: {env_path}")
        print("   Crea el archivo .env con las siguientes variables:")
        print("   DATABASE_NAME=ruta_academica")
        print("   DATABASE_USER=postgres")
        print("   DATABASE_PASSWORD=tu_password")
        print("   DATABASE_HOST=localhost")
        print("   DATABASE_PORT=5432")
        return False
    
    print()
    print("📋 Variables de entorno leídas:")
    print("-" * 60)
    
    # Leer variables según lo que espera settings.py
    try:
        db_name = config('DATABASE_NAME', default=None)
        db_user = config('DATABASE_USER', default=None)
        db_password = config('DB_PASSWORD', default=None)
        db_host = config('DATABASE_HOST', default=None)
        db_port = config('DATABASE_PORT', default=None)
        
        print(f"  DATABASE_NAME: {db_name if db_name else '❌ NO CONFIGURADO'}")
        print(f"  DATABASE_USER: {db_user if db_user else '❌ NO CONFIGURADO'}")
        
        if db_password:
            print(f"  DB_PASSWORD: {'*' * len(db_password)} ({len(db_password)} caracteres)")
        else:
            print(f"  DB_PASSWORD: ❌ NO CONFIGURADO O VACÍO")
        
        print(f"  DATABASE_HOST: {db_host if db_host else '❌ NO CONFIGURADO'}")
        print(f"  DATABASE_PORT: {db_port if db_port else '❌ NO CONFIGURADO'}")
        
        print()
        
        # Verificar que todas las variables estén configuradas
        faltantes = []
        if not db_name:
            faltantes.append('DATABASE_NAME')
        if not db_user:
            faltantes.append('DATABASE_USER')
        if not db_password:
            faltantes.append('DB_PASSWORD')
        if not db_host:
            faltantes.append('DATABASE_HOST')
        if not db_port:
            faltantes.append('DATABASE_PORT')
        
        if faltantes:
            print("❌ Variables faltantes en .env:")
            for var in faltantes:
                print(f"   - {var}")
            print()
            print("💡 Solución:")
            print("   Edita el archivo .env y agrega las variables faltantes.")
            if 'DB_PASSWORD' in faltantes:
                print("   IMPORTANTE: DB_PASSWORD no debe estar vacío.")
            return False
        else:
            print("✅ Todas las variables están configuradas")
            return True
            
    except Exception as e:
        print(f"❌ Error al leer variables: {e}")
        return False


def verificar_conexion():
    """Verifica la conexión a PostgreSQL"""
    print()
    print("=" * 60)
    print("🔌 VERIFICACIÓN DE CONEXIÓN A POSTGRESQL")
    print("=" * 60)
    print()
    
    try:
        # Obtener configuración de la base de datos
        db_config = settings.DATABASES['default']
        
        print(f"📊 Configuración de conexión:")
        print(f"   Motor: {db_config['ENGINE']}")
        print(f"   Base de datos: {db_config['NAME']}")
        print(f"   Usuario: {db_config['USER']}")
        print(f"   Host: {db_config['HOST']}")
        print(f"   Puerto: {db_config['PORT']}")
        print()
        
        # Intentar conectar
        print("🔄 Intentando conectar a PostgreSQL...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Conexión exitosa!")
            print()
            print(f"📦 Versión de PostgreSQL:")
            print(f"   {version}")
            print()
            
            # Verificar que la base de datos existe
            cursor.execute("SELECT current_database();")
            current_db = cursor.fetchone()[0]
            print(f"📂 Base de datos actual: {current_db}")
            print()
            
            # Verificar tablas existentes
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tablas = cursor.fetchall()
            
            if tablas:
                print(f"📋 Tablas encontradas ({len(tablas)}):")
                for tabla in tablas[:10]:  # Mostrar máximo 10
                    print(f"   - {tabla[0]}")
                if len(tablas) > 10:
                    print(f"   ... y {len(tablas) - 10} más")
            else:
                print("⚠️  No se encontraron tablas en la base de datos")
                print("   Ejecuta: python manage.py migrate")
            
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print()
        print("💡 Posibles soluciones:")
        print("   1. Verifica que PostgreSQL esté corriendo")
        print("   2. Verifica que las credenciales en .env sean correctas")
        print("   3. Verifica que la base de datos exista")
        print("   4. Verifica que el usuario tenga permisos")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print()
    print("🚀 VERIFICADOR DE CONEXIÓN A POSTGRESQL")
    print()
    
    # Paso 1: Verificar variables de entorno
    if not verificar_variables_env():
        print()
        print("❌ No se puede continuar sin las variables de entorno configuradas")
        sys.exit(1)
    
    # Paso 2: Verificar conexión
    if verificar_conexion():
        print()
        print("=" * 60)
        print("✅ VERIFICACIÓN COMPLETA - TODO ESTÁ CORRECTO")
        print("=" * 60)
        print()
        print("🎉 Tu proyecto está listo para ejecutarse!")
        print()
        print("📝 Próximos pasos:")
        print("   1. Ejecuta migraciones: python manage.py migrate")
        print("   2. Crea un superusuario: python manage.py createsuperuser")
        print("   3. Inicia el servidor: python manage.py runserver")
        print()
    else:
        print()
        print("=" * 60)
        print("❌ VERIFICACIÓN FALLIDA")
        print("=" * 60)
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()

