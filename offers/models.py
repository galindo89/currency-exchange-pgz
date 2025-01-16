"""
Models for the Offers app.
Defines Offer, Bid, and LatestExchangeRate models.
"""
from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    """
    Represents an offer to buy or sell currency.
    """
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    RATE_TYPE_CHOICES = [
        ('FIXED', 'Fixed'),
        ('FLEXIBLE', 'Flexible'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offers")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exchange_rate = models.DecimalField(
        max_digits=8, decimal_places=3, null=True, blank=True)
    is_buying = models.BooleanField()
    rate_type = models.CharField(
        max_length=10, choices=RATE_TYPE_CHOICES, default='FIXED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the offer.
        """

        return f"{'Buying' if self.is_buying else 'Selling'} {self.amount} \
        {self.currency} at {self.exchange_rate} ({self.rate_type})"

    class Meta:
        """
        Meta class for the Offer model.
        """
        ordering = ['-created_at']

    @property
    def conversion_amount(self):
        """
        Converts the offer amount to the target currency using the exchange
        rate.
        """
        if self.currency == "USD":
            return round(self.amount * self.exchange_rate, 2)
        elif self.currency == "EUR":
            return round(self.amount / self.exchange_rate, 2)
        return None


class LatestExchangeRate(models.Model):
    """
    Represents the latest exchange rate between two currencies.
    """
    base_currency = models.CharField(max_length=3, default="USD")
    target_currency = models.CharField(max_length=3, default="EUR")
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the exchange rate.
        """
        return f"{self.base_currency} to {self.target_currency}: {self.rate} \
        (updated {self.timestamp})"


class Bid(models.Model):
    """
    Represents a bid on an offer.
    """
    STATUS_CHOICES = [
        ('AWAITING', 'Awaiting Response'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    offer = models.ForeignKey(
        'Offer', on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Offer.CURRENCY_CHOICES)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='AWAITING')
    contact_shared = models.BooleanField(default=False)

    class Meta:
        """
        Meta class for the Bid model.
        """
        unique_together = ('user', 'offer')

    def __str__(self):
        """
        Returns a string representation of the bid.
        """
        return f"Bid by {self.user.username} on {self.offer} \
        - Amount: {self.amount} ({self.get_status_display()})"
