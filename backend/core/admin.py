from django.contrib import admin
from .models import Cliente, Proyecto, Tarea, SubTarea


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Configuración del admin para Cliente"""
    list_display = ['nombre', 'email', 'empresa', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'email', 'empresa']
    readonly_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    """Configuración del admin para Proyecto"""
    list_display = ['nombre', 'cliente', 'estado', 'progreso', 'fecha_inicio', 'fecha_entrega']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['nombre', 'descripcion', 'cliente__nombre']
    readonly_fields = ['progreso']
    ordering = ['-fecha_inicio']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'cliente')
        }),
        ('Estado y Progreso', {
            'fields': ('estado', 'progreso')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_entrega')
        }),
    )


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    """Configuración del admin para Tarea"""
    list_display = ['titulo', 'proyecto', 'estado', 'progreso', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'proyecto__nombre']
    readonly_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']


@admin.register(SubTarea)
class SubTareaAdmin(admin.ModelAdmin):
    """Configuración del admin para SubTarea"""
    list_display = ['titulo', 'tarea', 'completada', 'fecha_creacion']
    list_filter = ['completada', 'fecha_creacion']
    search_fields = ['titulo', 'tarea__titulo']
    readonly_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']