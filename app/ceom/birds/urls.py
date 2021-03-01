#TODO: Is this conf import needed?
from django.conf.urls import *
from django.urls import re_path

import ceom.birds.views

urlpatterns = [
    re_path(r'^$', ceom.birds.views.index),
    re_path(r'^all.kml$', ceom.birds.views.kml),
]
