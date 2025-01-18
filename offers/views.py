"""
Views for the Offers app.
Defines the logic for handling offer and bid-related operations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Offer, LatestExchangeRate, Bid
from .forms import OfferForm
from .utils import fetch_and_update_exchange_rate


@login_required
def create_offer(request):
    """
    Handles the creation of new offers.
    """
    next_url = request.GET.get('next', 'offers:view_offers')
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            if offer.rate_type == "FLEXIBLE" or not offer.exchange_rate:
                try:
                    latest_rate = LatestExchangeRate.objects.latest(
                                  "timestamp").rate
                except LatestExchangeRate.DoesNotExist:
                    latest_rate = fetch_and_update_exchange_rate()

                offer.exchange_rate = latest_rate

            offer.save()
            messages.success(request, "Offer created successfully.")
            return redirect(next_url)
    else:
        form = OfferForm()
    return render(request, 'offers/create_offer.html', {'form': form})


@login_required
def view_offers(request):
    """
    Displays a list of all available offers with optional filters.
    """
    offers = Offer.objects.prefetch_related('bids').all()
    is_buying = request.GET.get('is_buying')
    currency = request.GET.get('currency')
    rate_type = request.GET.get('rate_type')

    if is_buying in ['0', '1']:
        offers = offers.filter(is_buying=bool(int(is_buying)))

    if currency:
        offers = offers.filter(currency=currency)

    if rate_type:
        offers = offers.filter(rate_type=rate_type)

    for offer in offers:
        offer.user_bid = offer.bids.filter(user=request.user).first()
        offer.converted_amount = (
            round(offer.amount / offer.exchange_rate
                  if offer.currency == "EUR"
                  else offer.amount * offer.exchange_rate, 2)
        )
        offer.converted_amount_currency = ("EUR"
                                           if offer.currency == "USD"
                                           else "USD")
        offer.action = "Buying" if offer.is_buying else "Selling"
        if offer.user_bid:
            offer.bid_converted_amount = round(
                offer.user_bid.amount / offer.user_bid.exchange_rate
                if offer.user_bid.currency == "EUR"
                else offer.user_bid.amount * offer.user_bid.exchange_rate, 2
            )
            offer.bid_converted_currency = (
                "EUR" if offer.user_bid.currency == "USD" else "USD"
            )
        else:
            offer.bid_converted_amount = None
            offer.bid_converted_currency = None

    return render(request, 'offers/view_offers.html', {'offers': offers})


@login_required
def edit_offer(request, pk):
    """
    Handles the editing of existing offers.
    """
    offer = get_object_or_404(Offer, pk=pk)
    next_url = request.GET.get('next', 'offers:view_offers')
    if offer.user != request.user:
        return HttpResponseForbidden()

    if offer.bids.filter(status='ACCEPTED').exists():
        messages.error(
            request, "You cannot edit this offer as it has at least one \
            accepted bid.")
        return redirect(next_url)
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            updated_offer = form.save(commit=False)
            if updated_offer.rate_type == "FLEXIBLE":
                try:
                    latest_rate = LatestExchangeRate.objects.latest(
                        "timestamp").rate
                except LatestExchangeRate.DoesNotExist:
                    latest_rate = fetch_and_update_exchange_rate()

                updated_offer.exchange_rate = latest_rate

            updated_offer.save()
            messages.success(request, "Offer updated successfully.")
            return redirect(next_url)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form})


@login_required
def delete_offer(request, pk):
    """
    Handles the deletion of existing offers.
    """
    offer = get_object_or_404(Offer, pk=pk)
    if offer.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        offer.delete()
        messages.success(request, "Offer deleted successfully.")
        next_url = request.GET.get('next', 'offers:view_offers')
        return redirect(next_url)

    return render(request, 'offers/delete_offer.html', {'offer': offer})


@login_required
def place_bid(request, offer_id):
    """
    Handles the placement of bids on offers.
    """
    offer = get_object_or_404(Offer, id=offer_id)
    existing_bid = Bid.objects.filter(offer=offer, user=request.user).first()
    next_url = request.GET.get('next', 'offers:view_offers')

    if existing_bid:
        messages.error(
            request, "You have already placed a bid for this offer.")
        return redirect(next_url)

    if request.method == "POST":
        bid = Bid(
            offer=offer,
            user=request.user,
            amount=offer.amount,
            currency=offer.currency,
            exchange_rate=offer.exchange_rate,
        )
        bid.save()
        messages.success(request, "Bid placed successfully.")
        return redirect(next_url)

    return render(request, 'offers/place_bid.html', {'offer': offer})


@login_required
def view_bids(request, offer_id):
    """
    Displays a list of all bids on a particular offer.
    """
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)
    offer.action = "Buying" if offer.is_buying else "Selling"
    offer.converted_amount = (
        round(offer.amount / offer.exchange_rate
              if offer.currency == "EUR"
              else offer.amount * offer.exchange_rate, 2))
    offer.converted_amount_currency = ("EUR"
                                       if offer.currency == "USD" else "USD")

    bids = offer.bids.all()
    has_accepted_bids = offer.bids.filter(status='ACCEPTED').exists()
    has_awaiting_bids = offer.bids.filter(status='AWAITING').exists()
    bids_exist = offer.bids.exists()
    for bid in bids:
        bid.converted_amount = (
            round(bid.amount / bid.exchange_rate
                  if bid.offer.currency == "EUR"
                  else bid.amount * bid.exchange_rate, 2)
        )
        bid.converted_amount_currency = ("EUR"
                                         if offer.currency == "USD" else "USD")
        bid.action = "Selling" if bid.offer.is_buying else "Buying"

    return render(request,
                  'offers/view_bids.html',
                  {'offer': offer,
                   'bids': bids,
                   'has_accepted_bids': has_accepted_bids,
                   'has_awaiting_bids': has_awaiting_bids,
                   'bids_exist': bids_exist
                   })


@login_required
def edit_bid(request, bid_id):
    """
    Handles the editing of existing bids.
    """
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)
    offer = bid.offer
    next_url = request.GET.get('next', 'offers:view_offers')

    if bid.status != "AWAITING":
        messages.error(request,
                       "You cannot edit this bid as \
                       it has already been processed."
                       )
        return redirect(next_url)

    if offer.rate_type != "FLEXIBLE":
        messages.error(request,
                       "Bids can only be updated for offers with a flexible \
                       exchange rate.")
        return redirect(next_url)

    if request.method == "POST":
        try:
            latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
        except LatestExchangeRate.DoesNotExist:
            latest_rate = offer.exchange_rate

        bid.exchange_rate = latest_rate
        bid.save()
        messages.success(request,
                         "Your bid has been updated with the latest exchange \
                         rate.")
        return redirect(next_url)

    return render(request, 'offers/edit_bid.html',
                  {'bid': bid, 'next': next_url, 'offer': offer})


@login_required
def accept_bid(request, bid_id):
    """
    Handles the acceptance of bids by offer owners.
    """
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.offer.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        bid.status = "ACCEPTED"
        bid.save()
        messages.success(request, "You have accepted the bid.")
        next_url = request.GET.get('next', 'offers:view_offers')
        return redirect(next_url)


@login_required
def reject_bid(request, bid_id):
    """
    Handles the rejection of bids by offer owners.
    """
    bid = get_object_or_404(Bid, id=bid_id)
    if request.user != bid.offer.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        bid.status = "REJECTED"
        bid.save()
        messages.success(request, "You have rejected the bid.")
        next_url = request.GET.get('next', 'offers:view_offers')
        return redirect(next_url)


@login_required
def delete_bid(request, bid_id):
    """
    Handles the deletion of bids by users.
    """
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)
    next_url = request.GET.get('next', 'offers:view_offers')

    if request.method == "POST":
        bid.delete()
        messages.success(request, "Your bid has been removed.")
        return redirect(next_url)

    return redirect(next_url)


@login_required
def share_contact(request, bid_id):
    """
    Shares contact details with the bidder.
    """
    bid = get_object_or_404(Bid, id=bid_id, offer__user=request.user,
                            status='ACCEPTED')

    if request.method == 'POST':
        bid.contact_shared = True
        bid.save()
        messages.success(request, "Contact details have been  \
                          shared with the bidder.")
        return redirect('offers:view_bids', offer_id=bid.offer.id)

    return HttpResponseForbidden()
