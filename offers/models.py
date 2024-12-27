from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Offer(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    RATE_TYPE_CHOICES = [
        ('FIXED', 'Fixed'),
        ('VARIABLE', 'Variable'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_buying = models.BooleanField() 
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES, default='FIXED') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Buying' if self.is_buying else 'Selling'} {self.amount} {self.currency} at {self.exchange_rate} ({self.rate_type})"

    class Meta:
        ordering = ['-created_at']
        
