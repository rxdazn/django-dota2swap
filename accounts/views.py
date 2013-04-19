from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import django.contrib.auth

from accounts.models import Member
from shop.models import Item

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

def _chunks(obj_list, n):
    """ Yield successive n-sized chunks from obj_list.
    """
    for i in xrange(0, len(obj_list), n):
        yield obj_list[i:i+n]

def user_profile(request, user_id):
    try:
        view_user = Member.objects.get(id=user_id)
        backpack_items = view_user.items.order_by('slot_number')
    except:
        messages.error(request, 'The requested user does not exist.')
        return redirect('home')
    backpack = []
    if backpack_items:
        backpack = [item_page for item_page in _chunks(backpack_items, 25)]
        for item in backpack[0]:
            print 'item', item.base_item.name


    return render(request, 'user_profile.html', {'view_user': view_user,
        'backpack': backpack})

def get_backpack_page(page=1):
    items = Item.objects.all().order_by('slot_nb')
    paginator = Paginator(items, 25)
    print 'get packack'
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
        #items = items.filter(slot_nb=range(((page*25)-25), ((page*25)-1)))
    except (EmptyPage, InvalidPage):
        items = paginator.page(1)

    return items
        
