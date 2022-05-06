from django.urls import path
from .views import (
    PosDataListView, PosDataDetailView,
    RestaurantListView,RestaurantDetailView,
)

urlpatterns = [
    path('pos', PosDataListView.as_view(), name='pos-list'),
    path('pos/<int:pk>', PosDataDetailView.as_view(), name='pos-detail'),
    path('restaurants', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>', RestaurantDetailView.as_view(), name='restaurnt-detail'),
]
