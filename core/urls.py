from django.urls import path
from .views import home_redirect, dashboard,view_contact_details

urlpatterns = [
    path('', home_redirect, name='home'),  
    path('dashboard/', dashboard, name='dashboard'),
    path('bids/<int:bid_id>/view-contact/', view_contact_details, name='view_contact_details'),

]