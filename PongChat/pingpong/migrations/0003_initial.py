# Generated by Django 5.0.4 on 2024-06-29 08:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pingpong", "0002_remove_match_game_remove_match_player1_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score1", models.IntegerField(default=0)),
                ("score2", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("ongoing", "Ongoing"), ("done", "Done")],
                        default="ongoing",
                        max_length=10,
                    ),
                ),
                ("date_start", models.DateTimeField(auto_now_add=True)),
                ("date_end", models.DateTimeField(blank=True, null=True)),
                (
                    "player1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "player2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_won",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]