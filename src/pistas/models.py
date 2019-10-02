from django.db import models
from django.urls import reverse

# Create your models here.
class Pista(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False, unique=True)
    hora_apertura = models.TimeField(blank=False, null=False)
    hora_cierre = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('pista-detail', kwargs={'pk': self.pk})
