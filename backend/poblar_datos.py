#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba
Ejecutar con: python manage.py shell < poblar_datos.py
O mejor: python manage.py shell
Luego copiar y pegar el contenido de este archivo
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from apps.estudiantes.models import Estudiante
from apps.materias.models import Materia
from apps.notas.models import Nota
from apps.asistencias.models import Asistencia
from apps.alertas.models import Alerta, TipoAlerta
from datetime import date, timedelta
import random

def crear_datos_prueba():
    """Crea datos de prueba para la aplicación"""
    
    print("🗑️  Limpiando datos existentes...")
    # Limpiar datos existentes (opcional, comentar si quieres mantener datos)
    Nota.objects.all().delete()
    Asistencia.objects.all().delete()
    Alerta.objects.all().delete()
    Estudiante.objects.all().delete()
    Materia.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    print("👤 Creando usuarios y estudiantes...")
    # Crear estudiantes
    estudiantes_data = [
        {
            'username': 'juan.perez',
            'email': 'juan.perez@example.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'codigo': '2024001',
            'carrera': 'Ingeniería de Sistemas',
            'semestre_actual': 5
        },
        {
            'username': 'maria.garcia',
            'email': 'maria.garcia@example.com',
            'first_name': 'María',
            'last_name': 'García',
            'codigo': '2024002',
            'carrera': 'Ingeniería de Sistemas',
            'semestre_actual': 3
        },
        {
            'username': 'carlos.rodriguez',
            'email': 'carlos.rodriguez@example.com',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'codigo': '2024003',
            'carrera': 'Ingeniería de Sistemas',
            'semestre_actual': 7
        }
    ]
    
    estudiantes = []
    for data in estudiantes_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123',
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        estudiante = Estudiante.objects.create(
            user=user,
            codigo=data['codigo'],
            carrera=data['carrera'],
            semestre_actual=data['semestre_actual']
        )
        estudiantes.append(estudiante)
        print(f"  ✓ Creado: {estudiante}")
    
    print("\n📚 Creando materias...")
    # Crear materias
    materias_data = [
        {
            'codigo': 'MAT101',
            'nombre': 'Matemáticas I',
            'creditos': 4,
            'descripcion': 'Curso introductorio de matemáticas',
            'prerequisitos': []
        },
        {
            'codigo': 'PROG101',
            'nombre': 'Programación I',
            'creditos': 5,
            'descripcion': 'Fundamentos de programación',
            'prerequisitos': ['MAT101']
        },
        {
            'codigo': 'EST101',
            'nombre': 'Estructuras de Datos',
            'creditos': 5,
            'descripcion': 'Estructuras de datos y algoritmos',
            'prerequisitos': ['PROG101']
        },
        {
            'codigo': 'BD101',
            'nombre': 'Bases de Datos',
            'creditos': 4,
            'descripcion': 'Diseño y gestión de bases de datos',
            'prerequisitos': ['PROG101']
        },
        {
            'codigo': 'WEB101',
            'nombre': 'Desarrollo Web',
            'creditos': 5,
            'descripcion': 'Desarrollo de aplicaciones web',
            'prerequisitos': ['PROG101', 'BD101']
        }
    ]
    
    materias = {}
    for data in materias_data:
        materia = Materia.objects.create(
            codigo=data['codigo'],
            nombre=data['nombre'],
            creditos=data['creditos'],
            descripcion=data['descripcion']
        )
        materias[data['codigo']] = materia
        print(f"  ✓ Creada: {materia}")
    
    # Agregar prerequisitos
    print("\n🔗 Configurando prerequisitos...")
    for data in materias_data:
        materia = materias[data['codigo']]
        for prereq_codigo in data['prerequisitos']:
            if prereq_codigo in materias:
                materia.prerequisitos.add(materias[prereq_codigo])
                print(f"  ✓ {materia.codigo} requiere {prereq_codigo}")
    
    print("\n📝 Creando notas...")
    # Crear notas para el primer estudiante
    estudiante = estudiantes[0]
    materias_estudiante = [materias['MAT101'], materias['PROG101'], materias['EST101']]
    
    for materia in materias_estudiante:
        # Crear varias notas por materia
        notas_data = [
            {'valor': 15.5, 'porcentaje': 30, 'descripcion': 'Parcial 1'},
            {'valor': 16.0, 'porcentaje': 30, 'descripcion': 'Parcial 2'},
            {'valor': 14.5, 'porcentaje': 20, 'descripcion': 'Trabajos'},
            {'valor': 17.0, 'porcentaje': 20, 'descripcion': 'Proyecto Final'},
        ]
        
        for nota_data in notas_data:
            Nota.objects.create(
                estudiante=estudiante,
                materia=materia,
                valor=nota_data['valor'],
                porcentaje=nota_data['porcentaje'],
                descripcion=nota_data['descripcion']
            )
        print(f"  ✓ Notas creadas para {estudiante.codigo} - {materia.codigo}")
    
    print("\n📅 Creando asistencias...")
    # Crear asistencias
    estudiante = estudiantes[0]
    materia = materias['PROG101']
    
    # Crear asistencias para las últimas 4 semanas
    fecha_inicio = date.today() - timedelta(days=28)
    for i in range(20):  # 20 clases
        fecha_clase = fecha_inicio + timedelta(days=i*2)
        asistio = random.random() > 0.15  # 85% de asistencia
        Asistencia.objects.create(
            estudiante=estudiante,
            materia=materia,
            fecha=fecha_clase,
            asistio=asistio,
            justificada=not asistio and random.random() > 0.5
        )
    print(f"  ✓ Asistencias creadas para {estudiante.codigo} - {materia.codigo}")
    
    print("\n🔔 Generando alertas...")
    # Generar alertas automáticas
    from apps.alertas.utils import generar_alertas_automaticas
    for estudiante in estudiantes:
        alertas = generar_alertas_automaticas(estudiante)
        if alertas:
            print(f"  ✓ {len(alertas)} alertas generadas para {estudiante.codigo}")
    
    print("\n✅ ¡Datos de prueba creados exitosamente!")
    print("\n📊 Resumen:")
    print(f"  - Estudiantes: {Estudiante.objects.count()}")
    print(f"  - Materias: {Materia.objects.count()}")
    print(f"  - Notas: {Nota.objects.count()}")
    print(f"  - Asistencias: {Asistencia.objects.count()}")
    print(f"  - Alertas: {Alerta.objects.count()}")
    print("\n🌐 Puedes ver los datos en:")
    print("  - Frontend: http://localhost:8000")
    print("  - Admin: http://localhost:8000/admin")
    print("  - API: http://localhost:8000/api/")

if __name__ == '__main__':
    crear_datos_prueba()

