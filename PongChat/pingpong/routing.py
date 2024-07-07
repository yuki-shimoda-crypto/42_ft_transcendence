from django.urls import re_path

from .consumers import GameConsumer, GameSessionConsumer

websocket_urlpatterns = [
    # re_path(r"ws/game/(?P<room_name>\w+)/$", GameConsumer.as_asgi())
    re_path(r"ws/game/$", GameConsumer.as_asgi()),
    re_path(r"ws/game/(?P<game_id>\w+)/$", GameSessionConsumer.as_asgi()),
]
