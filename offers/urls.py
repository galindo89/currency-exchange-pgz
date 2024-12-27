from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.view_offers, name='view_offers'),
    path('create/', views.create_offer, name='create_offer'),
    path('edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('delete/<int:pk>/', views.delete_offer, name='delete_offer'),
]