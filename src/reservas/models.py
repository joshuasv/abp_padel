import pytz
from datetime import timedelta, datetime, date

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone

from pistas.models import Pista, HorarioPista


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE) # ManyToOne
    horario_pista = models.ForeignKey(HorarioPista, on_delete=models.CASCADE, related_name="horario_pista")
    fecha = models.DateField()


    def __str__(self):
        return f"{self.usuario} {self.pista} ({self.horario_pista.hora_inicio},{self.horario_pista.hora_fin})"

    def get_absolute_url(self):
        return reverse('reserva-detail', kwargs={'pk': self.pk})

    def clean(self):
        date_time_fin = datetime.combine(self.fecha, self.horario_pista.hora_fin)
        now = datetime.now()
        if(date_time_fin < now):
            raise ValidationError('Espacio de tiempo pasado!')
        if self.fecha > (date.today() + timedelta(days=7)):
            raise ValidationError('Máximo con una semana de antelación!')
        if Reserva.objects.filter(pista=self.pista, horario_pista=self.horario_pista, fecha=self.fecha).count() > 0:
            raise ValidationError('Ese espacio de tiempo no esta disponible!')

    def get_reservas_activas(usuario):
        return Reserva.objects.filter(usuario=usuario).filter(Q(fecha__gt=date.today()) | Q(horario_pista__hora_fin__gte=datetime.now()))

# Si es la última pista libre para esa fecha y hora se deben eliminar todas las
# promociones de partidos para esa fecha y hora.
