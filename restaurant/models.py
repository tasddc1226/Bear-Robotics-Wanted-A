from django.db import models
from core.models import TimeStamp

class Restaurant(TimeStamp):
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

    class Meta:
        db_table = 'restaurants'    

class RestaurantMenu(TimeStamp):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'menu'

class RestaurantGroup(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'groups'    

