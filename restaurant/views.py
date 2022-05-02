from http.client import responses
from kpi.models import PosResultData
from .serializers import PosDataListSerializer, PosDataDetailSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
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