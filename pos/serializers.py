from .models import PosResultData
from rest_framework import serializers

class PosDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []

class PosDataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []