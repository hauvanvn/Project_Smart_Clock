from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import send_deviceData
from .models import Devices, DeviceEvent, DeivceArlam
from .forms import ArlarmForm
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

# Create your views here.
@login_required(login_url="users:login")
def deviceDashboard(request, slug):
    user = request.user
    device = Devices.objects.get(id=slug)
    events = DeviceEvent.objects.filter(device=device)
    current_time = datetime.now(ZoneInfo(device.timezone))
    utc_offset = current_time.strftime('%z')

    arlam = {"time": "No upcoming arlam"}
    if DeivceArlam.objects.filter(device=device).exists():
        arlams = [x for x in DeivceArlam.objects.filter(device=device).order_by('time') if not x.is_past_arlam()]
        if len(arlams) != 0:
            arlam = min(arlams, key=lambda date: abs(date.time - datetime.now()))

    if request.method == "POST":
        if "change-timezone" in request.POST:
            new_timezone = request.POST.get("timezone_offset")
            device.timezone = new_timezone
            device.save()
            messages.success(request, "Change timezone successfully")
            return redirect('device:dashboard', slug=slug)
        elif "set_arlam" in request.POST:
            new_time = request.POST.get("alarm_date")
            new_arlam = ArlarmForm({'device': device, 'time': new_time})

            if new_arlam.is_valid():
                new_arlam.save()
                messages.success(request, "Add arlam successfully")
            return redirect('device:dashboard', slug=slug)
            
    return render(request, 'device/device.html', {
        'user': user, 
        'device': device, 
        'currentTime': current_time,
        'utc_offset': utc_offset,
        'events': events,
        'arlam': arlam
    })