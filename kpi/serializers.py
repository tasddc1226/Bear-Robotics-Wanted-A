from restaurant.models import Restaurant
from .models import PosResultData
from rest_framework import serializers


### KPI뷰에서 공통적으로 쓰일 Serializer ###
class RestaurantKpiSerializer(serializers.ModelSerializer):
    term = serializers.DateTimeField()
    total_price = serializers.IntegerField()

    class Meta:
        model = PosResultData
        fields = ['term','total_price']
        read_only_fields = []

class PaymentKpiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PosResultData
        fileds = '__all__'
        read_only_fields = []

class PartyNumberKpiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []

