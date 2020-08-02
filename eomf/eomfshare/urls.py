from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()
import eomf.eomfshare.views

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.eomfshare.views
urlpatterns = [
        (r'^$', 'upload_form_view'),
        (r'^submit/$', 'success_upload'),
]