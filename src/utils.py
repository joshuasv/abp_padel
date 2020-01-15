import string, random
import time
from users.models import User
from campeonatos.models import Pareja, Campeonato, Normativa, Enfrentamiento

def crear_usuarios():
    # Eliminar todos los usuarios menos el admin
    User.objects.filter(is_superuser=False).delete()
    print("Creando usuarios...")
    for i in range(40):
        username = 'user{0}'.format(i)
        dni = "".join(random.sample(string.digits, k=8)) + "".join(random.sample(string.ascii_uppercase, k=1))
        usuario = User.objects.create(username=username, email=username + '@at.com', sex='F', dni=dni)
        usuario.set_password('test')
        usuario.save()

    for i in range(40, 86):
        username = 'user{0}'.format(i)
        dni = "".join(random.sample(string.digits, k=8)) + "".join(random.sample(string.ascii_uppercase, k=1))
        usuario = User.objects.create(username=username, email=username + '@at.com', sex='M', dni=dni)
        usuario.set_password('test')
        usuario.save()
    print("\tUsuarios creados.")

def crear_parejas():
    # Eliminar las parejas existentes
    Pareja.objects.all().delete()
    males = User.objects.filter(sex='M')
    females = User.objects.filter(sex='F')
    females_used = []
    males_used = []
    print("Creando parejas...")
    # Parejas femeninas
    for i in range(0, len(females) - 8, 2):
        pareja = Pareja.objects.create(capitan=females[i], miembro=females[i + 1])
        pareja.save()
        females_used.append(females[i])
        females_used.append(females[i + 1])
    # Parejas masculinas
    for i in range(0, len(males) - 8, 2):
        pareja = Pareja.objects.create(capitan=males[i], miembro=males[i + 1])
        pareja.save()
        males_used.append(males[i])
        males_used.append(males[i + 1])
    # Parejas mixtas
    males = males.exclude(username__in=males_used)
    females = females.exclude(username__in=females_used)
    for i in range(8):
        parejas = Pareja.objects.create(capitan=males[i], miembro=females[i])
        parejas.save()
    print("\tParejas creadas. {0}".format(len(Pareja.objects.all())))

def registrar_parejas_campeonato():
    campeonato = Campeonato.objects.all()[0]
    normativas = Normativa.objects.filter(campeonato=campeonato)
    parejas = Pareja.objects.all()
    print("Registrando parejas en campeonato...")
    for pareja in parejas:
        if(pareja.capitan.sex == 'M' and pareja.miembro.sex == 'M'):
            pareja.normativa = normativas.get(categoria='M')
        if(pareja.capitan.sex == 'F' and pareja.miembro.sex == 'F'):
            pareja.normativa = normativas.get(categoria='F')
        if((pareja.capitan.sex == 'M' and pareja.miembro.sex == 'F') or (pareja.capitan.sex == 'F' and pareja.miembro.sex == 'M')):
            pareja.normativa = normativas.get(categoria='X')
        pareja.save()
    print("\tParejas registradas. Masc:{0} - Fem:{1} - Mix:{2}".format(
        len(Pareja.objects.filter(normativa=Normativa.objects.get(categoria='M'))),
        len(Pareja.objects.filter(normativa=Normativa.objects.get(categoria='F'))),
        len(Pareja.objects.filter(normativa=Normativa.objects.get(categoria='X')))
    ))


# rellenar_puntuaciones_enfrentamientos(8,0)
def rellenar_puntuaciones_enfrentamientos(campeonato, ronda):
    enfrentamientos = Enfrentamiento.objects.filter(campeonato__id=campeonato, ronda=ronda)

    if ronda == 0: # Poner puntuaciones a 0
        for enf in enfrentamientos:
            enf.pareja_1.puntuacion_clasificacion = 0
            enf.pareja_2.puntuacion_clasificacion = 0
            enf.pareja_1.save()
            enf.pareja_2.save()

    enfrentamientos = Enfrentamiento.objects.filter(campeonato__id=campeonato, ronda=ronda)

    for enf in enfrentamientos:
        parejas = [enf.pareja_1, enf.pareja_2]
        if random.choice(parejas) == enf.pareja_1:
            enf.set_1_pareja_1 = '4'
            enf.set_1_pareja_2 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]
        else:
            enf.set_1_pareja_2 = '4'
            enf.set_1_pareja_1 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]
        if random.choice(parejas) == enf.pareja_1:
            enf.set_2_pareja_1 = '4'
            enf.set_2_pareja_2 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]
        else:
            enf.set_2_pareja_2 = '4'
            enf.set_2_pareja_1 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]
        if random.choice(parejas) == enf.pareja_1:
            enf.set_3_pareja_1 = '4'
            enf.set_3_pareja_2 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]
        else:
            enf.set_3_pareja_2 = '4'
            enf.set_3_pareja_1 = random.choice(Enfrentamiento.PUNTUACION_CHOICE[1:-1])[0]

        enf.save()
        # time.sleep(1)
        print(enf.pareja_1, enf.pareja_2)
        print(enf.pareja_1.puntuacion_clasificacion,enf.pareja_2.puntuacion_clasificacion)
        print("........")
