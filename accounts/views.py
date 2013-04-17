from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import django.contrib.auth

from accounts.models import Member

def login_success(request):
    messages.success(request, 'Welcome %s!' % request.user.username)
    return redirect('home')

def login_error(request):
    messages.error(request, 'Login failed.')
    return redirect('home')

def logout(request):
    django.contrib.auth.logout(request)
    messages.success(request, 'You are now disconnected.')
    return redirect('home')

def user_profile(request, user_id):
    try:
        view_user = Member.objects.get(id=user_id)
        backpack_items = view_user.items.order_by('slot_number')
    except:
        messages.error(request, 'The requested user does not exist.')
        return redirect('home')
    return render(request, 'user_profile.html', {'view_user': view_user,
        'backpack_items': backpack_items})
