from django.urls import path

from .views import PromocionPartidoListView, PromocionPartidoDetailView, inscripcion, desinscripcion


urlpatterns = [
    path('', PromocionPartidoListView.as_view(), name='promocion-list'),
    path('<int:pk>/', PromocionPartidoDetailView.as_view(), name='promocion-detail'),
    path('<int:promocion_id>/inscripcion', inscripcion, name='promocion-inscripcion'),
    path('<int:promocion_id>/desinscripcion', desinscripcion, name='promocion-desinscripcion'),
]
