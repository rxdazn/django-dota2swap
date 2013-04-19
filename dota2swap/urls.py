from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'dota2swap.views.home', name='home'),
     url(r'^heroes$', 'dota2swap.views.hero_list', name='hero_list'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'', include('accounts.urls')),
     url(r'', include('shop.urls')),
     url(r'', include('social_auth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
