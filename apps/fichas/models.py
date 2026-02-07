from django.db import models
from django.conf import settings # Para relacionar con tu Usuario (Encuestador)
from apps.ubigeo.models import Distrito, Provincia, Departamento

# =======================================================
# PARTE 1: MAESTROS (Configuración del Sistema)
# =======================================================

class Institucion(models.Model):
    """
    MAESTRO: Instituciones educativas donde se realizan las encuestas.
    [cite_start][cite: 3, 4] Se registran los datos completos del colegio.
    """
    codigo_modular = models.CharField('Código Modular', max_length=20, unique=True)
    nombre = models.CharField('Nombre / Descripción', max_length=200)
    direccion = models.CharField('Dirección', max_length=200, blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    
    # Datos del contacto (Directora, Profesor OBE, etc.)
    nombre_contacto = models.CharField('Nombre del Contacto', max_length=150)
    correo_contacto = models.EmailField('Correo Electrónico', blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Dimension(models.Model):
    """Ej: A. Socioeconómicas, B. Estructura Familiar"""
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    """La pregunta específica del cuestionario"""
    enunciado = models.TextField('Pregunta')
    orden = models.PositiveIntegerField()
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return f"{self.orden}. {self.enunciado[:50]}..."

class Opcion(models.Model):
    """Las alternativas de respuesta y sus puntajes"""
    texto = models.CharField('Alternativa', max_length=200)
    puntaje = models.IntegerField('Puntaje', default=0)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')

    def __str__(self):
        return f"{self.texto} ({self.puntaje} pts)"

# =======================================================
# PARTE 2: LA FICHA SOCIOFAMILIAR (Operación)
# =======================================================

class FichaEvaluacion(models.Model):
    # --- PUNTAJES POR DIMENSIÓN (Para reportes rápidos) ---
    puntaje_dimension_a = models.IntegerField('A. Socioeconómicas', default=0)
    puntaje_dimension_b = models.IntegerField('B. Estructura Familiar', default=0)
    puntaje_dimension_c = models.IntegerField('C. Indicadores Educativos', default=0)
    puntaje_dimension_d = models.IntegerField('D. Psicosociales', default=0)
    puntaje_dimension_e = models.IntegerField('E. Acceso Servicios', default=0)
    puntaje_dimension_f = models.IntegerField('F. Factores Protectores', default=0)
    """
    Cabecera de la Ficha. Contiene Auditoría + Datos Generales del Estudiante.
    """
    # --- AUDITORÍA Y CONTROL ---
    usuario_registra = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='fichas_realizadas',
        verbose_name='Agente_de_campo'
    )
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='Institución Evaluada')
    fecha_registro = models.DateTimeField('Fecha de Aplicación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # --- 1. DATOS GENERALES DEL ESTUDIANTE ---
    nombres_evaluado = models.CharField('Nombres', max_length=100)
    apellidos_evaluado = models.CharField('Apellidos', max_length=100)
    dni_evaluado = models.CharField('DNI', max_length=8)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    edad_evaluado = models.IntegerField('Edad')
    sexo_evaluado = models.CharField('Sexo', max_length=10, choices=(('M', 'Masculino'), ('F', 'Femenino')))
    
    # Datos Académicos - eliminar grado y carrera
    NIVEL_EDUCATIVO = (('Primaria', 'Primaria'), ('Secundaria', 'Secundaria'), ('Universidad', 'Universidad'))
    nivel_educativo = models.CharField('Nivel Educativo', max_length=20, choices=NIVEL_EDUCATIVO, default='Secundaria')
    

    # Ubicación y Contacto
    direccion_domicilio = models.CharField('Dirección Actual', max_length=200)

    ubigeo_departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='fichas_dep')
    ubigeo_provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, related_name='fichas_prov')
    ubigeo_distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True, related_name='fichas_dist')

    # distrito = models.CharField('Distrito', max_length=100)
    # provincia = models.CharField('Provincia', max_length=100)
    # lugar_origen = models.CharField('Lugar de Origen', max_length=100)
    telefono_contacto = models.CharField('Teléfono', max_length=20)
    email_contacto = models.EmailField('Email', blank=True)

    # Contacto de Emergencia
    emergencia_nombres = models.CharField('Nombre Emergencia', max_length=150)
    emergencia_telefono = models.CharField('Teléfono Emergencia', max_length=20)
    emergencia_parentesco = models.CharField('Parentesco', max_length=50)

    # --- 2. ESTRUCTURA FAMILIAR (Cabecera) ---
    jefe_hogar = models.CharField('Jefe de Hogar', max_length=150)
    num_integrantes = models.IntegerField('Número de Integrantes')
    observaciones_familia = models.TextField('Observaciones Familiares', blank=True)

    # --- RESULTADOS Y DIAGNÓSTICO ---
    puntaje_total = models.IntegerField(default=0)
    nivel_riesgo = models.CharField(max_length=50, blank=True) # Ej: RIESGO SEVERO
    conclusion = models.TextField('Conclusión Diagnóstica', blank=True)
    plan_intervencion = models.TextField('Plan de Intervención Recomendado', blank=True)

    def __str__(self):
        return f"Ficha {self.id}: {self.nombres_evaluado} {self.apellidos_evaluado}"
    

from django.db import models
from django.conf import settings

# ... tus otros modelos (Institucion, etc.)

class FichaHistorial(models.Model):
    """
    Registra cada edición realizada en una ficha para fines de auditoría.
    """
    ficha = models.ForeignKey(FichaEvaluacion, on_delete=models.CASCADE, related_name='historial_cambios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_edicion = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=255, default="Edición de datos")
    
    # Cambia help_count por help_text
    detalles = models.TextField(blank=True, help_text="Ej: Cambió el nivel de riesgo de Bajo a Alto")

    class Meta:
        ordering = ['-fecha_edicion']

    def __str__(self):
        return f"{self.usuario.username} editó la ficha {self.ficha.id} el {self.fecha_edicion}"

# =======================================================
# PARTE 3: DETALLES DE LA FICHA
# =======================================================

class FamiliarDelEvaluado(models.Model):
    """
    Tabla detallada de los familiares (Padre, Madre, Hermanos, etc.)
    """
    ficha = models.ForeignKey(FichaEvaluacion, on_delete=models.CASCADE, related_name='familiares')
    
    nombres = models.CharField('Nombres y Apellidos', max_length=150)
    parentesco = models.CharField('Parentesco', max_length=50) # Ej: Padre, Madre
    edad = models.IntegerField('Edad')
    sexo = models.CharField('Sexo', max_length=10, choices=(('M', 'M'), ('F', 'F')))
    estado_civil = models.CharField('Estado Civil', max_length=50, blank=True)
    nivel_educativo = models.CharField('Nivel Educativo', max_length=50, blank=True)
    ocupacion = models.CharField('Ocupación/Estudios', max_length=100, blank=True)
    ingresos = models.DecimalField('Ingresos Mensuales', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombres} ({self.parentesco})"



class FichaDetalle(models.Model):
    """
    Guarda la respuesta seleccionada para cada pregunta del cuestionario.
    """
    ficha = models.ForeignKey(FichaEvaluacion, on_delete=models.CASCADE, related_name='detalles')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.PROTECT)
    
    # Snapshot: Guardamos el puntaje aquí para mantener el histórico
    # aunque cambien los valores maestros en el futuro.
    puntaje_obtenido = models.IntegerField()