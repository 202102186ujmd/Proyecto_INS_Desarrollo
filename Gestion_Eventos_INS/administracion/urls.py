# administracion/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    AdminDashboardView,
    profile_view,
    UserListView, UserCreateView, UserDeleteView,
    RolListView, RolCreateEditView, RolDeleteView,
)

urlpatterns = [
    
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Rutas para usuarios
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('usuario/crear/', UserCreateView.as_view(), name='crear_usuario'),
    path('usuario/eliminar/', UserDeleteView.as_view(), name='eliminar_usuario'),
    

    # Rutas para roles
    path('rol_list/', RolListView.as_view(), name='rol_list'),
    path('roles/crear/', RolCreateEditView.as_view(), name='crear_rol'),  # Crear rol
    path('roles/editar/<int:rol_id>/', RolCreateEditView.as_view(), name='editar_rol'),  # Editar rol
    path('roles/eliminar/', RolDeleteView.as_view(), name='eliminar_rol'),  # Eliminar rol
]
