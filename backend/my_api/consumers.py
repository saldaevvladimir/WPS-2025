import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from .models import *



from .serializers import setStateSerializer


class InfoConsumer(WebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def connect(self):
		self.room_group_name = f'laboratory'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept()

	def receive(self, text_data=None, bytes_data=None):
		data = json.loads(text_data)
		state = State.objects.create(
			state1=data['state1'],
			state2=data['state2'],
		)

		self.send_message_with_state_to_group(state, self.channel_layer)

	def send_data(self, event):
		state = event['state']

		self.send(text_data=json.dumps({
			'state': state.return_self()
		}))

	def send_message_with_state_to_group(self, state, layer=get_channel_layer()):
		self.room_group_name = f'laboratory'
		async_to_sync(layer.group_send)(
			self.room_group_name, {
				'type': 'send_data',
				'state': state
			}
		)