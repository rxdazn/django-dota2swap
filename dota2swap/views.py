from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

def home(request):
    if request.user.is_authenticated():
        return render_to_response('home.html', {'username': request.openid})
    else:
        return render_to_response('home.html', {'auth_url': '/openid/login/'})

def next_works(request):
    return HttpResponse('?next= bit works')

@login_required
def require_authentication(request):
    return HttpReponse('This page requires authentication')

def login(request):
    pass
