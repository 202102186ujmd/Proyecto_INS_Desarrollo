# autenticacion/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone  # Importa timezone para manejar la fecha y hora
from .forms import CustomPasswordResetForm  # Importa el formulario personalizado para restablecimiento de contraseña



# Obtener el modelo de usuario personalizado
Usuario = get_user_model()

# Vista personalizada para el inicio de sesión
class CustomLoginView(LoginView):
    template_name = 'autenticacion/login.html'
    
    def form_valid(self, form):
        usuario = form.get_user()
        
        # Verificar si el usuario está bloqueado
        if usuario.is_locked:
            messages.error(self.request, "Tu cuenta está bloqueada. Contacta al administrador.")
            return redirect('login')
        
        # Reinicia los intentos fallidos y actualiza la última actividad si el inicio de sesión es exitoso
        usuario.reset_failed_attempts()
        usuario.ultima_actividad = timezone.now()  # Actualiza la última actividad
        usuario.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Obtiene el nombre de usuario ingresado
        email = form.data.get('username')
        try:
            # Buscar al usuario en la base de datos
            usuario = Usuario.objects.get(username=email)
            usuario.failed_attempts += 1
            
            # Bloquea al usuario si tiene 3 intentos fallidos
            if usuario.failed_attempts >= 3:
                usuario.lock_user()
                messages.error(self.request, "Tu cuenta ha sido bloqueada debido a múltiples intentos fallidos.")
            else:
                usuario.save()
                messages.error(self.request, f"Intento fallido. Te quedan {3 - usuario.failed_attempts} intentos.")
        except Usuario.DoesNotExist:
            messages.error(self.request, "El usuario no existe.")
        
        return super().form_invalid(form)

    def get_success_url(self):
        usuario = self.request.user
        # Redirecciona según el rol del usuario
        if usuario.rol and usuario.rol.nombre == 'Administrador':
            return reverse_lazy('admin_dashboard')
        elif usuario.rol and usuario.rol.nombre == 'Editor':
            return reverse_lazy('editor_dashboard')
        elif usuario.rol and usuario.rol.nombre == 'Participante':
            return reverse_lazy('participante_dashboard')
        else:
            return reverse_lazy('home')

# Vista personalizada para solicitar restablecimiento de contraseña
class CustomPasswordResetView(PasswordResetView):
    template_name = 'autenticacion/password_reset.html'
    form_class = CustomPasswordResetForm  # Usar el formulario personalizado
    success_url = reverse_lazy('password_reset_done')

# Vista personalizada para mostrar mensaje de correo enviado
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'autenticacion/password_reset_done.html'

# Vista personalizada para establecer nueva contraseña después de hacer clic en el enlace
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'autenticacion/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# Vista personalizada para el mensaje de confirmación final de restablecimiento de contraseña
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'autenticacion/password_reset_complete.html'
