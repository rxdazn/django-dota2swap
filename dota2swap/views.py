from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    print 'request.user.is_authenticated', request.user.is_authenticated()
    return render(request, 'home.html')
