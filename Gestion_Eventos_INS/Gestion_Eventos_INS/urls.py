# Gestion_Eventos_INS/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from gestion_eventos.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include('autenticacion.urls')),  # Incluir las URLs de autenticación
    path('admin_dashboard/', include('administracion.urls')),  # Rutas del módulo de administración
    path('editor_dashboard/', include('gestion_eventos.urls')),  # Rutas del módulo de gestión de eventos
    path('participante_dashboard/', include('participantes.urls')),  # Rutas del módulo de participantes
    path('', HomeView.as_view(), name='home'),
    path('administracion/', include('administracion.urls')),
        path('gestion_eventos/', include('gestion_eventos.urls')),
]

# Agrega esta línea para servir archivos de medios en desarrollo
if settings.DEBUG:  # Solo para desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
