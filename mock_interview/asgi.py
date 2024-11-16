import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from interview.routing import websocket_urlpatterns  # Replace 'your_app_name' with the actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mock_interview.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket requests
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
