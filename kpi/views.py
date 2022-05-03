from datetime import datetime
from django.http import HttpResponse, JsonResponse
from restaurant.models import Restaurant, RestaurantGroup, RestaurantMenu
from .models import PosResultData
from .serializers import RestaurantKpiSerializer, PosResultDataSerializer
from django.db.models import Avg, Max, Count, Q, F, Value, Sum
from django.db.models.functions import TruncDate, TruncDay, TruncMonth, TruncYear, TruncHour
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class RestaurantKpiView(APIView):
    def get(self, request, format=None):
        restaurant = get_object_or_404(Restaurant)
        serializer = RestaurantKpiSerializer(restaurant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentKpiView(APIView):
    def get(self, request, format=None):
        pos = PosResultData.objects.all()

        # search_group = Restaurant.objects.filter(restaurant_name='비비고').values('id')

        # filter 1) term
        start_time = '2022-02-27 00:14:01'
        end_time = '2022-02-28 23:12:32'
        time_format = '%Y-%m-%d %H:%M:%S'
        start_time = datetime.strptime(start_time, time_format)
        end_time = datetime.strptime(end_time, time_format)
        pos = pos.filter(timestamp__gte=start_time, timestamp__lte=end_time)

        # filter 2) price range
        start_price = 10000
        end_price = 1000000
        pos = pos.filter(price__gte=start_price, price__lte=end_price)


        # filter 3) number_of_party
        start_number = 2
        end_number = 3
        pos = pos.filter(number_of_party__gte=start_number, number_of_party__lte=end_number)

        
        # filter 4) restaurant_group (이거 나중에 구현) - 난이도 있음

        #이거 그룹테이블로 찾으면 속도가 빨라짐
        # search_group = Restaurant.objects.filter(restaurant_name='비비고').values('id')
        # 위의 쿼리결과를 바로 pos에 적용시키거나(최종목표)
        # 이게 안된다면 위의 결과의 id만 뽑아내서 for문 돌려야함. 
        # 
        

        # KPI : price__sum per Time window
        # pos_hour = pos.annotate(hour=TruncHour('timestamp')).values('hour')\
        #                                     .annotate(Sum('price')).values('hour','price__sum')
        pos_day = pos.annotate(day=TruncDay('timestamp')).values('day')\
                                            .annotate(Sum('price')).values('day','price__sum')
        # pos_month = pos.annotate(month=TruncMonth('timestamp')).values('month')\
        #                                     .annotate(Sum('price')).values('month','price__sum')
        # pos_year = pos.annotate(year=TruncYear('timestamp')).values('year')\
        #                                     .annotate(Sum('price')).values('year','price__sum')
    

        serializer = PosResultDataSerializer(pos_day, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class Restaurant(TimeStamp):
#     id = models.IntegerField(primary_key=True, unique=True)
#     restaurant_name = models.CharField(max_length=80, null=False, blank=False)
#     group = models.CharField(max_length=50, null=False, blank=False)
#     city = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)

# class PosResultData(TimeStamp):
#     timestamp = models.DateTimeField()
#     price = models.PositiveIntegerField(default=0)
#     restaurant = models.ForeignKey(Restaurant, max_length=50, null=False, blank=False, on_delete=models.CASCADE)
#     number_of_party = models.PositiveSmallIntegerField(default=0)
#     payment = models.CharField(max_length=20, choices=PAYMENTS)

