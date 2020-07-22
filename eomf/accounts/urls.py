from django.conf.urls import url,include,patterns
from django.contrib.auth.models import User
from forms import LoginForm

info_users = {
    "queryset": User.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', 'eomf.accounts.views.index'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'},name='logout'),

    url(r'^mobile_login/$', 'eomf.accounts.views.mobile_login',name='mobile_login'),    

    url(r'^register/$', 'eomf.accounts.views.register',name='register'),

    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'},name='password_change'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'},name='password_change_done'),

    url(r'^reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'accounts/password_reset_form.html','email_template_name':'accounts/password_reset_email.html'},name='password_reset'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/token/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html'},name='password_reset_confirm'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',name='password_reset_confirm'),
    url(r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html'},name='password_reset_complete'),

    url(r'^profile/$', 'eomf.accounts.views.profile_authed',name='profile_authed'),
    url(r'^profile/edit/$', 'eomf.accounts.views.profile_edit',name='profile_edit'),
    url(r'^profile/(?P<username>\w+)/$', 'eomf.accounts.views.profile', name='user_detail'),

    #url(r'^id_from_username/$', 'eomf.accounts.views.id_from_username', name = 'id_from_username'),
)
