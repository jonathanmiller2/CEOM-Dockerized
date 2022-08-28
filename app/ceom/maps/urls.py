from django.conf.urls import *
from django.urls import re_path, path

import ceom.maps.views

urlpatterns = [
    re_path(r'^$', ceom.maps.views.index),
    re_path(r'^geocatter/$', ceom.maps.views.geocatter)
]