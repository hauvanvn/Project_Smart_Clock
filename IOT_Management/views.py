from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from device.models import Devices
from device.forms import DevicesForm
from device.utils import getType

@login_required(login_url="users:login")
def homePage(request):
    user = request.user
    devices = Devices.objects.filter(owner__id=user.id)

    print(devices)

    if request.method == "POST":
        id = request.POST.get('device_id')
        name = request.POST.get('device_name')
        type = getType(id)

        TOPIC_INP = id + "/inp"
        TOPIC_OUT = id + "/out"

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER, PORT, keepalive=60)

        client.loop_start()

        connected = False
        waitTime = 10
        while waitTime:
            if client.on_message:
                connected = True
                TOPIC_INP = ""
                TOPIC_OUT = ""
                client.loop_stop()
                client.disconnect()
                break
            msg = '{"connect":"1", "LED":"2", "touched":"True"}'
            client.publish(TOPIC_INP, msg)
            waitTime -= 1
            time.sleep(1)

        if connected:
            newDevice = DevicesForm({'id': id, 'name': name, 'type': type, 'owner': user})

            if newDevice.is_valid():
                messages.success(request, "Device added successfully")
                newDevice.save()
                return render(request, 'home')
            else:
                messages.warning(request, "Missing device name")
        else:
            messages.warning(request, "Wrong ID")

    return render(request, 'home.html', {'user': user, 'devices': devices})