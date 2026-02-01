from django.contrib import admin
from .models import (
    Institucion, Dimension, Pregunta, Opcion, 
    FichaEvaluacion, FamiliarDelEvaluado, FichaDetalle
)

# =======================================================
# 1. CONFIGURACIÓN DE MAESTROS
# =======================================================

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_modular', 'telefono', 'nombre_contacto', 'fecha_registro')
    search_fields = ('nombre', 'codigo_modular')
    list_filter = ('fecha_registro',)

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 0
    min_num = 2  # Obliga a tener al menos 2 opciones

@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'descripcion')
    ordering = ('orden',)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    inlines = [OpcionInline]
    list_display = ('orden', 'enunciado_corto', 'dimension')
    list_filter = ('dimension',)
    search_fields = ('enunciado',)
    ordering = ('dimension', 'orden')
    list_per_page = 20

    def enunciado_corto(self, obj):
        return obj.enunciado[:80] + "..." if len(obj.enunciado) > 80 else obj.enunciado
    enunciado_corto.short_description = "Enunciado"

# =======================================================
# 2. CONFIGURACIÓN DE LA FICHA (El corazón del sistema)
# =======================================================

class FamiliarInline(admin.TabularInline):
    """Permite editar los familiares directamente en la ficha"""
    model = FamiliarDelEvaluado
    extra = 0
    classes = ('collapse',) # Por defecto colapsado para no ocupar espacio visual
    fields = ('nombres', 'parentesco', 'edad', 'sexo', 'ocupacion', 'ingresos')

class DetalleInline(admin.TabularInline):
    """Muestra las respuestas marcadas (Solo lectura para integridad)"""
    model = FichaDetalle
    extra = 0
    can_delete = False
    # Hacemos los campos de solo lectura para evitar manipulación de respuestas desde el admin
    readonly_fields = ('pregunta', 'opcion_seleccionada', 'puntaje_obtenido')
    classes = ('collapse',) 

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(FichaEvaluacion)
class FichaEvaluacionAdmin(admin.ModelAdmin):
    # --- LISTADO PRINCIPAL ---
    list_display = (
        'id',
        'nombres_evaluado', 
        'apellidos_evaluado', 
        'nivel_riesgo_colored', # Usamos una función para darle color
        'puntaje_total', 
        'institucion', 
        'fecha_registro'
    )
    
    list_display_links = ('id', 'nombres_evaluado')
    
    # Filtros laterales
    list_filter = (
        'nivel_riesgo', 
        'institucion', 
        'nivel_educativo', 
        'sexo_evaluado',
        'fecha_registro'
    )
    
    # Buscador
    search_fields = (
        'nombres_evaluado', 
        'apellidos_evaluado', 
        'dni_evaluado', 
        'usuario_registra__username'
    )

    # Inlines (Tablas hijas)
    inlines = [FamiliarInline, DetalleInline]
    
    # Campos de solo lectura (Auditoría y cálculos)
    readonly_fields = (
        'fecha_registro', 'fecha_modificacion', 
        'puntaje_total', 'puntaje_dimension_a', 'puntaje_dimension_b',
        'puntaje_dimension_c', 'puntaje_dimension_d', 'puntaje_dimension_e', 'puntaje_dimension_f'
    )

    # --- ORGANIZACIÓN VISUAL (FIELDSETS) ---
    fieldsets = (
        ('📍 Auditoría y Contexto', {
            'fields': (
                ('usuario_registra', 'institucion'),
                ('fecha_registro', 'fecha_modificacion')
            ),
            'classes': ('collapse',), # Ocultable
        }),
        ('👤 Datos Personales del Estudiante', {
            'fields': (
                ('nombres_evaluado', 'apellidos_evaluado'),
                ('dni_evaluado', 'fecha_nacimiento', 'edad_evaluado'),
                ('sexo_evaluado', 'nivel_educativo')
            )
        }),
        ('🏠 Ubicación Geográfica', {
            'fields': (
                'direccion_domicilio',
                ('ubigeo_departamento', 'ubigeo_provincia', 'ubigeo_distrito')
            )
        }),
        ('📞 Contacto y Emergencia', {
            'fields': (
                ('telefono_contacto', 'email_contacto'),
                ('emergencia_nombres', 'emergencia_parentesco', 'emergencia_telefono')
            )
        }),
        ('👨‍👩‍👧‍👦 Resumen Familiar', {
            'fields': (
                ('jefe_hogar', 'num_integrantes'),
                'observaciones_familia'
            )
        }),
        ('📊 Diagnóstico y Resultados', {
            'fields': (
                ('puntaje_total', 'nivel_riesgo'),
                'conclusion',
                'plan_intervencion'
            ),
            'description': "Resultados calculados automáticamente por el sistema."
        }),
        ('📈 Desglose de Puntajes (Solo Lectura)', {
            'fields': (
                ('puntaje_dimension_a', 'puntaje_dimension_b'),
                ('puntaje_dimension_c', 'puntaje_dimension_d'),
                ('puntaje_dimension_e', 'puntaje_dimension_f')
            ),
            'classes': ('collapse',)
        }),
    )

    # --- FUNCIONES EXTRA ---
    
    # Colorear el riesgo en la lista
    def nivel_riesgo_colored(self, obj):
        from django.utils.html import format_html
        colors = {
            'RIESGO BAJO': 'green',
            'RIESGO MODERADO': 'orange',
            'RIESGO SEVERO': 'red',
            'RIESGO CRÍTICO': 'darkred',
        }
        color = colors.get(obj.nivel_riesgo, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>', 
            color, 
            obj.nivel_riesgo
        )
    nivel_riesgo_colored.short_description = 'Nivel de Riesgo'