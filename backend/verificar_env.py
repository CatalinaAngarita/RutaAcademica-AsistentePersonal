#!/usr/bin/env python
"""
Script para verificar que las variables de entorno se están leyendo correctamente
"""
from decouple import config
import os

print("🔍 Verificando variables de entorno...")
print("")

# Verificar si el archivo .env existe
if os.path.exists('.env'):
    print("✅ Archivo .env encontrado")
else:
    print("❌ Archivo .env NO encontrado")
    print("   Ubicación esperada:", os.path.abspath('.env'))

print("")
print("📋 Variables leídas desde .env:")
print("")

try:
    db_name = config('DB_NAME', default='NO_CONFIGURADO')
    db_user = config('DB_USER', default='NO_CONFIGURADO')
    db_password = config('DB_PASSWORD', default='NO_CONFIGURADO')
    db_host = config('DB_HOST', default='NO_CONFIGURADO')
    db_port = config('DB_PORT', default='NO_CONFIGURADO')
    
    print(f"DB_NAME: {db_name}")
    print(f"DB_USER: {db_user}")
    
    # Mostrar password solo si está configurado (por seguridad, mostrar solo longitud)
    if db_password and db_password != 'NO_CONFIGURADO':
        print(f"DB_PASSWORD: {'*' * len(db_password)} ({len(db_password)} caracteres)")
    else:
        print(f"DB_PASSWORD: ❌ NO CONFIGURADO O VACÍO")
    
    print(f"DB_HOST: {db_host}")
    print(f"DB_PORT: {db_port}")
    
    print("")
    if db_password == '' or db_password == 'NO_CONFIGURADO':
        print("❌ PROBLEMA: DB_PASSWORD está vacío o no configurado")
        print("")
        print("Solución:")
        print("1. Abre el archivo .env")
        print("2. Busca la línea: DB_PASSWORD=")
        print("3. Cámbiala por: DB_PASSWORD=tu_password_de_postgres")
        print("4. Guarda el archivo")
    else:
        print("✅ Todas las variables están configuradas")
        
except Exception as e:
    print(f"❌ Error al leer variables: {e}")

