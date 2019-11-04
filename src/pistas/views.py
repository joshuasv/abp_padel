from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Pista

# Create your views here.

class PistaListView(LoginRequiredMixin, ListView):
    model = Pista
    # template_name = 'pista/pistas.html'
    context_object_name = 'pistas'
    # añadir el paginate_by

class PistaDetailView(LoginRequiredMixin, DetailView):
    model = Pista

class PistaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pista
    fields = ['nombre', 'hora_apertura', 'hora_cierre']

    def test_func(self):
        return self.request.user.is_superuser

class PistaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pista
    fields = ['nombre', 'hora_apertura', 'hora_cierre']

    def test_func(self):
        return self.request.user.is_superuser

class PistaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pista
    success_url = '/pista/'

    def test_func(self):
        return self.request.user.is_superuser
