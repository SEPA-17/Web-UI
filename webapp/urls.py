from django.urls import path
from .views import MeterDataView, graph
from . import views

urlpatterns = [
    path('', views.home, name='webapp-home'),
    path('meterdata', MeterDataView.as_view(), name='meterdata'),
    path('graph', graph.monthly, name='graph-monthly'),
    path('graph/monthly', graph.monthly, name='graph-monthly'),
    path('graph/monthly.png', graph.monthly_png, name='graph-monthly'),
    path('graph/yearly', graph.yearly, name='graph-yearly')
]