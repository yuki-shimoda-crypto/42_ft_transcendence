from django.urls import path

from .views import (
    chat_view,
    get_or_create_chatroom,
    profile_view,
    user_block_post,
    user_list,
)

urlpatterns = [
    path("", user_list, name="chat-home"),
    path("<username>", get_or_create_chatroom, name="start-chat"),
    path("room/<chatroom_name>", chat_view, name="chatroom"),
    path("@<username>/", profile_view, name="profile"),
    path("block/<str:username>", user_block_post, name="block"),
]
