from datetime import datetime, timedelta

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from pistas.models import HorarioPista
from .models import Reserva
from .forms import ReservaCreateModelForm


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    context_object_name = 'reservas'

    def get_queryset(self):
        return Reserva.get_reservas_activas(self.request.user)


class ReservaHistorialView(LoginRequiredMixin, ListView):
    model = Reserva
    context_object_name = 'reservas'
    template_name = 'reservas/reserva_historial.html'

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)


class ReservaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Reserva

    def test_func(self):
        self.get_object().is_ultima_pista()
        return (self.request.user == self.get_object().usuario) or self.request.user.is_superuser


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaCreateModelForm
    template_name = 'reservas/reserva_form.html'
    # success_url = reverse('reserva-list')

    def form_valid(self, form):
        if((not self.request.user.is_superuser) and (len(Reserva.get_reservas_activas(self.request.user)) >= 5)):
            messages.error(self.request, "Límite de reservas alcanzado! (5)")
            return redirect('reserva-list')
        else:
            form.instance.usuario = self.request.user
        return super().form_valid(form)


def load_horario_pista(request):
    pista_id = request.GET.get('pista')
    horario_pista = HorarioPista.objects.filter(pista_id=pista_id)
    return render(request, 'reservas/horario_pista_dropdown_list_options.html', {'horario_pista': horario_pista})


class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reserva
    template_name = 'reservas/reserva_form.html'
    form_class = ReservaCreateModelForm

    def test_func(self):
        return (self.request.user == self.get_object().usuario) or self.request.user.is_superuser

class ReservaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reserva
    success_url = '/reserva/'

    def test_func(self):
        user_is_authorized = (self.request.user == self.get_object().usuario) or self.request.user.is_superuser

        return user_is_authorized

    def delete(self, *args, **kwargs):
        hora_inicio = self.get_object().horario_pista.hora_inicio
        fecha = self.get_object().fecha
        date_time = datetime.combine(fecha, hora_inicio)
        now = datetime.now()
        if(now + timedelta(hours=12) >= date_time):
            messages.error(self.request, "Sólo se pueden cancelar reservas hasta 12 horas antes de su comienzo!")
            return HttpResponseRedirect(reverse('reserva-list'))
        return super(ReservaDeleteView, self).delete(*args, **kwargs)
