from django.contrib import admin
from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'materia', 'valor', 'porcentaje', 'valor_ponderado', 'fecha']
    list_filter = ['materia', 'fecha']
    search_fields = ['estudiante__codigo', 'materia__codigo', 'materia__nombre']
    readonly_fields = ['fecha', 'valor_ponderado']
    
    def valor_ponderado(self, obj):
        return f"{obj.valor_ponderado:.2f}"
    valor_ponderado.short_description = 'Valor Ponderado'

