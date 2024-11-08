# participantes/views.py
from django.shortcuts import render
from django.views import View

class ParticipanteDashboardView(View):
    template_name = 'participantes/participante_dashboard.html'  # Asegúrate de tener esta plantilla

    def get(self, request):
        return render(request, self.template_name)
