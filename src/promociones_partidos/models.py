from datetime import timedelta

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from pistas.models import Pista, HorarioPista
from users.models import User
from reservas.models import Reserva

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
    cerrado = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre + " [" + self.fecha_inicio.strftime("%d-%b-%Y (%H:%M)") + "]"

    def clean(self, *args, **kwargs):
        # Establecer la fecha de fin lo que durará el partido de 90 minutos.
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(minutes=90)

        super(PromocionPartido, self).clean(*args, **kwargs)

    def delete(self):
        if self.reserva:
            reserva = Reserva.objects.get(pk=self.reserva.pk)
            reserva.delete()
        super(PromocionPartido, self).delete()

    def save(self, *args, **kwargs):
        super(PromocionPartido, self).save(*args, **kwargs)

        if self.participantes.count() == 4:
            # Pistas que tienen un horario_pista igual al intervalo de horas de la promocion
            fecha_inicio_delta = self.fecha_inicio + timedelta(hours=1)
            horarios_pistas = HorarioPista.objects.filter(hora_inicio=fecha_inicio_delta.time())
            # Reservas que tengan ese horario_pista y la fecha de la promocion
            if horarios_pistas:
                reservas = Reserva.objects.filter(fecha=fecha_inicio_delta.date(), horario_pista__in=horarios_pistas)
                # Excluir los horarios que tengan alguna de las pistas en reservas. Nos quedamos con los horarios libres.
                if reservas:
                    for reserva in reservas:
                        horarios_pistas = horarios_pistas.exclude(pista=reserva.pista)
            # Comprobar que haya alguno
            if horarios_pistas.count() > 0:
                # Realizar la reserva para el primer horario del QuerySet
                reserva = Reserva.objects.create(
                    usuario=User.objects.get(pk=1),
                    pista=horarios_pistas.first().pista,
                    horario_pista=horarios_pistas.first(),
                    fecha=fecha_inicio_delta.date())
                reserva.save()
                self.reserva = reserva
                self.cerrado = True
                super(PromocionPartido, self).save(*args, **kwargs)
            else:
                # Cancelar la promocion
                self.cancelado = True
                super(PromocionPartido, self).save(*args, **kwargs)
                # Avisar a los participantes
