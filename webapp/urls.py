from django.urls import path
from django.contrib.auth import views as auth_views
from .views import MeterDataView, graph_view, DataUsageView
from . import views

urlpatterns = [
    path('', views.home, name='webapp-home'),
    path('meterdata', MeterDataView.as_view(), name='meter-data'),
    path('datausage', DataUsageView.as_view(), name='data-usage'),

    path('graph', graph_view.monthly, name='graph'),
    path('graph/monthly', graph_view.monthly, name='graph-monthly'),
    path('graph/monthly.png', graph_view.monthly_png, name='graph-monthly-png'),
    path('graph/yearly', graph_view.yearly, name='graph-yearly'),

    path('user/login', auth_views.LoginView.as_view(template_name='webapp/user/login.html'), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(template_name='webapp/user/logout.html'), name='logout')
]
