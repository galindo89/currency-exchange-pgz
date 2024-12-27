from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Offer
from .forms import OfferForm

# Create your views here.


@login_required
def create_offer(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
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
            form.save()
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
