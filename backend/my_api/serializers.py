from rest_framework import serializers
from .models import *

class setStateSerializer(serializers.ModelSerializer):
	state1 = serializers.CharField(read_only=True)
	state2 = serializers.BooleanField(read_only=True)
