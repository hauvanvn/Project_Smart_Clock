from django.urls import path
from .import views

app_name = 'device'

urlpatterns = [
    path('<slug:slug>/', views.deviceDashboard, name="dashboard"),
]
