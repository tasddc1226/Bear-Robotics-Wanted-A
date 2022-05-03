from restaurant.models import Restaurant
from .models import PosResultData
from rest_framework import serializers


### KPI뷰에서 공통적으로 쓰일 Serializer ###
class RestaurantKpiSerializer(serializers.ModelSerializer):
    term = serializers.DateTimeField()
    total_price = serializers.IntegerField()

    class Meta:
        model = PosResultData
        fields = ['term','total_price','restaurant_id']
        read_only_fields = []

class PaymentKpiSerializer(serializers.ModelSerializer):
    term = serializers.DateTimeField()
    total_price = serializers.IntegerField()
    count = serializers.IntegerField()
    
    class Meta:
        model = PosResultData
        fields = ['term','total_price','restaurant_id','payment','count']
        read_only_fields = []

class PartyNumberKpiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []

