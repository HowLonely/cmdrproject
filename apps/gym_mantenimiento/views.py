from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views import View



# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class EncargadoSolicitudListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'encargado/solicitud_list.html'
    
    def test_func(self):
        return self.request.user.rol == 'ENCARGADO'  # Ajusta según tu modelo de roles