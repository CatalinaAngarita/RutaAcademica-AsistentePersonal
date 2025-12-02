from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(ModelAdmin):
    list_display = ['estudiante', 'materia', 'fecha', 'asistencia_badge', 'justificada_badge']
    list_filter = ['asistio', 'justificada', 'fecha', 'materia']
    search_fields = ['estudiante__codigo', 'estudiante__user__first_name', 'estudiante__user__last_name', 'materia__codigo', 'materia__nombre']
    date_hierarchy = 'fecha'
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        ('Información de Asistencia', {
            'fields': ('estudiante', 'materia', 'fecha', 'asistio', 'justificada'),
            'classes': ('wide',),
        }),
    )
    
    @display(description='Asistencia')
    def asistencia_badge(self, obj):
        if obj.asistio:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Presente</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✗ Ausente</span>'
        )
    
    @display(description='Justificada')
    def justificada_badge(self, obj):
        if obj.justificada:
            return format_html(
                '<span style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">Sí</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">No</span>'
        )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('estudiante', 'estudiante__user', 'materia')

