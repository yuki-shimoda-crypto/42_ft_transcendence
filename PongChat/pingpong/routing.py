from chat.consumers import ChatroomConsumer
from django.urls import path, re_path

from .consumers import GameConsumer

websocket_urlpatterns = [
    # re_path(r"ws/game/(?P<room_name>\w+)/$", GameConsumer.as_asgi())
    re_path(r"ws/game/$", GameConsumer.as_asgi()),
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
]
