from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario 
ESTILO_BASE = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-brand-600 focus:border-brand-600 block w-full p-2.5"
ESTILO_ERROR = "bg-red-50 border border-red-500 text-red-900 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5"

class LoginForm(AuthenticationForm):
    """Formulario de Login personalizado con estilos Bootstrap"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True
        }),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña'
        }),
        label="Contraseña"
    )

# --- 2. FORMULARIO DE PERFIL (Con Validaciones Nuevas) ---
class PerfilForm(forms.ModelForm):
    sexo = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': ESTILO_BASE}), # Le pasamos el estilo aquí directo
        label="Sexo"
    )
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'dni', 'telefono', 'direccion', 'fecha_nacimiento', 'sexo']
        
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['dni'].widget.attrs.update({        
            'placeholder': 'DNI (8) o CE (9)',
            'maxlength': '12', # Damos holgura para CE o Pasaportes
            'inputmode': 'numeric', # Quita esto si quieres aceptar letras de pasaportes antiguos
            # Usamos un oninput que permite números Y letras (para pasaportes/CE antiguos)
            # Si quieres SOLO números para CE moderno, usa: .replace(/[^0-9]/g, '')
            'oninput': "this.value = this.value.replace(/[^0-9]/g, '')" 
        })

        # Ejemplo: El Teléfono con un fondo ligeramente azul
        self.fields['telefono'].widget.attrs.update({
            'placeholder': '9 dígitos',
            # Candado 1: Límite de caracteres
            'maxlength': '9',
            'minlength': '9', # Opcional: Para avisar si escribió menos
            # Candado 2: Teclado numérico en móviles
            'inputmode': 'numeric',
            # Candado 3: Javascript que borra letras automáticamente
            'oninput': "this.value = this.value.replace(/[^0-9]/g, '')"
        })

        # Ejemplo: Nombres y Apellidos (Estilo estándar pero quizás con mayúsculas visuales)
        self.fields['nombres'].widget.attrs.update({
            # Expresión regular: Solo letras (a-z), acentos y espacios
            'pattern': "[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", 
            'title': 'Por favor, ingrese solo letras (sin números ni símbolos)',
            # Opcional: JavaScript para bloquear números mientras escriben
            'oninput': "this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]/g, '')" 
        })
        self.fields['apellidos'].widget.attrs.update({
            # Expresión regular: Solo letras (a-z), acentos y espacios
            'pattern': "[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", 
            'title': 'Por favor, ingrese solo letras (sin números ni símbolos)',
            # Opcional: JavaScript para bloquear números mientras escriben
            'oninput': "this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]/g, '')" 
        })


        # Aplicar el estilo base a todos los campos que no tengan uno específico
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ESTILO_BASE

    # --- ZONA DE VALIDACIONES ---

    def clean_apellidos(self):
        """Valida que los apellidos no contengan números ni caracteres especiales"""
        apellidos = self.cleaned_data.get('apellidos')
        
        if not apellidos:
            return apellidos # Si está vacío, lo dejamos pasar (o lanza error si es requerido en modelo)

        if not all(c.isalpha() or c.isspace() for c in apellidos):
            raise ValidationError("Los apellidos solo deben contener letras.")
            
        return apellidos

    def clean_nombres(self):
        """Valida que los nombres no contengan números ni caracteres especiales"""
        nombres = self.cleaned_data.get('nombres')
        
        if not nombres:
            return nombres # Si está vacío, lo dejamos pasar (o lanza error si es requerido en modelo)

        if not all(c.isalpha() or c.isspace() for c in nombres):
            raise ValidationError("Los nombres solo deben contener letras.")
            
        return nombres

    def clean_telefono(self):
        """Valida que el teléfono sean 9 dígitos numéricos"""
        telefono = self.cleaned_data.get('telefono')
        
        if not telefono:
            return telefono # Si está vacío, lo dejamos pasar (o lanza error si es requerido en modelo)

        if not telefono.isdigit():
            raise ValidationError("El teléfono solo debe contener números.")
        
        if len(telefono) != 9:
            raise ValidationError("El teléfono debe tener exactamente 9 dígitos.")
            
        return telefono

    def clean_dni(self):
        documento = self.cleaned_data.get('dni')
        
        if not documento:
            return documento

        # 1. Validación de solo números (Si tu sistema solo acepta CE numéricos)
        if not documento.isdigit():
             raise ValidationError("El documento solo debe contener números.")

        # 2. Validación de Longitud (Aquí está el cambio clave)
        longitud = len(documento)
        
        # Si tiene 8 es DNI, si tiene 9 es CE, si tiene otro número es error
        if longitud not in [8, 9]: 
            raise ValidationError("El documento debe tener 8 dígitos (DNI) o 9 dígitos (CE).")
            
        # 3. Validación de duplicados (Igual que antes)
        if Usuario.objects.filter(dni=documento).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este documento ya está registrado.")

        return documento
    
# --- 3. FORMULARIO DE ADMINISTRACIÓN DE USUARIOS (Crear/Editar) ---
class UsuarioAdminForm(forms.ModelForm):
    # --- CAMPOS EXTRAS ---
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'class': ESTILO_BASE}),
        label="Contraseña"
    )

    rol = forms.ChoiceField(
        choices=Usuario.ROLES, 
        widget=forms.Select(attrs={'class': ESTILO_BASE, 'id': 'select-rol', 'onchange': 'toggleCampos()'}),
        label="Rol del Sistema"
    )

    sexo = forms.ChoiceField(
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        widget=forms.Select(attrs={'class': ESTILO_BASE}),
        label="Sexo"
    )

    class Meta:
        model = Usuario
        fields = [
            # Generales
            'email', 'nombres', 'apellidos', 'dni', 'rol', 'is_active', 
            'telefono', 'direccion', 'fecha_nacimiento', 'sexo', 'edad',
            # Supervisor
            'profesion', 'numero_colegiatura', 'centro_labores',
            # Encuestador
            'codigo', 'institucion_procedencia', 'ciclo', 'especialidad', 
            'supervisor_asignado', 'institucion_asignada'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user_sesion = kwargs.pop('user_sesion', None)
        super().__init__(*args, **kwargs)
        
        # 1. Aplicar estilos base a TODO
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ESTILO_BASE
        
        self.fields['nombres'].required = True
        self.fields['apellidos'].required = True
        self.fields['email'].required = True
        self.fields['dni'].required = True
        self.fields['telefono'].required = True
        self.fields['direccion'].required = True # Agregado según tu petición
        
        campos_condicionales = [
            'institucion_procedencia', 
            'codigo', 'ciclo', 'especialidad', 'supervisor_asignado', 'institucion_asignada', # Encuestador
            'profesion', 'numero_colegiatura', 'centro_labores' # Supervisor
        ]

        for campo in campos_condicionales:
            if campo in self.fields:
                self.fields[campo].required = False

        # 7. LÓGICA DE PERMISOS (Aquí usamos self.user_sesion que capturamos arriba)
        # if self.user_sesion and self.user_sesion.rol == 'SUPERVISOR':
        #     if 'rol' in self.fields:
        #         self.fields['rol'].widget = forms.HiddenInput()
        #         self.fields['rol'].initial = 'ENCUESTADOR'
            
        #     if 'supervisor_asignado' in self.fields:
        #         self.fields['supervisor_asignado'].widget = forms.HiddenInput()

        # 2. Checkbox bonito
        self.fields['is_active'].widget.attrs.update({'class': 'w-5 h-5 text-brand-600 rounded focus:ring-brand-500 border-gray-300'})

        # 3. Validaciones visuales específicas
        self.fields['dni'].widget.attrs.update({'oninput': "this.value = this.value.replace(/[^0-9]/g, '')", 'maxlength': '12'})
        self.fields['telefono'].widget.attrs.update({'oninput': "this.value = this.value.replace(/[^0-9]/g, '')", 'maxlength': '9'})

        # 4. Placeholder de contraseña
        if self.instance.pk:
            self.fields['password'].widget.attrs['placeholder'] = "Dejar vacío para mantener la actual"
        else:
            self.fields['password'].required = True
            self.fields['password'].widget.attrs['placeholder'] = "Contraseña inicial obligatoria"
        
        self.fields['nombres'].widget.attrs.update({
            # Expresión regular: Solo letras (a-z), acentos y espacios
            'pattern': "[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", 
            'title': 'Por favor, ingrese solo letras (sin números ni símbolos)',
            # Opcional: JavaScript para bloquear números mientras escriben
            'oninput': "this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]/g, '')" 
        })

        self.fields['apellidos'].widget.attrs.update({
            # Expresión regular: Solo letras (a-z), acentos y espacios
            'pattern': "[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", 
            'title': 'Por favor, ingrese solo letras (sin números ni símbolos)',
            # Opcional: JavaScript para bloquear números mientras escriben
            'oninput': "this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]/g, '')" 
        })

# --- VALIDACIÓN (SOLO VERIFICA QUE DATOS NO FALTEN) ---
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')

        if rol == 'SUPERVISOR':
            if not cleaned_data.get('profesion'): self.add_error('profesion', 'Campo obligatorio.')
            if not cleaned_data.get('numero_colegiatura'): self.add_error('numero_colegiatura', 'Campo obligatorio.')
            if not cleaned_data.get('centro_labores'): self.add_error('centro_labores', 'Campo obligatorio.')

        if rol == 'ENCUESTADOR':
            if not cleaned_data.get('codigo'): self.add_error('codigo', 'Campo obligatorio.')
            if not cleaned_data.get('ciclo'): self.add_error('ciclo', 'Campo obligatorio.')
            if not cleaned_data.get('especialidad'): self.add_error('especialidad', 'Campo obligatorio.')
            if not cleaned_data.get('institucion_procedencia'): self.add_error('institucion_procedencia', 'Campo obligatorio.')

        return cleaned_data

    # --- GUARDADO CON LIMPIEZA PROFUNDA (AQUÍ ESTÁ LA SOLUCIÓN) ---
    def save(self, commit=True):
        # 1. Obtenemos la instancia pero NO la guardamos aún
        user = super().save(commit=False)
        
        # 2. Detectamos el ROL final
        rol = self.cleaned_data.get('rol')

        # 3. LIMPIEZA AGRESIVA SEGÚN ROL
        # Nota: Los CharField se limpian con "" (vacío), los ForeignKey con None (nulo)
        
        if rol == 'ADMIN':
            # Admin no tiene nada de lo demás
            user.profesion = ""
            user.numero_colegiatura = ""
            user.centro_labores = ""
            user.codigo = ""
            user.institucion_procedencia = "Universidad Nacional de Trujillo – UNT" # Valor por defecto
            user.ciclo = ""
            user.especialidad = ""
            user.supervisor_asignado = None
            user.institucion_asignada = None

        elif rol == 'SUPERVISOR':
            # Supervisor no tiene datos de alumno
            user.codigo = ""
            # user.institucion_procedencia = "" # Opcional: Si quieres limpiarlo o dejar el default
            user.ciclo = ""
            user.especialidad = ""
            user.supervisor_asignado = None
            user.institucion_asignada = None

        elif rol == 'ENCUESTADOR':
            # Encuestador no tiene datos de profesional
            user.profesion = ""
            user.numero_colegiatura = ""
            user.centro_labores = ""

        # 4. Contraseña
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        # 5. Guardado final
        if commit:
            user.save()
            
        return user

    def estilar_errores(self):
        for field_name in self.errors:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['class'] = ESTILO_ERROR

# --- 4. FORMULARIO SIMPLIFICADO PARA SUPERVISOR CREE ENCUESTADORES ---
class EncuestadorForm(UsuarioAdminForm):
    """ Formulario simplificado para que el Supervisor cree Encuestadores """
    class Meta:
        model = Usuario
        # Solo pedimos datos personales y académicos
        fields = [
            'nombres', 'apellidos', 'dni', 'email', 'telefono', 'direccion', 
            'codigo', 'ciclo', 'especialidad', 'institucion_procedencia','institucion_asignada','fecha_nacimiento','edad',
            'password', 'is_active' # Password es necesario para crear
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña temporal', 'class': 'w-full ...'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Eliminamos campos que hereda del padre pero no queremos ver
        campos_prohibidos = ['rol', 'supervisor_asignado', 'profesion', 'numero_colegiatura', 'centro_labores']
        for campo in campos_prohibidos:
            if campo in self.fields:
                del self.fields[campo]
        
        # Ajustamos textos para que sean amigables
        self.fields['codigo'].label = "Código de Alumno/Agente de campo"
        self.fields['institucion_procedencia'].label = "Universidad / Instituto"

        self.fields['nombres'].required = True
        self.fields['apellidos'].required = True
        self.fields['fecha_nacimiento'].required = True
        self.fields['edad'].required = True
        self.fields['email'].required = True
        self.fields['dni'].required = True
        self.fields['telefono'].required = True
        self.fields['direccion'].required = True 
        # Campos condicionales
        campos_condicionales = [
            'institucion_procedencia', 
            'codigo', 'ciclo', 'especialidad', 'institucion_asignada'
        ]
        for campo in campos_condicionales:
            if campo in self.fields:
                self.fields[campo].required = True
        