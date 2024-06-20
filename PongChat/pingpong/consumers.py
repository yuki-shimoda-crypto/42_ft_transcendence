import json
from urllib.parse import urljoin
import random
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "waiting_room",
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "waiting_room",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        if action == "start_match":
            players = await self.channel_layer.group_list("waiting_room")
            if len(players) >= 2:
                chosen_players = random.sample(players, 2)
                await self.start_game_session(chosen_players)

    async def start_game_session(self, players):
        game_id = f"game_{random.randint(1000, 9999)}"
        host = self.scope["headers"].get(b"host", b"localhost").decode("utf-8")
        scheme = self.scope["scheme"]
        base_url = f"{scheme}://{host}"
        game_url = urljoin(base_url, f"/game/{game_id}/")

        for player in players:
            await self.channel_layer.group_add(game_id, player)
            await self.channel_layer.group_discard("waiting_room", player)
            await self.channel_layer.send(
                player,
                {
                    "type": "game.start",
                    "game_id": game_id,
                    "message": "match_found",
                    "url": game_url
                }
            )

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            "game_id": event["game_id"],
            "message": event["message"]
        }))
