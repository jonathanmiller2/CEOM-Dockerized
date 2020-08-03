#TODO: Is this conf import needed?
from django.conf.urls import *
from django.urls import re_path

import eomf.birds.views

urlpatterns = [
    re_path(r'^$', eomf.birds.views.index),
    re_path(r'^all.kml$', eomf.birds.views.kml),
]
