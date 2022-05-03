from restaurant.models import Restaurant
from .models import PosResultData
from rest_framework import serializers

class RestaurantKpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = []





### KPI뷰에서 공통적으로 쓰일 Serializer ###
class PosResultDataSerializer(serializers.ModelSerializer):
    day = serializers.DateTimeField()
    # hour = serializers.DateTimeField()
    price__sum = serializers.IntegerField()

    class Meta:
        model = PosResultData
        fields = ['day','price__sum']
        # fields = '__all__'
        read_only_fields = []