from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Estudiante, Carrera


@admin.register(Carrera)
class CarreraAdmin(ModelAdmin):
    list_display = ['nombre', 'fija_badge', 'activa', 'total_estudiantes', 'fecha_creacion']
    list_filter = ['fija', 'activa', 'fecha_creacion']
    search_fields = ['nombre']
    readonly_fields = ['fija', 'fecha_creacion', 'total_estudiantes_display']
    list_per_page = 25
    
    fieldsets = (
        ('Información de la Carrera', {
            'fields': ('nombre', 'fija', 'activa'),
            'classes': ('wide',),
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'total_estudiantes_display'),
            'classes': ('collapse',),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer el campo 'nombre' de solo lectura para carreras fijas"""
        readonly = list(self.readonly_fields)
        if obj and obj.fija:
            readonly.append('nombre')
        return readonly
    
    def has_delete_permission(self, request, obj=None):
        """Prevenir eliminación de carreras fijas"""
        if obj and obj.fija:
            return False
        return super().has_delete_permission(request, obj)
    
    @display(description='Tipo', boolean=True)
    def fija_badge(self, obj):
        if obj.fija:
            return format_html(
                '<span style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">🔒 Fija</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">Editable</span>'
        )
    
    @display(description='Total Estudiantes')
    def total_estudiantes(self, obj):
        count = obj.estudiantes.count()
        return format_html(
            '<span style="font-weight: 600;">{}</span>',
            count
        )
    
    @display(description='Total de Estudiantes')
    def total_estudiantes_display(self, obj):
        if obj:
            count = obj.estudiantes.count()
            return format_html(
                '<span style="font-size: 16px; font-weight: 600; color: #3b82f6;">{}</span> estudiantes',
                count
            )
        return '-'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('estudiantes')


@admin.register(Estudiante)
class EstudianteAdmin(ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'carrera', 'semestre_actual', 'estado_badge', 'fecha_ingreso']
    list_filter = ['activo', 'carrera', 'semestre_actual', 'fecha_ingreso']
    search_fields = ['codigo', 'user__username', 'user__first_name', 'user__last_name', 'user__email', 'carrera__nombre']
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
        return super().get_queryset(request).select_related('user', 'carrera')

