from django.urls import path
from .views import PosDataListView,PosDataDetailView

urlpatterns = [
    path('pos', PosDataListView.as_view(), name='pos-list'),
    path('pos/<int:pk>', PosDataDetailView.as_view(), name='pos-detail'),
]
