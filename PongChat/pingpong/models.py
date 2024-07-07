from django.conf import settings
from django.db import models


class Game(models.Model):
    player1: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games_as_player1",
        null=True,
    )

    player2: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games_as_player2",
        null=True,
    )

    score1: models.IntegerField = models.IntegerField(default=0)
    score2: models.IntegerField = models.IntegerField(default=0)
    score_last_update: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    status: models.CharField = models.CharField(
        max_length=10,
        choices=[("ongoing", "Ongoing"), ("done", "Done")],
        default="ongoing",
    )

    date_start: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    date_end: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    winner: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="games_won",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}: {self.player1} vs {self.player2}"
