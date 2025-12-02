#!/usr/bin/env python
"""
Script interactivo para configurar la contraseña de PostgreSQL en el archivo .env
"""
from pathlib import Path
import getpass
import re

def configurar_password():
    """Configura la contraseña en el archivo .env"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    print("🔐 CONFIGURACIÓN DE CONTRASEÑA DE POSTGRESQL")
    print("=" * 60)
    print()
    
    # Leer contenido actual
    contenido = env_path.read_text(encoding='utf-8')
    
    # Verificar si ya tiene contraseña
    match = re.search(r'^DB_PASSWORD=(.+)$', contenido, re.MULTILINE)
    if match and match.group(1).strip():
        password_actual = match.group(1)
        print(f"⚠️  Ya existe una contraseña configurada ({len(password_actual)} caracteres)")
        respuesta = input("¿Deseas cambiarla? (s/n): ").strip().lower()
        if respuesta != 's':
            print("✅ Manteniendo la contraseña actual")
            return True
    
    print()
    print("💡 Ingresa la contraseña de PostgreSQL")
    print("   (Usuario: postgres, Base de datos: ruta_academica)")
    print()
    
    # Pedir contraseña de forma segura
    password = getpass.getpass("Contraseña: ")
    
    if not password:
        print("❌ La contraseña no puede estar vacía")
        return False
    
    # Confirmar contraseña
    password_confirm = getpass.getpass("Confirma la contraseña: ")
    
    if password != password_confirm:
        print("❌ Las contraseñas no coinciden")
        return False
    
    # Actualizar el archivo
    contenido_actualizado = re.sub(
        r'^DB_PASSWORD=.*$',
        f'DB_PASSWORD={password}',
        contenido,
        flags=re.MULTILINE
    )
    
    # Crear backup
    backup_path = env_path.with_suffix('.env.backup')
    backup_path.write_text(contenido, encoding='utf-8')
    
    # Escribir archivo actualizado
    env_path.write_text(contenido_actualizado, encoding='utf-8')
    
    print()
    print("✅ Contraseña configurada correctamente")
    print(f"💾 Backup guardado en: {backup_path}")
    return True


if __name__ == '__main__':
    try:
        if configurar_password():
            print()
            print("=" * 60)
            print("✅ Configuración completada")
            print()
            print("📝 Próximo paso: Ejecuta python verificar_conexion_db.py")
        else:
            print()
            print("❌ No se pudo configurar la contraseña")
    except KeyboardInterrupt:
        print()
        print("\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")

