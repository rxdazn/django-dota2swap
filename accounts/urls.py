from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^logout$', 'logout', name='logout'),
    url(r'^profile$', 'profile', name='profile'), 
)
