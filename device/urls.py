from django.urls import path
from .import views

app_name = 'device'

urlpatterns = [
    path('', views.deviceDashboard, name="dashboard"),
]
