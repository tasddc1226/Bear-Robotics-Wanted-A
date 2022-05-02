from kpi.models import PosResultData
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class PosDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []

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
    class Meta:
        model = PosResultData
        fields = '__all__'
        read_only_fields = []

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