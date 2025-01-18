"""
This file contains the tests for the offers app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from offers.models import Offer, LatestExchangeRate


class OfferCreationTest(TestCase):
    """
    Tests for creating offers.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.user = User.objects.create_user(username="testuser",
                                             password="password")
        self.latest_rate = LatestExchangeRate.objects.create(
            base_currency="USD",
            target_currency="EUR",
            rate=1.10,
        )
        self.create_offer_url = reverse("offers:create_offer")

    def test_create_offer_fixed_rate(self):
        """
        Test creating an offer with a fixed rate.
        """
        self.client.login(username="testuser", password="password")

        data = {
            "currency": "USD",
            "amount": 1000,
            "exchange_rate": 1.05,
            "is_buying": True,
            "rate_type": "FIXED",
        }

        response = self.client.post(self.create_offer_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Offer.objects.filter(currency="USD", rate_type="FIXED").exists()
        )

    def test_create_offer_flexible_rate(self):
        """
        Test creating an offer with a flexible rate.
        """
        self.client.login(username="testuser", password="password")

        data = {
            "currency": "EUR",
            "amount": 500,
            "is_buying": False,
            "rate_type": "FLEXIBLE",
        }

        response = self.client.post(self.create_offer_url, data)

        self.assertEqual(response.status_code, 302)
        offer = Offer.objects.filter(currency="EUR",
                                     rate_type="FLEXIBLE").first()
        self.assertIsNotNone(offer)
        self.assertEqual(offer.exchange_rate, self.latest_rate.rate)

    def test_invalid_offer_submission(self):
        """
        Test submitting an invalid offer.
        """
        self.client.login(username="testuser", password="password")

        data = {
            "currency": "USD",
            "amount": -100,
            "is_buying": True,
            "rate_type": "FIXED",
        }

        response = self.client.post(self.create_offer_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form",
                             "amount", "Amount must be between 1 and 100,000.")
