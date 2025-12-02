from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Nota


@admin.register(Nota)
class NotaAdmin(ModelAdmin):
    list_display = ['estudiante', 'materia', 'nota_badge', 'porcentaje_badge', 'valor_ponderado_badge', 'fecha']
    list_filter = ['materia', 'fecha']
    search_fields = ['estudiante__codigo', 'estudiante__user__first_name', 'estudiante__user__last_name', 'materia__codigo', 'materia__nombre']
    readonly_fields = ['fecha', 'valor_ponderado']
    list_per_page = 25
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Nota', {
            'fields': ('estudiante', 'materia', 'valor', 'porcentaje', 'valor_ponderado', 'fecha'),
            'classes': ('wide',),
        }),
    )
    
    @display(description='Nota')
    def nota_badge(self, obj):
        # Colores según la nota
        if obj.valor >= 4.5:
            color = '#10b981'  # Verde - Excelente
        elif obj.valor >= 3.5:
            color = '#3b82f6'  # Azul - Bueno
        elif obj.valor >= 3.0:
            color = '#f59e0b'  # Amarillo - Aceptable
        else:
            color = '#ef4444'  # Rojo - Bajo
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{:.2f}</span>',
            color, obj.valor
        )
    
    @display(description='Porcentaje')
    def porcentaje_badge(self, obj):
        return format_html(
            '<span style="background-color: #6366f1; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{}%</span>',
            obj.porcentaje
        )
    
    @display(description='Valor Ponderado')
    def valor_ponderado_badge(self, obj):
        return format_html(
            '<span style="background-color: #8b5cf6; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{:.2f}</span>',
            obj.valor_ponderado
        )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('estudiante', 'estudiante__user', 'materia')

