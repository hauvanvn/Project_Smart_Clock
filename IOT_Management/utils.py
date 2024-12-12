import paho.mqtt.client as mqtt
import time

from django.conf import settings

TOPIC_INP = ""
TOPIC_OUT = ""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Wokwi MQTT Broker!")
        client.subscribe(TOPIC_OUT)
        print(f"Subscribed to topic: {TOPIC_OUT}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

def check_connection(id):
    TOPIC_INP = id + "/inp"
    TOPIC_OUT = id + "/opt"
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.BROKER, PORT, keepalive=60)