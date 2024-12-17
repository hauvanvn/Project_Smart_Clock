from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import send_deviceData
from .models import Devices, DeviceEvent, DeviceArlam
from .forms import ArlarmForm, EventForm
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
    if DeviceArlam.objects.filter(device=device).exists():
        arlams = [x for x in DeviceArlam.objects.filter(device=device).order_by('time') if not x.is_past_arlam()]
        if len(arlams) != 0:
            arlam = min(arlams, key=lambda date: abs(date.time - datetime.now()))

    today_event = {"time": "", "note": "No event today"}
    if DeviceEvent.objects.filter(device=device).exists():

        event_list = []
        for event in events:
            dateTime = event.time

            event_list.append(event.note)
            event_list.append(event.tag)
            event_list.append(dateTime.strftime("%Y"))
            event_list.append(dateTime.strftime("%m"))
            event_list.append(dateTime.strftime("%d"))
            event_list.append(dateTime.strftime("%H:%M"))
        

    if request.method == "POST":
        if "change-timezone" in request.POST:
            new_timezone = request.POST.get("timezone_offset")
            device.timezone = new_timezone
            device.save()
            messages.success(request, "Change timezone successfully")
            return redirect('device:dashboard', slug=slug)
        elif "set_arlam" in request.POST:
            new_time = request.POST.get("alarm_dateTime")
            new_arlam = ArlarmForm({'device': device, 'time': new_time})

            if new_arlam.is_valid():
                new_arlam.save()
                messages.success(request, "Add arlam successfully")
            return redirect('device:dashboard', slug=slug)
        elif "add_event":
            event_content = request.POST.get("event_content")
            event_time = request.POST.get("event_dateTime")
            event_tag = request.POST.get("note_color")

            new_event = EventForm({'device': device, 'time': event_time, 'tag': event_tag, 'note': event_content})
            if new_event.is_valid():
               new_event.save()
               messages.success(request, "Add event successfully")
            return redirect('device:dashboard', slug=slug)

    return render(request, 'device/device.html', {
        'user': user, 
        'device': device, 
        'currentTime': current_time,
        'utc_offset': utc_offset,
        'events': event_list,
        'arlam': arlam
    })