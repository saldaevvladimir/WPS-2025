import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import my_api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wsp.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
	'http': get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter(
			my_api.routing.websocket_urlpatterns
		)
	),
})