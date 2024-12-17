from django.db import models
from user.models import User
from datetime import datetime

# Create your models here.

class Devices(models.Model):
    class Type(models.TextChoices):
        CL = "SMART CLOCK", "Smart Clock"
        NONE = "NONE", "None"

    class LedMode(models.TextChoices):
        MODE_1 = "MODE 1", "Mode 1"
        MODE_2 = "MODE 2", "Mode 2"
        MODE_3 = "MODE 3", "Mode 3"

    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type, default=Type.NONE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timezone = models.CharField(max_length=50, default="Asia/Ho_Chi_Minh")
    ledmode = models.CharField(max_length=6, choices=LedMode, default=LedMode.MODE_1)

    def is_connected(self):
        from .mqtt import check_connection
        if check_connection(self.id):
            return "Connected"
        else:
            return "Disconnected"
        
class DeviceArlam(models.Model):
    id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def is_past_arlam(self):
        return self.time < datetime.now()
    
class DeviceEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    time = models.DateTimeField()
    tag = models.CharField(max_length=50, null=True)
    note = models.TextField()

    def is_past_event(self):
        return self.time < datetime.now()

class THdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: Temp={self.temperature}, Hum={self.humidity}"