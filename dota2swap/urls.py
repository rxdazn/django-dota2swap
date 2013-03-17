from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'dota2swap.views.home', name='home'),
     #url(r'^login/', 'dota2swap.views.login', name='login'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'', include('accounts.urls')),
     url(r'', include('social_auth.urls')),
)
