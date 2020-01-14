from django.urls import path

from .views import CampeonatoListView, CampeonatoDetailView, EnfrentamientoFormView, inscripcion, desinscripcion, aceptar_enfrentamiento, rechazar_enfrentamiento, clasificacion

urlpatterns = [
    path('', CampeonatoListView.as_view(), name='campeonato-list'),
    path('<int:pk>/', CampeonatoDetailView.as_view(), name='campeonato-detail'),
    path('<int:campeonato_id>/inscripcion/', inscripcion, name='campeonato-inscripcion'),
    path('<int:campeonato_id>/desinscripcion/', desinscripcion, name='campeonato-desinscripcion'),
    path('<int:pareja_id>/clasificacion/', clasificacion, name='campeonato-clasificacion'),
    path('enfrentamiento/<int:pk>/', EnfrentamientoFormView.as_view(), name='enfrentamiento-detail'),
    path('enfrentamiento/<int:pk>/aceptar/', aceptar_enfrentamiento, name='enfrentamiento-aceptar'),
    path('enfrentamiento/<int:pk>/rechazar/', rechazar_enfrentamiento, name='enfrentamiento-rechazar')
]
