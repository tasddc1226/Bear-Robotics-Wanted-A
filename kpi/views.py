from datetime import datetime
from restaurant.models import Restaurant, RestaurantGroup, RestaurantMenu
from .models import PosResultData
from .serializers import (
    RestaurantKpiSerializer,
    PaymentKpiSerializer,
    PartyNumberKpiSerializer
)
from django.db.models import Avg, Max, Count, Q, F, Value, Sum
from django.db.models.functions import TruncDate, TruncDay, TruncMonth, TruncYear, TruncHour
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class RestaurantKpiView(APIView):
    """
    1번문제. 현재 여기는 날코딩이라 추후에 함수로 빼내서 재사용 가능하게 만들 예정
    """
    def get(self, request, format=None):
        pos = PosResultData.objects.all()


        '''
        # [필수] filter 1) term
        - start ~ end filter요소
        - date 바꾸는 format변환
        - filter 적용
        '''
        # - start ~ end filter요소
        start_time = request.GET.get('start-time', None)
        if start_time is None :
            return Response({"message":"start-time 쿼리를 입력하세요. \
                            주의) 만약 2022-04-08일까지 확인하고 싶다면 2022-04-08 23:59:59를 입력하셔야합니다."}, status=status.HTTP_400_BAD_REQUEST)
        end_time = request.GET.get('end-time', None)
        if end_time is None :
            return Response({"message":"end-time 쿼리를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # - date 바꾸는 format변환
        time_format = '%Y-%m-%d %H:%M:%S'
        try:
            start_time = datetime.strptime(start_time, time_format)
        except:
            return Response({"message":" start-time 입력형식은 YYYY-MM-DD hh:mm:ss 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            end_time = datetime.strptime(end_time, time_format)
        except:
            return Response({"message":" end-time 입력형식은 YYYY-MM-DD hh:mm:ss 입니다. \
                            주의) 만약 2022-04-08일까지 확인하고 싶다면 2022-04-08 23:59:59를 입력하셔야합니다."}, status=status.HTTP_400_BAD_REQUEST)
        # - filter 적용
        pos = pos.filter(timestamp__gte=start_time, timestamp__lte=end_time)

        '''
        # [옵션] filter 2) price range
        - 옵션조건
        - start ~ end filter 요소
        - integer인지 확인하는 요소
        - integer요소는 start와 end의 대소비교
        - filter 적용
        '''

        # - start ~ end filter 요소  + integer인지 확인하는 요소
        start_price = request.GET.get('start-price', None)
        if start_price is not None :
            try:
                start_price = int(start_price)
            except:
                return Response({"message":"start-price는 자연수를 입력하세요. "}, status=status.HTTP_400_BAD_REQUEST)
            if start_price < 0:
                return Response({"message":"숫자 0 이상 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

            end_price = request.GET.get('end-price', None)
            if end_price is None :
                return Response({"message":"end-price를 입력하세요. start-price를 입력했다면 함께 넣어야 하는 요소입니다."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                end_price = int(end_price)
            except:
                return Response({"message":"end-price는 자연수를 입력하세요. "}, status=status.HTTP_400_BAD_REQUEST)
            if end_price < 0:
                return Response({"message":"숫자 0 이상 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

            # - integer요소는 start와 end의 대소비교
            if start_price > end_price:
                return Response({"message":"start-price는 end-price보다 작아야합니다."}, status=status.HTTP_400_BAD_REQUEST)

            # - filter 적용
            pos = pos.filter(price__gte=start_price, price__lte=end_price)

        '''
        # [옵션] filter 3) number_of_party
        - start ~ end filter 요소
        - integer인지 확인하는 요소
        - integer요소는 start와 end의 대소비교
        - filter 적용
        '''
        start_number_of_people = request.GET.get('start-number-of-people', None)
        if start_number_of_people is not None :
            try:
                start_number_of_people = int(start_number_of_people)
            except:
                return Response({"message":"start-number-of-people은 자연수를 입력하세요. "}, status=status.HTTP_400_BAD_REQUEST)
            if start_number_of_people < 0:
                return Response({"message":"숫자 0 이상 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

            end_number_of_people = request.GET.get('end-number-of-people', None)
            if end_number_of_people is None :
                return Response({"message":"end-number-of-people를 입력하세요. start-number-of-people를(을) 입력했다면 함께 넣어야 하는 요소입니다."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                end_number_of_people = int(end_number_of_people)
            except:
                return Response({"message":"end-number-of-people은 자연수를 입력하세요. "}, status=status.HTTP_400_BAD_REQUEST)
            if end_number_of_people < 0:
                return Response({"message":"숫자 0 이상 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

            # - integer요소는 start와 end의 대소비교
            if start_number_of_people > end_number_of_people:
                return Response({"message":"start-number_of_people는 end-number_of_people보다 작아야합니다."}, status=status.HTTP_400_BAD_REQUEST)

            # - filter 적용
            pos = pos.filter(number_of_party__gte=start_number_of_people, number_of_party__lte=end_number_of_people)

        '''
        # [옵션] filter 4) restaurant_group
        ### group_names는 RestaurantGroup에서 가져오는 코드가 필요하나 현재 모델에서 어려운듯? 모델 수정이 필요..!?!
        - 쿼리 리스트 가져오기
        - 쿼리 받아서 리스트와 비교하기
        - 필터 적용하기
        '''
        # - 쿼리 받기
        restaurant_group = request.GET.get('restaurant-group', None)

        # - 비교할 리스트 가져오기
        group_name_list = ['비비고','빕스버거']
        
        #  옵션조건이기에 None인지 확인한 후 리스트와 비교하기
        if restaurant_group is not None :
            if not restaurant_group in group_name_list:
                return Response({"message":"restaurant-group의 입력 인자는 '비비고','빕스버거' 중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
            search_group = Restaurant.objects.filter(restaurant_name=restaurant_group).values('id')
            pos = pos.filter(restaurant_id__in=search_group)

        '''
        # [필수] Time window
        '''
        time_window_archive = ['HOUR', 'DAY', 'MONTH', 'YEAR']
        time_window = request.GET.get('time-window', None)
        if time_window is None :
            return Response({"message":"time-window 쿼리를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        if not time_window in time_window_archive:
            return Response({"message":"time-window의 입력 인자는 'HOUR', 'DAY', 'MONTH', 'YEAR'중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if time_window == 'HOUR':
            pos = pos.annotate(term=TruncHour('timestamp')).values('term')\
                                                .annotate(total_price=Sum('price')).values('term','total_price')
        elif time_window == 'DAY':
            pos = pos.annotate(term=TruncDay('timestamp')).values('term')\
                                                .annotate(total_price=Sum('price')).values('term','total_price')
        elif time_window == 'MONTH':
            pos = pos.annotate(term=TruncMonth('timestamp')).values('term')\
                                                .annotate(total_price=Sum('price')).values('term','total_price')
        elif time_window == 'YEAR':
            pos = pos.annotate(term=TruncYear('timestamp')).values('term')\
                                                .annotate(total_price=Sum('price')).values('term','total_price')
    
        serializer = RestaurantKpiSerializer(pos, many=True)
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


class PaymentKpiView(APIView):
    def get(self, request, format=None):
        pos = PosResultData.objects.all()
        serializer = PaymentKpiSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)


class PartyNumberKpiView(APIView):
    def get(self, request, format=None):
        pos = PosResultData.objects.all()
        serializer = PartyNumberKpiSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)
    