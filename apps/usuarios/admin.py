from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombres', 'apellidos', 'rol', 'supervisor_asignado', 'is_active')
    list_filter = ('rol', 'is_active', 'sexo', 'institucion_asignada')
    search_fields = ('email', 'nombres', 'apellidos', 'codigo', 'dni')
    ordering = ('email',)
    
    # Organizar los campos en grupos visuales
    fieldsets = (
        ('Credenciales de Acceso', {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'dni', 'codigo', 'fecha_nacimiento', 'edad', 'sexo', 'telefono', 'direccion')}),
        ('Rol y Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser')}),
        ('Datos de Alumno / Encuestador', {'fields': ('institucion_procedencia', 'ciclo', 'especialidad', 'supervisor_asignado', 'institucion_asignada')}),
        ('Datos de Supervisor', {'fields': ('profesion', 'numero_colegiatura', 'centro_labores')}),
    )