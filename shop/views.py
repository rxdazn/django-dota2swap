from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.models import Member
from shop.models import Item
from shop.forms import NewTransactionForm
from shop.models import InventoryItem
from shop.models import Transaction
from dota2swap.models import Hero

def all_transactions(request):
    transactions = Transaction.objects.filter(active=True)
    return render(request, 'all_transactions.html', {'transactions': transactions})

def all_transactions_by_hero(request, hero_id):
    try:
        hero_id = int(hero_id)
        hero = Hero.objects.get(unique_id=hero_id)
    except:
        messages.error('This hero doesn\'t exist.')
        return redirect('home')

    result = Transaction.objects.filter(active=True)
    transactions = []
    for tr in result:
        for item in tr.item_pack.all():
            if item.base_item.hero:
                print item.base_item.hero.__dict__
                print type(item.base_item.hero.unique_id), type(hero_id)
                if item.base_item.hero.unique_id == hero_id:
                    transactions.append(tr)
                    break
    return render(request, 'all_transactions_by_hero.html', {'transactions': transactions, 'hero': hero})

def _chunks(obj_list, n):
    """ Yield successive n-sized chunks from obj_list.
    """
    for i in xrange(0, len(obj_list), n):
        yield obj_list[i:i+n]

def new_transaction(request):
    if not request.user.is_authenticated():
        messages.error(request, 'You have to be authenticated to perform this action.')
        return render(request, 'new_transaction.html')
    try:
        view_user = request.user
        backpack_items = view_user.items.order_by('slot_number')
    except:
        messages.error(request, 'The requested user does not exist.')
        return redirect('home')
    backpack = []
    if backpack_items:
        backpack = [item_page for item_page in _chunks(backpack_items, 25)]
    if request.method == 'POST':
        form = NewTransactionForm(request.POST)
        if form.is_valid():
            items = [int(x) for x in request.POST.getlist('item')]
            result = InventoryItem.objects.filter(member=request.user).filter(unique_id__in=items)
            if len(items) == len(result):
                tr = Transaction()
                tr.comment = form.cleaned_data['comment']
                tr.seller = request.user
                tr.save()
                for it in result:
                    tr.item_pack.add(it)
                tr.save()
                messages.success(request, 'Your transaction has been created.')
                return redirect('my_transactions')
            else:
                messages.error(request, 'One or more items you wanted to trade are not in your backpack.')
    else:
        form = NewTransactionForm()
    return render(request, 'new_transaction.html', {'form': form, 'backpack': backpack})

def my_transactions(request):
    if not request.user.is_authenticated():
        messages.error(request, 'You have to be authenticated to perform this action.')
        return render(request, 'my_transactions.html')
    transactions = Transaction.objects.filter(seller=request.user)
    return render(request, 'my_transactions.html', {'transactions': transactions})
