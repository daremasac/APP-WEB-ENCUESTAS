# apps/fichas/forms.py
from django import forms
from .models import Institucion, Dimension, Pregunta, Opcion, FichaEvaluacion
from django.forms import inlineformset_factory

class TailwindModelForm(forms.ModelForm):
    """Clase base para inyectar estilos Tailwind a todos los inputs automáticamente"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Estilo base para inputs
            clases = "w-full rounded-lg border-gray-300 bg-gray-50 px-4 py-2.5 text-gray-900 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm"
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = "w-5 h-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            else:
                field.widget.attrs['class'] = clases

class InstitucionForm(TailwindModelForm):
    class Meta:
        model = Institucion
        fields = ['codigo_modular', 'nombre', 'direccion', 'telefono', 'nombre_contacto', 'correo_contacto']

class DimensionForm(TailwindModelForm):
    class Meta:
        model = Dimension
        fields = ['nombre', 'descripcion', 'orden']

class PreguntaForm(TailwindModelForm):
    class Meta:
        model = Pregunta
        fields = ['dimension', 'orden', 'enunciado']
        widgets = {
            'enunciado': forms.Textarea(attrs={'rows': 3}),
        }

class OpcionForm(TailwindModelForm):
    """Formulario individual para cada fila de opción"""
    class Meta:
        model = Opcion
        fields = ['texto', 'puntaje']
        widgets = {
            'texto': forms.TextInput(attrs={'placeholder': 'Ej: Siempre / A veces'}),
            'puntaje': forms.NumberInput(attrs={'placeholder': '0'}),
        }

OpcionFormSet = inlineformset_factory(
    parent_model=Pregunta,
    model=Opcion,
    form=OpcionForm,
    extra=0,            # Cuántas filas vacías mostrar al inicio (0 para limpieza)
    can_delete=True,    # Permitir borrar opciones
    min_num=1,          # Mínimo 1 opción requerida (opcional)
    validate_min=True
)

from apps.ubigeo.models import Departamento, Provincia, Distrito

class FichaEvaluacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicamos clases de Tailwind a todos los campos automáticamente
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            })
        # Lógica de carga para Edición
        if self.instance.pk:
            if self.instance.ubigeo_departamento:
                # Cargamos las provincias de ese departamento
                self.fields['ubigeo_provincia'].queryset = Provincia.objects.filter(
                    departamento=self.instance.ubigeo_departamento
                )
            if self.instance.ubigeo_provincia:
                # Cargamos los distritos de esa provincia
                self.fields['ubigeo_distrito'].queryset = Distrito.objects.filter(
                    provincia=self.instance.ubigeo_provincia
                )

    class Meta:
        model = FichaEvaluacion
        fields = [
            'nombres_evaluado', 'apellidos_evaluado', 'dni_evaluado', 
            'fecha_nacimiento','edad_evaluado','sexo_evaluado', 'direccion_domicilio','nivel_educativo','ubigeo_departamento', 'ubigeo_provincia', 'ubigeo_distrito', 
            'telefono_contacto', 'email_contacto', 'emergencia_nombres','emergencia_telefono', 'emergencia_parentesco',
            'jefe_hogar', 'observaciones_familia'
         
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'observaciones_familia': forms.Textarea(attrs={'rows': 2}),
        }