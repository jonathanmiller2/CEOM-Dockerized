from django.urls import re_path
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

import ceom.accounts.views
import django.contrib.auth.views

info_users = {
    "queryset": User.objects.all(),
}

urlpatterns = [
    re_path(r'^$', ceom.accounts.views.index),

    re_path(r'^login/$', ceom.accounts.views.login, name="login"),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'accounts/logout.html'},name='logout'),

    re_path(r'^mobile_login/$', ceom.accounts.views.mobile_login,name='mobile_login'),    

    re_path(r'^register/$', ceom.accounts.views.register,name='register'),

    re_path(r'^password/change/$', auth_views.PasswordChangeView.as_view(), {'template_name': 'accounts/password_change_form.html'},name='password_change'),
    re_path(r'^password/done/$', auth_views.PasswordChangeDoneView.as_view(), {'template_name': 'accounts/password_change_done.html'},name='password_change_done'),

    re_path(r'^reset/$', auth_views.PasswordResetView.as_view(email_template_name='accounts/password_reset_email.html'),name='password_reset'),
    re_path(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': 'accounts/password_reset_done.html'},name='password_reset_done'),
    re_path(r'^reset/token/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), {'template_name': 'accounts/password_reset_confirm.html'},name='password_reset_confirm'),
    re_path(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), {'template_name': 'accounts/password_reset_complete.html'},name='password_reset_complete'),

    re_path(r'^profile/$', ceom.accounts.views.profile_authed,name='profile_authed'),
    re_path(r'^profile/edit/$', ceom.accounts.views.profile_edit,name='profile_edit'),
    re_path(r'^profile/(?P<username>\w+)/$', ceom.accounts.views.profile, name='user_detail'),
]
