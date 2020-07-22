from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
import views


urlpatterns = patterns('eomf.eomfshare.views',
        (r'^$', 'upload_form_view'),
        (r'^submit/$', 'success_upload'),
    )