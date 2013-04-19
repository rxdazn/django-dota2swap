from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render

from shop.forms import NewTransactionForm
from shop.models import InventoryItem
from shop.models import Transaction
from dota2swap.models import Hero

def all_transactions(request):
    transactions = Transaction.objects.filter(active=True)
    return render(request, 'all_transactions.html', {'transactions': transactions})

def all_transactions_by_hero(request, hero_id):
    try:
        hero = Hero.objects.get(id=hero_id)
    except:
        messages.error('This hero doesn\'t exist.')
        return redirect('home')

    result = Transaction.objects.filter(active=True)
    transactions = []
    for tr in result:
        for item in tr.item_pack.all():
            if item.base_item.hero_id == hero_id:
                transactions.append(tr)
                break
    return render(request, 'all_transactions_by_hero.html', {'transactions': transactions, 'hero': hero})

def new_transaction(request):
    if not request.user.is_authenticated():
        messages.error(request, 'You have to be authenticated to perform this action.')
        return render(request, 'new_transaction.html')
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
            else:
                messages.error('One or more items you wanted to trade are not in your backpack.')
    else:
        form = NewTransactionForm()
    return render(request, 'new_transaction.html', {'form': form})

def my_transactions(request):
    if not request.user.is_authenticated():
        messages.error(request, 'You have to be authenticated to perform this action.')
        return render(request, 'my_transactions.html')
    transactions = Transaction.objects.filter(seller=request.user)
    return render(request, 'my_transactions.html', {'transactions': transactions})
