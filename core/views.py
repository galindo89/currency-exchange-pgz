from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from offers.models import Offer, LatestExchangeRate, Bid

# Create your views here.

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
    return redirect('/accounts/login/')

@login_required
def dashboard(request):
    my_offers = Offer.objects.filter(user=request.user)
    my_bids = Bid.objects.filter(user=request.user)

    return render(request, 'core/dashboard.html', {
        'my_offers': my_offers,
        'my_bids': my_bids,
    })