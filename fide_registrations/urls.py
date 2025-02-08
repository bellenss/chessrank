from django.urls import path
from .views import view_registered_tournaments

urlpatterns = [
    path('registered-tournaments/', view_registered_tournaments, name='registered_tournaments'),
]
