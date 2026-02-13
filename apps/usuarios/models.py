from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission # Importa esto
from .managers import UsuarioManager

class Usuario(AbstractUser):
    username = None 
    
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('ENCUESTADOR', 'Profesional'),
    )

    # --- DATOS GENERALES ---
    email = models.EmailField('Correo Electrónico', unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='ENCUESTADOR')
    
    nombres = models.CharField('Nombres', max_length=150)
    apellidos = models.CharField('Apellidos', max_length=150)
    dni = models.CharField('DNI', max_length=8, unique=True, null=True, blank=True)
    codigo = models.CharField('Código', max_length=20, blank=True, null=True)
    
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    edad = models.PositiveIntegerField('Edad', null=True, blank=True)
    sexo = models.CharField('Sexo', max_length=10, choices=(('M', 'M'), ('F', 'F')), blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    direccion = models.CharField('Dirección', max_length=200, blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # --- CAMPOS DE ENCUESTADOR ---
    institucion_procedencia = models.CharField('Institución Procedencia', max_length=100, default='Universidad Nacional de Trujillo – UNT')
    ciclo = models.CharField('Cip', max_length=20, blank=True)
    especialidad = models.CharField('Especialidad', max_length=100, blank=True)
    
    supervisor_asignado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='encuestadores_a_cargo', 
        limit_choices_to={'rol': 'SUPERVISOR'}
    )
    
    # Referencia a la app 'fichas' (Gracias al label en apps.py, esto funciona)
    institucion_asignada = models.ForeignKey(
        'fichas.Institucion', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='encuestadores_asignados'
    )

    # --- CAMPOS DE SUPERVISOR ---
    profesion = models.CharField('Profesión', max_length=100, blank=True)
    numero_colegiatura = models.CharField('N° Colegiatura', max_length=50, blank=True)
    centro_labores = models.CharField('Centro de Labores', max_length=100, blank=True)

    # --- CORRECCIÓN DEL ERROR "CLASHES" ---
    # Esto soluciona el error rojo redefiniendo los campos conflictivos
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="usuario_set", # Nombre único para evitar choque
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set", # Nombre único para evitar choque
        related_query_name="usuario",
    )

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['nombres', 'apellidos'] 

    objects = UsuarioManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"