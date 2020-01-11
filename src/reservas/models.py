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

import promociones_partidos as promociones_partidos
from pistas.models import Pista, HorarioPista


class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE) # ManyToOne
    horario_pista = models.ForeignKey(HorarioPista, on_delete=models.CASCADE, related_name="horario_pista")
    fecha = models.DateField()


    def __str__(self):
        return f"{self.usuario} {self.pista} ({self.horario_pista.hora_inicio},{self.horario_pista.hora_fin})"

    def get_absolute_url(self):
        return reverse('reserva-list')
        # return reverse('reserva-list', kwargs={'pk': self.pk})

    def clean(self):
        date_time_fin = datetime.combine(self.fecha, self.horario_pista.hora_fin)
        now = datetime.now()
        if(date_time_fin < now):
            raise ValidationError('Espacio de tiempo pasado!')
        if self.fecha > (date.today() + timedelta(days=7)):
            raise ValidationError('Máximo con una semana de antelación!')
        if Reserva.objects.filter(pista=self.pista, horario_pista=self.horario_pista, fecha=self.fecha).count() > 0:
            raise ValidationError('Ese espacio de tiempo no esta disponible!')
        self.is_ultima_pista()

    def get_reservas_activas(usuario):
        return Reserva.objects.filter(usuario=usuario).filter(Q(fecha__gt=date.today()) | Q(horario_pista__hora_fin__gte=datetime.now()))

    def is_ultima_pista(self):
        # 1) Verificar si es la úlitma pista libre para esa fecha y horario
        # Coge todas los horarios_pistas que coincidan con el de la reserva, excluyendo el de la reserva mismo.
        horarios_pistas = HorarioPista.objects.filter(hora_inicio=self.horario_pista.hora_inicio).exclude(pk=self.horario_pista.id)
        # Obtiene las reservas para el conjunto de horarios_pistas con la misma fecha que la reserva.
        reservas_fecha_hora = Reserva.objects.filter(horario_pista__in=horarios_pistas, fecha=self.fecha)
        # 2) Eliminar de horarios_pistas aquellas reservas que contenga uno de ellos
        for reserva in reservas_fecha_hora:
            horarios_pistas = horarios_pistas.exclude(pista=reserva.pista)
        if horarios_pistas.count() <= 0:
            # 3) Coger las promociones que tengan el mismo horario_pista y fecha que la reserva
            # Convierte la fecha y hora_inicio en un tipo de dato datetime
            fecha_horaraio_reserva = datetime.combine(self.fecha, self.horario_pista.hora_inicio)
            print(fecha_horaraio_reserva)
            promociones = promociones_partidos.models.PromocionPartido.objects.filter(fecha_inicio=fecha_horaraio_reserva, cerrado=False)
            for promocion in promociones:
                promocion.cancelado = True
                promocion.save()
