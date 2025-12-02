#!/usr/bin/env python
"""
Script para probar la conexión a la base de datos
Ejecutar con: python manage.py shell < test_db.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia
from apps.notas.models import Nota
from apps.asistencias.models import Asistencia
from apps.alertas.models import Alerta

def test_conexion():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    try:
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Conexión a la base de datos: OK")
            print(f"   Base de datos: {connection.settings_dict['NAME']}")
            print(f"   Motor: {connection.settings_dict['ENGINE']}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    print("\n📊 Verificando modelos...")
    try:
        # Contar registros
        print(f"  - Estudiantes: {Estudiante.objects.count()}")
        print(f"  - Materias: {Materia.objects.count()}")
        print(f"  - Notas: {Nota.objects.count()}")
        print(f"  - Asistencias: {Asistencia.objects.count()}")
        print(f"  - Alertas: {Alerta.objects.count()}")
        
        # Mostrar algunos ejemplos
        if Estudiante.objects.exists():
            print("\n👤 Ejemplo de estudiante:")
            estudiante = Estudiante.objects.first()
            print(f"   - {estudiante.codigo}: {estudiante.nombre_completo}")
            print(f"   - Carrera: {estudiante.carrera}")
            print(f"   - Semestre: {estudiante.semestre_actual}")
        
        if Materia.objects.exists():
            print("\n📚 Ejemplo de materia:")
            materia = Materia.objects.first()
            print(f"   - {materia.codigo}: {materia.nombre}")
            print(f"   - Créditos: {materia.creditos}")
            prerequisitos = materia.prerequisitos.all()
            if prerequisitos:
                print(f"   - Prerequisitos: {', '.join([p.codigo for p in prerequisitos])}")
        
        if Nota.objects.exists():
            print("\n📝 Ejemplo de nota:")
            nota = Nota.objects.first()
            print(f"   - Estudiante: {nota.estudiante.codigo}")
            print(f"   - Materia: {nota.materia.codigo}")
            print(f"   - Valor: {nota.valor} ({nota.porcentaje}%)")
            print(f"   - Valor ponderado: {nota.valor_ponderado:.2f}")
        
        print("\n✅ Todos los modelos funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al consultar modelos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_conexion()

