from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Offer, LatestExchangeRate
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


def view_offers(request):
    offers = Offer.objects.all()
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
