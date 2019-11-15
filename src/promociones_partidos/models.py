from datetime import timedelta

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from reservas.models import Reserva
from pistas.models import Pista, HorarioPista
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
            # Pistas que tienen un horario_pista igual al intervalo de horas de la promocion
            fecha_inicio_delta = self.fecha_inicio + timedelta(hours=1)
            horarios_pistas = HorarioPista.objects.filter(hora_inicio=fecha_inicio_delta.time())
            # Reservas que tengan ese horario_pista y la fecha de la promocion
            reservas = Reserva.objects.filter(fecha=fecha_inicio_delta.date(), horario_pista=horarios_pistas[0])
            # Excluir los horarios que tengan alguna de las pistas en reservas. Nos quedamos con los horarios libreas.
            horarios_pistas = horarios_pistas.exclude(pista=reservas[0].pista)
            # Comprobar que haya alguno
            if horarios_pistas.count() > 0:
                # Realizar la reserva para el primer horario del QuerySet
                reserva = Reserva.objects.create(
                    usuario=User.objects.get(pk=1),
                    pista=horarios_pistas.first().pista,
                    horario_pista=horarios_pistas.first(),
                    fecha=fecha_inicio_delta.date())
                reserva.save()
            else:
                # Cancelar la promocion
                # Avisar a los participantes
                pass


# No se realiza la reserva hasta que se inscriben 4 jugadores.
# Si no hay ninguna pista disponible para esa hora se cancela la promoción.
