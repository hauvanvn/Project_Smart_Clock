from django.core.management.base import BaseCommand
from device.mqtt import initialize_mqtt_clients

class Command(BaseCommand):
    help = "Run the MQTT client"


    def handle(self, *args, **options):
        self.stdout.write(f"Starting MQTT client...")
        initialize_mqtt_clients()
        self.stdout.write(f"Stopped MQTT client.")
