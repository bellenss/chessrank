from django.db import models
from .tournament import Tournament

class Player(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    fide_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=5, blank=True, null=True)
    federation = models.CharField(max_length=10)
    club = models.CharField(max_length=255, blank=True, null=True)
    fide_rating = models.PositiveIntegerField(blank=True, null=True)
    national_rating = models.PositiveIntegerField(blank=True, null=True)
    birth_year = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)
    points = models.FloatField(blank=True, null=True)
    performance = models.PositiveIntegerField(blank=True, null=True)
    tie_breaks = models.JSONField(default=dict)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="players")

    def __str__(self):
        return f"{self.name} ({self.fide_id})"
