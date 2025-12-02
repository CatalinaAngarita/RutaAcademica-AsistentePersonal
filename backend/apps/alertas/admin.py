from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(ModelAdmin):
    list_display = ['estudiante', 'titulo', 'tipo_badge', 'estado_badge', 'leida_badge', 'fecha_creacion']
    list_filter = ['tipo', 'activa', 'leida', 'fecha_creacion']
    search_fields = ['estudiante__codigo', 'estudiante__user__first_name', 'estudiante__user__last_name', 'titulo', 'mensaje']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('estudiante', 'tipo', 'titulo', 'mensaje'),
            'classes': ('wide',),
        }),
        ('Estado', {
            'fields': ('activa', 'leida', 'fecha_creacion'),
            'classes': ('wide',),
        }),
    )
    
    @display(description='Tipo')
    def tipo_badge(self, obj):
        colors = {
            'info': '#3b82f6',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'success': '#10b981',
        }
        color = colors.get(obj.tipo.lower(), '#6b7280')
        tipo_display = obj.tipo.capitalize()
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, tipo_display
        )
    
    @display(description='Estado')
    def estado_badge(self, obj):
        if obj.activa:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Activa</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✗ Inactiva</span>'
        )
    
    @display(description='Leída')
    def leida_badge(self, obj):
        if obj.leida:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Leída</span>'
            )
        return format_html(
            '<span style="background-color: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">● No leída</span>'
        )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('estudiante', 'estudiante__user')

