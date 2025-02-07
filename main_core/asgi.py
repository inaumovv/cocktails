import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main_core.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main_core.routing.websocket_urlpatterns
        )
    ),
})
