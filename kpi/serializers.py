from datetime import datetime
from .models import PosResultData
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RestaurantKpiSerializer(serializers.ModelSerializer):
    """
    RestaurantKpiView Serializer
    """
    term = serializers.DateTimeField()
    total_price = serializers.IntegerField()

    class Meta:
        model = PosResultData
        fields = ['term','total_price','restaurant_id']
        read_only_fields = []

    def check_none_necessary_string(self, var, msg):
        '''
        사용법
        첫 번째 변수 : None인치 체크할 variable
        두 번째 변수 : 쿼리명 string
        '''
        if var is None :
            raise ValidationError(f"{msg} 쿼리를 입력하세요.")

    def change_format_to_datetime(self, input_time, msg, time_format, input_exapmle):
        """
        사용법
        첫 번째 변수 : 입력형식이 맞는지 확인하는 날짜 string
        두 번째 변수 : query 이름 string
        세 번째 변수 : 입력받고자 하는 날짜 포맷
        네 번째 변수 : 입력해야 하는 날짜 string의 예시
        """
        try:
            input_time = datetime.strptime(input_time, time_format)
        except:
            raise ValidationError(f"{msg} 입력형식은 {input_exapmle} 입니다.")

            ##  is_integer
    def is_zero_or_more_numbers(self, var, msg):
        """
        사용법
        첫 번째 변수 : 0이상의 숫자인지 체크할 variable
        두 번째 변수 : 쿼리명 string
        """
        try:
            var = int(var)
        except:
            raise ValidationError(f"{msg}는 0 이상의 숫자 입력하세요.")
        if var < 0:
            raise ValidationError(f"{msg}는 0 이상의 숫자 입력하세요.")

    def is_equal_or_larger_size(self, small_val, large_val):
        """
        사용법
        첫 번째 변수 : 작은 값
        두 번째 변수 : 큰 값
        """
        if large_val < small_val:
            raise ValidationError(f"{large_val} >= {small_val} 조건을 만족해야 합니다.")

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

