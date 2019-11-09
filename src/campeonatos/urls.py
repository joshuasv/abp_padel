from django.urls import path

from .views import CampeonatoListView, CampeonatoDetailView, inscripcion, desinscripcion

urlpatterns = [
    path('', CampeonatoListView.as_view(), name='campeonato-list'),
    path('<int:pk>/', CampeonatoDetailView.as_view(), name='campeonato-detail'),
    path('<int:campeonato_id>/inscripcion/', inscripcion, name='campeonato-inscripcion'),
    path('<int:campeonato_id>/desinscripcion/', desinscripcion, name='campeonato-desinscripcion'),

]
