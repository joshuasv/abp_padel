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

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('pista-detail', kwargs={'pk': self.pk})
