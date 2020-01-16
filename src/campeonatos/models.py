import string
import itertools
import datetime
import random

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

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
        parejas = Pareja.selfects.all()
        for pareja in parejas:
            pareja.grupo = None
            pareja.save()

    # def make_parejas(self):
    #     usuarios = list(User.selfects.all())
    #     campeonato = Campeonato.selfects.get(pk=1)
    #     normativa = Normativa.selfects.get(campeonato=campeonato, pk=1)
    #     for i in range(1, len(usuarios) - 1, 2):
    #         pareja = Pareja(capitan=usuarios[i], miembro=usuarios[i + 1], normativa=normativa)
    #         pareja.save()

    # https://medium.com/@bencleary/django-scheduled-tasks-queues-part-1-62d6b6dc24f8 [AUTOMATICO!!!]
    # crontab django
    def make_groups(self):
        self.limpiar_grupos()
        # Comprobar que la fecha actual es mayor o igual que la de fin_inscripciones
        if timezone.now() >= self.fin_inscripciones:
            alphabet = string.ascii_uppercase
            # Coger todas las normativas para ese campeonato
            normativas = Normativa.selfects.filter(campeonato=self)
            for normativa in normativas:
                # Para cada normativa ver cuantas parejas tiene
                parejas = list(Pareja.selfects.filter(normativa=normativa))
                num_parejas = len(parejas)
                grupos = []
                # Crear los grupos máximos de 8 integrantes
                for i in range(num_parejas // 8):
                    grupo = Grupo(campeonato=self, nombre=alphabet[i], normativa=normativa)
                    # grupo.clean()
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
        # print("Crear enfrentamientos")
        grupos = []
        normativas = Normativa.selfects.filter(campeonato=self)
        for norm in normativas:
            grupo = Grupo.selfects.filter(normativa=norm)
            if grupo:
                grupos.append(grupo)
        letras = string.ascii_uppercase
        for grupo in grupos:
            for sub_grupo in grupo:
                parejas_grupo = list(Pareja.selfects.filter(grupo=sub_grupo))
                combinaciones = list(itertools.combinations(parejas_grupo, 2))
                for combinacion in combinaciones:
                    enfrentamiento = Enfrentamiento(campeonato=self, ronda=0, pareja_1=combinacion[0], pareja_2=combinacion[1])
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
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    normativa = models.ForeignKey(Normativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.normativa.campeonato.nombre}] Grupo {self.nombre} ({self.normativa.get_categoria_display()}, {self.normativa.get_nivel_display()})";

    def clean(self, *args, **kwargs):
        if Grupo.selfects.filter(nombre=self.nombre, normativa=self.normativa).count() > 0:
            raise ValidationError('Ya existe este grupo')
        if Pareja.selfects.filter(grupo=self, normativa=self.normativa).count() >= 12:
            raise ValidationError('Número máximo de parejas por grupo (12) alcanzado.')
        super(Grupo, self).clean(*args, **kwargs)

    def get_parejas_number(self):
        return Pareja.selfects.filter(grupo=self).count()


class Pareja(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    normativa = models.ForeignKey(Normativa, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    capitan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capitan')
    miembro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='miembro')
    puntuacion_clasificacion = models.IntegerField(default=0)

    def __str__(self):
        return "Capitan: " + self.capitan.email + "-Miembro: " + self.miembro.email


class Enfrentamiento(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    ronda = models.IntegerField()
    pareja_1 = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='pareja_1')
    pareja_2 = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='pareja_2')
    acepto_pareja = models.BooleanField(default=False)
    TURNO_CHOICE = [('1', pareja_1), ('2', pareja_2)]
    turno_fecha = models.CharField(max_length=1, choices=TURNO_CHOICE, default='1')
    fecha = models.DateField(null=True, blank=True, default=None)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True, default=None)
    PUNTUACION_CHOICE = [('0', 'No jugado'), ('1', 15), ('2', 30), ('3', 40), ('4', 'juego')]
    set_1_pareja_1 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    set_1_pareja_2 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    set_2_pareja_1 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    set_2_pareja_2 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    set_3_pareja_1 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    set_3_pareja_2 = models.CharField(max_length=1, choices=PUNTUACION_CHOICE, default='0')
    ganador = models.ForeignKey(Pareja, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.pareja_1} VS. {self.pareja_2}"


    def save(self, *args, **kwargs):
        if (self.set_1_pareja_1 != '0') and (self.set_2_pareja_1 != '0') and (self.set_3_pareja_1 != '0') and (self.set_1_pareja_2 != '0') and (self.set_2_pareja_2 != '0') and (self.set_3_pareja_2 != '0'):
            # Establecer ganador
            juegos_pareja_1 = 0
            juegos_pareja_2 = 0
            if self.set_1_pareja_1 == '4':
                juegos_pareja_1 += 1
            if self.set_2_pareja_1 == '4':
                juegos_pareja_1 += 1
            if self.set_3_pareja_1 == '4':
                juegos_pareja_1 += 1
            if self.set_1_pareja_2 == '4':
                juegos_pareja_2 += 1
            if self.set_2_pareja_2 == '4':
                juegos_pareja_2 += 1
            if self.set_3_pareja_2 == '4':
                juegos_pareja_2 += 1

            if juegos_pareja_1 > juegos_pareja_2:
                self.ganador = self.pareja_1
                # Actualizar la puntación de la clasificación
                self.pareja_1.puntuacion_clasificacion += 3
                self.pareja_2.puntuacion_clasificacion += 1
            else:
                self.ganador = self.pareja_2
                # Actualizar la puntación de la clasificación
                self.pareja_1.puntuacion_clasificacion += 1
                self.pareja_2.puntuacion_clasificacion += 3

            self.pareja_1.save()
            self.pareja_2.save()

        super(Enfrentamiento, self).save(*args, **kwargs)
        if self.is_roda_enfrentamientos_grupo_jugados(self.ronda, self.pareja_1.grupo):
            self.crear_siguiente_ronda(self.ronda, self.pareja_1.grupo)

    def is_roda_enfrentamientos_grupo_jugados(self, ronda, grupo):
        parejas_grupo = Pareja.objects.filter(grupo=grupo)
        enfrentamientos_parejas = Enfrentamiento.objects.filter(Q(pareja_1__in=parejas_grupo) | Q(pareja_2__in=parejas_grupo), ronda=ronda)
        for enfrent in enfrentamientos_parejas:
            # Ver si se jugaron
            if (enfrent.set_1_pareja_1 == '0') or (enfrent.set_2_pareja_1 == '0') or (enfrent.set_3_pareja_1 == '0') or (enfrent.set_1_pareja_2 == '0') or (enfrent.set_2_pareja_2 == '0') or (enfrent.set_3_pareja_2 == '0'):
                return False
        return True

    def crear_siguiente_ronda(self, ronda_actual, grupo):
        if ronda_actual == 0:
            self.crear_enfrentamientos_cuartos(grupo)
        elif ronda_actual == 1:
            self.crear_enfrentamientos_semifinales(grupo)
        elif ronda_actual == 2:
            self.crear_enfrentamientos_final(grupo)
        else:
            print("Invalido")

    def crear_enfrentamientos_cuartos(self, grupo):
        parejas_grupo = Pareja.objects.filter(grupo=grupo)
        if Enfrentamiento.objects.filter(Q(pareja_1__in=parejas_grupo) | Q(pareja_2__in=parejas_grupo), ronda=1).count() <= 0:
            print("Creando cuartos...")
            parejas_grupo = list(Pareja.objects.filter(grupo=grupo).order_by('-puntuacion_clasificacion')[:8])
            parejas_ultima_mitad = parejas_grupo[4:]
            parejas_ultima_mitad.reverse()
            for i in range(4):
                enfrentamiento = Enfrentamiento.objects.create(
                    campeonato = self.campeonato,
                    ronda = 1,
                    pareja_1 = parejas_grupo[i],
                    pareja_2 = parejas_ultima_mitad[i]
                )
                enfrentamiento.save()

    def crear_enfrentamientos_semifinales(self, grupo):
        parejas_grupo = Pareja.objects.filter(grupo=grupo)
        if Enfrentamiento.objects.filter(Q(pareja_1__in=parejas_grupo) | Q(pareja_2__in=parejas_grupo), ronda=2).count() <= 0:
            parejas_grupo = list(Pareja.objects.filter(grupo=grupo).order_by('-puntuacion_clasificacion')[:4])
            random.shuffle(parejas_grupo)
            for i in range(0, 3, 2):
                enfrentamiento = Enfrentamiento.objects.create(
                    campeonato = self.campeonato,
                    ronda = 2,
                    pareja_1 = parejas_grupo[i],
                    pareja_2 = parejas_grupo[i + 1],
                )
                enfrentamiento.save()

    def crear_enfrentamientos_final(self, grupo):
        parejas_grupo = Pareja.objects.filter(grupo=grupo)
        if Enfrentamiento.objects.filter(Q(pareja_1__in=parejas_grupo) | Q(pareja_2__in=parejas_grupo), ronda=3).count() <= 0:
            parejas_grupo = list(Pareja.objects.filter(grupo=grupo).order_by('-puntuacion_clasificacion')[:2])
            enfrentamiento = Enfrentamiento.objects.create(
                campeonato = self.campeonato,
                ronda = 3,
                pareja_1 = parejas_grupo[0],
                pareja_2 = parejas_grupo[1],
            )
            enfrentamiento.save()
            print("Enfrentamiento final hecho")
