from django.db import models

# Create your models here.

class Restaurant(models.Model):
    # 레스토랑 id
    id = models.IntegerField(primary_key=True, unique=True)
    # 레스토랑 이름 
    restaurant_name = models.CharField(max_length=80, null=False, blank=False)
    # 그룹 번호
    group = models.CharField(max_length=50, null=False, blank=False)
    # 도시
    city = models.CharField(max_length=50)
    # 주소
    address = models.CharField(max_length=100)
    # 등록 일자
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정 일자
    updated_at = models.DateTimeField()

class PosResultData(models.Model):
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
    restaurant = models.ForeignKey(Restaurant, max_length=50, null=False, blank=False, on_delete=models.CASCADE)
    # 파티원 수
    number_of_party = models.PositiveSmallIntegerField(default=0)
    # 결제 수단
    payment = models.CharField(max_length=20, choices=PAYMENTS)

