from django.urls import path
from .views import (
    PistaListView,
    PistaDetailView,
    PistaCreateView,
    PistaUpdateView,
    PistaDeleteView
)

urlpatterns = [
    path('', PistaListView.as_view(), name='pista-list'),
    path('<int:pk>/', PistaDetailView.as_view(), name='pista-detail'),
    path('new/', PistaCreateView.as_view(), name='pista-create'),
    path('<int:pk>/update/', PistaUpdateView.as_view(), name='pista-update'),
    path('<int:pk>/delete/', PistaDeleteView.as_view(), name='pista-delete')
]
