from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Materia


@admin.register(Materia)
class MateriaAdmin(ModelAdmin):
    list_display = ['codigo', 'nombre', 'creditos_badge', 'prerequisitos_count', 'estado_badge']
    list_filter = ['activa', 'creditos']
    search_fields = ['codigo', 'nombre', 'descripcion']
    filter_horizontal = ['prerequisitos']
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'creditos', 'descripcion', 'activa'),
            'classes': ('wide',),
        }),
        ('Prerequisitos', {
            'fields': ('prerequisitos',),
            'description': 'Selecciona las materias que son prerequisitos para esta materia.',
        }),
    )
    
    @display(description='Créditos')
    def creditos_badge(self, obj):
        color = '#3b82f6' if obj.creditos >= 4 else '#10b981'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 600;">{} créditos</span>',
            color, obj.creditos
        )
    
    @display(description='Prerequisitos')
    def prerequisitos_count(self, obj):
        count = obj.prerequisitos.count()
        if count == 0:
            return format_html('<span style="color: #6b7280;">Sin prerequisitos</span>')
        return format_html(
            '<span style="color: #3b82f6; font-weight: 600;">{} prerequisito(s)</span>',
            count
        )
    
    @display(description='Estado', boolean=True)
    def estado_badge(self, obj):
        if obj.activa:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Activa</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✗ Inactiva</span>'
        )

