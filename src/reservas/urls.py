from django.urls import path

from .views import (
    ReservaListView,
    ReservaDetailView,
    ReservaCreateView,
    ReservaUpdateView,
    ReservaDeleteView
)


urlpatterns = [
    path('', ReservaListView.as_view(), name='reserva-list'),
    path('<int:pk>/', ReservaDetailView.as_view(), name='reserva-detail'),
    path('new/', ReservaCreateView.as_view(), name='reserva-create'),
    path('<int:pk>/update/', ReservaUpdateView.as_view(), name='reserva-update'),
    path('<int:pk>/delete/', ReservaDeleteView.as_view(), name='reserva-delete')
]
