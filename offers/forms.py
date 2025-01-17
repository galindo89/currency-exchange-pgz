"""
Forms for the Offers app.
Contains forms for creating and validating offers and bids.
"""

from django import forms
from .models import Offer, LatestExchangeRate, Bid
from .utils import fetch_and_update_exchange_rate


class OfferForm(forms.ModelForm):
    """
    A form for creating and updating Offer objects.
    """
    class Meta:
        model = Offer
        fields = [
            'currency', 'amount', 'exchange_rate', 'is_buying', 'rate_type']
        widgets = {
            'currency': forms.Select(attrs={
                'class': 'form-control'                
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount to buy or sell'}),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave empty for latest rate'}),
            'rate_type': forms.Select(attrs={
                'class': 'form-control'}),
            'is_buying': forms.CheckboxInput(attrs={
                'class': 'form-check-input'}),
        }
        labels = {
            'currency': 'Currency',
            'amount': 'Amount',
            'exchange_rate': 'Exchange Rate',
            'is_buying': 'Click here if you are buying the desired currency',
            'rate_type': 'Rate Type',
            }

    def clean_amount(self):
        """
        Validates the amount field to ensure it is positive and within the
        allowed range.
        """
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0 or amount > 100000:
            raise forms.ValidationError(
                "Amount must be between 1 and 100,000.")
        return amount

    def clean_exchange_rate(self):
        """
        Validates or sets the exchange rate field based on the rate type.
        """
        rate_type = self.cleaned_data.get("rate_type")
        exchange_rate = self.cleaned_data.get("exchange_rate")

        try:
            latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
        except LatestExchangeRate.DoesNotExist:
            latest_rate = fetch_and_update_exchange_rate()

        if rate_type == "FLEXIBLE":
            return latest_rate

        if rate_type == "FIXED" and not exchange_rate:
            return latest_rate

        if exchange_rate is not None and exchange_rate <= 0:
            raise forms.ValidationError(
                "Exchange rate must be a positive number.")

        return exchange_rate
