import os
import django
import matplotlib.pyplot as plt
import numpy as np

# Replace 'myproject' with the name of your Django project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IOT_Management.settings")
django.setup()

from device.models import THdata  # Replace 'myapp' with your app name
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models.functions import ExtractHour
from django.db.models import Avg
from device.utils import get_THdata_list

# Get the current date
today = datetime.now()
# start_of_day = make_aware(datetime.combine(today, datetime.min.time()))  # Start of today
# end_of_day = make_aware(datetime.combine(today, datetime.max.time()))    # End of today

# # Fetch the device (replace 'CL01234567' with the device ID you're working with)
# device_id = "CL01234567"
# device_temperatures = list(
#     THdata.objects.filter(
#         device_id=device_id,
#         timestamp__range=(start_of_day, end_of_day)
#     ).values_list("temperature", flat=True)  # Fetch only temperature field
# )

# device_temperatures_time = list(
#     THdata.objects.filter(
#         device_id=device_id,
#         timestamp__range=(start_of_day, end_of_day)
#     ).values_list("timestamp", flat=True)  # Fetch only temperature field
# )

# # define data values
# y = np.array(device_temperatures)  # X-axis points
# x = np.array(device_temperatures_time)  # Y-axis points

# plt.plot(x, y)  # Plot the chart
# plt.show()  # display

# device_id = "CL01234567"  # Replace with your device ID
# hourly_averages = (
#     THdata.objects.filter(
#         device_id=device_id,
#         timestamp__range=(start_of_day, end_of_day)
#     )
#     .annotate(hour=ExtractHour('timestamp'))  # Extract hour from timestamp
#     .values('hour')                          # Group by hour
#     .annotate(avg_temp=Avg('temperature'))   # Calculate average temperature
#     .order_by('hour')                        # Order by hour
# )
# print(hourly_averages)

# # Find rows with `timestamp` as null
# invalid_rows = THdata.objects.filter(timestamp__isnull=True)
# print(invalid_rows)


# Prepare data for charting
# chart_data = [{"hour": entry["hour"], "average_temperature": entry["avg_temp"]} for entry in hourly_averages]

# # print(chart_data)

# hours = [entry["hour"] for entry in chart_data]
# temperatures = [entry["average_temperature"] for entry in chart_data]

# # Create the chart
# plt.plot(hours, temperatures, marker='o')
# plt.title("Hourly Temperature Changes")
# plt.xlabel("Hour of the Day")
# plt.ylabel("Average Temperature")
# plt.xticks(range(24))  # Ensure all hours are shown
# plt.grid(True)
# plt.show()

list = get_THdata_list("daily", "CL01234567", today)
# print(len(list[0]))

x = np.array([i for i in range(1, 25)])
y = list[0]
print(x)
# define data values
# x = np.array([1, 2, 3, 4])  # X-axis points
# y = x*2  # Y-axis points

plt.plot(x, y)  # Plot the chart
plt.show()  # display