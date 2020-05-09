from django.urls import path
from .views import MeterDataView
from . import views

urlpatterns = [
    path('', views.home, name='webapp-home'),
    path('meterdata', MeterDataView.as_view(), name='meterdata')
]