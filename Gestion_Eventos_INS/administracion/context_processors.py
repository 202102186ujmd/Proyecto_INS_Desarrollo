# administracion/context_processors.py
from autenticacion.models import Usuario  # Importar desde autenticacion.models en lugar de administracion.models

def user_info(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto_perfil = usuario.foto_perfil.url if usuario.foto_perfil else '/static/img/default_profile.png'
        return {
            'foto_perfil': foto_perfil,
            'nombre_usuario': f"{usuario.nombre} {usuario.apellido}",
            'rol_usuario': usuario.rol.nombre if usuario.rol else 'Sin Rol',
        }
    return {}
