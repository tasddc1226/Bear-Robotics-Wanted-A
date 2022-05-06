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
from drf_yasg.utils       import swagger_auto_schema

class RestaurantKpiView(APIView):
    """
        Writer : 윤상민
        Reviewer : 양수영
        Refactor : 윤상민, 양수영, 권은경 
    """
    @swagger_auto_schema(tags=[' KPI sales (price) per restaurant.'], query_serializer=RestaurantKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI sales (price) per restaurant
            Only GET method exsists.
            base url: http://127.0.0.1:8000/api/v1/kpi/restaurant
        """

        """ [NECESSARY] query params """
        start_time  = request.GET.get('start_time', None)
        end_time    = request.GET.get('end_time', None)
        time_window = request.GET.get('time_window', None)

        """ [OPTIONAL 1] query params """
        start_price = request.GET.get('start_price', None)
        end_price   = request.GET.get('end_price', None)

        """ [OPTIONAL 2] query params """
        start_number_of_people = request.GET.get('start_number_of_people', None)
        end_number_of_people   = request.GET.get('end_number_of_people', None)

        """ [OPTIONAL 3] query params """
        restaurant_group = request.GET.get('restaurant_group', None)
        
        # Validate start_time, end_time params
        check_none_necessary_string(start_time, "start_time")
        check_none_necessary_string(end_time, "end_time")
        
        # Change date format
        start_time = change_format_to_datetime(start_time, 'start_time','%Y-%m-%d', 'YYYY-MM-DD')
        end_time = change_format_to_datetime(end_time, 'end_time' ,'%Y-%m-%d', 'YYYY-MM-DD')
        
        is_equal_or_larger_size(start_time, end_time)

        time_window_archive = {
            'hour' : ExtractHour('timestamp'),
            'day'  : TruncDate('timestamp'),
            'week' : TruncWeek('timestamp'),
            'month': ExtractMonth('timestamp'),
            'year' : ExtractYear('timestamp')
        }
        
        # Validate time_window params
        check_none_necessary_string(time_window, "time_window")
        if not time_window in time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (start_price is not None) or (end_price is not None):
            check_none_necessary_string(start_price, 'start_price')
            check_none_necessary_string(end_price, 'end_price')
            is_zero_or_more_numbers(start_price, 'start_price')
            is_zero_or_more_numbers(end_price, 'end_price')
            is_equal_or_larger_size(int(start_price), int(end_price))

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            check_none_necessary_string(start_number_of_people, 'start_number_of_people')
            check_none_necessary_string(end_number_of_people, 'end_number_of_people')
            is_zero_or_more_numbers(start_number_of_people, 'start_number_of_people')
            is_zero_or_more_numbers(end_number_of_people, 'end_number_of_people')
            is_equal_or_larger_size(int(start_number_of_people), int(end_number_of_people))

        if (restaurant_group is not None):
            check_none_necessary_string(restaurant_group, 'restaurant_group')
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

    @swagger_auto_schema(tags=['KPI count of each payment method per restaurant.'], query_serializer=PaymentKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI sales (price) per restaurant
            Only GET method exsists.
            base url: http://127.0.0.1:8000/api/v1/kpi/payment
        """

        start_time  = request.GET.get('start_time', None)
        end_time    = request.GET.get('end_time', None)
        time_window = request.GET.get('time_window', None)
        start_price = request.GET.get('start_price', None)
        end_price   = request.GET.get('end_price', None)
        start_number_of_people = request.GET.get('start_number_of_people', None)
        end_number_of_people   = request.GET.get('end_number_of_people', None)
        restaurant_group = request.GET.get('restaurant_group', None)
        payment = request.GET.get('payment', None)
        
        check_none_necessary_string(start_time, "start_time")
        check_none_necessary_string(end_time, "end_time")
        
        start_time = change_format_to_datetime(start_time, 'start_time','%Y-%m-%d', 'YYYY-MM-DD')
        end_time = change_format_to_datetime(end_time, 'end_time' ,'%Y-%m-%d', 'YYYY-MM-DD')
        
        is_equal_or_larger_size(start_time, end_time)

        time_window_archive = {
            'hour' : ExtractHour('timestamp'),
            'day'  : TruncDate('timestamp'),
            'week' : TruncWeek('timestamp'),
            'month': ExtractMonth('timestamp'),
            'year' : ExtractYear('timestamp')
        }
        
        check_none_necessary_string(time_window, "time_window")
        if not time_window in time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (start_price is not None) or (end_price is not None):
            check_none_necessary_string(start_price, 'start_price')
            check_none_necessary_string(end_price, 'end_price')
            is_zero_or_more_numbers(start_price, 'start_price')
            is_zero_or_more_numbers(end_price, 'end_price')
            is_equal_or_larger_size(int(start_price), int(end_price))

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            check_none_necessary_string(start_number_of_people, 'start_number_of_people')
            check_none_necessary_string(end_number_of_people, 'end_number_of_people')
            is_zero_or_more_numbers(start_number_of_people, 'start_number_of_people')
            is_zero_or_more_numbers(end_number_of_people, 'end_number_of_people')
            is_equal_or_larger_size(int(start_number_of_people), int(end_number_of_people))

        if (restaurant_group is not None):
            check_none_necessary_string(restaurant_group, 'restaurant_group')
            restaurant = Restaurant.objects.filter(group=restaurant_group).first()
            if not restaurant:
                return Response(
                    {"message":"찾고자 하는 점포의 그룹이 없습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if (payment is not None):
            # TODO: payment 예외처리
            pass
        
        q = Q()
        q &= Q(timestamp__range=(start_time, end_time + timedelta(days=1)))

        if start_price and end_price:
            q &= Q(price__range=(start_price, end_price))
        
        if start_number_of_people and end_number_of_people:
            q &= Q(number_of_party__range=(start_number_of_people, end_number_of_people))
        
        if restaurant_group:
            q &= Q(restaurant__group=restaurant_group)
        
        if payment:
            q &= Q(payment=payment)

        result_data_set = PosResultData.objects.filter(q)\
                                                .annotate(date=time_window_archive[time_window]).values('date')\
                                                .annotate(restaurant_id=F('restaurant'), payment=F('payment'))\
                                                .annotate(count=Count('payment'))\
                                                .values('date', 'restaurant_id', 'payment', 'count')
        return Response(result_data_set, status=status.HTTP_200_OK)

class PartyNumberKpiView(APIView):

    @swagger_auto_schema(tags=['A REST API to show KPI count of each party size per restaurant.'], query_serializer=PartyNumberKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI count of each party size per restaurant
            Only GET method exsists.
            base url: http://127.0.0.1:8000/api/v1/kpi/partynumber
        """

        start_time  = request.GET.get('start_time', None)
        end_time    = request.GET.get('end_time', None)
        time_window = request.GET.get('time_window', None)
        start_price = request.GET.get('start_price', None)
        end_price   = request.GET.get('end_price', None)
        start_number_of_people = request.GET.get('start_number_of_people', None)
        end_number_of_people   = request.GET.get('end_number_of_people', None)
        restaurant_group = request.GET.get('restaurant_group', None)
        
        check_none_necessary_string(start_time, "start_time")
        check_none_necessary_string(end_time, "end_time")
        
        start_time = change_format_to_datetime(start_time, 'start_time','%Y-%m-%d', 'YYYY-MM-DD')
        end_time = change_format_to_datetime(end_time, 'end_time' ,'%Y-%m-%d', 'YYYY-MM-DD')
        
        is_equal_or_larger_size(start_time, end_time)

        time_window_archive = {
            'hour' : ExtractHour('timestamp'),
            'day'  : TruncDate('timestamp'),
            'week' : TruncWeek('timestamp'),
            'month': ExtractMonth('timestamp'),
            'year' : ExtractYear('timestamp')
        }
        
        check_none_necessary_string(time_window, "time_window")
        if not time_window in time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (start_price is not None) or (end_price is not None):
            check_none_necessary_string(start_price, 'start_price')
            check_none_necessary_string(end_price, 'end_price')
            is_zero_or_more_numbers(start_price, 'start_price')
            is_zero_or_more_numbers(end_price, 'end_price')
            is_equal_or_larger_size(int(start_price), int(end_price))

        if (start_number_of_people is not None) or (end_number_of_people is not None):
            check_none_necessary_string(start_number_of_people, 'start_number_of_people')
            check_none_necessary_string(end_number_of_people, 'end_number_of_people')
            is_zero_or_more_numbers(start_number_of_people, 'start_number_of_people')
            is_zero_or_more_numbers(end_number_of_people, 'end_number_of_people')
            is_equal_or_larger_size(int(start_number_of_people), int(end_number_of_people))

        if (restaurant_group is not None):
            check_none_necessary_string(restaurant_group, 'restaurant_group')
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
                                                .annotate(restaurant_id=F('restaurant'))\
                                                .annotate(number_of_party=F('number_of_party'))\
                                                .annotate(count=Count('number_of_party'))\
                                                .values('date', 'restaurant_id', 'number_of_party', 'count')
        return Response(result_data_set, status=status.HTTP_200_OK)
