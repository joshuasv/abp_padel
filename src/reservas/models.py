import datetime
import pytz
from datetime import timedelta

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.conf import settings

from pistas.models import Pista


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE) # ManyToOne
    hora_inicio = models.DateTimeField(blank=False, null=False)
    hora_fin = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.usuario} reservo: {self.pista} ({self.hora_inicio},{self.hora_fin})"

    def get_absolute_url(self):
        return reverse('reserva-detail', kwargs={'pk': self.pk})

    def clean(self):
        pista = self.pista
        hora_inicio = self.hora_inicio
        hora_fin = hora_inicio + timedelta(minutes=90)

        if Reserva.objects.filter(pista=pista).filter(Q(hora_inicio__range=(hora_inicio, hora_fin)) or Q(hora_fin__range=(hora_inicio, hora_fin))):
            raise ValidationError('Ese espacio de tiempo no esta disponible!')

    def get_reservas_activas(usuario):
        timezone = pytz.timezone(settings.TIME_ZONE)
        time = timezone.localize(datetime.datetime.now())
        return Reserva.objects.filter(usuario=usuario, hora_inicio__gte=time)

# Si es la última pista libre para esa fecha y hora se deben eliminar todas las
# promociones de partidos para esa fecha y hora.
