from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.contrib import messages
from .forms import UserForm, RolForm
from autenticacion.models import Usuario, Rol
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    template_name = 'administracion/admin_dashboard.html'

    def get(self, request):
        usuario = request.user
        foto_perfil = usuario.foto_perfil.url if usuario.foto_perfil else '/static/img/default_profile.png'

        context = {
            "total_users": Usuario.objects.count(),
            "total_roles": Rol.objects.count(),
            'foto_perfil': foto_perfil,
            'nombre_usuario': f"{usuario.nombre} {usuario.apellido}",
            'rol_usuario': usuario.rol.nombre if usuario.rol else 'Sin Rol'
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = Usuario
    template_name = 'administracion/user_list.html'
    context_object_name = 'usuarios'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        rol_filter = self.request.GET.get('rol', '')
        estado_filter = self.request.GET.get('estado', '')

        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(apellido__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if rol_filter:
            queryset = queryset.filter(rol__id=rol_filter)
        
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        context['roles'] = Rol.objects.all()
        context['estados'] = [('True', 'Activo'), ('False', 'Inactivo')]
        return context

    def render_to_response(self, context, **response_kwargs):
        # Verificar si es una solicitud AJAX en lugar de usar is_ajax()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            usuarios = self.get_queryset()
            data = list(usuarios.values(
                'id', 'nombre', 'apellido', 'genero', 'telefono', 
                'fecha_nacimiento', 'foto_perfil', 'rol__nombre', 'email', 'estado'
            ))
            return JsonResponse({'usuarios': data})
        
        return super().render_to_response(context, **response_kwargs)


@method_decorator(login_required, name='dispatch')
class UserCreateView(View):
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            usuarios = Usuario.objects.values(
                'id', 'nombre', 'apellido', 'genero', 'telefono',
                'fecha_nacimiento', 'foto_perfil', 'rol__nombre', 'email', 'estado'
            )
            data = list(usuarios)  # Convertimos el queryset a una lista de diccionarios
            return JsonResponse({'success': True, 'usuarios': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})


@method_decorator(login_required, name='dispatch')
class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        usuario.delete()
        
        usuarios = Usuario.objects.values(
            'id', 'nombre', 'apellido', 'genero', 'telefono',
            'fecha_nacimiento', 'foto_perfil', 'rol__nombre', 'email', 'estado'
        )
        data = list(usuarios)
        
        messages.success(request, "Usuario eliminado correctamente.")
        return JsonResponse({'success': True, 'usuarios': data})


@login_required
def profile_view(request):
    return render(request, 'administracion/profile.html', {'user': request.user})


@method_decorator(login_required, name='dispatch')
class RolListView(ListView):
    model = Rol
    template_name = 'administracion/rol_list.html'
    context_object_name = 'roles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RolForm()
        return context


@method_decorator(login_required, name='dispatch')
class RolCreateEditView(View):
    def get(self, request, *args, **kwargs):
        rol_id = request.GET.get('rol_id')
        rol = get_object_or_404(Rol, id=rol_id) if rol_id else None
        form = RolForm(instance=rol)
        return render(request, 'administracion/rol_form.html', {'form': form, 'rol': rol})

    def post(self, request, *args, **kwargs):
        rol_id = request.POST.get('rol_id')
        rol = get_object_or_404(Rol, id=rol_id) if rol_id else None
        form = RolForm(request.POST, instance=rol)

        if form.is_valid():
            form.save()
            action = 'actualizado' if rol_id else 'creado'
            messages.success(request, f'Rol {action} correctamente.')
            return redirect('rol_list')

        roles = Rol.objects.all()
        return render(request, 'administracion/rol_list.html', {'form': form, 'roles': roles})


@method_decorator(login_required, name='dispatch')
class RolDeleteView(View):
    def post(self, request, *args, **kwargs):
        rol_id = request.POST.get('rol_id')
        rol = get_object_or_404(Rol, id=rol_id)
        rol.delete()
        messages.success(request, "Rol eliminado correctamente.")
        return redirect('rol_list')
