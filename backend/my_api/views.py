import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *


@api_view(['POST'])
def post_data(request):
	if request.method != 'POST':
		return Response({'error': 'Method is not POST'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		data = json.loads(request.data)
		state = State.objects.create(
			laboratory_id = data['laboratory_id'],
			state1=data['state1'],
			state2=data['state2'],
		)
	except Exception as e:
		return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

	return Response(status=status.HTTP_201_CREATED)