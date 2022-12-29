from django.conf.urls import *
from django.urls import re_path, path

import ceom.maps.views

urlpatterns = [
    re_path(r'^$', ceom.maps.views.index),
    re_path(r'^geocatter/$', ceom.maps.views.geocatter),
    re_path(r'^validation/$', ceom.maps.views.map_validation),
    re_path(r'^validation_data/$', ceom.maps.views.map_validation_data),
    re_path(r'^leaderboard/$', ceom.maps.views.leaderboard),
    re_path(r'^pixels_validation/$', ceom.maps.views.pixels_validation),
    re_path(r'^pixels_validation_csv/$', ceom.maps.views.pixels_validation_csv),
]