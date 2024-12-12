import paho.mqtt.client as mqtt
import time
import json

# Define MQTT Broker details (use Wokwi broker details)
BROKER = "test.mosquitto.org"  # Replace with your broker address
PORT = 1883  # Default MQTT port for Wokwi
TOPIC_INP = "CL01234567/inp"  # Replace with the topic you want to publish to
TOPIC_OUT = "CL01234567/out"

# Callback for connection
def on_connect(client, userdata, flags, rc, TOPIC_out):
    if rc == 0:
        print("Connected to Wokwi MQTT Broker!")
        client.subscribe("CL01234567/opt")
        print(f"Subscribed to topic: CL01234567/opt")
    else:
        print(f"Failed to connect, return code {rc}")

# Initialize MQTT Client
client = mqtt.Client()

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

# Attach callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, keepalive=60)  # Replace with your Wokwi broker address and port

# Start the loop
client.loop_start()

try:
    while True:
        # Data to publish
        message = '{"connect":"1", "LED":"2", "touched":"True"}'
        
        # Publish the message
        client.publish(TOPIC_INP, message)
        print(f"Published: '{message}' to topic: '{TOPIC_INP}'")
        # Wait before sending next message
        time.sleep(20)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
