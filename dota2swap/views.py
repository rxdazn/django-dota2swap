from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dota2swap.models import Hero
from shop.models import Transaction

def home(request):
    last_transactions = Transaction.objects.filter(active=True).order_by('-id')[0:10]
    return render(request, 'home.html', {'last_transactions': last_transactions})

def hero_list(request):
    heroes = Hero.objects.filter(available=True)
    return render(request, 'hero_list.html', {'heroes': heroes})
