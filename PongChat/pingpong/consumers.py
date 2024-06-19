import json
from channels.generic.websocket import AsyncWebsocketConsumer


# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data["action"]

#         if action == "request_match":
#             opponent_username = data["opponent"]
#             # Send the match request to the specified opponent
#             await self.channel_layer.group_send(
#                 f"user_{opponent_username}",
#                 {
#                     "type": "match_request",
#                     "from_user": self.scope["user"].username,
#                 }
#             )

#     async def match_request(self, event):
#         # Forward the match request to the user
#         from_user = event["from_user"]
#         await self.send(text_data=json.dumps({
#             "action": "match_request",
#             "from_user": from_user,
#         }))

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive(self, text_data):
        print("Received")
        await self.send(text_data=f"Message: {text_data}")

    async def send_message(self, res):
        print("Sent message")
        await self.send(text_data=res)
