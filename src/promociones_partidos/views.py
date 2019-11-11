from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PromocionPartido


class PromocionPartidoListView(ListView):
    model = PromocionPartido
    context_object_name = 'promociones'
    paginate_by = 5

    def get_queryset(self):
        # Devolver sólo los que estén en fecha
        return PromocionPartido.objects.all().order_by('fecha_inicio')


class PromocionPartidoDetailView(DetailView):
    model = PromocionPartido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activos'] = self.object.participantes.count()
        context['inactivos'] = 4 - self.object.participantes.count()

        return context

def inscripcion(request, promocion_id):
    promocion = PromocionPartido.objects.get(pk=promocion_id)

    if promocion.participantes.filter(id=request.user.pk).exists():
        messages.error(request, f"Ya estás inscrito en: {promocion.nombre}!")
        return redirect('promocion-list')

    if promocion.participantes.count() >= 4:
        messages.error(request, 'Límite de participantes (4) alcanzado!')
        return redirect('promocion-list')
    else:
        promocion.participantes.add(request.user)
        promocion.save()

    messages.success(request, f"Te has inscrito correctamente en: {promocion.nombre}!")
    return redirect('promocion-list')

def desinscripcion(request, promocion_id):
    promocion = PromocionPartido.objects.get(pk=promocion_id)

    if not promocion.participantes.filter(id=request.user.pk).exists():
        messages.error(request, f"Aún no te has inscrito en: {promocion.nombre}!")
        return redirect('promocion-detail', pk=promocion_id)
    else:
        promocion.participantes.remove(request.user)
        promocion.save()

    messages.success(request, f"Te has desinscrito correctamente de: {promocion.nombre}!")
    return redirect('promocion-list')
