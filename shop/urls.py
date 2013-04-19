from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
    url(r'^transaction/all', 'all_transactions', name="all_transactions"),
    url(r'^transaction/new', 'new_transaction', name="new_transaction"),
    url(r'^transaction/list', 'my_transactions', name="my_transactions"),
    url(r'^transaction/hero/(?P<hero_id>([0-9]+))', 'all_transactions_by_hero', name='all_transactions_by_hero'),
)