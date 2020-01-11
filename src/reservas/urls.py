from django.urls import path

from .views import (
    ReservaListView,
    ReservaHistorialView,
    ReservaDetailView,
    ReservaCreateView,
    ReservaUpdateView,
    ReservaDeleteView,
    load_horario_pista
)


urlpatterns = [
    path('', ReservaListView.as_view(), name='reserva-list'),
    path('all/', ReservaHistorialView.as_view(), name='reserva-historial'),
    path('<int:pk>/', ReservaDetailView.as_view(), name='reserva-detail'),
    path('new/', ReservaCreateView.as_view(), name='reserva-create'),
    # path('<int:pk>/update/', ReservaUpdateView.as_view(), name='reserva-update'),
    path('<int:pk>/delete/', ReservaDeleteView.as_view(), name='reserva-delete'),


    path('ajax/load-horario-pista/', load_horario_pista, name='ajax_load_horario_pista')
]
