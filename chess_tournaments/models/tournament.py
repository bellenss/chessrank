from django.db import models

class Tournament(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    fide_event_id = models.CharField(max_length=20, blank=True, null=True)
    organiser = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    arbiter = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    rounds = models.PositiveIntegerField()
    time_control = models.CharField(max_length=50)
    rating_average = models.PositiveIntegerField(blank=True, null=True)
    rated_fide = models.BooleanField(default=False)
    rated_national = models.BooleanField(default=False)
    federation = models.CharField(max_length=10)
    tie_breaks = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
