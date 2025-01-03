from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Offer, LatestExchangeRate, Bid
from .forms import OfferForm
from .utils import fetch_and_update_exchange_rate

# Create your views here.

@login_required
def create_offer(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            if offer.rate_type == "FLEXIBLE" or not offer.exchange_rate:
                try:
                    latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
                except LatestExchangeRate.DoesNotExist:
                    latest_rate = fetch_and_update_exchange_rate()
                
                offer.exchange_rate = latest_rate

            offer.save()
            return redirect('offers:view_offers')
    else:
        form = OfferForm()
    return render(request, 'offers/create_offer.html', {'form': form})


@login_required

def view_offers(request):
    offers = Offer.objects.prefetch_related('bids').all()

    for offer in offers:
        offer.user_has_bid = offer.bids.filter(user=request.user).exists() if request.user.is_authenticated else False

        offer.user_bid = offer.bids.filter(user=request.user).first() if request.user.is_authenticated else None

    return render(request, 'offers/view_offers.html', {'offers': offers})


@login_required
def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if offer.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            updated_offer = form.save(commit=False)
            if updated_offer.rate_type == "FLEXIBLE":
                try:
                    latest_rate = LatestExchangeRate.objects.latest("timestamp").rate
                except LatestExchangeRate.DoesNotExist:
                    latest_rate = fetch_and_update_exchange_rate()
                
                updated_offer.exchange_rate = latest_rate

            updated_offer.save()
            return redirect('offers:view_offers')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form})


@login_required
def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if offer.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        offer.delete()
        return redirect('offers:view_offers')
    return render(request, 'offers/delete_offer.html', {'offer': offer})

@login_required
def place_bid(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    existing_bid = Bid.objects.filter(user=request.user, offer=offer).first()

    if existing_bid:
        messages.error(request, "You have already placed a bid for this offer.")
        return redirect('offers:view_offers')

    if request.method == "POST":
        amount = request.POST.get('amount')
        Bid.objects.create(user=request.user, offer=offer, amount=amount)
        messages.success(request, "Your bid has been placed.")
        return redirect('offers:view_offers')


@login_required
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.offer.user != request.user:
        return HttpResponseForbidden()

    bid.status = "REJECTED"
    bid.save()
    messages.success(request, "You have rejected the bid.")
    return redirect('offers:view_offers')
@login_required
def edit_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get('amount')
        bid.amount = amount
        bid.save()
        messages.success(request, "Your bid has been updated.")
        return redirect('offers:view_offers')

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if bid.offer.user != request.user:
        return HttpResponseForbidden()

    bid.status = "ACCEPTED"
    bid.save()
    messages.success(request, "You have accepted the bid.")
    return redirect('offers:view_offers')

@login_required
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if request.user != bid.offer.user:
        return HttpResponseForbidden()     
    bid.status = 'REJECTED'
    bid.save()
    return redirect('offers:view_offers')
@login_required
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)

    if request.method == "POST":
        bid.delete()
        messages.success(request, "Your bid has been removed.")
        return redirect('offers:view_offers')

