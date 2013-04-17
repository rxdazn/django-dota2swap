from dota2swap.accounts.views import get_backpack_page
from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def pagination(request, page_number):
    items = get_backpack_page(user_id, page_number)
    render = render_to_string('backpack_page.html', {'items': items})

    dajax = Dajax()
    dajax.assign("#backpack, 'innerHTML', render)
    return dajax.json()

