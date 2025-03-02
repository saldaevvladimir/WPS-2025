import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

from .serializers import setStateSerializer


class InfoConsumer(WebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def connect(self):
		self.laboratory_id = self.scope['url_route']['kwargs']['laboratory_id']

		self.room_group_name = f'laboratory_{self.laboratory_id}'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept()

	def receive(self, text_data=None, bytes_data=None):
		state = State.objects.order_by('-id')[0]

		self.send_message_with_state_to_group(state)

	def send_data(self, event):
		state = event['state']

		self.send(text_data=json.dumps({
			'state': state
		}))

	def send_message_with_state_to_group(self, state, laboratory_id=-1):
		if laboratory_id == -1:
			laboratory_id = self.laboratory_id

		self.room_group_name = f'laboratory_{laboratory_id}'
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name, {
				'type': 'send_data',
				'state': state
			}
		)