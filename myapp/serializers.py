from rest_framework import serializers
from .models import BardResponse,BardRequest

class BardResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BardResponse
        fields = ['answer'] 

class BardRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BardRequest
        fields = ['question'] 