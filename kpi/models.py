from django.db import models
from core.models import TimeStamp
from restaurant.models import Restaurant

class PosResultData(TimeStamp):
    # 결제 수단 정의
    PAYMENTS = [
        ('1', 'CARD'),
        ('2', 'CASH'),
        ('3', 'PHONE'),
        ('4', 'BITCOIN')
        ]
    timestamp = models.DateTimeField(verbose_name="결제 시각")
    price = models.PositiveIntegerField(verbose_name="결제 금액", default=0)
    restaurant = models.ForeignKey(Restaurant, max_length=50, null=False, verbose_name="결제 레스토랑 id", blank=False, on_delete=models.CASCADE)
    number_of_party = models.PositiveSmallIntegerField(verbose_name="파티원 수", default=0)
    payment = models.CharField(max_length=20, verbose_name="결제 수단", choices=PAYMENTS)

    class Meta:
        db_table = 'pos_result_data'    

