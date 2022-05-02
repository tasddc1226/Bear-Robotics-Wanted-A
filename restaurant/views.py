from http.client import responses
from kpi.models import PosResultData
from .models import Restaurant
from .serializers import (
    PosDataListSerializer, PosDataDetailSerializer,
    RestaurantListSerializer, RestaurantDetailSerializer,
)
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# PosData get, post
class PosDataListView(APIView):
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

class PosDataDetailView(APIView):
    def get(self, request, pk, format=None):
        pos_data = get_object_or_404(PosResultData, pk=pk)
        serializer = PosDataDetailSerializer(pos_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 개발용으로 만들어둔거
# 레스토랑 데이타 get, post, update, delete
class RestaurantListView(APIView):
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

class RestaurantDetailView(APIView):
    def get(self, request, pk, format=None):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk, format=None):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantDetailSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)