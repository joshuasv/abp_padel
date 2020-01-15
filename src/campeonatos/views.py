from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView, FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q

from .forms import EnvioEnfrentamientoForm
from .models import Campeonato, Normativa, Pareja, Enfrentamiento, Grupo
from reservas.models import Reserva
from pistas.models import HorarioPista, Pista
from users.models import User


class CampeonatoListView(ListView):
    model = Campeonato
    context_object_name = 'campeonatos'
    paginate_by = 5

    def get_queryset(self):
        return Campeonato.objects.all().order_by('-fin_inscripciones')


class CampeonatoDetailView(LoginRequiredMixin, DetailView):
    model = Campeonato

    def get_context_data(self, **kwargs):
        # Hace los grupos si se excede la fecha de inscripcion
        # Y si todavía no han sido creado enfrentamintos para el campeonato
        if (Enfrentamiento.objects.filter(campeonato=self.get_object()).count() <= 0) and (Grupo.objects.filter().count() <= 0):
            self.get_object().make_groups()
            self.get_object().make_enfrentamientos_liga_regular()

        context = super().get_context_data(**kwargs)
        normativas = Normativa.objects.filter(campeonato=self.object.id)
        parejas = Pareja.objects.filter(capitan=self.request.user)
        pareja = Pareja.objects.filter(Q(miembro=self.request.user) | Q(capitan=self.request.user)).filter(normativa__in=normativas)
        primera_ronda = Enfrentamiento.objects.filter(Q(pareja_1__in=pareja) | Q(pareja_2__in=pareja)).filter(ronda=0)
        cuartos = Enfrentamiento.objects.filter(Q(pareja_1__in=pareja) | Q(pareja_2__in=pareja)).filter(ronda=1)
        context['normativas'] = normativas
        context['parejas'] = parejas
        context['pareja'] = pareja.first()
        context['primera_ronda'] = primera_ronda
        context['cuartos'] = cuartos

        return context


class EnfrentamientoFormView(LoginRequiredMixin, FormView):
    model = Enfrentamiento
    form_class = EnvioEnfrentamientoForm
    template_name = 'campeonatos/enfrentamiento_detail.html'

    def form_valid(self, form):
        fecha = form.cleaned_data.get('fecha')
        if(fecha):
            enfrentamiento = self.get_context_data()['enfrent']
            enfrentamiento.fecha = fecha
            if enfrentamiento.turno_fecha == '1':
                enfrentamiento.turno_fecha = '2'
            else:
                enfrentamiento.turno_fecha = '1'
            enfrentamiento.save()
            print(form.cleaned_data.get('fecha'))
            messages.info(self.request, "Petición de enfrentamiento enviada al otro equipo!")
            return redirect('enfrentamiento-detail', pk=enfrentamiento.pk)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs);

        enfrentamiento = Enfrentamiento.objects.get(pk=self.kwargs['pk'])
        context['enfrent'] = enfrentamiento
        if (enfrentamiento.pareja_1.capitan.id == self.request.user.id) or (enfrentamiento.pareja_1.miembro.id == self.request.user.id):
            context['pareja'] = enfrentamiento.pareja_1
            context['num_pareja'] = '1'
        else:
            context['pareja'] = enfrentamiento.pareja_2
            context['num_pareja'] = '2'

        return context


def inscripcion(request, campeonato_id):

    # Comprobar inscripcion fuera de fecha
    print(timezone.now())
    print(Campeonato.objects.get(pk=campeonato_id).fin_inscripciones)
    if timezone.now() >= Campeonato.objects.get(pk=campeonato_id).fin_inscripciones:
        messages.error(request, "El periodo de inscripciones ha finalizado!")
        return redirect('campeonato-list')

    try:
        selected_normativa = Normativa.objects.get(pk=request.POST['normativa'])
    except(KeyError, Normativa.DoesNotExist):
        messages.error(request, "Escoge una normativa!")
        return redirect('campeonato-detail', pk=campeonato_id)

    try:
        selected_pareja = Pareja.objects.get(pk=request.POST['parejas'])
    except(KeyError, Pareja.DoesNotExist):
        messages.error(request, "Escoge una pareja!")
        return redirect('campeonato-detail', pk=campeonato_id)

    # Solo el capitan puede inscribir en un campeonato
    if (selected_pareja.capitan.sex == selected_normativa.categoria) and (selected_pareja.miembro.sex == selected_normativa.categoria):
        selected_pareja.normativa = selected_normativa
        selected_pareja.save()
        messages.success(request, "Tu pareja ha sido inscrita correctamente!")
        return redirect('campeonato-list')
    else:
        messages.error(request, "La pareja no cumple la normativa!")
        return redirect('campeonato-detail', pk=campeonato_id)



def desinscripcion(request, campeonato_id):
    try:
        selected_pareja = Pareja.objects.get(pk=request.POST['pareja_placeholder'])
    except:
        messages.error(request, "Escoge una pareja!")
        return redirect('campeonato-detail', pk=campeonato_id)

    if not selected_pareja.normativa:
        messages.error(request, "Esta pareja no esta registrada!")
        return redirect('campeonato-detail', pk=campeonato_id)
    else:
        selected_pareja.normativa = None;
        selected_pareja.save()

    messages.success(request, "Tu pareja ha sido desinscrita correctamente!")
    return redirect('campeonato-list')

def aceptar_enfrentamiento(request, pk):
    enfrentamiento = Enfrentamiento.objects.get(pk=pk)
    horarios_pistas = HorarioPista.objects.all()

    # Eliminar los horarios que no estén libres
    reservas = Reserva.objects.filter(fecha=enfrentamiento.fecha)
    for reserva in reservas:
        horarios_pistas = horarios_pistas.exclude(pk=reserva.horario_pista.pk)
    # Si hay huecos para ese día hacer la reserva
    if len(horarios_pistas) > 0:
        # Marcar enfrentamiento aceptado
        enfrentamiento.acepto_pareja = True
        horario = horarios_pistas.first()
        reserva = Reserva.objects.create(
            usuario=User.objects.get(pk=1),
            pista=horario.pista,
            horario_pista=horario,
            fecha=enfrentamiento.fecha)
        reserva.save()
        enfrentamiento.reserva = reserva
        enfrentamiento.save()
    else: # No hay huecos, volver a establecer fecha
        messages.error(request, "Escoge otra fecha! No hay huecos disponibles!")
        enfrentamiento.fecha = None;
        return redirect('enfrentamiento-detail', pk=pk)

    messages.success(request, "Enfrentamiento aceptado!")
    return redirect('enfrentamiento-detail', pk=pk)


def rechazar_enfrentamiento(request, pk):
    enfrentamiento = Enfrentamiento.objects.get(pk=pk)
    # Eliminar la fecha
    enfrentamiento.fecha = None

    enfrentamiento.save()
    return redirect('enfrentamiento-detail', pk=pk)

def clasificacion(request, pareja_id):
    pareja = Pareja.objects.get(id=pareja_id)
    parejas_campeonato = Pareja.objects.filter(normativa=pareja.normativa)
    # Ordenar parejas por puntos
    parejas_campeonato = parejas_campeonato.order_by('-puntuacion_clasificacion')

    context = {'campeonato': pareja.normativa.campeonato, 'parejas': parejas_campeonato, 'p': pareja }


    return render(request, 'campeonatos/clasificacion.html', context)
