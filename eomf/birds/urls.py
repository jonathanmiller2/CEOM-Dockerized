from django.conf.urls import *
from django.urls import re_path

import eomf.birds.views

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.birds.views
urlpatterns = [
    re_path(r'^$', eomf.birds.views.index),
    re_path(r'^all.kml$', eomf.birds.views.kml),
]
