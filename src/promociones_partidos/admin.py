from django.contrib import admin

from .models import PromocionPartido


class PromocionPartidoAdmin(admin.ModelAdmin):
    fields = ['nombre', 'fecha_inicio', 'reserva', 'participantes']


admin.site.register(PromocionPartido, PromocionPartidoAdmin)
