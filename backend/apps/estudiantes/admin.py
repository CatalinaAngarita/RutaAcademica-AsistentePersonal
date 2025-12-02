from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'carrera', 'semestre_actual', 'estado_badge', 'fecha_ingreso']
    list_filter = ['activo', 'carrera', 'semestre_actual', 'fecha_ingreso']
    search_fields = ['codigo', 'user__username', 'user__first_name', 'user__last_name', 'user__email', 'carrera']
    readonly_fields = ['fecha_ingreso', 'email_display']
    list_per_page = 25
    list_max_show_all = 100
    date_hierarchy = 'fecha_ingreso'
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'email_display'),
            'classes': ('wide',),
        }),
        ('Información Académica', {
            'fields': ('codigo', 'carrera', 'semestre_actual', 'activo'),
            'classes': ('wide',),
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso',),
            'classes': ('collapse',),
        }),
    )
    
    @display(description='Estado', boolean=True)
    def estado_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Activo</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✗ Inactivo</span>'
        )
    
    @display(description='Email')
    def email_display(self, obj):
        return obj.email or '-'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

