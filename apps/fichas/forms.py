# apps/fichas/forms.py
from django import forms
from .models import Institucion, Dimension, Pregunta, Opcion
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
