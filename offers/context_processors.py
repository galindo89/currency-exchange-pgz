from .models import LatestExchangeRate
from .utils import fetch_and_update_exchange_rate

def exchange_rate_processor(request):
    try:
        latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
        print(f"Latest exchange rate fetched from database: {latest_rate}")
    except LatestExchangeRate.DoesNotExist:
        try:
            # If no rate exists in the database, fetch it from the API from openexchangerates.org
            latest_rate = fetch_and_update_exchange_rate()
            print(f"Latest exchange rate fetched: {latest_rate}")
        except ValueError as e:
            # Handle API errors gracefully and fallback to "N/A". Not desired. Let's check
            print(f"Error fetching exchange rate: {e}")
            latest_rate = "N/A"

    return {
        "exchange_rate": round(latest_rate,3)
    }
