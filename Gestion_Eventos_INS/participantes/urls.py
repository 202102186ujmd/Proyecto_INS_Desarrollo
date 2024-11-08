# participantes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParticipanteDashboardView.as_view(), name='participante_dashboard'),
    # Rutas adicionales para inscripciones y participación en eventos
]
