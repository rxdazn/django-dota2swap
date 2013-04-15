from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import django.contrib.auth

def logout(request):
    django.contrib.auth.logout(request)
    messages.success(request, 'You are now disconnected.')
    return redirect('home')

@login_required
def profile(request):
    ''' user profile '''
    return render(request, 'profile.html')
