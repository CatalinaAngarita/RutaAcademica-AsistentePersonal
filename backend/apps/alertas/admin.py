from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'titulo', 'tipo', 'activa', 'leida', 'fecha_creacion']
    list_filter = ['tipo', 'activa', 'leida', 'fecha_creacion']
    search_fields = ['estudiante__codigo', 'titulo', 'mensaje']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_creacion'

