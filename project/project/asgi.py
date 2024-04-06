import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import users.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            users.routing.websocket_urlpatterns
        ),

    }
)