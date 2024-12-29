from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Offer model
class Offer(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    RATE_TYPE_CHOICES = [
        ('FIXED', 'Fixed'),
        ('FLEXIBLE', 'Flexible'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=3,null=True, blank=True)
    is_buying = models.BooleanField()
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES, default='FIXED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Buying' if self.is_buying else 'Selling'} {self.amount} {self.currency} at {self.exchange_rate} ({self.rate_type})"

    class Meta:
        ordering = ['-created_at']
    
    @property
    def conversion_amount(self):       
        if self.currency == "USD":          
            return round(self.amount * self.exchange_rate, 2)
        elif self.currency == "EUR":
           return round(self.amount / self.exchange_rate, 2)
        return None

# LatestExchangeRate model
class LatestExchangeRate(models.Model):
    base_currency = models.CharField(max_length=3, default="USD")
    target_currency = models.CharField(max_length=3, default="EUR")
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency}: {self.rate} (updated {self.timestamp})"


