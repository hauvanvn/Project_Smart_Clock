from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import paho.mqtt.client as mqtt
from .models import Devices, AggregateData
from django.db.models import Avg
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime, timedelta
from device.mqtt import stop_mqt_client
from channels.db import database_sync_to_async

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

def send_changeChart(user, device_id, temp, humi):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mqtt_front_end",
        {
            "type": "send_event",
            "message": {
                "user": user,
                "deviceId": device_id,
                "dht22_data": {
                    "temp": temp,
                    "humi": humi
                }
            },
        }
    )

def convert2Fahrenheit(celsius):
        return celsius * (9/5) + 32

def get_THdata_average(type, device_id, date):
    if type == "hourly":
        # Hourly data
        start_time = date.replace(hour=date.hour, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1) - timedelta(seconds=1)

        if AggregateData.objects.filter(device=device_id, 
                                        timestamp__range=(start_time,end_time)).exists():
            hourly_avg = AggregateData.objects.filter(
                device=device_id, 
                timestamp__range=(start_time,end_time)
            ).aggregate(
                avg_temp = Avg('avg_temperature'),
                avg_humi = Avg('avg_humidity')
            )
            return hourly_avg
        else:
            return {
                'avg_temp': 0,
                'avg_humi': 0
            }
        
    elif type == "daily":
        # Daily data
        if AggregateData.objects.filter(device=device_id,
                                 timestamp__date=date).exists():
            daily_avg = AggregateData.objects.filter(
                device=device_id,
                timestamp__date=date
            ).aggregate(
                avg_temp=Avg('avg_temperature'),
                avg_humi=Avg('avg_humidity')
            )
            return daily_avg
        else:
            return {
                'avg_temp': 0,
                'avg_humi': 0
            }
        
    elif type == "monthly":
        # Monthly data
        if AggregateData.objects.filter(device=device_id,
                                 timestamp__year=date.year,
                                 timestamp__month=date.month).exists():
            
            monthly_avg = AggregateData.objects.filter(
                device=device_id,
                timestamp__year=date.year,
                timestamp__month=date.month
            ).aggregate(
                avg_temp=Avg('avg_temperature'),
                avg_humi=Avg('avg_humidity')
            )
            return monthly_avg
        else:
            return {
                'avg_temp': 0,
                'avg_humi': 0
            }
    else:
        # Yearly data
        if AggregateData.objects.filter(device=device_id,
                                 timestamp__year=date.year).exists():
            yearly_avg = AggregateData.objects.filter(
                device=device_id,
                timestamp__year=date.year
            ).aggregate(
                avg_temp=Avg('avg_temperature'),
                avg_humi=Avg('avg_humidity')
            )
            return yearly_avg
        else:
            return {
                'avg_temp': 0,
                'avg_humi': 0
            }

def get_THdata_list(type, device_id, date):
     if type == "daily":
        daily_temp = []
        daily_humi = []

        for Hour in range(24):
            data = get_THdata_average("hourly", device_id, date.replace(hour=Hour, minute=0, second=0))
            
            daily_temp.append(data["avg_temp"])
            daily_humi.append(data["avg_humi"])
        return daily_temp, daily_humi
     
     elif type == "monthly":
        monthly_temp = []
        monthly_humi = []
        next_month = (date.replace(day=28) + timedelta(days=4))
        days_in_month = (next_month - timedelta(days=next_month.day)).day

        for day in range(1, days_in_month+1):
            data = get_THdata_average("daily", device_id, date.replace(day=day, hour=0, minute=0))
            monthly_temp.append(data["avg_temp"])
            monthly_humi.append(data["avg_humi"])
        return monthly_temp, monthly_humi
     else:
        yearly_temp = []
        yearly_humi = []

        for month in range(1, 13):
            data = get_THdata_average("monthly", device_id, date.replace(month=month))
            yearly_temp.append(data["avg_temp"])
            yearly_humi.append(data["avg_humi"])
        return yearly_temp, yearly_humi
          

def getType(serial):
     if serial[:2] == "CL":
          return Devices.Type.CL
     else:
          return Devices.Type.NONE