from django.db import models
from core.models import TimeStamp

class Restaurant(TimeStamp):
    id = models.IntegerField(verbose_name="레스토랑 id", primary_key=True, unique=True)
    restaurant_name = models.CharField(verbose_name="레스토랑 이름", max_length=80, null=False, blank=False)
    group = models.CharField(verbose_name="프랜차이져 그룹 번호", max_length=50, null=False, blank=False)
    city = models.CharField(verbose_name="도시명", max_length=50)
    address = models.CharField(verbose_name="상세주소", max_length=100)

    class Meta:
        db_table = 'restaurants'    

class RestaurantMenu(TimeStamp):
    name = models.CharField(verbose_name="메뉴 이름", max_length=100)
    price = models.DecimalField(verbose_name="메뉴 가격", max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'menu'

class RestaurantGroup(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'groups'    

