from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/laboratory/(?P<laboratory_id>\d+)/$', consumers.InfoConsumer.as_asgi()),
]