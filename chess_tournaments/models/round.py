from django.db import models
from .tournament import Tournament

class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="tournament_rounds")
    round_number = models.PositiveIntegerField()
    date = models.DateField()

    class Meta:
        unique_together = ("tournament", "round_number")

    def __str__(self):
        return f"Round {self.round_number} - {self.tournament.name}"
