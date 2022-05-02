from django.urls import path
from .views import RestaurantView

urlpatterns = [
    path('restaurant', RestaurantView.as_view(), name='restaurant-view'),
]
