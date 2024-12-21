# Create data of temperture and humidity manually for statistic testing in dashboard line chart
# Remember to Change auto_now_add=True to false in timestamp of AggregateData models
# After changing model remember to makemigrations and migrate

import os
import django
from random import uniform
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IOT_Management.settings')  # Replace 'myproject' with your project name
django.setup()

from device.models import AggregateData, Devices  # Replace 'myapp' with your app name

# Fetch or create a test device  
test_device = Devices.objects.get(id="CL0001")

rootTime = datetime(year=2024, month=12, day=20)

print(rootTime)
print("ROOT TIME ABOVE")
# Generate dummy data
for i in range(8760):  # Generate 100 entries
    if i % 24 == 0:
        print("Done days: ", i // 24)
    currentTime = rootTime + timedelta(hours=i)
    AggregateData.objects.create(
        device=test_device,
        avg_temperature=round(uniform(20.0, 30.0), 2),  # Random temperature between 20 and 30
        avg_humidity=round(uniform(30.0, 60.0), 2),     # Random humidity between 30 and 60
        timestamp=currentTime  # Recent timestamps
    )
    # print(THdata.objects.get(id=i+1))

print("Dummy data inserted successfully!")
