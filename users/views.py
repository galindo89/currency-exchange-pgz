from django.shortcuts import render,redirect
from django.contrib.auth import logout

# Create your views here.


def custom_logout(request):
    logout(request)
    request.session.flush()  
    response = redirect('/')  
    response.delete_cookie('sessionid')  
    return response