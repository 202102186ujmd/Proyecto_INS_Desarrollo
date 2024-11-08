# autenticacion/forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Usuario, Rol  # Importa Rol para el campo de rol

# Formulario de restablecimiento de contraseña personalizado
class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = Usuario.objects.filter(email=email, is_active=True, is_locked=False)
        return (u for u in active_users if u.has_usable_password())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Usuario.objects.filter(email=email, is_locked=False).exists():
            raise forms.ValidationError("No existe ningún usuario registrado con este correo electrónico.")
        return email

# Formulario de creación de usuario personalizado
class UsuarioCreationForm(forms.ModelForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True, label="Rol")  # Agrega el campo de rol

    class Meta:
        model = Usuario
        fields = [
            'username',
            'password',
            'nombre',
            'apellido',
            'genero',
            'rol',  # Incluye el campo de rol aquí
            'email',
            'telefono',
            'fecha_nacimiento',
            'foto_perfil',
            'estado',
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ocultar campos de control si es el formulario de creación
        if not self.instance.pk:
            self.fields.pop('fecha_registro', None)
            self.fields.pop('ultima_actividad', None)
            self.fields.pop('fecha_cambio_contrasena', None)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("El campo de contraseña es obligatorio.")
        return password
