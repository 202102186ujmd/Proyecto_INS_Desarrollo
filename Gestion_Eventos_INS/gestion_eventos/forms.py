from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'ubicacion', 'estado', 'privacidad', 'imagen_evento']  # Asegúrate de que 'imagen_evento' esté en el modelo
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),  # Puedes ajustar el tamaño del área de texto si deseas
        }

    # Si deseas agregar validaciones adicionales, puedes hacerlo aquí
