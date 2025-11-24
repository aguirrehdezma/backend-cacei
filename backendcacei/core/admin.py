from django.contrib import admin
from core.models import Profesor, ProgramaEducativo, Curso, Institucion, Organizacion, Periodo

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    """Admin para el modelo Profesor"""
    list_display = ['numero_empleado', 'nombre_completo', 'nombramiento_actual', 'tiene_acceso_sistema', 'created_at']
    list_filter = ['experiencia_ingenieria', 'created_at']
    search_fields = ['numero_empleado', 'nombres', 'apellido_paterno', 'apellido_materno']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_empleado', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento')
        }),
        ('Información Profesional', {
            'fields': ('nombramiento_actual', 'antiguedad', 'experiencia_ingenieria')
        }),
        ('Acceso al Sistema', {
            'fields': ('user',),
            'description': 'Vincular con un usuario para que el profesor tenga acceso como docente'
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProgramaEducativo)
class ProgramaEducativoAdmin(admin.ModelAdmin):
    """Admin para ProgramaEducativo"""
    list_display = ['clave', 'nombre', 'estatus', 'fecha_creacion']
    list_filter = ['estatus', 'fecha_creacion']
    search_fields = ['clave', 'nombre']
    readonly_fields = ['fecha_creacion', 'created_at', 'updated_at']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin para Curso"""
    list_display = ['clave', 'nombre', 'programa', 'tipo', 'horas_totales']
    list_filter = ['tipo', 'programa']
    search_fields = ['clave', 'nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    """Admin para Institucion"""
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    """Admin para Organizacion"""
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    """Admin para Periodo"""
    list_display = ['nombre', 'semestre', 'anio', 'fecha_inicio', 'fecha_fin']
    list_filter = ['semestre', 'anio']
    search_fields = ['nombre']
    readonly_fields = ['nombre', 'created_at', 'updated_at']
