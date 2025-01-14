from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Offer, LatestExchangeRate, Bid
from .forms import OfferForm
from .utils import fetch_and_update_exchange_rate
from .forms import BidForm

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

    # Filters
    is_buying = request.GET.get('is_buying')
    currency = request.GET.get('currency')
    rate_type = request.GET.get('rate_type')

    if is_buying in ['0', '1']: 
        offers = offers.filter(is_buying=bool(int(is_buying)))

    if currency:
        offers = offers.filter(currency=currency)

    if rate_type:
        offers = offers.filter(rate_type=rate_type)

    # Annotate offers with user's bid if exists
    for offer in offers:
        offer.user_bid = offer.bids.filter(user=request.user).first()

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
        messages.success(request, "Offer deleted successfully.")
        
        
        next_url = request.GET.get('next', 'offers:view_offers')  
        return redirect(next_url)

    return render(request, 'offers/delete_offer.html', {'offer': offer})

@login_required
def place_bid(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    existing_bid = Bid.objects.filter(offer=offer, user=request.user).first()

    if existing_bid:
        messages.error(request, "You have already placed a bid for this offer.")
        return redirect('offers:view_offers')

    if request.method == "POST":
        form = BidForm(request.POST,offer=offer)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.offer = offer
            bid.user = request.user
            bid.save()
            messages.success(request, "Bid placed successfully.")
            return redirect('offers:view_offers')
    else:
        form = BidForm(offer=offer)

    return render(request, 'offers/place_bid.html', {'form': form, 'offer': offer})

@login_required
def view_bids(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)
    bids = offer.bids.all()
    has_accepted_bids = offer.bids.filter(status='ACCEPTED').exists()
    for bid in bids:
        bid.converted_amount = (
            round(bid.amount / offer.exchange_rate if offer.currency == "USD" else bid.amount * offer.exchange_rate, 2)
        )

    return render(request, 'offers/view_bids.html', {'offer': offer, 'bids': bids, 'has_accepted_bids': has_accepted_bids})

   
@login_required
def edit_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)
    offer = bid.offer 

    if request.method == "POST":
        form = BidForm(request.POST, instance=bid, offer=offer)  
        if form.is_valid():
            form.save()
            messages.success(request, "Your bid has been updated successfully.")
            return redirect('offers:view_offers')
    else:
        form = BidForm(instance=bid, offer=offer)

    return render(request, 'offers/edit_bid.html', {'form': form, 'bid': bid})


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
        
       
        next_url = request.GET.get('next', 'dashboard')  
        return redirect(next_url)

    return redirect('dashboard')  
    
@login_required
def share_contact(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, offer__user=request.user, status='ACCEPTED')

    if request.method == 'POST':
        bid.contact_shared = True
        bid.save()
     
        messages.success(request, "Contact details have been shared with the bidder.")
        return redirect('offers:view_bids', offer_id=bid.offer.id)

    return HttpResponseForbidden()