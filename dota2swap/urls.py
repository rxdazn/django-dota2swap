from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'dota2swap.views.home', name='home'),
     url(r'^login/', 'dota2swap.views.login', name='login'),
     #url(r'^dota2swap/', include('dota2swap.foo.urls')),
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^openid/', include('django_openid_auth.urls'))
     #url(r'^openid/$', 'django_openid_consumer.views.begin'),
     #url(r'^openid/complete/$', 'django_openid_consumer.views.complete'),
     #url(r'^openid/signout/$', 'django_openid_consumer.views.signout'),
)
