from django.db import models
from user.models import User

# Create your models here.

class Devices(models.Model):
    class Type(models.TextChoices):
        CL = "SMART CLOCK", "Smart Clock"
        NONE = "NONE", "None"

    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type, default=Type.NONE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class THdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: Temp={self.temperature}, Hum={self.humidity}"
