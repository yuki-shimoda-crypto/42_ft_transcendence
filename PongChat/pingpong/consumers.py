import json
import random

import redis
from channels.generic.websocket import AsyncWebsocketConsumer

redis_client = redis.Redis(host="redis", port=6379, db=0)


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        redis_client.sadd("waiting_room", self.channel_name)

    async def disconnect(self, close_code):
        redis_client.srem("waiting_room", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        if action == "start_match":
            players = list(redis_client.smembers("waiting_room"))
            if len(players) >= 2:
                chosen_players = random.sample(players, 2)
                await self.start_game_session(chosen_players)

    async def start_game_session(self, players):
        game_id = f"game_{random.randint(1000, 9999)}"

        # host = self.get_header("host", "localhost")
        # scheme = self.scope.get("scheme", "ws")
        # base_url = f"{scheme}://{host}"
        # game_url = urljoin(base_url, f"/pingpong/multiplayer_play_remote/{game_id}/")
        game_url = "http://localhost:8001/pingpong/multiplayer_play_remote/" + game_id

        for player in players:
            # redis_client.sadd(game_id, player)
            redis_client.srem("waiting_room", player)

            await self.channel_layer.send(
                player.decode("utf-8"),
                {
                    "type": "game_start",
                    "game_id": game_id,
                    "message": "match_found",
                    "url": game_url,
                },
            )

    # def get_header(self, header_name, default=None):
    #     header_name = header_name.encode("utf-8")
    #     for name, value in self.scope["headers"]:
    #         if name == header_name:
    #             return value.decode("utf-8")
    #     return default

    async def game_start(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "game_id": event["game_id"],
                    "message": event["message"],
                    "url": event["url"],
                }
            )
        )


class GameSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.group_name = f"game_{self.game_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        redis_client.incr(f"{self.group_name}_size")
        group_size = int(redis_client.get(f"{self.group_name}_size") or 0)
        player_position = "left" if group_size % 2 == 0 else "right"

        await self.send(
            json.dumps(
                {
                    "type": "player_position",
                    "position": player_position,
                }
            )
        )

    async def disconnect(self, close_code):
        redis_client.decr(f"{self.group_name}_size")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get("type")

        if type == "update_paddle":
            paddle_data = {
                "type": "paddle_update",
                "paddle_position_ratio": data["paddle_position_ratio"],
                "player_position": data["player_position"],
            }

            await self.channel_layer.group_send(self.group_name, paddle_data)

        if type == "update_ball":
            ball_data = {
                "type": "ball_update",
                "ball_position_ratio_x": data["ball_position_ratio_x"],
                "ball_position_ratio_y": data["ball_position_ratio_y"],
                "ball_position_ratio_dx": data["ball_position_ratio_dx"],
                "ball_position_ratio_dy": data["ball_position_ratio_dy"],
            }

            await self.channel_layer.group_send(self.group_name, ball_data)

    async def paddle_update(self, event):
        await self.send(json.dumps(event))
    
    async def ball_update(self, event):
        await self.send(json.dumps(event))
