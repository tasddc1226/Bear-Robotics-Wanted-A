from kpi.models import PosResultData
from .models import Restaurant
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PosDataListSerializer(serializers.ModelSerializer):
    """
    Pos Data GET, POST
    """
    class Meta:
        model = PosResultData
        fields = ['id','timestamp','restaurant','price','number_of_party','payment','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

    def validate(self, attrs):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            read_only_keys = set(self.initial_data.keys()) & set(getattr(self.Meta, 'read_only_fields', None))
            # Field에 없는 key를 입력하였을 때 에러메세지
            if unknown_keys:
                raise ValidationError(f"Got unknown fields: {unknown_keys}")
            # Read_only_field key를 입력하였을 때 에러메시지
            elif read_only_keys:
                raise ValidationError(f"Got readOnly fields: {read_only_keys}")
        return attrs


class PosDataDetailSerializer(serializers.ModelSerializer):
    """
    Pos Data detail GET
    """
    class Meta:
        model = PosResultData
        fields = ['id','timestamp','restaurant','price','number_of_party','payment','created_at','updated_at']
        read_only_fields = ['created_at','updated_at','id']

    def validate(self, attrs):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            read_only_keys = set(self.initial_data.keys()) & set(getattr(self.Meta, 'read_only_fields', None))
            # Field에 없는 key를 입력하였을 때 에러메세지
            if unknown_keys:
                raise ValidationError(f"Got unknown fields: {unknown_keys}")
            # Read_only_field key를 입력하였을 때 에러메시지
            elif read_only_keys:
                raise ValidationError(f"Got readOnly fields: {read_only_keys}")
        return attrs


class RestaurantListSerializer(serializers.ModelSerializer):
    """
    Restaurant Data GET, POST
    """
    class Meta:
        model = Restaurant
        fields = ['id','restaurant_name','group','city','address','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            read_only_keys = set(self.initial_data.keys()) & set(getattr(self.Meta, 'read_only_fields', None))
            # Field에 없는 key를 입력하였을 때 에러메세지
            if unknown_keys:
                raise ValidationError(f"Got unknown fields: {unknown_keys}")
            # Read_only_field key를 입력하였을 때 에러메시지
            elif read_only_keys:
                raise ValidationError(f"Got readOnly fields: {read_only_keys}")
        return attrs


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """
    Restaurant Data detail GET, PUT, DELETE
    """
    class Meta:
        model = Restaurant
        fields = ['id','restaurant_name','group','city','address','created_at','updated_at']
        read_only_fields = ['id','group','created_at','updated_at']

    def validate(self, attrs):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            read_only_keys = set(self.initial_data.keys()) & set(getattr(self.Meta, 'read_only_fields', None))
            # Field에 없는 key를 입력하였을 때 에러메세지
            if unknown_keys:
                raise ValidationError(f"Got unknown fields: {unknown_keys}")
            # Read_only_field key를 입력하였을 때 에러메시지
            elif read_only_keys:
                raise ValidationError(f"Got readOnly fields: {read_only_keys}")
        return attrs