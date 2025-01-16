"""
Utility functions for the Offers app.
Contains helper methods for handling exchange rates and other reusable logic.
"""
import requests
from django.conf import settings
from .models import LatestExchangeRate


def fetch_and_update_exchange_rate():
    """
    Fetches the latest exchange rate from the Open Exchange Rates API
    and updates the database.
    """
    API_KEY = getattr(settings, 'OPENEXCHANGERATES_API_KEY', None)
    if not API_KEY:
        raise ValueError(
            "OPENEXCHANGERATES_API_KEY is \not set in environment variables.")

    url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}&base=USD&symbols=EUR"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"]["EUR"]
        LatestExchangeRate.objects.update_or_create(
            base_currency="USD",
            target_currency="EUR",
            defaults={"rate": rate}
        )
        return rate
    except Exception as e:
        raise ValueError(f"Error fetching exchange rate: {e}")
