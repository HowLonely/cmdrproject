from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views import View

from apps.gym_mantenimiento.models import Solicitud



# Create your views here.
class IndexView(View):
    def getSolicitudes(self):
        return Solicitud.objects.all()
    
    def get(self, request):
        solicitudes = self.getSolicitudes()
        return render(request, 'index.html', {'solicitudes': solicitudes})
    
class EncargadoSolicitudListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'encargado/solicitud_list.html'
    
    def test_func(self):
        return self.request.user.rol == 'ENCARGADO'  # Ajusta según tu modelo de roles