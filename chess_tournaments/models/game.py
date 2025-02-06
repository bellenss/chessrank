from django.db import models

class Game(models.Model):
    round = models.ForeignKey("chess_tournaments.Round", on_delete=models.CASCADE, related_name="games")
    board = models.PositiveIntegerField()

    white = models.ForeignKey(
        "chess_tournaments.Player", on_delete=models.CASCADE, related_name="white_games", null=True, blank=True
    )
    black = models.ForeignKey(
        "chess_tournaments.Player", on_delete=models.CASCADE, related_name="black_games", null=True, blank=True
    )

    white_rating = models.PositiveIntegerField(null=True, blank=True)
    black_rating = models.PositiveIntegerField(null=True, blank=True)

    RESULT_CHOICES = [
        ("1-0", "White Wins"),
        ("0-1", "Black Wins"),
        ("½-½", "Draw"),
        ("*", "Unplayed"),
    ]
    result = models.CharField(max_length=5, choices=RESULT_CHOICES, blank=True, null=True)

    forfeit = models.BooleanField(default=False)

    class Meta:
        unique_together = ("round", "board")  # Ensures a unique game per board in a round

    def __str__(self):
        white_name = self.white.name if self.white else "BYE"
        black_name = self.black.name if self.black else "BYE"
        return f"Board {self.board}: {white_name} vs {black_name} ({self.result})"
