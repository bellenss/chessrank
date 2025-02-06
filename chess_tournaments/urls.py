from django.urls import path
from .views import create_tournament, tournament_list, tournament_detail

urlpatterns = [
    path("api/tournament/create/", create_tournament, name="create_tournament"),
    path("tournaments/", tournament_list, name="tournament_list"),
    path("tournaments/<int:tournament_id>/", tournament_detail, name="tournament_detail"),
]
