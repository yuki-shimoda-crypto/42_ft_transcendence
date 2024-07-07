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


# guest_user
# - id
# - username

# TournamentMatch
# - id
# - tournament_id(tournament.id)
# - round
# - user1(gusest_user.id)
# - user2(guest_user_id)
# - winner(guest_user_id)

# tournament
# - id
# - partipants_amount
# - timestamp
# - winner(guest_user_id)


class GuestUser(models.Model):
    username: models.CharField = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Tournament(models.Model):
    participants_amount: models.IntegerField = models.IntegerField()
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    winner: models.ForeignKey = models.ForeignKey(
        GuestUser,
        on_delete=models.CASCADE,
        related_name="tournaments_won",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}: {self.participants_amount} participants"


class TournamentMatch(models.Model):
    tournament: models.ForeignKey = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="results",
    )
    round: models.IntegerField = models.IntegerField()
    user1: models.ForeignKey = models.ForeignKey(
        GuestUser,
        on_delete=models.CASCADE,
        related_name="tournament_results_as_user1",
    )
    user2: models.ForeignKey = models.ForeignKey(
        GuestUser,
        on_delete=models.CASCADE,
        related_name="tournament_results_as_user2",
    )
    winner: models.ForeignKey = models.ForeignKey(
        GuestUser,
        on_delete=models.CASCADE,
        related_name="tournament_results_as_winner",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"tournament{self.tournament.id}:\
            {self.user1} vs {self.user2} in round {self.round}"
