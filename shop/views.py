from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render

def item_list(request):
    return render(request, 'item_list.html')
