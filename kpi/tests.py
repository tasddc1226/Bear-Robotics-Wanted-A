<<<<<<< HEAD
import json

from django.test import TestCase, Client
from datetime import datetime

from restaurant.models import Restaurant, RestaurantGroup, RestaurantMenu
from kpi.models import PosResultData

class KpiPartyNumber(TestCase):
    """
    권은경 - 파티 인원별 조회 테스트 
    """
    def setUp(self):
        
=======
from django.test import TestCase
from .models import Restaurant
from kpi.models import PosResultData
from .views import RestaurantKpiView
from rest_framework.test import APIRequestFactory
from rest_framework import status

factory = APIRequestFactory()
view = RestaurantKpiView.as_view()


"""
테스트 케이스 명세

1. 케이스 설정 방법
    1) error case
        - 예상되는 에러코드를 입력하고 같은 지 확인한다.
    2) success case
        - 예상되는 성공 응답코드를 입력하고 같은 지 확인한다. 

2. 케이스 종류
    1) 필수요소 3개
        - 성공할 것으로 예상되는 테스트 29개 (3^3^3+2=29)
    2) 필수요소 1개 + 옵션요소 3개
        - 필수요소는 성공케이스는 통과했으므로 대표케이스 1개를 Default로 두고
        - start-price & end-price & restaurant-group의 
        - Success 조합 테스트 27개
    3) 필수요소 3개
        - 실패케이스 27개 (3^3^3 = 27)
    4) 필수요소 1개 + 옵션요소 3개
        - 필수요소 실패케이스는 통과했으므로 대표케이스 1개를 Default로 두고
        - start-price & end-price & restaurant-group의 
        - Fail 조합 테스트 27개
    
3. Query String List
    - start-time = "YY-MM-DD"
    - end-time = "YY-MM-DD"
    - time-window = ["HOUR", "DAY", "WEEK", "MONTH", "YEAR"] 중 하나
    - start-price = 0 이상의 정수 (를 요구하는 메시지를 띄우지만 float을 입력해도 에러가 안나야함)
    - end-price = N > start-price
    - restaurant-group = ["빕스버거", "비비고"] <- Group 테이블에 있는 필드명들

4. Setup Database
    - 제공된 csv파일을 참고하여 pos_data 8개, restaurant 4개 입력

5. 한계
    - 성공하였을 때와 실패하였을 때의 응답 데이터도 입력데이터에 따라 예측할 수 있을 것(?) 같지만 구현하지는 않았음
        그래서 데이터의 에러메시지 검증을 할 수 없으며, 또 한편으로는 리턴값이 정확하게 나오는지에 대한 검증도 할 수 없는 테스트케이스임. 
    - 성공할 것이라고 예측되는 것, 실패할 것이라고 예측되는 것과 그 응답코드만 확인할 수 있다는 점이 아쉬운 코드임
    - DB입력도 실제 데이터를 자동으로 넣어주는 방식으로 좀 더 많이 넣을 수 있다면 좋겠으나 시간상 수기 입력으로 대체했음
"""


"""
Success Case를 위한 dummy data
현재 코드들은 3 가지만 입력가능하도록 되어있다. 
"""
field = ['start-time','end-time','time-window','start-price','end-price','restaurant-group']
value = {
    'start-time' : ['2022-02-22', '2022-02-25','2022-03-02'],
    'end-time' : ['2022-03-08', '2022-04-17','2022-05-29'],
    'time-window' : ["HOUR", "DAY", "WEEK", "MONTH", "YEAR"],
    'start-price' : [0, 10000, 20000],
    'end-price' : [20000, 30000, 100000],
    'restaurant-group' : ['빕스버거', '비비고','비비고']
}

"""
Fail Case를 위한 dummy data
"""
f_field = [ 'dsjlfj', 12703, None ]
f_value = {
    'start-time' : ['2029-02-22', 123, None],
    'end-time' : ['1999-03-08', 20220328, None],
    'time-window' : ['sdf', 30, None],
    'start-price' : [-500, 10000000, None],
    'end-price' : [1000, 'BEAR', None],
    'restaurant-group' : ['절대로있을수없는맛있는버거집가게상호명노브랜드로보틱스베어', 123, None]
}



class RestaurantNecessarySuccessTest(TestCase):
    """
    Setup DB
    제공된 csv파일을 참고하여 pos_data 8개, restaurant 4개 입력
    """
    def setUp(self):
        Restaurant.objects.create(
            id = 21,
            restaurant_name = '비비고',
        )
        Restaurant.objects.create(
            id = 22,
            restaurant_name = '비비고',
        )
        Restaurant.objects.create(
            id = 31,
            restaurant_name = '빕스버거',
        )
        Restaurant.objects.create(
            id = 32,
            restaurant_name = '빕스버거',
        )
        PosResultData.objects.create(
            timestamp = '2022-05-02 14:59:33.817393',
            price = 10000,
            number_of_party = 1,
            payment='CARD',
            restaurant_id=21
        )
        PosResultData.objects.create(
            timestamp = '2022-04-22 14:59:33.817393',
            price = 15000,
            number_of_party = 1,
            payment='CARD',
            restaurant_id=21
        )
        PosResultData.objects.create(
            timestamp = '2021-05-12 18:59:33.817393',
            price = 20000,
            number_of_party = 2,
            payment='CARD',
            restaurant_id=22
        )
        PosResultData.objects.create(
            timestamp = '2022-08-05 18:59:33.817393',
            price = 25000,
            number_of_party = 2,
            payment='CARD',
            restaurant_id=22
        )
        PosResultData.objects.create(
            timestamp = '2022-06-30 17:59:33.817393',
            price = 30000,
            number_of_party = 3,
            payment='CARD',
            restaurant_id=31
        )
        PosResultData.objects.create(
            timestamp = '2023-12-31 13:59:33.817393',
            price = 35000,
            number_of_party = 4,
            payment='CARD',
            restaurant_id=31
        )
        PosResultData.objects.create(
            timestamp = '1999-01-01 10:59:33.817393',
            price = 40000,
            number_of_party = 3,
            payment='CARD',
            restaurant_id=32
        )
        PosResultData.objects.create(
            timestamp = '2022-05-02 18:59:33.817393',
            price = 20000,
            number_of_party = 2,
            payment='CARD',
            restaurant_id=32
        )
    """
    필수요소 3개 QueryString 
    29가지 성공 테스트 ( 3 ^ 3 ^ 3 + 2 = 29)
    """
    def test_necessary_success001(self, i=0, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success002(self, i=0, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success003(self, i=0, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success004(self, i=0, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success005(self, i=0, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success006(self, i=0, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success007(self, i=0, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success008(self, i=0, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success009(self, i=0, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success010(self, i=1, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success011(self, i=1, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success012(self, i=1, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success013(self, i=1, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success014(self, i=1, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success015(self, i=1, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success016(self, i=1, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success017(self, i=1, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success018(self, i=1, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success019(self, i=2, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success020(self, i=2, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success021(self, i=2, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success022(self, i=2, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success023(self, i=2, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success024(self, i=2, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success025(self, i=2, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success026(self, i=2, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success027(self, i=2, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success028(self, i=2, j=2, k=3):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_success029(self, i=2, j=2, k=4):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][i]}&{field[1]}={value[field[1]][j]}&{field[2]}={value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    """

    필수요소는 통과했으므로 대표케이스 1개를 Default로 두고
    + start-price & end-price & restaurant-group의 
    Success 조합 테스트 27개

    """
    def test_necessary_and_optional_success001(self, i=0, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success002(self, i=0, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success003(self, i=0, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success004(self, i=0, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success005(self, i=0, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success006(self, i=0, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success007(self, i=0, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success008(self, i=0, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success009(self, i=0, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success010(self, i=1, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success011(self, i=1, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success012(self, i=1, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success013(self, i=1, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success014(self, i=1, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success015(self, i=1, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success016(self, i=1, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success017(self, i=1, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success018(self, i=1, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success019(self, i=2, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success020(self, i=2, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success021(self, i=2, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success022(self, i=2, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success023(self, i=2, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success024(self, i=2, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success025(self, i=2, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success026(self, i=2, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_necessary_and_optional_success027(self, i=2, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{field[0]}={value[field[0]][0]}&{field[1]}={value[field[1]][0]}&{field[2]}={value[field[2]][0]}&{field[3]}={value[field[3]][i]}&{field[4]}={value[field[4]][j]}&{field[5]}={value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    """

    필수요소 3개 QueryString 의 
    실패케이스 29가지 ( 3 ^ 3 ^ 3 = 27)

    """
    def test_necessary_fail001(self, i=0, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail002(self, i=0, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail003(self, i=0, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail004(self, i=0, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail005(self, i=0, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail006(self, i=0, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail007(self, i=0, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail008(self, i=0, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail009(self, i=0, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail010(self, i=1, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail011(self, i=1, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail012(self, i=1, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail013(self, i=1, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail014(self, i=1, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail015(self, i=1, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail016(self, i=1, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail017(self, i=1, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail018(self, i=1, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail019(self, i=2, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail020(self, i=2, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail021(self, i=2, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail022(self, i=2, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail023(self, i=2, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail024(self, i=2, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail025(self, i=2, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail026(self, i=2, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_fail027(self, i=2, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][i]}&{f_field[1]}={f_value[field[1]][j]}&{f_field[2]}={f_value[field[2]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """

    필수요소 실패케이스는 통과했으므로 대표케이스 1개를 Default로 두고
    + start-price & end-price & restaurant-group의 
    Fail 조합 테스트 27개

    """
    def test_necessary_and_optional_fail001(self, i=0, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail002(self, i=0, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail003(self, i=0, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail004(self, i=0, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail005(self, i=0, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail006(self, i=0, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail007(self, i=0, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail008(self, i=0, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail009(self, i=0, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail010(self, i=1, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail011(self, i=1, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail012(self, i=1, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail013(self, i=1, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail014(self, i=1, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail015(self, i=1, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail016(self, i=1, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail017(self, i=1, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail018(self, i=1, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail019(self, i=2, j=0, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail020(self, i=2, j=0, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail021(self, i=2, j=0, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail022(self, i=2, j=1, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail023(self, i=2, j=1, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail024(self, i=2, j=1, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail025(self, i=2, j=2, k=0):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail026(self, i=2, j=2, k=1):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_necessary_and_optional_fail027(self, i=2, j=2, k=2):
        request = factory.get(f'/api/v1/kpi/restaurant?{f_field[0]}={f_value[field[0]][0]}&{f_field[1]}={f_value[field[1]][0]}&{f_field[2]}={f_value[field[2]][0]}&{f_field[i]}={f_value[field[3]][i]}&{f_field[j]}={f_value[field[4]][j]}&{f_field[k]}={f_value[field[5]][k]}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
>>>>>>> ad955c863c84e8fcd0dfc919b7b682a9d7dfb3bc
