from asgiref.sync import async_to_sync, sync_to_async
import asyncio
import websockets
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from django.conf import settings
from .models import THdata, Devices, DeviceEvent, DeviceArlam
import json
import time
import threading
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Send device status to Front-end
channel_layer = get_channel_layer()
def handle_device_status_message(device_id, status):
    async_to_sync(channel_layer.group_send)(
        "mqtt_front_end",
        {
            "type": "send_event",
            "message": {
                "device_status": {
                    "device_id": device_id,
                    "status": status,
                }
            },
        }
    )

def handle_device_LedMode_message(device_id, ledMode):
    async_to_sync(channel_layer.group_send)(
        "mqtt_front_end",
        {
            "type": "send_event",
            "message": {
                "change_ledmode": {
                    "device_id": device_id,
                    "ledMode": ledMode
                }
            },
        }
    )

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
    
    userdata['last_message'] = {
        "time": time.time()
    }
    status = "Connected" if check_connection(device_id) else "Disconnected"
    handle_device_status_message(device_id, status)
    device = Devices.objects.get(id=device_id)

    payload = json.loads(msg.payload.decode('utf-8'))
    if ("change_led_mode" in payload):
        if device.ledmode == "MODE 1":
            device.ledmode = "MODE 2"
        elif device.ledmode == "MODE 2":
            device.ledmode = "MODE 3"
        else: 
            device.ledmode = "MODE 1"

        device.save()
        handle_device_LedMode_message(device.id, device.ledmode)

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

def check_connection(device_id):
    if device_id not in mqtt_clients:
        print(device_id)
        return False
    
    device = mqtt_clients[device_id]
    timeout = 10
    start_time = device._userdata.get('last_message', {}).get('time')
    #print(start_time, " ", time.time(), " ", time.time() - start_time)
    if (time.time() - start_time > timeout):
        return False
    return True
    

def create_mqtt_client(device_id, topic, on_mesage=on_message):
    if device_id not in mqtt_clients:
        client = mqtt.Client(userdata={"TOPIC": topic, "last_message": {"time": time.time()}})
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
    if device_id in mqtt_clients:
        return mqtt_clients[device_id]
    return None

heartbeat_stop_event = asyncio.Event() # Stop websocket
async def websocket_client():
    uri = "ws://localhost:8000/ws/mqtt/back-end"

    try:
        async with websockets.connect(uri) as webSocket:
            print("Connected to Back-end.")
            # Keep connection alive
            async def send_heartbeat():
                while not heartbeat_stop_event.is_set():
                    try:
                        await webSocket.send(json.dumps({"command": "ping"}))
                        print("Ping sent to server")
                        await asyncio.sleep(30)
                    except websockets.ConnectionClosed:
                        print("Connection closed while sending heartbeat.")
                        break

                await webSocket.close()

            heartbet_task = asyncio.create_task(send_heartbeat())
            # Send message

            # Reivce Message
            while True:
                try:
                    response = await webSocket.recv()
                    data = json.loads(response)

                    if data['command'] == "add_device":
                        create_mqtt_client(data['device_id'], data['topic'])
                    elif data['command'] == "delete_device":
                        stop_mqt_client(data['device_id'])

                    print(f"Message received from server: {data}")
                except websockets.ConnectionClosed:
                    print("Connection closed by server.")
                    break
            
            heartbeat_stop_event.set()
            await heartbet_task

    except Exception as e:
        print(f"Error: {e}")

def create_client():
    asyncio.run(websocket_client())

stop_thread_mqtt_event = threading.Event()
def send_data():
    while not stop_thread_mqtt_event.is_set():
        devices = [device for device in Devices.objects.all() if check_connection(device.id)]

        for device in devices:
            current_time = datetime.now(ZoneInfo(device.timezone))
            timee = current_time.strftime("%H%M%S")
            date = current_time.strftime("%a, %b %d, %Y")
            arlamSig = False
            event_1 = ""
            event_2 = ""

            # Nearest 2 event
            events = DeviceEvent.objects.filter(device=device)
            today_event = []
            if (events.exists()):
                events = events.filter(time__date=datetime.today()).order_by("time")
                events = [x for x in events if not x.is_past_event()]
                for event in events:
                    today_event.append(f"{event.time.strftime("%H:%M")} {event.note}")
            if (len(today_event) >= 1): 
                event_1 = today_event[0]
            if (len(today_event) >= 2): 
                event_2 = today_event[1]

            # Nearest arlam
            arlam = []
            if DeviceArlam.objects.filter(device=device).exists():
                arlams = [x for x in DeviceArlam.objects.filter(device=device).order_by('time') if x.is_past_arlam()]
                if len(arlams) != 0:
                    arlam = min(arlams, key=lambda date: abs(date.time - datetime.now()))
            if arlam != [] and abs(arlam.time - datetime.now()) <= timedelta(seconds=1):
                arlamSig = True

            # Send data to Client
            topic = f"{settings.MAIN_TOPIC}/{device.id}/inp"
            data = {
                "time": timee, 
                "date": date,
                "arlamSig": arlamSig,
                "event_1": event_1,
                "event_2": event_2,
                "led": device.ledmode, 
                "buzzer": device.buzzermode
                }
            client = get_mqtt_client(device.id)
            client.publish(topic, json.dumps(data))
            # print(f"Sended to {topic}: {json.dumps(data)}")

        time.sleep(0.5)

def initialize_mqtt_clients():
    devices = Devices.objects.all()
    for device in devices:
        topic = f"{settings.MAIN_TOPIC}/{device.id}/out"
        create_mqtt_client(device.id, topic)
    print(f"Initialized MQTT clients for {len(devices)} devices.")

    thread_socket = threading.Thread(target=create_client)
    # thread_mqtt = threading.Thread(target=send_data)
    thread_socket.start()
    # thread_mqtt.start()

    try:
        while True:
            for device_id in mqtt_clients:
                status = "Connected" if check_connection(device_id) else "Disconnected"
                # print(f"Check connection of {device_id}: {status}")
                handle_device_status_message(device_id, status)
            time.sleep(5)
            # print("Next_loop")
    except KeyboardInterrupt:
        counter = 0
        stop_thread_mqtt_event.set()
        for device_id in list(mqtt_clients.keys()):
            stop_mqt_client(device_id)
            counter += 1
        
        print(f"Stopped MQTT clients for {counter} devices.")
        
        heartbeat_stop_event.set()
