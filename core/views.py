from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    
@login_required
def view_contact_details(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, user=request.user)

   
    if bid.status == 'ACCEPTED' and bid.contact_shared:
        user = bid.offer.user
        contact_details = {
            'name': f"{user.first_name} {user.last_name}".strip() or "Not Provided",  
            'email': user.email  
        }
        return JsonResponse({'success': True, 'contact_details': contact_details})

    return JsonResponse({'success': False, 'message': 'Contact details not available.'})

