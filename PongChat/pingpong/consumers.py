import json
import logging
import random

import redis
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Game

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host="redis", port=6379, db=0)

User = get_user_model()


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user_info = json.dumps(
            {
                "channel_name": self.channel_name,
                "user_id": self.scope["user"].id,
            }
        )
        redis_client.sadd("waiting_room", user_info)

    async def disconnect(self, close_code):
        user_info = json.dumps(
            {
                "channel_name": self.channel_name,
                "user_id": self.scope["user"].id,
            }
        )
        redis_client.srem("waiting_room", user_info)

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
        game_url = "http://localhost:8001/pingpong/multiplayer_play_remote/" + game_id
        player_ids = [json.loads(player).get("user_id") for player in players]
        await self.create_game_coloum(game_id, player_ids[0], player_ids[1])

        for user_info in players:
            # redis_client.sadd(game_id, player)
            channel_name = json.loads(user_info).get("channel_name")
            redis_client.srem("waiting_room", user_info)

            await self.channel_layer.send(
                channel_name,
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

    @database_sync_to_async
    def create_game_coloum(self, game_id, player_id_1, player_id_2):
        player1 = User.objects.get(id=player_id_1)
        player2 = User.objects.get(id=player_id_2)
        game_id_num = int("".join(filter(str.isdigit, game_id)))
        game = Game.objects.create(id=game_id_num, player1=player1, player2=player2)
        game.save()
        # return game

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

        logger.info(f"Connected to {self.channel_name}")

        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_id_num = int("".join(filter(str.isdigit, self.game_id)))
        self.user = self.scope["user"]
        self.game = await self.get_game(self.game_id_num)
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

        await self.send(
            json.dumps(
                {
                    "type": "score_update",
                    "score1": self.game.score1,
                    "score2": self.game.score2,
                }
            )
        )

        await self.send(
            json.dumps(
                {
                    "type": "set_user_id",
                    "user_id": self.user.id,
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

        elif type == "update_ball":
            ball_data = {
                "type": "ball_update",
                "ball_position_ratio_x": data["ball_position_ratio_x"],
                "ball_position_ratio_y": data["ball_position_ratio_y"],
                "ball_position_ratio_dx": data["ball_position_ratio_dx"],
                "ball_position_ratio_dy": data["ball_position_ratio_dy"],
            }

            await self.channel_layer.group_send(self.group_name, ball_data)

        elif type == "update_score":
            if self.is_valid_score_update(data):
                logger.info("-----------------------------------------------------")
                await self.update_game_score(data)
                score_data = {
                    "type": "score_update",
                    "score1": self.game.score1,
                    "score2": self.game.score2,
                }
                await self.channel_layer.group_send(self.group_name, score_data)
            else:
                logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                error_data = {
                    "type": "score_update_error",
                    "error": "Wait for 1 second before updating the score again.",
                }
                await self.channel_layer.group_send(self.group_name, error_data)

        elif type == "end_game":
            await self.finalize_game()

    async def paddle_update(self, event):
        await self.send(json.dumps(event))

    async def ball_update(self, event):
        await self.send(json.dumps(event))

    async def score_update(self, event):
        await self.send(json.dumps(event))

    async def score_update_error(self, event):
        await self.send(json.dumps(event))

    # @database_sync_to_async
    # def create_or_update_game(self, game_id, player):
    #     game, created = Game.objects.get_or_create(
    #         id=game_id, defaults={"player1": player}
    #     )
    #     if not created and game.player1 is None:
    #         game.player1 = player
    #         game.save()
    #     elif not created and game.player2 is None:
    #         game.player2 = player
    #         game.save()
    #     return game

    @database_sync_to_async
    def get_game(self, game_id):
        # if not Game.objects.filter(id=game_id).exists():
        #     game = Game.objects.create(
        #         id=game_id,
        #     )
        #     return game
        return Game.objects.get(id=game_id)

    @database_sync_to_async
    def is_valid_score_update(self, data):
        is_valid_score = False
        is_valid_time = False
        current_score1 = self.game.score1
        current_score2 = self.game.score2
        last_update_time = self.game.score_last_update

        if data["score1"] == current_score1 + 1 and data["score2"] == current_score2:
            is_valid_score = True
        elif data["score2"] == current_score2 + 1 and data["score1"] == current_score1:
            is_valid_score = True

        if last_update_time + timezone.timedelta(seconds=1) < timezone.now():
            is_valid_time = True

        if is_valid_score and is_valid_time:
            return True
        return False

    @database_sync_to_async
    def update_game_score(self, data):
        current_score1 = self.game.score1
        current_score2 = self.game.score2
        logger.info(f"Current database scores: {current_score1}, {current_score2}")
        logger.info(
            f"data['score1']: {data['score1']}, data['score2']: {data['score2']}"
        )

        if data["score1"] == current_score1 + 1:
            self.game.score1 += 1
        elif data["score2"] == current_score2 + 1:
            self.game.score2 += 1
        self.game.score_last_update = timezone.now()

        self.game.save()

        # score_data = {
        #     "type": "score_update",
        #     "score1": self.game.score1,
        #     "score2": self.game.score2,
        # }
        # self.channel_layer.group_send(self.group_name, score_data)

    @database_sync_to_async
    def finalize_game(self):
        self.game.date_end = timezone.now()
        if self.game.score1 > self.game.score2:
            self.game.winner = self.game.player1
        elif self.game.score1 < self.game.score2:
            self.game.winner = self.game.player2
        self.game.status = "done"
        self.game.save()
        self.channel_layer.group_send(
            self.group_name,
            {
                "type": "game_end",
                "winner": self.game.winner.username,
            },
        )
