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
admin.site.register(Enfrentamiento)
