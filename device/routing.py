from django.urls import path
from .consumers import MQTTFrontEndConsumer, MQTTBackEndConsumer

websocket_urlpatterns = [
    path('ws/mqtt/front-end', MQTTFrontEndConsumer.as_asgi()),
    path('ws/mqtt/back-end', MQTTBackEndConsumer.as_asgi()),
]
