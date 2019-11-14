from datetime import timedelta

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from reservas.models import Reserva
from pistas.models import Pista
from users.models import User

class PromocionPartido(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        blank=True, null=True,
        default=None)
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        default=None)

    def __str__(self):
        return self.nombre + " [" + self.fecha_inicio.strftime("%d-%b-%Y (%H:%M)") + "]"

    def clean(self, *args, **kwargs):
        # Establecer la fecha de fin lo que durará el partido de 90 minutos.
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(minutes=90)

        super(PromocionPartido, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(PromocionPartido, self).save(*args, **kwargs)

        if self.participantes.count() == 4:
            # Conseguir las pistas disponibles en fecha_inicio / fecha_fin
            # Reservar en una de ellas
            # Pistas que coinciden con el horario de apertura y cierre
            pistas = Pista.objects.filter(hora_apertura__lte=self.fecha_inicio.time()).filter(hora_cierre__gte=self.fecha_fin.time())
            # Reservas hechas en el intervalo de hora de inicio y fin de la promocion
            reservas = Reserva.objects.filter((Q(hora_inicio__gte=self.fecha_fin) and Q(hora_inicio__lte=self.fecha_fin)) or (Q(hora_fin__lte=self.fecha_inicio and Q(hora_fin__gte=self.fecha_fin))))
            # Retira del Queryset de pistas las ocupadas en esa hora
            for reserva in reservas:
                pistas = pistas.exclude(pk=reserva.pista.pk)
            # Si hay pistas disponibles
            if pistas.count() > 0:
                # Crea una reserva a nombre del admin
                reserva_promocion = Reserva.objects.create(
                    usuario=User.objects.get(pk=1),
                    pista=pistas.first(),
                    hora_inicio=self.fecha_inicio,
                    hora_fin=self.fecha_fin)
                reserva_promocion.save()
            else:
                # Cancelar promocion y avisar a los participantes???
                pass


# No se realiza la reserva hasta que se inscriben 4 jugadores.
# Si no hay ninguna pista disponible para esa hora se cancela la promoción.
