"""
ASGI config for PongChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# flake8: noqa
# isort: skip_file
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PongChat.settings")
django_asgi_app = get_asgi_application()

import pingpong.routing
from channels.auth import AuthMiddlewareStack  # type:ignore
from channels.routing import ProtocolTypeRouter, URLRouter  # type:ignore
from channels.security.websocket import AllowedHostsOriginValidator  # type:ignore


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(pingpong.routing.websocket_urlpatterns)),
        ),
    }
)
