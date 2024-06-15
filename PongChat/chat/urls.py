from django.urls import path

from .views import chat_view, get_or_create_chatroom, profile_view

urlpatterns = [
    path("", chat_view, name="home"),
    path("chat", chat_view, name="public-chat"),
    path("<username>", get_or_create_chatroom, name="start-chat"),
    path("room/<chatroom_name>", chat_view, name="chatroom"),
    path("@<username>/", profile_view, name="profile"),
]
