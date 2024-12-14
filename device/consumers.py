import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MQTTFrontEndConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "mqtt_front_end"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        print(f"Back-End received: {message}")

    async def send_event(self, event):
        await self.send(text_data=json.dumps(event["message"]))

class MQTTBackEndConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "mqtt_back_end"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if (data["command"] == "ping"):
            print("Back-End received: keep-alive")
        else:
            print(f"Back-End received: {data}")


    async def send_event(self, event):
        await self.send(text_data=json.dumps(event["message"]))
