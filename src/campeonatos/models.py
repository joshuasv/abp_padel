from django.db import models
from django.conf import settings


class Campeonato(models.Model):
    nombre = models.CharField(max_length=100)
    inicio_campeonato=models.DateTimeField()
    fin_inscripciones = models.DateTimeField()

    def __str__(self):
        return self.nombre


class Normativa(models.Model):
    CATEGORIA_CHOICE = [('M', 'Male'), ('F', 'Female')]
    NIVEL_CHOICE = [('B', 'Bajo'), ('M', 'Medio'), ('A', 'Alto')]
    categoria = models.CharField(max_length=1, choices=CATEGORIA_CHOICE)
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)

    def __str__(self):
        return self.categoria + "--" + self.nivel


class Grupo(models.Model):
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE)

    def __str__(self):
        return "Grupo " + self.normativa.categoria + " nivel: " + self.normativa.nivel


class Pareja(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, blank=True, null=True, default=None)
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE, blank=True, null=True, default=None)
    capitan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capitan')
    miembro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='miembro')

    def __str__(self):
        return "Capitan: " + self.capitan.email + "-Miembro: " + self.miembro.email
