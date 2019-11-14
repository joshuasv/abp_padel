from django.contrib import admin

from .models import Campeonato, Normativa, Grupo, Pareja, Enfrentamiento

admin.site.register(Campeonato)
admin.site.register(Normativa)
admin.site.register(Grupo)
admin.site.register(Pareja)
admin.site.register(Enfrentamiento)
