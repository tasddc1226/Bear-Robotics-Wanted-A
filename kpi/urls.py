from django.urls import path
from .views import RestaurantKpiView

urlpatterns = [
    path('restaurant', RestaurantKpiView.as_view(), name='restaurant-view'),
]
