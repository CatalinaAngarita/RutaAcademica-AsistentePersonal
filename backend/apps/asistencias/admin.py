from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'materia', 'fecha', 'asistio', 'justificada']
    list_filter = ['asistio', 'justificada', 'fecha', 'materia']
    search_fields = ['estudiante__codigo', 'materia__codigo', 'materia__nombre']
    date_hierarchy = 'fecha'

