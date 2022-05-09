from datetime import timedelta
from restaurant.models import Restaurant
from .models import PosResultData
from .serializers import (
    RestaurantKpiSerializer,
    PaymentKpiSerializer,
    PartyNumberKpiSerializer
)
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import (
    ExtractHour, ExtractDay, ExtractWeek ,ExtractMonth, ExtractYear,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .validate import *
from drf_yasg.utils import swagger_auto_schema

class KPIUtils:
    # Define time windows
    time_window_archive = {
        'hour' : ExtractHour('timestamp'),
        'day'  : ExtractDay('timestamp'),
        'week' : ExtractWeek('timestamp'),
        'month': ExtractMonth('timestamp'),
        'year' : ExtractYear('timestamp')
    }

    def make_filter_with_validate_params(self, data):

        """ [NECESSARY] query params """
        start_time  = data.GET.get('start_time', None)
        end_time    = data.GET.get('end_time', None)
        
        """ [OPTIONAL 1] query params """
        start_price = data.GET.get('start_price', None)
        end_price   = data.GET.get('end_price', None)

        """ [OPTIONAL 2] query params """
        start_number_of_people = data.GET.get('start_number_of_people', None)
        end_number_of_people   = data.GET.get('end_number_of_people', None)

        """ [OPTIONAL 3] query params """
        restaurant_group = data.GET.get('restaurant_group', None)

        """ [OPTIONAL 4] query params """
        payment = data.GET.get('payment', None)
        
        # Validate start_time, end_time params
        check_none_necessary_string(start_time, "start_time")
        check_none_necessary_string(end_time, "end_time")
        
        # Change date format and check size
        start_time = change_format_to_datetime(start_time, 'start_time', '%Y-%m-%d', 'YYYY-MM-DD')
        end_time = change_format_to_datetime(end_time, 'end_time', '%Y-%m-%d', 'YYYY-MM-DD')
        is_equal_or_larger_size(start_time, end_time)

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
        
        # Query
        q = Q()

        # 기간 검색
        q &= Q(timestamp__range=(start_time, end_time + timedelta(days=1)))

        # 금액 범위 검색
        if start_price and end_price:
            q &= Q(price__range=(start_price, end_price))

        # 인원 범위 검색
        if start_number_of_people and end_number_of_people:
            q &= Q(number_of_party__range=(start_number_of_people, end_number_of_people))

        # 특정 레스토랑 검색
        if restaurant_group:
            q &= Q(restaurant__group=restaurant_group)

        # 결재수단 검색
        if payment:
            q &= Q(payment=payment)

        return PosResultData.objects.filter(q)


class RestaurantKpiView(APIView, KPIUtils):
    """
        Writer : 윤상민
        Reviewer : 양수영
        Refactor : 윤상민, 양수영, 권은경 
    """
    @swagger_auto_schema(tags=['KPI sales (price) per restaurant.'], query_serializer=RestaurantKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI sales (price) per restaurant
            Only GET method exsists.
            base url: /api/v1/kpi/restaurant
        """       
        queryset = self.make_filter_with_validate_params(request)
        time_window = request.GET.get('time_window', None)

        check_none_necessary_string(time_window, "time_window")
        if not time_window in self.time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Aggreate
        annotate_options = {
            time_window: self.time_window_archive[time_window.lower()],
            'total_price': Sum('price')
        }
        data = queryset.values('restaurant_id').annotate(**annotate_options)  # Changed: Response는 간략히

        return Response(data=data, status=status.HTTP_200_OK)

class PaymentKpiView(APIView, KPIUtils):

    @swagger_auto_schema(tags=['KPI count of each payment method per restaurant.'], query_serializer=PaymentKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI sales (price) per restaurant
            Only GET method exsists.
            base url: /api/v1/kpi/payment
        """
        queryset = self.make_filter_with_validate_params(request)
        time_window = request.GET.get('time_window', None)
        
        check_none_necessary_string(time_window, "time_window")
        if not time_window in self.time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        annotate_options = {
            time_window: self.time_window_archive[time_window],
            'payment': F('payment'),
            'count': Count('payment')
        }
        data = queryset.values('restaurant_id').annotate(**annotate_options)

        return Response(data=data, status=status.HTTP_200_OK)

class PartyNumberKpiView(APIView, KPIUtils):

    @swagger_auto_schema(tags=['A REST API to show KPI count of each party size per restaurant.'], query_serializer=PartyNumberKpiSerializer, responses={200: 'Success'})
    def get(self, request):
        """
            A REST API to show KPI count of each party size per restaurant
            Only GET method exsists.
            base url: /api/v1/kpi/partynumber
        """
        queryset = self.make_filter_with_validate_params(request)
        time_window = request.GET.get('time_window', None)
        
        check_none_necessary_string(time_window, "time_window")
        if not time_window in self.time_window_archive:
            return Response(
                {"message":"time-window의 입력 인자는 'hour','day','week','month','year'중의 하나입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        annotate_options = {
            time_window: self.time_window_archive[time_window],
            'number_of_party': F('number_of_party'),
            'count': Count('number_of_party')
        }
        data = queryset.values('restaurant_id').annotate(**annotate_options)

        return Response(data=data, status=status.HTTP_200_OK)
