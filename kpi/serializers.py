from .models import PosResultData
from rest_framework import serializers

class RestaurantKpiSerializer(serializers.ModelSerializer):
    """
    RestaurantKpiView Serializer
    """
    # date = serializers.DateTimeField()
    # total_price = serializers.IntegerField()

    class Meta:
        model = PosResultData
        fields = (
            "id",
            "timestamp",
            "restaurant",
            "price",
            "number_of_party",
            "payment",
        )
        read_only_fields = []

class PaymentKpiSerializer(serializers.ModelSerializer):
    """
    PaymentKpiView Serializer
    """
    term = serializers.DateTimeField()
    count = serializers.IntegerField()
    
    class Meta:
        model = PosResultData
        fields = ['term','restaurant_id','payment','count']
        read_only_fields = []

class PartyNumberKpiSerializer(serializers.ModelSerializer):
    """
    PartyNumberKpiView Serializer
    """
    term = serializers.DateTimeField()
    count = serializers.IntegerField()
    
    class Meta:
        model = PosResultData
        fields = ['term','restaurant_id','number_of_party','count']
        read_only_fields = []

