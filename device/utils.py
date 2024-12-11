from .models import THdata
from django.db.models import Avg
import datetime

def convert2Fahrenheit(celsius):
        return celsius * (9/5) + 32

def get_THdata_average(type):
    today = datetime.now()

    if type == "daily":
        # Daily data
        daily_avg = THdata.objects.filter(
            timestamp__date=today.date()
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_hum=Avg('humidity')
        )
        return daily_avg
    elif type == "monthly":
        # Monthly data
        monthly_avg = THdata.objects.filter(
            timestamp__year=today.year,
            timestamp__month=today.month
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_hum=Avg('humidity')
        )
        return monthly_avg
    else:
        # Yearly data
        yearly_avg = THdata.objects.filter(
            timestamp__year=today.year
        ).aaggregate(
            avg_temp=Avg('temperature'),
            avg_hum=Avg('humidity')
        )
        return yearly_avg
