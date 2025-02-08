from django.urls import path
from .views import create_tournament, process_tournament_report, tournament_list, tournament_detail

urlpatterns = [
    path("tournament/upload/", process_tournament_report, name="process_tournament_report"),
    path('tournaments/new/', create_tournament, name='create_tournament'),
    path("tournaments/", tournament_list, name="tournament_list"),
    path("tournaments/<int:tournament_id>/", tournament_detail, name="tournament_detail"),
]
