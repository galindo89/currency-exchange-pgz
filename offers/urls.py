from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.view_offers, name='view_offers'),
    path('create/', views.create_offer, name='create_offer'),
    path('edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('delete/<int:pk>/', views.delete_offer, name='delete_offer'),
    path('<int:offer_id>/place_bid/', views.place_bid, name='place_bid'),
    path('bids/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('bids/<int:bid_id>/reject/', views.reject_bid, name='reject_bid'),
    path('<int:bid_id>/edit_bid/', views.edit_bid, name='edit_bid'),
    path('<int:bid_id>/delete_bid/', views.delete_bid, name='delete_bid')
    
]