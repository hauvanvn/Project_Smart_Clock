import paho.mqtt.client as mqtt
from django.conf import settings
from .models import THdata, Devices
import json
import time

mqtt_clients = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        topic = userdata.get('TOPIC', 'default/topic')
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    parts = topic.split("/")
    if len(parts) != 3 or parts[0] != settings.MAIN_TOPIC:
        print(f"Unexpected topic structure: {topic}")
        return
    device_id = parts[1]
    if not Devices.objects.filter(id=device_id).exists():
        print(f"Uknown Device id: {device_id}")
        return
    device = Devices.objects.get(id=device_id)

    payload = json.loads(msg.payload.decode('utf-8'))
    # temp = payload.get("temperature")
    # humi = payload.get("humidity")
    # THdata.objects.create(device=device,temperature=temp,humidity=humi)


    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

def on_message_newClient(client, userdata, msg):
    userdata['last_message'] = {
        "topic": msg.topic,
        "payload": msg.payload.decode('utf-8'),
        "qos": msg.qos,
    }
    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

def check_connection(id):
    TOPIC_INP = id + "/inp"
    TOPIC_OUT = id + "/opt"
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.BROKER, settings.PORT, keepalive=60)
    

def create_mqtt_client(device_id, topic, on_mesage=on_message):
    if device_id not in mqtt_clients:
        client = mqtt.Client(userdata={"TOPIC": topic})
        client.on_connect = on_connect
        client.on_message = on_mesage
        client.connect(settings.BROKER, settings.PORT, keepalive=60)
        mqtt_clients[device_id] = client
        client.loop_start()
        print(f"Device {device_id} connected to {topic}.")
    else:
        print(f"MQTT client already exists for device {device_id}.")

def stop_mqt_client(device_id):
    if device_id in mqtt_clients:
        client = mqtt_clients.pop(device_id)
        topic = client._userdata.get("TOPIC")
        client.loop_stop()
        client.disconnect()
        print(f"Device {device_id} disconnected to {topic}")

def get_mqtt_client(device_id):
    return mqtt_clients[device_id]

def initialize_mqtt_clients():
    devices = Devices.objects.all()
    for device in devices:
        topic = f"{settings.MAIN_TOPIC}/{device.id}/out"
        create_mqtt_client(device.id, topic)

    print(f"Initialized MQTT clients for {len(devices)} devices.")

    try:
        while True:
            time.sleep(20)

    except KeyboardInterrupt:
        counter = 0
        for device_id in list(mqtt_clients.keys):
            stop_mqt_client(device_id)
            counter += 1
        
        print(f"Stopped MQTT clients for {counter} devices.")
