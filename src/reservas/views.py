from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Reserva
from .forms import ReservaCreateModelForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect



class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    context_object_name = 'reservas'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Reserva.objects.filter(usuario=self.request.user).order_by('-hora_inicio')
        else:
            return Reserva.objects.all().order_by('-hora_inicio')




class ReservaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Reserva

    def test_func(self):
        return (self.request.user == self.get_object().usuario) or self.request.user.is_superuser



class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaCreateModelForm
    template_name = 'reservas/reserva_form.html'


    def form_valid(self, form):
        # Comprueba que un usuario (no admin) no tenga más de 5 reservas activas.
        if((not self.request.user.is_superuser) and (len(Reserva.objects.filter(usuario=self.request.user)) >= 5)):
            messages.error(self.request, "Límite de reservas alcanzado! (5)")
            return redirect('reserva-list')
        else:
            form.instance.usuario = self.request.user
            return super().form_valid(form)


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
        hora_inicio = self.get_object().hora_inicio
        date_now = timezone.now()
        print("date_now=>", date_now)
        print("hora_inicio=>", hora_inicio)
        # Comprueba que la resreva se cancela antes de 12 horas de su comienzo.
        if((date_now + timedelta(hours=12)) >= hora_inicio):
            print("Entra")
            messages.error(self.request, "Sólo se pueden cancelar reservas hasta 12 horas antes de su comienzo!")
            print("Entra1")
            # return redirect('reserva-list')
            return HttpResponseRedirect(reverse('reserva-detail', args=(self.get_object().pk,)))

        return super(ReservaDeleteView, self).delete(*args, **kwargs)
