from django.urls import path

from . import views

app_name = "pingpong"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_game", views.create_game, name="create_game"),
    path("game_play", views.game_play, name="game_play"),
    path("home", views.home, name="home"),
    path("multiplayer_lobby", views.multiplayer_lobby, name="multiplayer_lobby"),
    path("multiplayer_options", views.multiplayer_options, name="multiplayer_options"),
    path("single_play_setup", views.single_play_setup, name="single_play_setup"),
    path("tournament_bracket", views.tournament_bracket, name="tournament_bracket"),
    path(
        "tournament_registration",
        views.tournament_registration,
        name="tournament_registration",
    ),
    path("start_single_play", views.start_single_play, name="start_single_play"),
]
