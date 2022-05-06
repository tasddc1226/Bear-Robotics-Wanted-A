from kpi.models import PosResultData
from .models import Restaurant
from .serializers import (
    PosDataListSerializer, PosDataDetailSerializer,
    RestaurantListSerializer, RestaurantDetailSerializer,
)
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class PosDataListView(GenericAPIView):
    """
    Pos 데이터의 리스트조회(GET), 입력(POST)
    """
    queryset = PosResultData.objects.all()
    serializer_class = PosDataListSerializer

    def get(self, request, format=None):
        pos_data = get_list_or_404(PosResultData)
        serializer = PosDataListSerializer(pos_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PosDataListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PosDataDetailView(GenericAPIView):
    """
    Pos데이터의 개별 조회(GET)
    """
    queryset = PosResultData.objects.all()
    serializer_class = PosDataDetailSerializer

    def get(self, request, pk, format=None):
        pos_data = get_object_or_404(PosResultData, pk=pk)
        serializer = PosDataDetailSerializer(pos_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RestaurantListView(GenericAPIView):
    """
    Restaurant 테이블의 리스트조회(GET), 데이터 입력(POST)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def get(self, request, format=None):
        restaurants = get_list_or_404(Restaurant)
        serializer = RestaurantListSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = RestaurantListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantDetailView(GenericAPIView):
    """
    Restaurant 테이블의 개별조회(GET), 수정(PUT), 삭제(DELETE)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer

    def get(self, request, pk, format=None):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=kwargs['pk'])
        serializer = RestaurantDetailSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)