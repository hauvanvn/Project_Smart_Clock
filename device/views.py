from django.shortcuts import render

# Create your views here.
def deviceDashboard(request):
    return render(request, 'device/device.html')