from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Modelo de roles
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

# Extender el modelo de usuario de Django
class Usuario(AbstractUser):
    # Campos personales
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)

    # Campos de cuenta
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(unique=True)  # Usa el campo de AbstractUser
    estado = models.BooleanField(default=True)  # True para activo, False para bloqueado
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    # Auditoría de actividad
    fecha_registro = models.DateTimeField(blank=True, null=True)  # Eliminar auto_now_add=True para evitar errores
    ultima_actividad = models.DateTimeField(blank=True, null=True)
    fecha_cambio_contrasena = models.DateTimeField(blank=True, null=True)

    # Métodos adicionales
    def lock_user(self):
        """Bloquea al usuario y reinicia los intentos fallidos"""
        self.is_locked = True
        self.failed_attempts = 0
        self.estado = False  # Cambia el estado a inactivo
        self.save()
    
    def reset_failed_attempts(self):
        """Reinicia el conteo de intentos fallidos"""
        self.failed_attempts = 0
        self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

    def save(self, *args, **kwargs):
        """Guardar la última actividad al actualizar el usuario"""
        if not self.fecha_registro:
            self.fecha_registro = timezone.now()  # Asigna una fecha de registro si no está configurada
        self.ultima_actividad = timezone.now()
        super().save(*args, **kwargs)
