from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from device.models import Devices

@login_required(login_url="users:login")
def homePage(request):
    user = request.user
    devices = Devices.objects.filter(owner__id=user.id)
    return render(request, 'home.html', {'user': user, 'devices': devices})