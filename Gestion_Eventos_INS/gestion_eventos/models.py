from django.db import models
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL

class Evento(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Cancelado', 'Cancelado'),
    ]
    
    PRIVACIDAD_CHOICES = [
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='Activo')
    privacidad = models.CharField(max_length=50, choices=PRIVACIDAD_CHOICES, default='Publico')
    
    # Cambia esta línea para usar AUTH_USER_MODEL
    id_usuario_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    
    # Campos adicionales que podrías considerar
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    imagen_evento = models.ImageField(upload_to='eventos/', blank=True, null=True)  # Para añadir una imagen del evento

    def __str__(self):
        return self.titulo
