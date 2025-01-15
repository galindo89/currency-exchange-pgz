import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_portal.settings')  # Replace with your settings module if different
django.setup()

from offers.models import Offer, Bid, LatestExchangeRate
from django.contrib.auth.models import User

def create_dummy_data():
    try:
        # Get test users
        user1 = User.objects.get(username='pablotablet')
        user2 = User.objects.get(username='pablogalindo')

        # Get the latest exchange rate
        latest_rate = LatestExchangeRate.objects.latest('timestamp').rate

        # Create offers and bids
        for i in range(1, 6):
            # Offers by user1
            offer_user1 = Offer.objects.create(
                user=user1,
                currency=random.choice(['USD', 'EUR']),
                amount=random.randint(100, 1000),
                exchange_rate=latest_rate,
                is_buying=random.choice([True, False]),
                rate_type=random.choice(['FLEXIBLE', 'FIXED']),
            )

            # Offers by user2
            offer_user2 = Offer.objects.create(
                user=user2,
                currency=random.choice(['USD', 'EUR']),
                amount=random.randint(100, 1000),
                exchange_rate=latest_rate,
                is_buying=random.choice([True, False]),
                rate_type=random.choice(['FLEXIBLE', 'FIXED']),
            )

            # Create bids for offer_user1
            if not Bid.objects.filter(offer=offer_user1, user=user2).exists():
                Bid.objects.create(
                    offer=offer_user1,
                    user=user2,
                    amount=offer_user1.amount,
                    currency=offer_user1.currency,
                    exchange_rate=offer_user1.exchange_rate,
                    status='AWAITING',
                )

            # Create bids for offer_user2
            if not Bid.objects.filter(offer=offer_user2, user=user1).exists():
                Bid.objects.create(
                    offer=offer_user2,
                    user=user1,
                    amount=offer_user2.amount,
                    currency=offer_user2.currency,
                    exchange_rate=offer_user2.exchange_rate,
                    status='AWAITING',
                )

        print("Dummy data created successfully.")

    except User.DoesNotExist:
        print("Test users not found. Please ensure 'pablotablet' and 'pablogalindo' exist.")
    except LatestExchangeRate.DoesNotExist:
        print("No exchange rate found. Please add one to the database.")

# Run the function
if __name__ == "__main__":
    create_dummy_data()
