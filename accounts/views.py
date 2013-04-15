from django.shortcuts import redirect
from django.contrib import messages
import django.contrib.auth

def logout(request):
    django.contrib.auth.logout(request)
    messages.success(request, 'You are now disconnected.')
    return redirect('home')
