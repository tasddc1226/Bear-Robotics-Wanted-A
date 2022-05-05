from datetime import timedelta
from restaurant.models import Restaurant, RestaurantGroup, RestaurantMenu
from .models import PosResultData
from .serializers import (
    RestaurantKpiSerializer,
    PaymentKpiSerializer,
    PartyNumberKpiSerializer
)
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import TruncDate, ExtractMonth, ExtractYear, ExtractHour, TruncWeek
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from typing import Dict
from .validate import *
class RestaurantKpiView(APIView):
    """
        Writer : 윤상민
        Reviewer : 양수영
        Refactor : 윤상민, 양수영
    """
    def get(self, request, format=None):
        """
            A REST API to show KPI sales (price) per restaurant
            Only GET method exsists.
            base url: http://127.0.0.1:8000/api/v1/kpi/restaurant
        """

        """ [NECESSARY] query params """
        start_time  = request.GET.get('start-time', None)
        end_time    = request.GET.get('end-time', None)
        time_window = request.GET.get('time-window', None)

        """ [OPTIONAL 1] query params """
        start_price = request.GET.get('start-price', None)
        end_price   = request.GET.get('end-price', None)

        """ [OPTIONAL 2] query params """
        start_number_of_people = request.GET.get('start-number-of-people', None)
        end_number_of_people   = request.GET.get('end-number-of-people', None)

        """ [OPTIONAL 3] query params """
        restaurant_group = request.GET.get('restaurant-group', None)

        """ [OPTIONAL 4] query params """ # 결제 수단은 아래 쪽으로 이동
        payment = request.GET.get('payment', None)
        
        # Validate start_time, end_time params
        check_none_necessary_string(start_time, "start_time")
        check_none_necessary_string(end_time, "end_time")
        
        # Change date format
        start_time = change_format_to_datetime(start_time, 'start-time','%Y-%m-%d', 'YYYY-MM-DD')
        end_time = change_format_to_datetime(end_time, 'end-time' ,'%Y-%m-%d', 'YYYY-MM-DD')
        
        is_equal_or_larger_size(start_time, end_time)

        time_window_archive = {
            'hour' : ExtractHour('timestamp'),
            'day'  : TruncDate('timestamp'),
            'week' : TruncWeek('timestamp'),
            'month': ExtractMonth('timestamp'),
            'year' : ExtractYear('timestamp')
        }
        
        # Validate time_window params
        check_none_necessary_string(time_window, "time-window")
        if not time_window in time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'HOUR','DAY','WEEK','MONTH','YEAR'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (start_price is not None) or (end_price is not None):
            check_none_necessary_string(start_price, 'start-price')
            check_none_necessary_string(end_price, 'end-price')
            is_zero_or_more_numbers(start_price, 'start-price')
            is_zero_or_more_numbers(end_price, 'end-price')
            is_equal_or_larger_size(int(start_price), int(end_price))

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            check_none_necessary_string(start_number_of_people, 'start-number-of-people')
            check_none_necessary_string(end_number_of_people, 'end-number-of-people')
            is_zero_or_more_numbers(start_number_of_people, 'start-number-of-people')
            is_zero_or_more_numbers(end_number_of_people, 'end-number-of-people')
            is_equal_or_larger_size(int(start_number_of_people), int(end_number_of_people))

        if (restaurant_group is not None):
            check_none_necessary_string(restaurant_group, 'restaurant_group')
            is_zero_or_more_numbers(restaurant_group, 'restaurant_group')
            restaurant = Restaurant.objects.filter(group=restaurant_group).first()
            if not restaurant:
                return Response(
                    {"message":"찾고자 하는 점포의 그룹이 없습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        q = Q()
        q &= Q(timestamp__range=(start_time, end_time + timedelta(days=1)))

        if start_price and end_price:
            q &= Q(price__range=(start_price, end_price))
        
        if start_number_of_people and end_number_of_people:
            q &= Q(number_of_party__range=(start_number_of_people, end_number_of_people))
        
        if restaurant_group:
            q &= Q(restaurant__group=restaurant_group)

        result_data_set = PosResultData.objects.filter(q)\
                                                .annotate(date=time_window_archive[time_window]).values('date')\
                                                .annotate(restaurant_id=F('restaurant'), total_price=Sum('price'))\
                                                .values('date', 'restaurant_id', 'total_price')
        return Response(result_data_set, status=status.HTTP_200_OK)

class PaymentKpiView(APIView):
    """
    A REST API to show KPI count of each payment method per restaurant
    Only GET method exsists.
    """

    def get(self, request, format=None):

        # Get POS Data
        pos = PosResultData.objects.all()

        """
        Filter 1. start_time to end_time [NECESSARY]
        """
        # Get query
        start_time = request.GET.get('start-time', None)
        end_time = request.GET.get('end-time', None)
        RestaurantKpiSerializer.check_none_necessary_string(self, start_time, 'start-time')
        RestaurantKpiSerializer.check_none_necessary_string(self, end_time, 'end-time')

        # Change date format
        RestaurantKpiSerializer.change_format_to_datetime(self, start_time, 'start-time','%Y-%m-%d', 'YYYY-MM-DD')
        RestaurantKpiSerializer.change_format_to_datetime(self, end_time, 'end-time' ,'%Y-%m-%d', 'YYYY-MM-DD')

        # Apply filter
        pos = pos.filter(timestamp__gte=start_time, timestamp__lte=end_time)

        """
        Filter 2. start_price to end_price [OPTIONAL]
        """
        # Get query
        start_price = request.GET.get('start-price', None)
        end_price = request.GET.get('end-price', None)

        # Validate positive number optionally
        if (start_price is not None) or (end_price is not None):
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, start_price, 'start-price')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, start_price, 'start-price')
            start_price = int(start_price)
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, end_price, 'end-price')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, end_price, 'end-price')
            end_price = int(end_price)

            #Compare size
            RestaurantKpiSerializer.is_equal_or_larger_size(self, start_price, end_price)

            # Apply filter
            pos = pos.filter(price__gte=start_price, price__lte=end_price)


        """
        Filter 3. number_of_party [OPTIONAL]
        """
        # Get query
        start_number_of_people = request.GET.get('start-number-of-people', None)
        end_number_of_people = request.GET.get('end-number-of-people', None)

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, start_number_of_people, 'start-number_of_people')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, start_number_of_people, 'start-number_of_people')
            start_number_of_people = int(start_number_of_people)
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, end_number_of_people, 'end-number_of_people')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, end_number_of_people, 'end-number_of_people')
            end_number_of_people = int(end_number_of_people)

            #Compare size
            RestaurantKpiSerializer.is_equal_or_larger_size(self, start_number_of_people, end_number_of_people)

            #Apply filter
            pos = pos.filter(number_of_party__gte=start_number_of_people, number_of_party__lte=end_number_of_people)


        """
        Filter 4. restaurant_group [OPTIONAL]
        """
        # Get query
        restaurant_group = request.GET.get('restaurant-group', None)

        # [이슈 = models 수정 이후에 반영 예정] Get checklist
        group_name_list = ['비비고','빕스버거']
        
        # Compare query to checklist Optionally
        if restaurant_group is not None :
            if not restaurant_group in group_name_list:
                return Response({"message":"restaurant-group의 입력 인자는 '비비고','빕스버거' 중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            #Apply filter
            search_group = Restaurant.objects.filter(restaurant_name=restaurant_group).values('id')
            pos = pos.filter(restaurant_id__in=search_group)

        '''
        Window : Aggregation Time window size
        '''
        # Get query
        time_window = request.GET.get('time-window', None)

        # Validate query
        time_window_archive = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
        RestaurantKpiSerializer.check_none_necessary_string(self, time_window, 'time-window')
        if not time_window in time_window_archive:
            return Response({"message":"time-window의 입력 인자는 'HOUR','DAY','WEEK','MONTH','YEAR'중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make time window
        if time_window == 'HOUR':
            pos = pos.annotate(term=TruncHour('timestamp')).values('term')\
                        .annotate(count=Count('payment')).values('term','restaurant_id','payment','count')
        elif time_window == 'DAY':
            pos = pos.annotate(term=TruncDay('timestamp')).values('term')\
                        .annotate(count=Count('payment')).values('term','restaurant_id','payment','count')
        elif time_window == 'WEEK':
            pos = pos.annotate(term=TruncWeek('timestamp')).values('term')\
                        .annotate(count=Count('payment')).values('term','restaurant_id','payment','count')
        elif time_window == 'MONTH':
            pos = pos.annotate(term=TruncMonth('timestamp')).values('term')\
                        .annotate(count=Count('payment')).values('term','restaurant_id','payment','count')
        elif time_window == 'YEAR':
            pos = pos.annotate(term=TruncYear('timestamp')).values('term')\
                        .annotate(count=Count('payment')).values('term','restaurant_id','payment','count')
        
        serializer = PaymentKpiSerializer(pos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartyNumberKpiView(APIView):
    """
    A REST API to show KPI count of each party size per restaurant
    Only GET method exsists.
    """

    def get(self, request, format=None):

        # Get POS Data
        pos = PosResultData.objects.all()

        """
        Filter 1. start_time to end_time [NECESSARY]
        """
        # Get query
        start_time = request.GET.get('start-time', None)
        end_time = request.GET.get('end-time', None)
        RestaurantKpiSerializer.check_none_necessary_string(self, start_time, 'start-time')
        RestaurantKpiSerializer.check_none_necessary_string(self, end_time, 'end-time')

        # Change date format
        RestaurantKpiSerializer.change_format_to_datetime(self, start_time, 'start-time','%Y-%m-%d', 'YYYY-MM-DD')
        RestaurantKpiSerializer.change_format_to_datetime(self, end_time, 'end-time' ,'%Y-%m-%d', 'YYYY-MM-DD')

        # Apply filter
        pos = pos.filter(timestamp__gte=start_time, timestamp__lte=end_time)

        """
        Filter 2. start_price to end_price [OPTIONAL]
        """
        # Get query
        start_price = request.GET.get('start-price', None)
        end_price = request.GET.get('end-price', None)

        # Validate positive number optionally
        if (start_price is not None) or (end_price is not None):
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, start_price, 'start-price')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, start_price, 'start-price')
            start_price = int(start_price)
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, end_price, 'end-price')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, end_price, 'end-price')
            end_price = int(end_price)

            #Compare size
            RestaurantKpiSerializer.is_equal_or_larger_size(self, start_price, end_price)

            # Apply filter
            pos = pos.filter(price__gte=start_price, price__lte=end_price)


        """
        Filter 3. number_of_party [OPTIONAL]
        """
        # Get query
        start_number_of_people = request.GET.get('start-number-of-people', None)
        end_number_of_people = request.GET.get('end-number-of-people', None)

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, start_number_of_people, 'start-number_of_people')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, start_number_of_people, 'start-number_of_people')
            start_number_of_people = int(start_number_of_people)
            # None이 아니라면 0 이상인지 체크
            RestaurantKpiSerializer.check_none_necessary_string(self, end_number_of_people, 'end-number_of_people')
            RestaurantKpiSerializer.is_zero_or_more_numbers(self, end_number_of_people, 'end-number_of_people')
            end_number_of_people = int(end_number_of_people)
            #Compare size
            RestaurantKpiSerializer.is_equal_or_larger_size(self, start_number_of_people, end_number_of_people)

            #Apply filter
            pos = pos.filter(number_of_party__gte=start_number_of_people, number_of_party__lte=end_number_of_people)


        """
        Filter 4. restaurant_group [OPTIONAL]
        """
        # Get query
        restaurant_group = request.GET.get('restaurant-group', None)

        # [이슈 = models 수정 이후에 반영 예정] Get checklist
        group_name_list = ['비비고','빕스버거']
        
        # Compare query to checklist Optionally
        if restaurant_group is not None :
            if not restaurant_group in group_name_list:
                return Response({"message":"restaurant-group의 입력 인자는 '비비고','빕스버거' 중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            #Apply filter
            search_group = Restaurant.objects.filter(restaurant_name=restaurant_group).values('id')
            pos = pos.filter(restaurant_id__in=search_group)

        '''
        Window : Aggregation Time window size
        '''
        # Get query
        time_window = request.GET.get('time-window', None)

        # Validate query
        time_window_archive = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
        RestaurantKpiSerializer.check_none_necessary_string(self, time_window, 'time-window')
        if not time_window in time_window_archive:
            return Response({"message":"time-window의 입력 인자는 'HOUR','DAY','WEEK','MONTH','YEAR'중의 하나입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make time window
        if time_window == 'HOUR':
            pos = pos.annotate(term=TruncHour('timestamp')).values('term')\
                                                .annotate(count=Count('number_of_party')).values('term','restaurant_id','number_of_party','count')
        elif time_window == 'DAY':
            pos = pos.annotate(term=TruncDay('timestamp')).values('term')\
                                                .annotate(count=Count('number_of_party')).values('term','restaurant_id','number_of_party','count')
        elif time_window == 'WEEK':
            pos = pos.annotate(term=TruncWeek('timestamp')).values('term')\
                                                .annotate(count=Count('number_of_party')).values('term','restaurant_id','number_of_party','count')
        elif time_window == 'MONTH':
            pos = pos.annotate(term=TruncMonth('timestamp')).values('term')\
                                                .annotate(count=Count('number_of_party')).values('term','restaurant_id','number_of_party','count')
        elif time_window == 'YEAR':
            pos = pos.annotate(term=TruncYear('timestamp')).values('term')\
                                                .annotate(count=Count('number_of_party')).values('term','restaurant_id','number_of_party','count')
        
        serializer = PartyNumberKpiSerializer(pos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

