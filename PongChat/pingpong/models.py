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

    def end_game(self):
        self.date_end = models.DateTimeField(auto_now_add=True)
        self.status = "done"
        if self.score1 > self.score2:
            self.winner = self.player1
        elif self.score1 < self.score2:
            self.winner = self.player2
        else:
            self.winner = None
        self.save()


# class Match(models.Model):
#     player1 = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="matches_as_player1",
#     )
#     player2 = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="matches_as_player2",
#     )
#     game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="matches")
#     date_played = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.player1} vs {self.player2}
# in {self.game} at {self.date_played}"
