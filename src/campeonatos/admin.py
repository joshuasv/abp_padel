from django.contrib import admin

from .models import Campeonato, Normativa, Grupo, Pareja, Enfrentamiento

class NormativaInline(admin.TabularInline):
    model = Normativa
    extra = 3

class CampeonatoAdmin(admin.ModelAdmin):
    inlines = [NormativaInline]

admin.site.register(Campeonato, CampeonatoAdmin)
# admin.site.register(Campeonato)
# admin.site.register(Normativa)
admin.site.register(Grupo)
admin.site.register(Pareja)


class EnfrentamientoAdmin(admin.ModelAdmin):
    # print(dir(admin.ModelAdmin))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Comprobar si están todos los huecos de puntuación llenos
        if (obj.set_1_pareja_1 != '0') and (obj.set_2_pareja_1 != '0') and (obj.set_3_pareja_1 != '0') and (obj.set_1_pareja_2 != '0') and (obj.set_2_pareja_2 != '0') and (obj.set_3_pareja_2 != '0'):
            # Establecer un ganador
            juegos_pareja_1 = 0
            juegos_pareja_2 = 0
            if obj.set_1_pareja_1 == '4':
                juegos_pareja_1 += 1
            if obj.set_2_pareja_1 == '4':
                juegos_pareja_1 += 1
            if obj.set_3_pareja_1 == '4':
                juegos_pareja_1 += 1
            if obj.set_1_pareja_2 == '4':
                juegos_pareja_2 += 1
            if obj.set_2_pareja_2 == '4':
                juegos_pareja_2 += 1
            if obj.set_3_pareja_2 == '4':
                juegos_pareja_2 += 1

            if juegos_pareja_1 > juegos_pareja_2:
                obj.ganador = obj.pareja_1
                # Actualizar la puntación de la clasificación
                obj.pareja_1.puntuacion_clasificacion += 3
                obj.pareja_2.puntuacion_clasificacion += 1
            else:
                obj.ganador = obj.pareja_2
                # Actualizar la puntación de la clasificación
                obj.pareja_1.puntuacion_clasificacion += 1
                obj.pareja_2.puntuacion_clasificacion += 3
                
            obj.pareja_1.save()
            obj.pareja_2.save()
            obj.save()

admin.site.register(Enfrentamiento, EnfrentamientoAdmin)
