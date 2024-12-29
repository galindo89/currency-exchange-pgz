from django.core.management.base import BaseCommand
from offers.utils import fetch_and_update_exchange_rate
from offers.models import Offer

class Command(BaseCommand):
    help = "Fetch the latest exchange rate and update flexible offers"

    def handle(self, *args, **kwargs):
        try:
            latest_rate = fetch_and_update_exchange_rate()
         
            Offer.objects.filter(rate_type="FLEXIBLE").update(exchange_rate=latest_rate)
            
            self.stdout.write(self.style.SUCCESS(f"Exchange rate updated successfully to {latest_rate}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error updating exchange rate: {str(e)}"))
