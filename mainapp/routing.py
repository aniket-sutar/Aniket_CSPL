# from django.urls import path
# from .consumers import OrderNotificationConsumer

# websocket_urlpatterns = [
#     path("ws/notifications/", OrderNotificationConsumer.as_asgi()),
# ]
from django.urls import path
from mainapp.consumers import OrderNotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/', OrderNotificationConsumer.as_asgi()),
]
