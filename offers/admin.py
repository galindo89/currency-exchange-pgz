from django.contrib import admin
from .models import Offer, LatestExchangeRate

# Register your models here.

admin.site.register(Offer)
admin.site.register(LatestExchangeRate)