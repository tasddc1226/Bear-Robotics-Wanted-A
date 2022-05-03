from django.urls import path
from .views import (
    RestaurantKpiView,
    PaymentKpiView,
    PartyNumberKpiView
)

urlpatterns = [
    path('restaurant', RestaurantKpiView.as_view(), name='restaurant-view'),
    path('payment', PaymentKpiView.as_view(), name='payment-view'),
    path('partynumber', PartyNumberKpiView.as_view(), name='party-number'),
]
