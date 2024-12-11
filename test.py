import paho.mqtt.client as mqtt
import time

# Define MQTT Broker details (use Wokwi broker details)
BROKER = "test.mosquitto.org"  # Replace with your broker address
PORT = 1883  # Default MQTT port for Wokwi
TOPIC = "vanduc/temp"  # Replace with the topic you want to publish to

# Callback for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Wokwi MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Initialize MQTT Client
client = mqtt.Client()

# Attach callbacks
client.on_connect = on_connect

# Connect to the broker
client.connect(BROKER, PORT)  # Replace with your Wokwi broker address and port

# Start the loop
client.loop_start()

try:
    while True:
        # Data to publish
        message = "Hello, Wokwi!"
        
        # Publish the message
        client.publish(TOPIC, message)
        print(f"Published: '{message}' to topic: '{TOPIC}'")
        
        # Wait before sending next message
        time.sleep(20)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
