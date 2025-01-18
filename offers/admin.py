"""
Admin module for the Offers app.
Handles registration of models to the Django admin interface.
"""
from django.contrib import admin
from .models import Offer, LatestExchangeRate, Bid

admin.site.register(Offer)
admin.site.register(LatestExchangeRate)
admin.site.register(Bid)
