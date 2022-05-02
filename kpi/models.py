from django.db import models
from core.models import TimeStamp

class PosResultData(TimeStamp):
    # 결제 수단 정의
    PAYMENTS = [
        ('1', 'CARD'),
        ('2', 'CASH'),
        ('3', 'PHONE'),
        ('4', 'BITCOIN')
        ]
    # 결제 시각
    timestamp = models.DateTimeField()
    # 결제 금액
    price = models.PositiveIntegerField(default=0)
    # 결제 레스토랑 id
    restaurant = models.ForeignKey('pos.Restaurant', max_length=50, null=False, blank=False, on_delete=models.CASCADE)
    # 파티원 수
    number_of_party = models.PositiveSmallIntegerField(default=0)
    # 결제 수단
    payment = models.CharField(max_length=20, choices=PAYMENTS)

    class Meta:
        db_table = 'pos_result_data'    

