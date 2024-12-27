from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['currency', 'amount', 'exchange_rate', 'rate_type', 'is_buying']
        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'exchange_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            "rate_type": forms.Select(attrs={'class': 'form-control'}),
            'is_buying': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
           
        }
        labels = {
            'is_buying': 'Are you buying?',
            'rate_type': 'Rate Type',
        }