from django.contrib import admin

from .models import PromocionPartido
from reservas.models import Reserva


class PromocionPartidoAdmin(admin.ModelAdmin):
    fields = ['nombre', 'fecha_inicio', 'cerrado', 'cancelado', 'reserva', 'participantes']

    def delete_view(self, request, object_id, extra_context=None):
        # Eliminar también la reserva para esa promocion en caso de que la tenga
        promocion = self.get_object(request, object_id)
        if promocion.reserva:
            reserva = Reserva.objects.get(pk=promocion.reserva.pk)
            reserva.delete()
        return super(PromocionPartidoAdmin, self).delete_view(request, object_id, extra_context=extra_context)

admin.site.register(PromocionPartido, PromocionPartidoAdmin)
