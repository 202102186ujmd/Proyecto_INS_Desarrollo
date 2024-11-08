# gestion_eventos/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventoForm
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class HomeView(View):
    template_name = 'gestion_eventos/index.html'

    def get(self, request):
        return render(request, self.template_name)

class EditorDashboardView(View):
    template_name = 'gestion_eventos/editor_dashboard.html'

    def get(self, request):
        return render(request, self.template_name)

class AboutView(View):
    template_name = 'gestion_eventos/about.html'

    def get(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class EventoCreateView(View):
    def get(self, request):
        form = EventoForm()
        return render(request, 'gestion_eventos/evento_form.html', {'form': form})

    def post(self, request):
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_usuario_creador = request.user
            evento.save()
            return JsonResponse({
                'success': True,
                'message': "Evento creado con éxito.",
                'evento': {
                    'id': evento.id_evento,
                    'titulo': evento.titulo,
                    'descripcion': evento.descripcion,
                    'fecha': evento.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    'ubicacion': evento.ubicacion,
                    'estado': evento.estado,
                    'privacidad': evento.privacidad
                }
            })
        else:
            print("Errores en el formulario:", form.errors)  # Añade este print para ver los errores en el servidor
            return JsonResponse({'success': False, 'errors': form.errors})
        
@method_decorator(login_required, name='dispatch')
class EventoListView(ListView):
    model = Evento
    template_name = 'gestion_eventos/evento_list.html'
    context_object_name = 'eventos'
    
    def get_queryset(self):
        return Evento.objects.all()
