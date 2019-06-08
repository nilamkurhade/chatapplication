from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import ChatApp.routing

application = ProtocolTypeRouter({          # the root routing configuration
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns
        )
    ),
})