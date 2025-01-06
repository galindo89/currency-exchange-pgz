from django.db import models
from django.contrib.auth.models import User


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
    
#Bids model

class Bid(models.Model):
    STATUS_CHOICES = [
        ('AWAITING', 'Awaiting Response'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AWAITING')
    
    class Meta:
        unique_together = ('user', 'offer')  

    def __str__(self):
        return f"Bid by {self.user.username} on {self.offer} - Amount: {self.amount} ({self.get_status_display()})"

