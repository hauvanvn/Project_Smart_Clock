import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IOT_Management.settings')
django.setup()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Devices

class MQTTFrontEndConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_device(self, id):
        return Devices.objects.get(id=id)
    
    @database_sync_to_async
    def save_device(self, device):
        device.save()
    
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
        
        if data["command"] == "change_led_mode":
            device = await self.get_device(data["device_id"])
            device.ledmode = data["newMode"]
            await self.save_device(device)
        elif data["command"] == "change_buzzer_mode":
            device = await self.get_device(data["device_id"])
            device.buzzermode = data["newMode"]
            await self.save_device(device)

        print(f"Back-End received from front-end: {data}")

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
            print("Back-End received from back-end: keep-alive")
        else:
            print(f"Back-End received from back-end: {data}")


    async def send_event(self, event):
        await self.send(text_data=json.dumps(event["message"]))
