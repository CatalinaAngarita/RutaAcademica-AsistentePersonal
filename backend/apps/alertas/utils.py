from django.utils import timezone
from datetime import timedelta
from .models import Alerta, TipoAlerta
from apps.notas.models import Nota
from apps.asistencias.models import Asistencia
import numpy as np


def calcular_riesgo_reprobacion(estudiante, materia):
    """
    Calcula el riesgo de reprobación basado en notas y asistencias
    
    Args:
        estudiante: Instancia de Estudiante
        materia: Instancia de Materia
    
    Returns:
        float: Probabilidad de reprobación (0-1)
    """
    # Obtener notas de la materia
    notas = Nota.objects.filter(estudiante=estudiante, materia=materia)
    
    # Obtener asistencias de la materia
    asistencias = Asistencia.objects.filter(estudiante=estudiante, materia=materia)
    
    # Calcular promedio de notas
    promedio_notas = 0
    if notas.exists():
        suma_ponderada = sum(nota.valor_ponderado for nota in notas)
        total_porcentaje = sum(nota.porcentaje for nota in notas)
        if total_porcentaje > 0:
            promedio_notas = (suma_ponderada / total_porcentaje) * 100
    
    # Calcular porcentaje de asistencia
    porcentaje_asistencia = 0
    if asistencias.exists():
        total = asistencias.count()
        presentes = asistencias.filter(asistio=True).count()
        porcentaje_asistencia = (presentes / total) * 100
    
    # Calcular riesgo basado en probabilidades
    # Nota mínima aprobatoria: 10 (en escala 0-20)
    riesgo_nota = max(0, (10 - promedio_notas) / 10) if promedio_notas < 10 else 0
    
    # Asistencia mínima: 70%
    riesgo_asistencia = max(0, (70 - porcentaje_asistencia) / 70) if porcentaje_asistencia < 70 else 0
    
    # Riesgo combinado (promedio ponderado)
    riesgo_total = (riesgo_nota * 0.7) + (riesgo_asistencia * 0.3)
    
    return min(1.0, max(0.0, riesgo_total))


def generar_alertas_automaticas(estudiante):
    """
    Genera alertas automáticas basadas en el rendimiento del estudiante
    
    Args:
        estudiante: Instancia de Estudiante
    
    Returns:
        list: Lista de alertas generadas
    """
    alertas_generadas = []
    
    # Obtener todas las materias del estudiante
    materias = set()
    notas = Nota.objects.filter(estudiante=estudiante)
    asistencias = Asistencia.objects.filter(estudiante=estudiante)
    
    for nota in notas:
        materias.add(nota.materia)
    for asistencia in asistencias:
        materias.add(asistencia.materia)
    
    # Generar alertas por materia
    for materia in materias:
        riesgo = calcular_riesgo_reprobacion(estudiante, materia)
        
        if riesgo > 0.7:
            # Riesgo alto
            alerta = Alerta.objects.create(
                estudiante=estudiante,
                tipo=TipoAlerta.DANGER,
                titulo=f"Riesgo alto de reprobación - {materia.nombre}",
                mensaje=f"Tu riesgo de reprobación en {materia.nombre} es del {riesgo*100:.1f}%. "
                       f"Te recomendamos revisar tus notas y asistencias.",
                activa=True
            )
            alertas_generadas.append(alerta)
        elif riesgo > 0.4:
            # Riesgo medio
            alerta = Alerta.objects.create(
                estudiante=estudiante,
                tipo=TipoAlerta.WARNING,
                titulo=f"Atención requerida - {materia.nombre}",
                mensaje=f"Tu riesgo de reprobación en {materia.nombre} es del {riesgo*100:.1f}%. "
                       f"Es importante mejorar tu rendimiento.",
                activa=True
            )
            alertas_generadas.append(alerta)
    
    # Alerta de asistencia baja
    if asistencias.exists():
        total = asistencias.count()
        presentes = asistencias.filter(asistio=True).count()
        porcentaje_asistencia = (presentes / total) * 100
        
        if porcentaje_asistencia < 70:
            alerta = Alerta.objects.create(
                estudiante=estudiante,
                tipo=TipoAlerta.WARNING,
                titulo="Asistencia baja",
                mensaje=f"Tu porcentaje de asistencia es del {porcentaje_asistencia:.1f}%. "
                       f"Recuerda que necesitas al menos 70% para aprobar.",
                activa=True
            )
            alertas_generadas.append(alerta)
    
    return alertas_generadas

