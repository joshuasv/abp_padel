import datetime

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Pista(models.Model):
    PAVIMENTO_CHOICES = [
        ('RS', 'Resina sintética'),
        ('CA', 'Césped artificial'),
        ('HP', 'Hormigón poroso'),
        ('C', 'Cemento')
    ]
    nombre = models.CharField(max_length=100, blank=False, null=False, unique=True)
    cubierta = models.BooleanField(default=False)
    pavimento = models.CharField(max_length=2, choices=PAVIMENTO_CHOICES)
    hora_apertura = models.TimeField(blank=False, null=False)
    hora_cierre = models.TimeField(blank=False, null=False)

    def clean(self, *args, **kwargs):
        dt_hora_apertura = datetime.datetime.combine(datetime.date.today(), self.hora_apertura)
        dt_hora_cierre = datetime.datetime.combine(datetime.date.today(), self.hora_cierre)
        if dt_hora_apertura + datetime.timedelta(minutes=90) > dt_hora_cierre:
            raise ValidationError({
                'hora_apertura': ValidationError(_('Mínimo 90 minutos.'), code='invalid'),
                'hora_cierre': ValidationError(_('Mínimo 90 minutos.'), code='invalid'),
            })
        super(Pista, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Pista, self).save(*args, **kwargs)
        
        hora_apertura = datetime.datetime.combine(datetime.date.today(), self.hora_apertura)
        hora_cierre = datetime.datetime.combine(datetime.date.today(), self.hora_cierre)
        intervalos = []
        i = hora_apertura
        while i < hora_cierre:
            i += datetime.timedelta(minutes=90)
            intervalos.append((hora_apertura.time(), i.time()))
            hora_apertura = i
        for intervalo in intervalos:
            horario_pista = HorarioPista(pista=self, hora_inicio=intervalo[0], hora_fin=intervalo[1])
            horario_pista.save()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('pista-detail', kwargs={'pk': self.pk})


class HorarioPista(models.Model):
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.pista.nombre} ({self.hora_inicio}, {self.hora_fin})"
