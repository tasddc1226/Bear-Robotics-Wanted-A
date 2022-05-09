from .models import PosResultData
from rest_framework import serializers

class RestaurantKpiSerializer(serializers.Serializer):
    """
    RestaurantKpiView Serializer
    """
    start_time  = serializers.CharField(help_text='검색 시작 날짜', required=True)
    end_time    = serializers.CharField(help_text='검색 종료 날짜', required=True)
    time_window = serializers.CharField(help_text='검색 범위', required=True)
    start_price = serializers.CharField(help_text='시작 가격', required=False)
    end_price   = serializers.CharField(help_text='종료 가격', required=False)
    start_number_of_people = serializers.CharField(help_text='시작 구성원 수', required=False)
    end_number_of_people   = serializers.CharField(help_text='종료 구성원 수', required=False)
    restaurant_group = serializers.CharField(help_text='레스토랑 그룹 번호', required=False)


class PaymentKpiSerializer(serializers.Serializer):
    """
    PaymentKpiView Serializer
    """
    start_time  = serializers.CharField(help_text='검색 시작 날짜', required=True)
    end_time    = serializers.CharField(help_text='검색 종료 날짜', required=True)
    time_window = serializers.CharField(help_text='검색 범위', required=True)
    start_price = serializers.CharField(help_text='시작 가격', required=False)
    end_price   = serializers.CharField(help_text='종료 가격', required=False)
    start_number_of_people = serializers.CharField(help_text='시작 구성원 수', required=False)
    end_number_of_people   = serializers.CharField(help_text='종료 구성원 수', required=False)
    restaurant_group = serializers.CharField(help_text='레스토랑 그룹 번호', required=False)
    payment = serializers.CharField(help_text='결제 방법', required=False)


class PartyNumberKpiSerializer(serializers.Serializer):
    """
    PartyNumberKpiView Serializer
    """
    start_time  = serializers.CharField(help_text='검색 시작 날짜', required=True)
    end_time    = serializers.CharField(help_text='검색 종료 날짜', required=True)
    time_window = serializers.CharField(help_text='검색 범위', required=True)
    start_price = serializers.CharField(help_text='시작 가격', required=False)
    end_price   = serializers.CharField(help_text='종료 가격', required=False)
    start_number_of_people = serializers.CharField(help_text='시작 구성원 수', required=False)
    end_number_of_people   = serializers.CharField(help_text='종료 구성원 수', required=False)
    restaurant_group = serializers.CharField(help_text='레스토랑 그룹 번호', required=False)
    payment = serializers.CharField(help_text='결제 방법', required=False)
    