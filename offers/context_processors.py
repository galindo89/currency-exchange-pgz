"""
Custom context processors for the Offers app.
Provides exchange rate data to templates.
"""
from .models import LatestExchangeRate
from .utils import fetch_and_update_exchange_rate


def exchange_rate_processor(request):
    """
    Adds the latest exchange rate to the context.
    If the rate is not available in the database, it fetches it from the API.
    """

    try:
        latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
        print(f"Latest exchange rate fetched from database: {latest_rate}")
    except LatestExchangeRate.DoesNotExist:
        try:
            latest_rate = fetch_and_update_exchange_rate()
            print(f"Latest exchange rate fetched: {latest_rate}")
        except ValueError as e:
            print(f"Error fetching exchange rate: {e}")
            latest_rate = "N/A"

    return {

        "exchange_rate": round(latest_rate, 3)
    }
