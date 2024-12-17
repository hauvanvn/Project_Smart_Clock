from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from .models import THdata, Devices
from django.db.models import Avg
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime, timedelta
from device.mqtt import stop_mqt_client

def send_newDevice(device_id, topic):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mqtt_back_end",
        {
            "type": "send_event",
            "message": {
                "command": "add_device",
                "device_id": device_id,
                "topic": topic,
            },
        }
    )

@receiver(post_delete, sender=Devices)
def delete_mqtt_client(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mqtt_back_end",
        {
            "type": "send_event",
            "message": {
                "command": "delete_device",
                "device_id": instance.id,
            },
        }
    )

def send_deviceData(timezone, ledmode):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mqtt_front_end",
        {
            "type": "send_event",
            "message": {
                "command": "device_data",
                "timezone": timezone,
                "ledmode": ledmode,
            },
        }
    )

def convert2Fahrenheit(celsius):
        return celsius * (9/5) + 32

def get_THdata_average(type, device_id, date):
    if type == "hourly":
        # Hourly data
        start_time = date.repalce(hour=date.hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        hourly_avg = THdata.objects.filter(
            device=device_id, 
            timestamp__range=(start_time,end_time)
        ).aaggregate(
            temp = Avg('temperature'),
            humi = Avg('humidity')
        )
        return hourly_avg
    elif type == "daily":
        # Daily data
        daily_avg = THdata.objects.filter(
            device=device_id,
            timestamp__date=date
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_humi=Avg('humidity')
        )
        return daily_avg
    elif type == "monthly":
        # Monthly data
        monthly_avg = THdata.objects.filter(
            device=device_id,
            timestamp__year=date.year,
            timestamp__month=date.month
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_humi=Avg('humidity')
        )
        return monthly_avg
    else:
        # Yearly data
        yearly_avg = THdata.objects.filter(
            device=device_id,
            timestamp__year=date.year
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_humi=Avg('humidity')
        )
        return yearly_avg

def get_THdata_list(type, device_id, date):
     if type == "daily":
        daily_temp = []
        daily_humi = []

        for hour in range(24):
            data = get_THdata_average("hourly", device_id, date.replace(hour=hour, minute=0, second=0, microsecond=0))
            daily_temp.append(data["temp"])
            daily_humi.append(data["humi"])
        return daily_temp, daily_humi
     elif type == "monthly":
        monthly_temp = []
        monthly_humi = []
        days_in_month = (date.repalce(day=28) + timedelta(days=4)).day

        for day in range(1, days_in_month+1):
            data = get_THdata_average("daily", device_id, date.replace(day=day, hour=0, minute=0, second=0, microsecond=0))
            monthly_temp.append(data["temp"])
            monthly_humi.append(data["humi"])
        return monthly_temp, monthly_humi
     else:
        yearly_temp = []
        yearly_humi = []

        for day in range(1, 13):
            data = get_THdata_average("monthly", device_id, date.replace(month=date.month))
            monthly_temp.append(data["temp"])
            monthly_humi.append(data["humi"])
        return monthly_temp, monthly_humi
          

def getType(serial):
     if serial[:2] == "CL":
          return Devices.Type.CL
     else:
          return Devices.Type.NONE