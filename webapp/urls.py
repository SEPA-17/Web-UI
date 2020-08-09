from django.urls import path
from django.contrib.auth import views as auth_views
from .views import MeterDataView, graph, user
from . import views

urlpatterns = [
    path('', views.home, name='webapp-home'),
    path('meterdata', MeterDataView.as_view(), name='meterdata'),

    path('graph', graph.monthly, name='graph'),
    path('graph/monthly', graph.monthly, name='graph-monthly'),
    path('graph/monthly.png', graph.monthly_png, name='graph-monthly-png'),
    path('graph/yearly', graph.yearly, name='graph-yearly'),

    path('user/login', auth_views.LoginView.as_view(template_name='webapp/user/login.html'), name='login'),
    path('user/logout', auth_views.LogoutView.as_view(template_name='webapp/user/logout.html'), name='logout')
]
