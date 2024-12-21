from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from device.models import Devices
from device.forms import DevicesForm
from device.utils import getType, send_newDevice
from device.mqtt import create_mqtt_client, stop_mqt_client, get_mqtt_client, on_message_newClient

import time

@login_required(login_url="users:login")
def homePage(request):
    user = request.user
    devices = Devices.objects.filter(owner__id=user.id)

    if request.method == "POST":
        if 'delete_device' in request.POST:
            # Delete device
            device = Devices.objects.get(id=request.POST.get('delete_device'))
            device.delete()
            messages.success(request, "Delete device successfully!")
            return redirect('home')
        
        if 'change_name' in request.POST:
            # Change device name
            device = Devices.objects.get(id=request.POST.get('change_name'))
            device.name = request.POST.get('new_name')
            device.save()
            messages.success(request, "Change name device successfully!")
            return redirect('home')

        # Add device
        id = request.POST.get('device_id')
        name = request.POST.get('device_name')
        type = getType(id)

        TOPIC_OUT = settings.MAIN_TOPIC + "/" + id + "/out"
        
        create_mqtt_client(id, TOPIC_OUT, on_message_newClient)

        for counter in range(11):
            client = get_mqtt_client(id)
            last_message = client._userdata.get("last_message")
            if "topic" in last_message:
                client.publish(TOPIC_OUT, "pong")
                stop_mqt_client(id)
                newDevice = DevicesForm({'id': id, 'name': name, 'type': type, 'owner': user})
                if newDevice.is_valid():
                    messages.success(request, "Device added successfully")
                    newDevice.save()
                    send_newDevice(id, TOPIC_OUT)
                    return redirect('home')
                
            if counter == 10:
                stop_mqt_client(id)
                messages.warning(request, "Invalid device ID")
                return redirect('home')
            time.sleep(1)

    return render(request, 'home.html', {'user': user, 'devices': devices})