from restaurant.models import Restaurant
from rest_framework import serializers

class RestaurantKpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = []