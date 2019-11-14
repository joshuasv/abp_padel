from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Campeonato, Normativa, Pareja


class CampeonatoListView(ListView):
    model = Campeonato
    context_object_name = 'campeonatos'
    paginate_by = 5
    # Campeonato.make_parejas(Campeonato.objects.get(pk=1))
    # Campeonato.make_groups(Campeonato.objects.get(pk=1))
    Campeonato.make_enfrentamientos_liga_regular(Campeonato.objects.get(pk=1))

    def get_queryset(self):
        return Campeonato.objects.all().order_by('inicio_campeonato')


class CampeonatoDetailView(LoginRequiredMixin, DetailView):
    model = Campeonato

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        normativas = Normativa.objects.filter(campeonato=self.object.id)
        parejas = Pareja.objects.filter(capitan=self.request.user)
        context['normativas'] = normativas
        context['parejas'] = parejas

        return context



def inscripcion(request, campeonato_id):
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
