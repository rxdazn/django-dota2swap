from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
import django.contrib.auth

from accounts.models import Member

def logout(request):
    django.contrib.auth.logout(request)
    messages.success(request, 'You are now disconnected.')
    return redirect('home')

def user_profile(request, steam_id):
    try:
        view_user = Member.objects.get(steam_id=steam_id)
    except:
        messages.error(request, 'The requested user does not exist.')
        return redirect('home')
    return render(request, 'user_profile.html', {'view_user': view_user})
