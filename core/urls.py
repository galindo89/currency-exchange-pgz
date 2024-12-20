from django.urls import path
from .views import home_redirect, dashboard

urlpatterns = [
    path('', home_redirect, name='home'),  
    path('dashboard/', dashboard, name='dashboard'),
]