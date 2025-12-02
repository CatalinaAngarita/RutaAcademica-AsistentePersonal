#!/usr/bin/env python
"""
Script para actualizar la contraseña en el archivo .env
"""
import os
import re

def actualizar_password():
    print("=" * 50)
    print("ACTUALIZAR CONTRASEÑA DE POSTGRESQL EN .env")
    print("=" * 50)
    print()
    
    # Leer el archivo .env
    env_path = '.env'
    if not os.path.exists(env_path):
        print("❌ Error: No se encuentra el archivo .env")
        return
    
    with open(env_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar el estado actual
    if 'DB_PASSWORD=' in contenido:
        # Ver si está vacío
        if re.search(r'DB_PASSWORD=\s*$', contenido, re.MULTILINE):
            print("⚠️  DB_PASSWORD está vacío en el archivo .env")
            print()
            print("Por favor, ingresa tu contraseña de PostgreSQL:")
            password = input("Contraseña: ").strip()
            
            if password:
                # Reemplazar DB_PASSWORD= vacío por DB_PASSWORD=password
                nuevo_contenido = re.sub(
                    r'DB_PASSWORD=\s*\n',
                    f'DB_PASSWORD={password}\n',
                    contenido
                )
                
                # Si no funcionó el regex, intentar de otra forma
                if nuevo_contenido == contenido:
                    nuevo_contenido = contenido.replace('DB_PASSWORD=', f'DB_PASSWORD={password}')
                
                # Guardar
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                
                print()
                print("✅ Archivo .env actualizado correctamente")
                print()
                print("Verificando...")
                print()
                
                # Verificar
                from decouple import config
                try:
                    pwd = config('DB_PASSWORD')
                    if pwd:
                        print(f"✅ DB_PASSWORD configurado: {'*' * len(pwd)} ({len(pwd)} caracteres)")
                    else:
                        print("❌ DB_PASSWORD sigue vacío")
                except Exception as e:
                    print(f"⚠️  Error al verificar: {e}")
            else:
                print("❌ No se ingresó contraseña")
        else:
            # Ya tiene contraseña
            from decouple import config
            try:
                pwd = config('DB_PASSWORD')
                if pwd:
                    print(f"✅ DB_PASSWORD ya está configurado: {'*' * len(pwd)} ({len(pwd)} caracteres)")
                    print()
                    print("Si quieres cambiarlo, edita manualmente el archivo .env")
                else:
                    print("⚠️  DB_PASSWORD está en el archivo pero parece estar vacío")
            except Exception as e:
                print(f"⚠️  Error al leer: {e}")
    else:
        print("❌ No se encuentra DB_PASSWORD en el archivo .env")
        print("Agrega esta línea al archivo:")
        print("DB_PASSWORD=tu_password")

if __name__ == '__main__':
    actualizar_password()

