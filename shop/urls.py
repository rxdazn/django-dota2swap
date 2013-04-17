from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
    url(r'^item/list', 'item_list', name="item_list"),
)
