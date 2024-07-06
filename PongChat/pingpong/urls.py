from django.urls import path

from . import views

app_name = "pingpong"

urlpatterns = [
    # path("create_game", views.create_game, name="create_game"),
    path("", views.index, name="index"),
    path("game_play", views.game_play, name="game_play"),
    path("home", views.home, name="home"),
    path("multiplayer_lobby", views.multiplayer_lobby, name="multiplayer_lobby"),
    path("multiplayer_options", views.multiplayer_options, name="multiplayer_options"),
    path(
        "multiplayer_play_local",
        views.multiplayer_play_local,
        name="multiplayer_play_local",
    ),
    path(
        "multiplayer_play_remote/<str:game_id>",
        views.multiplayer_play_remote,
        name="multiplayer_play_remote",
    ),
    path("single_play_setup", views.single_play_setup, name="single_play_setup"),
    path("single_play_start", views.single_play_start, name="single_play_start"),
    path("tournament_bracket", views.tournament_bracket, name="tournament_bracket"),
    path(
        "tournament_registration",
        views.tournament_registration,
        name="tournament_registration",
    ),
]
