import os
import django
from random import uniform
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IOT_Management.settings')  # Replace 'myproject' with your project name
django.setup()

from device.models import THdata, Devices  # Replace 'myapp' with your app name

# Fetch or create a test device  
test_device = Devices.objects.get(id="CL01234567")

rootTime = datetime.now()

print(rootTime)
print("ROOT TIME ABOVE")
# Generate dummy data
for i in range(21600):  # Generate 100 entries
    currentTime = rootTime + timedelta(seconds=i)
    THdata.objects.create(
        device=test_device,
        temperature=round(uniform(20.0, 30.0), 2),  # Random temperature between 20 and 30
        humidity=round(uniform(30.0, 60.0), 2),     # Random humidity between 30 and 60
        timestamp=currentTime  # Recent timestamps
    )
    # print(THdata.objects.get(id=i+1))

print("Dummy data inserted successfully!")
