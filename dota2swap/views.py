from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dota2swap.models import Hero

def home(request):
    return render(request, 'home.html')

def hero_list(request):
    heroes = Hero.objects.all()
    return render(request, 'hero_list.html', {'heroes': heroes})
