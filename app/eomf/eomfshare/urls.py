#TODO: Is this conf import needed?
from django.conf.urls import url, include

#TODO: Is this import needed?
from django.contrib import admin
admin.autodiscover()

from django.urls import re_path
import eomf.eomfshare.views

urlpatterns = [
        re_path(r'^$', eomf.eomfshare.views.upload_form_view),
        re_path(r'^submit/$', eomf.eomfshare.views.success_upload),
]