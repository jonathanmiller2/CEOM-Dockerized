from django.conf.urls import *
from django.urls import re_path, path

import ceom.maps.views

urlpatterns = [
    re_path(r'^$', ceom.maps.views.index),
    re_path(r'^geocatter/$', ceom.maps.views.geocatter),
    re_path(r'^geocatterphoto/(?P<photo_id>\d*)/?$', ceom.maps.views.geocatterphoto),
    re_path(r'^point_validation/$', ceom.maps.views.point_validation),
    re_path(r'^point_validation_csv/$', ceom.maps.views.point_validation_csv),
    re_path(r'^leaderboard/$', ceom.maps.views.leaderboard),
    re_path(r'^pixel_validation/$', ceom.maps.views.pixel_validation),
    re_path(r'^pixel_validation_csv/$', ceom.maps.views.pixel_validation_csv),
]