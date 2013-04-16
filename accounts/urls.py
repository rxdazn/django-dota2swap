from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^login/success', 'login_success', name='login_success'),
    url(r'^login/error', 'login_error', name='login_error'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^user/(?P<steam_id>([0-9]+))', 'user_profile', name='user_profile'),
)
