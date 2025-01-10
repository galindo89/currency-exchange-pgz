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
    user_bids_with_shared_contacts = Bid.objects.filter(user=request.user, contact_shared=True)

    return render(request, 'core/dashboard.html', {
        'user_bids_with_shared_contacts': user_bids_with_shared_contacts,
    })