"""
This module contains the views for the core app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from offers.models import Offer, LatestExchangeRate, Bid
from django.views.decorators.csrf import csrf_protect


@never_cache
@login_required
def home_redirect(request):
    """
    Redirects the user to the dashboard if they are logged in.
    Otherwise, redirects them to the login page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('/accounts/login/')


@login_required
def dashboard(request):
    """
    Displays the user's dashboard.
    """
    my_offers = Offer.objects.filter(user=request.user)
    my_bids = Bid.objects.filter(user=request.user)
    for offer in my_offers:
        offer.converted_amount = (
            round(offer.amount / offer.exchange_rate
                  if offer.currency == "EUR"
                  else offer.amount * offer.exchange_rate, 2)
            )
        offer.converted_amount_currency = ("EUR" if offer.currency == "USD"
                                           else "USD")
        offer.action = "Buying" if offer.is_buying else "Selling"

    for bid in my_bids:
        bid.converted_amount = (
            round(bid.amount / bid.exchange_rate if bid.currency == "EUR"
                  else bid.amount * bid.exchange_rate, 2)
        )

        bid.converted_amount_currency = ("EUR" if bid.currency == "USD"
                                         else "USD")
        bid.action = "Selling" if bid.offer.is_buying else "Buying"

    return render(request, 'core/dashboard.html', {
        'my_offers': my_offers,
        'my_bids': my_bids,
    })


@csrf_protect
@login_required
def view_contact_details(request, bid_id):
    """
    Returns the contact details of the user who placed the bid.
    """
    if request.method != 'POST':
        return JsonResponse(
            {'success': False,
             'message': 'Invalid request method.'}, status=405)

    bid = get_object_or_404(Bid, id=bid_id, user=request.user)

    if bid.status == 'ACCEPTED' and bid.contact_shared:
        user = bid.offer.user
        contact_details = {
            'name': f"{user.first_name} \
            {user.last_name}".strip() or "Not Provided",
            'email': user.email or "Not Provided",
        }
        return JsonResponse(
            {'success': True, 'contact_details': contact_details})
    return JsonResponse(
         {'success': False, 'message': 'Contact details not available.'})
