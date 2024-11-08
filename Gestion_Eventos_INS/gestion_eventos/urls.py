# gestion_eventos/urls.py
from django.urls import path
from . import views
from .views import EventoCreateView, EventoListView

urlpatterns = [
    path('', views.EditorDashboardView.as_view(), name='editor_dashboard'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('eventos/', EventoListView.as_view(), name='event_list'),  # Cambié 'evento_list' a 'event_list'
    path('eventos/crear/', EventoCreateView.as_view(), name='crear_evento'),  # Cambié el nombre de la ruta
]
