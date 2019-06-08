from django.conf.urls import url
from . import consumer

# route to the consumer
websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumer.ChatConsumer),
]
