from django import forms
from .models import Offer, LatestExchangeRate, Bid
from .utils import fetch_and_update_exchange_rate

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['currency', 'amount', 'exchange_rate', 'is_buying', 'rate_type']
        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'exchange_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'rate_type': forms.Select(attrs={'class': 'form-control'}),
            'is_buying': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0 or amount > 100000:
            raise forms.ValidationError("Amount must be between 1 and 100,000.")
        return amount

    def clean_exchange_rate(self):
        rate_type = self.cleaned_data.get("rate_type")
        exchange_rate = self.cleaned_data.get("exchange_rate")

        # Try to fetch the latest rate from the database
        try:
            latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
        except LatestExchangeRate.DoesNotExist:
            # If no rate exists, fetch it from the API
            latest_rate = fetch_and_update_exchange_rate()

        # If rate type is FLEXIBLE, always use the latest rate
        if rate_type == "FLEXIBLE":
            return latest_rate

        # If rate type is FIXED and exchange_rate is empty, use the latest rate
        if rate_type == "FIXED" and not exchange_rate:
            return latest_rate
        
          # Validate exchange_rate if provided
        if exchange_rate is not None and exchange_rate <= 0:
            raise forms.ValidationError("Exchange rate must be a positive number.")
       

        return exchange_rate
    
    
    
class BidForm(forms.ModelForm):
     class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bid amount'}),
        }
        
    
    
    
