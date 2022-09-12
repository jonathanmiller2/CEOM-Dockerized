from django.conf.urls import *
from django.urls import re_path, path

import ceom.maps.views

urlpatterns = [
    re_path(r'^$', ceom.maps.views.index),
    re_path(r'^geocatter/$', ceom.maps.views.geocatter),
    re_path(r'^validation/$', ceom.maps.views.map_validation),
    re_path(r'^validation_data/$', ceom.maps.views.map_validation_data),
]