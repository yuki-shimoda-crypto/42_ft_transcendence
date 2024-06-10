from django.urls import path

from . import views

app_name = "pingpong"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_game", views.create_game, name="create_game"),
]
