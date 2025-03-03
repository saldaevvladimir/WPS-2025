import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from channels.layers import get_channel_layer

from .consumers import InfoConsumer
from .models import *


@api_view(['POST'])
def post_data(request):
	if request.method != 'POST':
		return Response({'error': 'Method is not POST'}, status=status.HTTP_404_NOT_FOUND)
	try:
		data = json.loads(request.body)
		state = State.objects.create(
			state1=data['state1'],
			state2=data['state2'],
		)
	except Exception as e:
		return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

	channel_layer = get_channel_layer()

	InfoConsumer().send_message_with_state_to_group(state, channel_layer)

	return Response(status=status.HTTP_201_CREATED)