# interviews/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class InterviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if "offer" in data:
            # Handle offer from client, create an answer and send back
            await self.send(text_data=json.dumps({"answer": "Generated answer here"}))

    async def disconnect(self, close_code):
        pass
