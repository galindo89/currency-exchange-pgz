"""
Viwes for users app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.


def custom_logout(request):
    """
    Logs out the user, flushes the session, and deletes the session cookie.
    """
    logout(request)
    request.session.flush()
    response = redirect('/')
    response.delete_cookie('sessionid')
    return response
