from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.



@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
    return redirect('/accounts/login/')