from django.contrib import admin
from .models import Offer, LatestExchangeRate, Bid

# Register your models here.

admin.site.register(Offer)
admin.site.register(LatestExchangeRate)
admin.site.register(Bid)