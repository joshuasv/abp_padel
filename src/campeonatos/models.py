import string
import itertools
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import User
from reservas.models import Reserva


class Campeonato(models.Model):
    nombre = models.CharField(max_length=100)
    inicio_campeonato = models.DateTimeField()
    fin_inscripciones = models.DateTimeField()

    @property
    def paso_fecha_inscripcion(self):
        return timezone.now() >= self.fin_inscripciones

    def __str__(self):
        return self.nombre

    def limpiar_grupos(self):
        parejas = Pareja.objects.all()
        for pareja in parejas:
            pareja.grupo = None
            pareja.save()

    def make_parejas(self):
        usuarios = list(User.objects.all())
        campeonato = Campeonato.objects.get(pk=1)
        normativa = Normativa.objects.get(campeonato=campeonato, pk=1)
        for i in range(1, len(usuarios) - 1, 2):
            pareja = Pareja(capitan=usuarios[i], miembro=usuarios[i + 1], normativa=normativa)
            pareja.save()

    # https://medium.com/@bencleary/django-scheduled-tasks-queues-part-1-62d6b6dc24f8 [AUTOMATICO!!!]
    def make_groups(self):
        # self.limpiar_grupos()
        # Comprobar que la fecha actual es mayor o igual que la de fin_inscripciones
        if timezone.now() >= self.fin_inscripciones:
            alphabet = string.ascii_uppercase
            # Coger todas las normativas para ese campeonato
            normativas = Normativa.objects.filter(campeonato=self)
            for normativa in normativas:
                # Para cada normativa ver cuantas parejas tiene
                parejas = list(Pareja.objects.filter(normativa=normativa))
                num_parejas = len(parejas)
                grupos = []
                # Crear los grupos máximos de 8 integrantes
                for i in range(num_parejas // 8):
                    grupo = Grupo(nombre=alphabet[i], normativa=normativa)
                    grupo.clean()
                    grupo.save()
                    grupos.append(grupo)
                    miembros_grupo = parejas[0:8]
                    for miembro in miembros_grupo:
                        parejas.remove(miembro)
                        miembro.grupo = grupo
                        miembro.save()
                # Repartir las parejas sin grupo entre los grupos creados
                if grupos:
                    for pareja in parejas:
                        index = parejas.index(pareja) % len(grupos)
                        if grupos[index].get_parejas_number() < 12:
                            pareja.grupo = grupos[index]
                            pareja.save()

    def make_enfrentamientos_liga_regular(self):
        grupos = []
        normativas = Normativa.objects.filter(campeonato=self)
        for norm in normativas:
            grupo = Grupo.objects.filter(normativa=norm)
            if grupo:
                grupos.append(grupo)
        letras = string.ascii_uppercase
        for grupo in grupos:
            for sub_grupo in grupo:
                parejas_grupo = list(Pareja.objects.filter(grupo=sub_grupo))
                combinaciones = list(itertools.combinations(parejas_grupo, 2))
                for combinacion in combinaciones:
                    enfrentamiento = Enfrentamiento(pareja_1=combinacion[0], pareja_2=combinacion[1])
                    enfrentamiento.save()


class Normativa(models.Model):
    CATEGORIA_CHOICE = [('M', 'Masculino'), ('F', 'Femenino'), ('X', 'Mixto')]
    NIVEL_CHOICE = [('B', 'Bajo'), ('M', 'Medio'), ('A', 'Alto')]
    categoria = models.CharField(max_length=1, choices=CATEGORIA_CHOICE)
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)

    def __str__(self):
        return self.get_categoria_display() + "--" + self.get_nivel_display()


class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.normativa.campeonato.nombre}] Grupo {self.nombre} ({self.normativa.get_categoria_display()}, {self.normativa.get_nivel_display()})";

    def clean(self, *args, **kwargs):
        if Grupo.objects.filter(nombre=self.nombre, normativa=self.normativa).count() > 0:
            raise ValidationError('Ya existe este grupo')
        if Pareja.objects.filter(grupo=self, normativa=self.normativa).count() >= 12:
            raise ValidationError('Número máximo de parejas por grupo (12) alcanzado.')
        super(Grupo, self).clean(*args, **kwargs)

    def get_parejas_number(self):
        return Pareja.objects.filter(grupo=self).count()


class Pareja(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    normativa = models.ForeignKey(Normativa, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    capitan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capitan')
    miembro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='miembro')

    def __str__(self):
        return "Capitan: " + self.capitan.email + "-Miembro: " + self.miembro.email


class Enfrentamiento(models.Model):
    ronda = models.IntegerField()
    pareja_1 = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='pareja_1')
    pareja_2 = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='pareja_2')
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True, default=None)
    set_1_pareja_1 = models.IntegerField(null=True, blank=True, default=None)
    set_1_pareja_2 = models.IntegerField(null=True, blank=True, default=None)
    set_2_pareja_1 = models.IntegerField(null=True, blank=True, default=None)
    set_2_pareja_2 = models.IntegerField(null=True, blank=True, default=None)
    set_3_pareja_1 = models.IntegerField(null=True, blank=True, default=None)
    set_3_pareja_2 = models.IntegerField(null=True, blank=True, default=None)
    ganador = models.ForeignKey(Pareja, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.pareja_1} VS. {self.pareja_2}"


class AceptaEnfrentamiento(models.Model):
    enfrentamiento = models.ForeignKey(Enfrentamiento, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    acepta_pareja_1 = models.BooleanField(default=False)
    acepta_pareja_2 = models.BooleanField(default=False)
