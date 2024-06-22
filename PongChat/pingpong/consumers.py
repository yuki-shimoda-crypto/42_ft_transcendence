import json
from urllib.parse import urljoin
import random
from channels.generic.websocket import AsyncWebsocketConsumer
import redis

redis_client = redis.Redis(host="redis", port=6379, db=0)


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        redis_client.sadd("waiting_room", self.channel_name)
        # await self.channel_layer.group_add(
        #     "waiting_room",
        #     self.channel_name
        # )

    async def disconnect(self, close_code):
        redis_client.srem("waiting_room", self.channel_name)
        # await self.channel_layer.group_discard(
        #     "waiting_room",
        #     self.channel_name
        # )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        if action == "start_match":
            players = list(redis_client.smembers("waiting_room"))
            # players = await self.channel_layer.group_list("waiting_room")
            if len(players) >= 2:
                chosen_players = random.sample(players, 2)
                await self.start_game_session(chosen_players)

    async def start_game_session(self, players):
        game_id = f"game_{random.randint(1000, 9999)}"
        # host = self.get_header("host", "localhost")
        # scheme = self.scope.get("scheme", "ws")
        # base_url = f"{scheme}://{host}"
        # game_url = urljoin(base_url, f"/game/{game_id}/")

        for player in players:
            redis_client.sadd(game_id, player)
            redis_client.srem("waiting_room", player)

        for player in redis_client.smembers(game_id):
            await self.channel_layer.send(
                player.decode("utf-8"),
                {
                    "type": "game_start",
                    "game_id": game_id,
                    "message": "match_found",
                    "url": "http://localhost:8000/game/"
                }
            )

            # await self.channel_layer.group_add(game_id, player)
            # await self.channel_layer.group_discard("waiting_room", player)
            # await self.channel_layer.send(
            #     player,
            #     {
            #         "type": "game.start",
            #         "game_id": game_id,
            #         "message": "match_found",
            #         "url": "http://localhost:8000/game/"
            #     }
            # )
    
    # def get_header(self, header_name, default=None):
    #     header_name = header_name.encode("utf-8")
    #     for name, value in self.scope["headers"]:
    #         if name == header_name:
    #             return value.decode("utf-8")
    #     return default

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            "game_id": event["game_id"],
            "message": event["message"],
            "url": event["url"]
        }))
